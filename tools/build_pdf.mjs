// Сборка PDF-версии методички: node tools/build_pdf.mjs
//
// Что нужно: Node.js 22+, Microsoft Edge или Google Chrome, Python с пакетом PyMuPDF
// (для номеров страниц в оглавлении и закладок; без него PDF соберётся без номеров).
// Библиотеки markdown-it и Mermaid загружаются браузером с cdn.jsdelivr.net.
// Чтобы собрать без интернета, укажите локальные копии в переменных
// MARKDOWN_IT_JS и MERMAID_JS (пути к файлам *.min.js).

import { execFileSync } from "node:child_process";
import { existsSync, mkdtempSync, readdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { launch } from "./cdp.mjs";

const TOOLS = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(TOOLS, "..");
const OUT = process.argv.includes("--out") ? resolve(process.argv[process.argv.indexOf("--out") + 1]) : join(ROOT, "git-github-guide.pdf");
const CHECKED = "11 октября 2026 года";
// Ссылки на файлы, которых нет в PDF, ведут на их страницы на GitHub.
const REPO_URL = "https://github.com/RuslanKazyradzi13/git-github-guide/blob/main/";

const asUrl = (p) => (/^https?:/.test(p) ? p : pathToFileURL(resolve(p)).href);
const MARKDOWN_IT = asUrl(process.env.MARKDOWN_IT_JS || "https://cdn.jsdelivr.net/npm/markdown-it@14.1.0/dist/markdown-it.min.js");
const MERMAID = asUrl(process.env.MERMAID_JS || "https://cdn.jsdelivr.net/npm/mermaid@11.17.2/dist/mermaid.min.js");

const read = (rel) => readFileSync(join(ROOT, rel), "utf8");
// Блоки README только для GitHub (анимация, значки, кнопки) в PDF не нужны.
const skipWebOnly = (md) => md.replace(/<!-- pdf:skip -->[\s\S]*?<!-- \/pdf:skip -->\n?/g, "");

function repoFiles(dir = ROOT, base = "") {
  const out = [];
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    if (e.name === ".git" || e.name === "node_modules") continue;
    const rel = base + e.name;
    if (e.isDirectory()) out.push(rel, rel + "/", ...repoFiles(join(dir, e.name), rel + "/"));
    else out.push(rel);
  }
  return out;
}
const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

const PART1 = ["01_git_i_github.md", "02_ustanovka_i_nastroyka.md", "03_osnovnye_komandy.md", "04_rabota_s_github.md",
  "05_vetki_i_pull_requests.md", "06_oshibki_i_vosstanovlenie.md", "07_git_s_claude_code.md", "08_praktika_i_zadaniya.md"];
const PART2 = ["09_standarty_i_oformlenie_proektov.md", "10_litsenzii_i_avtorskie_prava.md", "11_bezopasnost_i_avtomatizatsiya.md"];
const TEMPLATES = [
  ["README.template.md", true], ["CONTRIBUTING.template.md", true], ["SECURITY.template.md", true],
  ["CHANGELOG.template.md", true], ["CODE_OF_CONDUCT.template.md", true], ["ISSUE_TEMPLATE.md", true],
  ["PULL_REQUEST_TEMPLATE.md", true], ["LICENSE_SELECTION_GUIDE.md", false], ["PROJECT_RELEASE_CHECKLIST.md", false],
];

