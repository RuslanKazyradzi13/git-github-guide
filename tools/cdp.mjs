// Минимальный клиент Chrome DevTools Protocol без внешних зависимостей.
// Запускает установленный Microsoft Edge или Google Chrome в фоновом режиме
// и позволяет открыть страницу, выполнить JavaScript, сделать снимок или PDF.
// Требуется Node.js 22+ (встроенные fetch и WebSocket).

import { spawn } from "node:child_process";
import { existsSync, mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const CANDIDATES = [
  process.env.BROWSER_PATH,
  "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
  "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  "/usr/bin/google-chrome",
  "/usr/bin/chromium",
].filter(Boolean);

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

export async function launch() {
  const exe = CANDIDATES.find((p) => existsSync(p));
  if (!exe) throw new Error("Не найден Edge или Chrome. Укажите путь в переменной BROWSER_PATH.");
  const profile = mkdtempSync(join(tmpdir(), "guide-cdp-"));
  const proc = spawn(exe, [
    "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
    "--allow-file-access-from-files", "--remote-debugging-port=0", "--force-color-profile=srgb",
    `--user-data-dir=${profile}`, "about:blank",
  ], { stdio: "ignore" });
  const portFile = join(profile, "DevToolsActivePort");
  for (let i = 0; i < 100 && !existsSync(portFile); i++) await sleep(100);
  await sleep(100);
  const [port, path] = readFileSync(portFile, "utf8").trim().split(/\r?\n/);
  const ws = new WebSocket(`ws://127.0.0.1:${port}${path}`);
  await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });

  let id = 0;
  const pending = new Map();
  const listeners = [];
  ws.onmessage = (ev) => {
    const msg = JSON.parse(ev.data);
    if (msg.id && pending.has(msg.id)) {
      const { resolve, reject } = pending.get(msg.id);
      pending.delete(msg.id);
      msg.error ? reject(new Error(msg.error.message)) : resolve(msg.result);
    } else if (msg.method) {
      for (const l of listeners) l(msg);
    }
  };
  const send = (method, params = {}, sessionId) => new Promise((resolve, reject) => {
    const mid = ++id;
    pending.set(mid, { resolve, reject });
    ws.send(JSON.stringify({ id: mid, method, params, sessionId }));
  });

  const { targetId } = await send("Target.createTarget", { url: "about:blank" });
  const { sessionId } = await send("Target.attachToTarget", { targetId, flatten: true });
  const page = (method, params) => send(method, params, sessionId);
  await page("Page.enable");
  await page("Runtime.enable");

  const consoleLog = [];
  listeners.push((m) => {
    if (m.sessionId !== sessionId) return;
    if (m.method === "Runtime.consoleAPICalled") {
      consoleLog.push(m.params.args.map((a) => a.value ?? a.description).join(" "));
    }
    if (m.method === "Runtime.exceptionThrown") {
      consoleLog.push("EXCEPTION: " + (m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text));
    }
  });

  return {
    consoleLog,
    async goto(url) {
      const loaded = new Promise((res) => listeners.push((m) => {
        if (m.sessionId === sessionId && m.method === "Page.loadEventFired") res();
      }));
      await page("Page.navigate", { url });
      await loaded;
    },
    async eval(expression) {
      const r = await page("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true });
      if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text);
      return r.result.value;
    },
    async waitFor(expression, timeoutMs = 60000) {
      const t0 = Date.now();
      while (Date.now() - t0 < timeoutMs) {
        if (await this.eval(expression)) return;
        await sleep(200);
      }
      throw new Error("Истекло время ожидания: " + expression);
    },
    async viewport(width, height, scale = 1) {
      await page("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: scale, mobile: false });
    },
    async screenshot() {
      const r = await page("Page.captureScreenshot", { format: "png", captureBeyondViewport: false });
      return Buffer.from(r.data, "base64");
    },
    async pdf(params) {
      const r = await page("Page.printToPDF", params);
      return Buffer.from(r.data, "base64");
    },
    async close() {
      try { await send("Browser.close"); } catch { /* браузер уже закрыт */ }
      ws.close();
      await sleep(500);
      try { proc.kill(); } catch { /* процесс уже завершён */ }
      try { rmSync(profile, { recursive: true, force: true }); } catch { /* файлы ещё заняты */ }
    },
  };
}
