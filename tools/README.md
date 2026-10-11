# Инструменты методички

Скрипты для тех, кто поддерживает методичку: перерисовать схемы, обновить оглавления, проверить ссылки и собрать PDF. Запускайте их из корня папки `git-github-guide`.

| Скрипт | Что делает | Требования |
| --- | --- | --- |
| `make_images.py` | Рисует все SVG-схемы в папке `images/`. Текст схем меняется в коде функций | Python 3.11+ |
| `toc.py` | Обновляет блоки «Содержание главы» между метками `<!-- toc -->` и `<!-- /toc -->`. Якоря строятся по правилам GitHub | Python 3.11+ |
| `check_links.py` | Проверяет относительные ссылки, якоря и изображения; с `--web` — ещё и внешние ссылки | Python 3.11+; для `--web` — интернет |
| `build_pdf.mjs` | Собирает `git-github-guide.pdf`: обложка, оглавление с номерами страниц, главы, приложения, закладки | Node.js 22+, Microsoft Edge или Google Chrome, Python с пакетом PyMuPDF |
| `cdp.mjs` | Управление браузером через Chrome DevTools Protocol | Используется `build_pdf.mjs` и `make_hero.mjs` |
| `pdf_render.js`, `pdf.css` | Отрисовка Markdown и Mermaid в браузере и оформление страниц PDF | Используются `build_pdf.mjs` |
| `pdf_pages.py` | Находит номера страниц заголовков и добавляет закладки в PDF | PyMuPDF |
| `make_hero.mjs` | Снимает кадры анимации из `hero.html` и собирает `images/hero-light.gif`, `images/hero-dark.gif` и картинку для соцсетей `images/social-preview.png` | Node.js 22+, Edge или Chrome, Python с пакетом Pillow, интернет (шрифты Google Fonts) |
| `hero.html`, `frames_to_gif.py` | Сцена анимации (терминал и граф коммитов) и склейка кадров в GIF с точным цветом фона | Используются `make_hero.mjs` |

## Типичный порядок после правок

```powershell
python tools/make_images.py      # если меняли схемы
python tools/toc.py              # если меняли заголовки разделов
python tools/check_links.py      # проверка ссылок и якорей
node tools/build_pdf.mjs         # новая PDF-версия
```

Те же проверки оглавлений, схем и ссылок запускаются на GitHub автоматически при каждом push в `main` и в каждом Pull Request — см. `.github/workflows/checks.yml`.

## Анимация для README

```powershell
python -m pip install pillow
node tools/make_hero.mjs
```

Сцена описана в `hero.html`: команды, подписи и тайминги — в массиве `STEPS`. Чтобы посмотреть анимацию без сборки, откройте в браузере `hero.html?play` (тёмная тема — `hero.html?play&theme=dark`, картинка для соцсетей — `hero.html?mode=social`). Частоту кадров меняет переменная `HERO_FPS` (по умолчанию 20; меньше — легче файл).

Картинку `images/social-preview.png` загружают вручную: **Settings** → **General** → **Social preview** → **Edit** → **Upload an image**.

## Сборка PDF

1. Установите PyMuPDF, если его нет: `python -m pip install pymupdf`.
2. Выполните `node tools/build_pdf.mjs`.

Браузер загружает библиотеки markdown-it 14.1.0 и Mermaid 11.17.2 с `cdn.jsdelivr.net`. Чтобы собрать без интернета, скачайте эти файлы заранее и укажите пути:

```powershell
$env:MARKDOWN_IT_JS = "C:\path\to\markdown-it.min.js"
$env:MERMAID_JS = "C:\path\to\mermaid.min.js"
node tools/build_pdf.mjs
```

Если браузер установлен в нестандартное место, укажите путь в переменной `BROWSER_PATH`. Переменная `KEEP_BUILD=1` сохраняет промежуточные HTML и PDF для отладки.

Ссылки на файлы, которых нет в PDF (например, `CONTRIBUTING.md` или `LICENSE`), ведут на их страницы на GitHub. Блоки README между метками `<!-- pdf:skip -->` и `<!-- /pdf:skip -->` (анимация, значки, кнопки) в PDF не попадают.

Сборка останавливается с ошибкой, если не удалось нарисовать диаграмму Mermaid или загрузить локальное изображение, — так ошибки не попадут в PDF незамеченными.
