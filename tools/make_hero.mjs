// Собирает анимацию для шапки README и картинку для соцсетей из tools/hero.html.
//
//   node tools/make_hero.mjs
//
// Результат: images/hero-light.gif, images/hero-dark.gif, images/social-preview.png.
// Нужны Node.js 22+, Edge или Chrome, Python с пакетом Pillow и доступ к Google Fonts.
// Частоту кадров можно изменить переменной HERO_FPS (по умолчанию 20).

import { execFileSync } from "node:child_process";
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { launch } from "./cdp.mjs";

const TOOLS = dirname(fileURLToPath(import.meta.url));
const ROOT = dirname(TOOLS);
const PAGE = pathToFileURL(join(TOOLS, "hero.html")).href;
const FPS = Number(process.env.HERO_FPS || 20);
const KEEP = { light: "#ffffff,#202124", dark: "#0d1117,#161b22" };

function python(args) {
  for (const exe of ["python", "py", "python3"]) {
    try {
      return execFileSync(exe, [join(TOOLS, "frames_to_gif.py"), ...args],
        { encoding: "utf8", env: { ...process.env, PYTHONIOENCODING: "utf-8" } });
    } catch (e) {
      if (e.code !== "ENOENT") throw e;
    }
  }
  throw new Error("Python не найден");
}

const work = mkdtempSync(join(tmpdir(), "guide-hero-"));
const browser = await launch();
try {
  for (const theme of ["light", "dark"]) {
    await browser.viewport(1280, 520);
    await browser.goto(`${PAGE}?theme=${theme}`);
    await browser.waitFor("window.ready === true");
    const duration = await browser.eval("DURATION");
    const count = Math.round(duration * FPS);
    const dir = join(work, theme);
    mkdirSync(dir);
    for (let i = 0; i < count; i++) {
      await browser.eval(`render(${i / FPS})`);
      writeFileSync(join(dir, `${String(i).padStart(4, "0")}.png`), await browser.screenshot());
    }
    const out = join(ROOT, "images", `hero-${theme}.gif`);
    console.log(python([dir, out, String(FPS), KEEP[theme]]).trim());
  }
  await browser.viewport(1280, 640);
  await browser.goto(`${PAGE}?theme=light&mode=social`);
  await browser.waitFor("window.ready === true");
  writeFileSync(join(ROOT, "images", "social-preview.png"), await browser.screenshot());
  console.log("images/social-preview.png");
  if (browser.consoleLog.length) console.log(browser.consoleLog.join("\n"));
} finally {
  await browser.close();
  rmSync(work, { recursive: true, force: true });
}