const h1Of = (md) => (md.match(/^# (.+)$/m) || [, ""])[1];

function divider(id, part, label, title, desc, files) {
  const items = files.map((f) => `<li>${esc(h1Of(read(f)))}</li>`).join("");
  return {
    kind: "html",
    tocEntry: { level: 1, text: `${label}. ${title}`, id, part, divider: true },
    html: `<section class="divider" id="${id}">{{MARK:${id}}}<div class="label">${label}</div>` +
      `<div class="title">${esc(title)}</div><div class="desc">${esc(desc)}</div><ul>${items}</ul></section>`,
  };
}

function buildBook(pass, tocPages) {
  const fileMap = { "README.md": "readme", "glossary.md": "glossary", "sources.md": "sources",
    "examples/tempconv/README.md": "example" };
  PART1.concat(PART2).forEach((f) => (fileMap[f] = "ch" + f.slice(0, 2)));
  for (const [f] of TEMPLATES) fileMap["templates/" + f] = "tpl-" + f.toLowerCase().replace(/[^a-z0-9]+/g, "-");

  const roadmap = pathToFileURL(join(ROOT, "images", "00-roadmap.svg")).href;
  const sections = [
    { kind: "html", html:
      `<section class="cover"><div class="bar"><span style="background:#1A73E8"></span><span style="background:#D93025"></span>` +
      `<span style="background:#F9AB00"></span><span style="background:#1E8E3E"></span></div>` +
      `<h1>Git и GitHub с нуля</h1><div class="subtitle">Методичка для начинающих: от первого коммита до профессионально ` +
      `оформленного проекта, лицензий, безопасности и работы с AI-ассистентами</div>` +
      `<div class="art"><img src="${roadmap}" alt="Маршрут обучения"></div>` +
      `<div class="meta">Сведения проверены по официальным источникам ${CHECKED} · Windows 10 и 11 · Git 2.56</div></section>` },
    { kind: "html", html: '<section class="toc" id="toc-list"></section>' },
    { kind: "md", id: "readme", file: "README.md", part: 0, tocDepth: 1,
      md: skipWebOnly(read("README.md")).replace(/^# .+$/m, "# О методичке") },
    divider("part1", 1, "Часть I", "Git и GitHub с нуля",
      "Как сохранять версии проекта, работать с GitHub, ветками и Pull Request, восстанавливать изменения и безопасно работать с AI.", PART1),
    ...PART1.map((f) => ({ kind: "md", id: fileMap[f], file: f, part: 1, tocDepth: 2, md: read(f) })),
    divider("part2", 2, "Часть II", "Как создавать, оформлять и публиковать программные проекты по международным практикам",
      "Структура репозитория, документация, версии, лицензии, стандарты, безопасность и автоматические проверки.", PART2),
    ...PART2.map((f) => ({ kind: "md", id: fileMap[f], file: f, part: 2, tocDepth: 2, md: read(f) })),
    divider("appendix", 3, "Приложения", "Справочные материалы",
      "Словарь терминов, источники, пример оформленного README и шаблоны документов проекта.",
      ["glossary.md", "sources.md"]),
    { kind: "md", id: "glossary", file: "glossary.md", part: 3, tocDepth: 1, md: read("glossary.md") },
    { kind: "md", id: "sources", file: "sources.md", part: 3, tocDepth: 1, md: read("sources.md") },
    { kind: "md", id: "example", file: "examples/tempconv/README.md", part: 3, tocDepth: 1,
      md: read("examples/tempconv/README.md").replace(/^# .+$/m, "# Пример README учебного проекта tempconv") },
    { kind: "templates", id: "templates", file: "templates/", part: 3, tocDepth: 1,
      intro: "# Шаблоны документов\n\nШаблоны из папки `templates/`. Пояснения в них записаны служебными комментариями " +
        "`<!-- ... -->`, поэтому семь шаблонов приведены как исходный текст. Руководство по выбору лицензии и чек-лист " +
        "публикации — обычные документы. Как применять шаблоны — в главе 9.\n",
      items: TEMPLATES.map(([f, asCode]) => ({
        id: fileMap["templates/" + f], file: "templates/" + f, title: f, asCode, md: read("templates/" + f),
      })) },
  ];
  return {
    pass, tocPages, fileMap, sections,
    rootUrl: pathToFileURL(ROOT).href + "/",
    repoUrl: REPO_URL, repoFiles: repoFiles(),
    partTitles: { 1: "Часть I · Git и GitHub с нуля", 2: "Часть II · Профессиональные проекты", 3: "Приложения" },
  };
}

function htmlPage(book) {
  const css = pathToFileURL(join(TOOLS, "pdf.css")).href;
  const js = pathToFileURL(join(TOOLS, "pdf_render.js")).href;
  const data = JSON.stringify(book).replace(/</g, "\\u003c");
  return `<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>Git и GitHub с нуля</title>
<link rel="stylesheet" href="${css}"></head><body><main id="book"></main>
<script id="book-data" type="application/json">${data}</script>
<script src="${MARKDOWN_IT}"></script><script src="${MERMAID}"></script><script src="${js}"></script></body></html>`;
}

function python(args) {
  for (const exe of ["python", "py", "python3"]) {
    try {
      return execFileSync(exe, [join(TOOLS, "pdf_pages.py"), ...args],
        { encoding: "utf8", env: { ...process.env, PYTHONIOENCODING: "utf-8" } });
    } catch (e) {
      if (e.code !== "ENOENT") throw e;
    }
  }
  throw new Error("Python не найден");
}

async function renderPass(browser, dir, pass, tocPages) {
  const page = join(dir, `book-${pass}.html`);
  writeFileSync(page, htmlPage(buildBook(pass, tocPages)), "utf8");
  await browser.goto(pathToFileURL(page).href);
  await browser.waitFor("window.__ready === true", 180000);
  const errors = await browser.eval("window.__errors");
  if (errors.length) {
    console.error("Ошибки отрисовки:\n" + errors.join("\n"));
    throw new Error(`Найдено ошибок: ${errors.length}`);
  }
  const params = { printBackground: true, preferCSSPageSize: true, displayHeaderFooter: false, generateTaggedPDF: true };
  let pdf;
  try {
    pdf = await browser.pdf(params);
  } catch {
    delete params.generateTaggedPDF;
    pdf = await browser.pdf(params);
  }
  const file = join(dir, `book-${pass}.pdf`);
  writeFileSync(file, pdf);
  return { file, markers: await browser.eval("window.__markers"), toc: await browser.eval("window.__toc") };
}

const dir = mkdtempSync(join(tmpdir(), "guide-pdf-"));
const browser = await launch();
try {
  console.log("Проход 1: вёрстка и поиск номеров страниц");
  const first = await renderPass(browser, dir, 1, {});
  let pages = {};
  try {
    writeFileSync(join(dir, "markers.json"), JSON.stringify(first.markers), "utf8");
    pages = JSON.parse(python(["find", first.file, join(dir, "markers.json")]));
  } catch (e) {
    console.warn("Номера страниц не определены (нужен Python с PyMuPDF): " + e.message);
  }
  console.log("Проход 2: оглавление с номерами страниц");
  const second = await renderPass(browser, dir, 2, pages);
  if (Object.keys(pages).length) {
    const outline = second.toc.filter((e) => pages[e.id]).map((e) => ({ ...e, page: pages[e.id] }));
    writeFileSync(join(dir, "outline.json"), JSON.stringify(outline), "utf8");
    console.log(python(["finish", second.file, join(dir, "outline.json"), OUT]).trim());
  } else {
    writeFileSync(OUT, readFileSync(second.file));
  }
  console.log("Готово: " + OUT);
} finally {
  await browser.close();
  if (!process.env.KEEP_BUILD) rmSync(dir, { recursive: true, force: true });
  else console.log("Временные файлы: " + dir);
}
