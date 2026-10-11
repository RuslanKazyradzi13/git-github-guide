"""Вспомогательный скрипт сборки PDF (нужен пакет PyMuPDF).

python pdf_pages.py find <pdf> <markers.json>
    Находит невидимые метки заголовков и печатает JSON {id: номер страницы}.
python pdf_pages.py finish <pdf> <outline.json> <out.pdf>
    Добавляет закладки и метаданные, сохраняет итоговый PDF.
"""

import json
import re
import sys

try:
    import pymupdf as fitz  # PyMuPDF
except ImportError:  # старые версии PyMuPDF
    import fitz


def find(pdf_path, markers_path):
    with open(markers_path, encoding="utf-8") as f:
        markers = json.load(f)
    pages = {}
    with fitz.open(pdf_path) as doc:
        for number, page in enumerate(doc, start=1):
            for code in re.findall(r"QQPM\d+QQ", page.get_text()):
                if code in markers:
                    pages.setdefault(markers[code], number)
    print(json.dumps(pages))


def finish(pdf_path, outline_path, out_path):
    with open(outline_path, encoding="utf-8") as f:
        entries = json.load(f)
    toc = []
    for e in entries:
        if e.get("divider"):
            toc.append([1, e["text"], e["page"]])
            continue
        if e["part"] == 0:
            level = e["level"]
        else:
            level = e["level"] + 1
        toc.append([level, e["text"], e["page"]])
    # Закладки не должны «перепрыгивать» уровни
    fixed, prev = [], 0
    for level, title, page in toc:
        level = min(level, prev + 1) if fixed else 1
        fixed.append([level, title, page])
        prev = level
    with fitz.open(pdf_path) as doc:
        doc.set_toc(fixed)
        doc.set_metadata({
            "title": "Git и GitHub с нуля",
            "author": "Ruslan Kazyradzi",
            "subject": "Методичка по Git, GitHub и оформлению программных проектов",
            "keywords": "Git, GitHub, Pull Request, лицензии, SemVer, CI, безопасность",
            "creator": "tools/build_pdf.mjs",
            "producer": "Chromium + PyMuPDF",
        })
        pages = doc.page_count
        doc.save(out_path, garbage=3, deflate=True)
    print(f"страниц: {pages}, закладок: {len(fixed)}")


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "find":
        find(sys.argv[2], sys.argv[3])
    elif mode == "finish":
        finish(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        sys.exit("неизвестный режим: " + mode)
