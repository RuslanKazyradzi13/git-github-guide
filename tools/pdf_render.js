// Выполняется в браузере при сборке PDF: превращает Markdown глав в HTML,
// рисует диаграммы Mermaid и строит оглавление. Данные приходят из build_pdf.mjs.
(async () => {
  const BOOK = JSON.parse(document.getElementById("book-data").textContent);
  const errors = [];
  const markers = {};
  const toc = [];
  window.__errors = errors;
  window.__markers = markers;
  window.__toc = toc;

  // Mermaid сам запускается по событию load — отключаем это до отрисовки глав.
  mermaid.initialize({
    startOnLoad: false,
    theme: "base",
    securityLevel: "strict",
    fontFamily: "Segoe UI, Roboto, Arial, sans-serif",
    themeVariables: {
      fontFamily: "Segoe UI, Roboto, Arial, sans-serif",
      fontSize: "14px",
      primaryColor: "#E8F0FE",
      primaryTextColor: "#202124",
      primaryBorderColor: "#1A73E8",
      secondaryColor: "#E6F4EA",
      tertiaryColor: "#F1F3F4",
      lineColor: "#5F6368",
      textColor: "#202124",
      actorBkg: "#E8F0FE",
      actorBorder: "#1A73E8",
      noteBkgColor: "#FEF7E0",
      git0: "#1A73E8", git1: "#1E8E3E", git2: "#F9AB00", git3: "#D93025",
      git4: "#9334E6", git5: "#5F6368", git6: "#12B5CB", git7: "#E8710A",
      gitBranchLabel0: "#FFFFFF", gitBranchLabel1: "#FFFFFF", gitBranchLabel2: "#202124",
      gitBranchLabel3: "#FFFFFF", commitLabelColor: "#202124", commitLabelBackground: "#F1F3F4",
    },
    flowchart: { htmlLabels: true, curve: "basis" },
    gitGraph: { mainBranchName: "main", showCommitLabel: true },
  });

  const ALERTS = { NOTE: "Примечание", TIP: "Совет", IMPORTANT: "Важно", WARNING: "Внимание", CAUTION: "Опасно" };
  const LANGS = {
    powershell: "PowerShell", bash: "Bash", yaml: "YAML", markdown: "Markdown", python: "Python",
    javascript: "JavaScript", json: "JSON", diff: "diff", ini: "INI", toml: "TOML",
    gitignore: ".gitignore", gitattributes: ".gitattributes", dotenv: ".env",
  };
  let markerSeq = 0;

  const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

  function ghSlug(text) {
    text = text.replace(/`([^`]*)`/g, "$1").replace(/\[([^\]]*)\]\([^)]*\)/g, "$1").replace(/\*/g, "");
    let out = "";
    for (const ch of text.toLowerCase()) if (/[\p{L}\p{N}\p{M}\-_ ]/u.test(ch)) out += ch;
    return out.replace(/ /g, "-");
  }
  const plain = (s) => s.replace(/`([^`]*)`/g, "$1").replace(/\*\*/g, "").replace(/\[([^\]]*)\]\([^)]*\)/g, "$1");

  function normalize(path) {
    const out = [];
    for (const part of path.split("/")) {
      if (part === "" || part === ".") continue;
      if (part === "..") out.pop(); else out.push(part);
    }
    return out.join("/");
  }
  const dirOf = (file) => (file.includes("/") ? file.slice(0, file.lastIndexOf("/") + 1) : "");

  function addMarker(id) {
    if (BOOK.pass !== 1) return "";
    const code = "QQPM" + ++markerSeq + "QQ";
    markers[code] = id;
    return `<span class="pm">${code}</span>`;
  }

  function resolveHref(href, env) {
    if (/^(https?:|mailto:)/.test(href)) return { href };
    if (href.startsWith("#")) return { href: `#${env.sec.id}--${decodeURIComponent(href.slice(1))}` };
    const [p, anchor] = href.split("#");
    const target = normalize(dirOf(env.sec.file) + decodeURIComponent(p));
    const id = BOOK.fileMap[target];
    if (!id) return { dead: true };
    return { href: anchor ? `#${id}--${decodeURIComponent(anchor)}` : `#${id}` };
  }

  const md = window.markdownit({ html: true, linkify: false, typographer: false });

  // GitHub alerts: > [!NOTE]
  md.core.ruler.before("inline", "gh_alerts", (state) => {
    const t = state.tokens;
    for (let i = 0; i + 2 < t.length; i++) {
      if (t[i].type !== "blockquote_open" || t[i + 1].type !== "paragraph_open" || t[i + 2].type !== "inline") continue;
      const m = t[i + 2].content.match(/^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\][ \t]*\n?/);
      if (!m) continue;
      t[i].meta = { alert: m[1] };
      t[i + 2].content = t[i + 2].content.slice(m[0].length);
    }
  });

  // Списки задач: - [ ] и - [x]
  md.core.ruler.after("inline", "task_lists", (state) => {
    const t = state.tokens;
    for (let i = 2; i < t.length; i++) {
      if (t[i].type !== "inline" || t[i - 1].type !== "paragraph_open" || t[i - 2].type !== "list_item_open") continue;
      const first = t[i].children[0];
      if (!first || first.type !== "text") continue;
      const m = first.content.match(/^\[([ xX])\]\s+/);
      if (!m) continue;
      first.content = first.content.slice(m[0].length);
      const box = new state.Token("html_inline", "", 0);
      box.content = `<span class="chk">${m[1] === " " ? "☐" : "☑"}</span>`;
      t[i].children.unshift(box);
      t[i - 2].attrSet("class", "task");
    }
  });

  const r = md.renderer.rules;
  r.blockquote_open = (tokens, idx, o, env) => {
    const alert = tokens[idx].meta && tokens[idx].meta.alert;
    env.quotes.push(Boolean(alert));
    return alert ? `<div class="callout ${alert.toLowerCase()}"><div class="ct">${ALERTS[alert]}</div>` : "<blockquote>";
  };
  r.blockquote_close = (tokens, idx, o, env) => (env.quotes.pop() ? "</div>" : "</blockquote>");

  r.heading_open = (tokens, idx, opts, env, self) => {
    const level = Number(tokens[idx].tag.slice(1)) + env.shift;
    const text = tokens[idx + 1].content;
    const base = ghSlug(text);
    const n = env.slugs[base] || 0;
    env.slugs[base] = n + 1;
    const slug = n ? `${base}-${n}` : base;
    const id = level === 1 ? env.sec.id : `${env.sec.id}--${slug}`;
    let html = `<h${level} id="${id}">`;
    if (level === 1) html += `<span id="${env.sec.id}--${slug}"></span>`;
    const inToc = level === 1 || (level === 2 && env.sec.tocDepth >= 2);
    if (inToc) {
      toc.push({ level, text: plain(text), id, part: env.sec.part || 0 });
      html += addMarker(id);
    }
    return html;
  };
  r.heading_close = (tokens, idx, opts, env) => `</h${Number(tokens[idx].tag.slice(1)) + env.shift}>\n`;

  r.link_open = (tokens, idx, opts, env, self) => {
    const res = resolveHref(tokens[idx].attrGet("href") || "", env);
    env.links.push(Boolean(res.dead));
    if (res.dead) return '<span class="deadlink">';
    tokens[idx].attrSet("href", res.href);
    return self.renderToken(tokens, idx, opts);
  };
  r.link_close = (tokens, idx, opts, env, self) => (env.links.pop() ? "</span>" : self.renderToken(tokens, idx, opts));

  r.image = (tokens, idx, opts, env) => {
    const t = tokens[idx];
    let src = t.attrGet("src");
    if (/^https?:/.test(src)) return "";  // значки и внешние картинки в PDF не нужны
    if (!/^(data:|file:)/.test(src)) src = new URL(normalize(dirOf(env.sec.file) + src), BOOK.rootUrl).href;
    return `<img src="${esc(src)}" alt="${esc(t.content)}">`;
  };

  r.fence = (tokens, idx) => {
    const t = tokens[idx];
    const lang = (t.info || "").trim().split(/\s+/)[0].toLowerCase();
    if (lang === "mermaid") return `<div class="mermaid">${esc(t.content)}</div>\n`;
    const lines = t.content.split("\n").length;
    const cls = [lang === "text" ? "output" : "", lines <= 16 ? "short" : ""].join(" ").trim();
    const label = LANGS[lang] ? `<span class="lang">${LANGS[lang]}</span>` : "";
    return `<pre class="${cls}">${label}<code>${esc(t.content.replace(/\n$/, ""))}</code></pre>\n`;
  };

  function render(src, sec, shift = 0) {
    src = src.replace(/<!-- toc -->[\s\S]*?<!-- \/toc -->/g, "");
    return md.render(src, { sec, shift, slugs: {}, quotes: [], links: [], });
  }

  const book = document.getElementById("book");
  const parts = [];
  for (const sec of BOOK.sections) {
    try {
      if (sec.kind === "html") {
        parts.push(sec.html.replace(/\{\{MARK:([^}]+)\}\}/g, (_, id) => addMarker(id)));
        if (sec.tocEntry) toc.push(sec.tocEntry);
      } else if (sec.kind === "md") {
        parts.push(`<section class="doc" id="sec-${sec.id}">${render(sec.md, sec)}</section>`);
      } else if (sec.kind === "templates") {
        let html = render(sec.intro, sec);
        for (const tpl of sec.items) {
          const sub = { id: tpl.id, file: tpl.file, part: sec.part, tocDepth: 0 };
          toc.push({ level: 2, text: tpl.title, id: tpl.id, part: sec.part });
          html += `<h2 id="${tpl.id}">${addMarker(tpl.id)}${esc(tpl.title)}</h2>`;
          html += `<p class="appendix-file">Файл: <code>${esc(tpl.file)}</code></p>`;
          html += tpl.asCode
            ? `<pre class="${"template"}"><span class="lang">Markdown — исходный текст</span><code>${esc(tpl.md)}</code></pre>`
            : render(tpl.md.replace(/^# .*\n/, ""), sub, 1);
        }
        parts.push(`<section class="doc" id="sec-${sec.id}">${html}</section>`);
      }
    } catch (e) {
      errors.push(`render ${sec.id || sec.kind}: ${e.stack || e}`);
    }
  }
  book.innerHTML = parts.join("\n");

  // Оглавление
  const pages = BOOK.tocPages || {};
  const partTitles = BOOK.partTitles;
  let html = '<h1 id="toc">Содержание</h1>';
  let lastPart = -1;
  for (const e of toc) {
    if (e.id === "toc" || e.divider) continue;
    if (e.part !== lastPart) {
      if (partTitles[e.part]) html += `<div class="part">${esc(partTitles[e.part])}</div>`;
      lastPart = e.part;
    }
    const cls = e.level === 1 ? "l1" : "l2";
    html += `<a class="toc-row ${cls}" href="#${e.id}"><span class="t">${esc(e.text)}</span><span class="dots"></span><span class="p">${pages[e.id] || ""}</span></a>`;
  }
  document.getElementById("toc-list").innerHTML = html;

  document.querySelectorAll("details").forEach((d) => (d.open = true));
  // Таблицы-карточки с пустой строкой заголовка: в PDF она не нужна
  document.querySelectorAll("thead").forEach((head) => {
    if (![...head.querySelectorAll("th")].some((c) => c.textContent.trim())) head.remove();
  });

  try {
    await document.fonts.ready;
    await Promise.all([...document.images].map((img) =>
      img.complete ? null : new Promise((res) => { img.onload = img.onerror = res; })));
    for (const img of document.images) if (!img.naturalWidth) errors.push("image not loaded: " + img.src);

    for (const node of document.querySelectorAll(".mermaid")) {
      const code = node.textContent;
      try {
        await mermaid.parse(code);
        await mermaid.run({ nodes: [node] });
      } catch (e) {
        errors.push("mermaid: " + (e.message || e).toString().slice(0, 300) + " :: " + code.slice(0, 80));
      }
    }
  } catch (e) {
    errors.push("finish: " + (e.stack || e));
  }
  window.__ready = true;
})();
