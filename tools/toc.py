"""Оглавления глав и якоря заголовков в стиле GitHub.

Скрипт находит в файлах глав метки <!-- toc --> и <!-- /toc -->
и вставляет между ними список разделов второго уровня (##).

    python tools/toc.py
"""

from __future__ import annotations

import pathlib
import re
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOC_RE = re.compile(r"<!-- toc -->.*?<!-- /toc -->", re.S)


def github_slug(text: str) -> str:
    """Якорь заголовка так, как его строит GitHub (github-slugger)."""
    text = re.sub(r"`([^`]*)`", r"\1", text)          # код без обратных кавычек
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # ссылки — только текст
    text = text.replace("**", "").replace("*", "")
    out = []
    for ch in text.lower():
        cat = unicodedata.category(ch)
        if ch in "-_ " or cat[0] in "LNM":
            out.append(ch)
    return "".join(out).replace(" ", "-")


def headings(md: str):
    """Заголовки (уровень, текст, якорь) вне блоков кода; дубликаты получают -1, -2."""
    seen: dict[str, int] = {}
    in_code = False
    for line in md.splitlines():
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if not m:
            continue
        level, title = len(m.group(1)), m.group(2)
        base = github_slug(title)
        n = seen.get(base, 0)
        seen[base] = n + 1
        yield level, title, base if n == 0 else f"{base}-{n}"


def build_toc(md: str) -> str:
    items = [f"- [{title}](#{slug})" for level, title, slug in headings(md) if level == 2]
    return "<!-- toc -->\n**Содержание главы**\n\n" + "\n".join(items) + "\n<!-- /toc -->"


def main():
    for path in sorted(ROOT.glob("[0-9][0-9]_*.md")):
        md = path.read_text(encoding="utf-8")
        if "<!-- toc -->" not in md:
            continue
        new = TOC_RE.sub(lambda _: build_toc(md), md)
        if new != md:
            path.write_text(new, encoding="utf-8", newline="\n")
            print("toc", path.name)


if __name__ == "__main__":
    main()
