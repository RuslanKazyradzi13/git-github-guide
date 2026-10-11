"""Проверка ссылок и изображений в Markdown-файлах методички.

    python tools/check_links.py            # локальные файлы и якоря
    python tools/check_links.py --web      # плюс внешние ссылки (нужен интернет)

Проверяет: существуют ли файлы, на которые ведут относительные ссылки;
есть ли нужный заголовок для ссылок с якорем (#...); существуют ли изображения.
"""

from __future__ import annotations

import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from toc import github_slug, headings  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
AUTOLINK_RE = re.compile(r"<(https?://[^>\s]+)>")
EXPLICIT_ANCHOR_RE = re.compile(r"""<a\s+(?:id|name)=["']([^"']+)["']""")


def strip_code(md: str) -> str:
    """Убирает блоки кода, HTML-комментарии и `код`, чтобы не проверять ссылки в примерах."""
    md = re.sub(r"```.*?```", "", md, flags=re.S)
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", md)


def anchors_of(path: pathlib.Path) -> set[str]:
    md = path.read_text(encoding="utf-8")
    found = {slug for _, _, slug in headings(md)}
    found |= set(EXPLICIT_ANCHOR_RE.findall(md))
    return found


def collect():
    files = [p for p in ROOT.rglob("*.md") if "node_modules" not in p.parts]
    local, web = [], set()
    for f in files:
        text = strip_code(f.read_text(encoding="utf-8"))
        for bang, _, target in LINK_RE.findall(text):
            if target.startswith(("http://", "https://")):
                web.add(target)
            elif target.startswith("mailto:"):
                continue
            elif f.parent.name == "templates" and not target.startswith("../"):
                # ссылки шаблонов ведут на файлы будущего проекта, а не методички
                continue
            else:
                local.append((f, target, bool(bang)))
        web.update(AUTOLINK_RE.findall(text))
    return files, local, web


def check_local(local):
    errors = []
    cache: dict[pathlib.Path, set[str]] = {}
    for src, target, is_image in local:
        raw_path, _, anchor = target.partition("#")
        path = urllib.parse.unquote(raw_path)
        dest = (src.parent / path).resolve() if path else src
        if not dest.exists():
            errors.append(f"{src.relative_to(ROOT)}: нет файла {target}")
            continue
        if anchor and dest.suffix == ".md":
            if dest not in cache:
                cache[dest] = anchors_of(dest)
            if urllib.parse.unquote(anchor) not in cache[dest]:
                errors.append(f"{src.relative_to(ROOT)}: нет якоря #{anchor} в {dest.name}")
    return errors


PLACEHOLDERS = ("OWNER", "ВЛАДЕЛЕЦ", "[")
BOT_PROTECTED = ("iso.org", "github.com/signup")  # отвечают 403 на автоматические запросы


def check_url(url: str):
    if any(p in url for p in PLACEHOLDERS):
        return url, "заполнитель"
    safe = urllib.parse.quote(url, safe=":/?#[]@!$&'()*+,;=%-._~")
    req = urllib.request.Request(safe, headers={"User-Agent": "Mozilla/5.0 (link check)"})
    for method in ("HEAD", "GET"):
        req.method = method
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return url, r.status
        except urllib.error.HTTPError as e:
            if method == "GET":
                return url, e.code
        except Exception as e:  # сеть, TLS, тайм-аут
            if method == "GET":
                return url, f"ошибка: {type(e).__name__}"
    return url, "?"


def main():
    files, local, web = collect()
    errors = check_local(local)
    print(f"Файлов Markdown: {len(files)}; локальных ссылок и изображений: {len(local)}; внешних ссылок: {len(web)}")
    for e in errors:
        print("ОШИБКА", e)
    if "--web" in sys.argv:
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = sorted(pool.map(check_url, sorted(web)))
        placeholders = [u for u, s in results if s == "заполнитель"]
        protected = [(u, s) for u, s in results if s == 403 and any(b in u for b in BOT_PROTECTED)]
        bad = [(u, s) for u, s in results
               if not (isinstance(s, int) and s < 400) and s != "заполнитель" and (u, s) not in protected]
        print(f"Внешние ссылки: {len(results) - len(bad) - len(placeholders) - len(protected)} доступны, "
              f"{len(placeholders)} — заполнители в шаблонах, {len(protected)} — сайт запрещает автоматическую "
              f"проверку (403), {len(bad)} — с ошибкой")
        for u, s in protected:
            print("ПРОВЕРИТЬ ВРУЧНУЮ", s, u)
        for u, s in bad:
            print("ВНЕШНЯЯ", s, u)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
