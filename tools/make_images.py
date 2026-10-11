"""Генератор учебных SVG-схем для методички.

Все схемы рисуются из кода, чтобы их было легко исправлять:
поменяйте текст в функции нужной схемы и запустите

    python tools/make_images.py

Файлы появятся в папке images/. Стиль: минимализм, палитра Google.
"""

from __future__ import annotations

import math
import pathlib
import re
from xml.sax.saxutils import escape

OUT = pathlib.Path(__file__).resolve().parent.parent / "images"

FONT = "'Google Sans','Roboto','Segoe UI',Arial,sans-serif"
MONO = "'Roboto Mono',Consolas,'Cascadia Mono','Courier New',monospace"

# цвет: (линия, заливка, тёмный текст)
C = {
    "blue": ("#1A73E8", "#E8F0FE", "#174EA6"),
    "green": ("#1E8E3E", "#E6F4EA", "#0D652D"),
    "red": ("#D93025", "#FCE8E6", "#A50E0E"),
    "yellow": ("#F9AB00", "#FEF7E0", "#9A5B00"),
    "grey": ("#5F6368", "#F1F3F4", "#3C4043"),
    "purple": ("#9334E6", "#F3E8FD", "#681DA8"),
}
INK = "#202124"
MUTED = "#5F6368"
LINE = "#DADCE0"
CODEBG = "#F8F9FA"


def esc(s: str) -> str:
    return escape(s, {'"': "&quot;"})


def char_w(ch: str, mono: bool) -> float:
    if mono:
        return 0.6
    if ch == " ":
        return 0.28
    if ch in "iljI.,:;!|'()[]·–":
        return 0.3
    if ch in "mwшщжюфыМШЩЖЮФЫW—":
        return 0.82
    if ch.isupper():
        return 0.66
    if ch.isdigit():
        return 0.55
    return 0.55


def segments(s: str):
    """Разбивает строку на части: `код` рисуется моноширинным шрифтом."""
    parts = re.split(r"(`[^`]*`)", s)
    for p in parts:
        if not p:
            continue
        if p.startswith("`") and p.endswith("`"):
            yield p[1:-1], True
        else:
            yield p, False


def text_width(s: str, size: float, mono: bool = False) -> float:
    total = 0.0
    for seg, m in segments(s):
        total += sum(char_w(ch, m or mono) for ch in seg) * size
    return total


def wrap(s: str, width: float, size: float, mono: bool = False) -> list[str]:
    words = s.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        # не разрываем `код` посередине: считаем ширину с учётом разметки
        if text_width(trial, size, mono) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    # если перенос разорвал `...`, склеиваем обратно
    fixed, buf = [], ""
    for ln in lines:
        buf = (buf + " " + ln).strip() if buf else ln
        if buf.count("`") % 2 == 0:
            fixed.append(buf)
            buf = ""
    if buf:
        fixed.append(buf)
    return fixed


class D:
    """Холст одной схемы."""

    def __init__(self, w, h, title=None, subtitle=None, badge=None):
        self.w, self.h = w, h
        self.el: list[str] = []
        self.rect(0.5, 0.5, w - 1, h - 1, "#FFFFFF", LINE, 16, sw=1)
        if title:
            self.text(40, 54, title, 24, INK, 500)
        if subtitle:
            y = 84
            for ln in wrap(subtitle, w - 80 - (190 if badge else 0), 15):
                self.text(40, y, ln, 15, MUTED)
                y += 21
        if badge:
            self.badge(w - 40, 48, badge)

    # --- примитивы -------------------------------------------------------
    def rect(self, x, y, w, h, fill="none", stroke=None, rx=12, sw=1.5, dash=None, opacity=None):
        a = f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx:g}" fill="{fill}"'
        if stroke:
            a += f' stroke="{stroke}" stroke-width="{sw:g}"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if opacity is not None:
            a += f' opacity="{opacity:g}"'
        self.el.append(a + "/>")

    def text(self, x, y, s, size=15, color=INK, weight=400, anchor="start", mono=False,
             italic=False, spacing=None):
        attrs = f'x="{x:g}" y="{y:g}" font-size="{size:g}" fill="{color}"'
        if weight != 400:
            attrs += f' font-weight="{weight}"'
        if anchor != "start":
            attrs += f' text-anchor="{anchor}"'
        if italic:
            attrs += ' font-style="italic"'
        if spacing:
            attrs += f' letter-spacing="{spacing:g}"'
        cls = ' class="m"' if mono else ""
        inner = ""
        for seg, m in segments(s):
            if m and not mono:
                inner += f'<tspan class="m">{esc(seg)}</tspan>'
            else:
                inner += esc(seg)
        self.el.append(f"<text{cls} {attrs}>{inner}</text>")

    def para(self, x, y, s, width, size=15, color=INK, lh=1.45, weight=400, anchor="start",
             mono=False):
        """Текст с переносом. Возвращает y следующей строки."""
        for ln in wrap(s, width, size, mono):
            self.text(x, y, ln, size, color, weight, anchor, mono)
            y += size * lh
        return y

    def line(self, x1, y1, x2, y2, color=LINE, sw=1.5, dash=None):
        a = f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" stroke="{color}" stroke-width="{sw:g}"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        self.el.append(a + "/>")

    def path(self, d, color=MUTED, sw=1.6, dash=None, head=True, fill="none"):
        key = next((k for k, v in C.items() if v[0] == color), "grey")
        a = f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{sw:g}" stroke-linecap="round" stroke-linejoin="round"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if head:
            a += f' marker-end="url(#ah-{key})"'
        self.el.append(a + "/>")

    def arrow(self, x1, y1, x2, y2, color=MUTED, sw=1.6, dash=None, head=True):
        self.path(f"M{x1:g},{y1:g} L{x2:g},{y2:g}", color, sw, dash, head)

    def circle(self, cx, cy, r, fill, stroke=None, sw=2):
        a = f'<circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" fill="{fill}"'
        if stroke:
            a += f' stroke="{stroke}" stroke-width="{sw:g}"'
        self.el.append(a + "/>")

    def num(self, cx, cy, n, color="blue", r=13):
        self.circle(cx, cy, r, C[color][0])
        self.text(cx, cy + 5, str(n), 14, "#FFFFFF", 600, "middle")

    def pill(self, cx, cy, s, color="grey", mono=True, size=13.5, filled=False, h=26):
        w = text_width(s, size, mono) + 22
        stroke, tint, dark = C[color]
        self.rect(cx - w / 2, cy - h / 2, w, h, tint if filled else "#FFFFFF", stroke, h / 2, sw=1.2)
        self.text(cx, cy + size * 0.36, s, size, dark, 500 if not mono else 400, "middle", mono)
        return w

    def badge(self, right_x, cy, s, color="yellow"):
        size = 12.5
        w = text_width(s, size) + 24
        stroke, tint, dark = C[color]
        self.rect(right_x - w, cy - 13, w, 26, tint, None, 13)
        self.text(right_x - w / 2, cy + 4.5, s, size, dark, 600, "middle")

    def label(self, x, y, s, color=MUTED):
        """Мелкая подпись группы прописными буквами."""
        self.text(x, y, s.upper(), 11.5, color, 600, spacing=1.2)

    def card(self, x, y, w, h, color, title=None, sub=None, body=None, pad=18,
             title_size=17, body_size=14.5, center=False, body_color=INK, outline=False):
        stroke, tint, dark = C[color]
        self.rect(x, y, w, h, "#FFFFFF" if outline else tint, stroke if outline else None, 12)
        cx = x + w / 2
        tx = cx if center else x + pad
        anchor = "middle" if center else "start"
        cy = y + pad + title_size * 0.8
        if title:
            for ln in wrap(title, w - 2 * pad, title_size):
                self.text(tx, cy, ln, title_size, dark, 600, anchor)
                cy += title_size * 1.3
            cy += 2
        if sub:
            self.text(tx, cy, sub, 13, MUTED, 400, anchor, mono=True)
            cy += 24
        if body:
            if title or sub:
                cy += 4
            for item in body if isinstance(body, list) else [body]:
                cy = self.para(tx, cy, item, w - 2 * pad, body_size, body_color, anchor=anchor)
        return cy

    def step(self, x, y, w, h, n, title, sub=None, color="blue", sub_mono=False):
        stroke, tint, dark = C[color]
        self.rect(x, y, w, h, tint, None, 12)
        self.num(x + 28, y + 30, n, color)
        self.text(x + 50, y + 35, title, 16, dark, 600)
        if sub:
            if sub_mono or (sub.startswith("`") and sub.endswith("`")):
                self.text(x + 18, y + h - 22, sub.strip("`"), 13, INK, 400, mono=True)
            elif "`" in sub:
                self.text(x + 18, y + h - 22, sub, 13.5, INK)
            else:
                self.para(x + 18, y + h - 22 - (0 if text_width(sub, 13.5) < w - 36 else 18),
                          sub, w - 36, 13.5, MUTED)

    # --- вывод ------------------------------------------------------------
    def svg(self, desc: str) -> str:
        markers = "".join(
            f'<marker id="ah-{k}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" '
            f'markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{v[0]}"/></marker>'
            for k, v in C.items()
        )
        style = (
            f"<style>text{{font-family:{FONT};}}"
            f".m{{font-family:{MONO};}}</style>"
        )
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
            f'viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{esc(desc)}">'
            f"<title>{esc(desc)}</title>{style}<defs>{markers}</defs>"
            + "".join(self.el)
            + "</svg>\n"
        )


DIAGRAMS: dict[str, tuple] = {}


def diagram(name, desc):
    def deco(fn):
        DIAGRAMS[name] = (fn, desc)
        return fn
    return deco


# ===========================================================================
# Часть I
# ===========================================================================

@diagram("00-roadmap.svg", "Маршрут обучения по главам методички")
def roadmap():
    d = D(960, 400, "Маршрут обучения",
          "Часть I — Git и GitHub с нуля. Часть II — профессиональное оформление проектов.")
    d.label(40, 138, "Часть I · Git и GitHub")
    labels = [("Основы", ""), ("Установка", ""), ("Команды", ""), ("GitHub", ""),
              ("Ветки", "и PR"), ("Ошибки", "и откат"), ("Git и", "Claude Code"), ("Итоговая", "практика")]
    w, gap = 100, (880 - 8 * 100) / 7
    for i, (a, b) in enumerate(labels):
        x = 40 + i * (w + gap)
        d.rect(x, 152, w, 96, C["blue"][1], None, 12)
        d.text(x + 14, 188, str(i + 1), 24, C["blue"][2], 600)
        d.text(x + 14, 214, a, 13.5, INK, 500)
        if b:
            d.text(x + 14, 232, b, 13.5, INK, 500)
    d.label(40, 290, "Часть II · Профессиональные проекты")
    items = [("9", "Структура, README, стандарты"), ("10", "Лицензии и авторские права"),
             ("11", "Безопасность и автоматизация")]
    w2 = (880 - 20) / 3
    for i, (n, t) in enumerate(items):
        x = 40 + i * (w2 + 10)
        d.rect(x, 304, w2, 60, C["green"][1], None, 12)
        d.text(x + 16, 341, n, 22, C["green"][2], 600)
        d.text(x + 56, 340, t, 14.5, INK, 500)
    return d


@diagram("01-git-vs-github.svg", "Инфографика: чем Git отличается от GitHub")
def git_vs_github():
    d = D(960, 540, "Git и GitHub: в чём разница",
          "Git сохраняет версии на вашем компьютере. GitHub хранит копию проекта в интернете и помогает работать вместе.")
    cols = [
        (40, "blue", "Git", "программа на вашем компьютере",
         ["Запоминает каждую сохранённую версию", "Работает без интернета",
          "Бесплатная, с открытым исходным кодом", "Управляется командами в терминале"],
         "История версий документа"),
        (550, "green", "GitHub", "сайт и облачный сервис",
         ["Хранит копию репозитория в интернете", "Показывает историю и изменения",
          "Pull Request, Issues, автопроверки", "Нужны интернет и аккаунт"],
         "Облачный диск и рабочее место команды"),
    ]
    for x, col, name, tag, bullets, analogy in cols:
        stroke, tint, dark = C[col]
        d.rect(x, 124, 370, 340, tint, None, 14)
        d.text(x + 26, 172, name, 30, dark, 600)
        d.text(x + 26, 198, tag, 15, MUTED)
        y = 240
        for b in bullets:
            d.circle(x + 31, y - 5, 3.2, stroke)
            d.text(x + 44, y, b, 15, INK)
            y += 34
        d.rect(x + 18, 384, 334, 62, "#FFFFFF", None, 10)
        d.text(x + 34, 408, "Аналогия", 12.5, MUTED, 500)
        d.text(x + 34, 432, analogy, 15, INK, 500)
    d.arrow(424, 250, 542, 250, C["blue"][0])
    d.pill(483, 250, "git push", "blue")
    d.text(483, 280, "отправить", 13, MUTED, anchor="middle")
    d.arrow(542, 340, 424, 340, C["green"][0])
    d.pill(483, 340, "git pull", "green")
    d.text(483, 370, "получить", 13, MUTED, anchor="middle")
    d.text(480, 506, "Git можно использовать без GitHub. Похожие сервисы: GitLab, Bitbucket, Gitea.",
           14, MUTED, anchor="middle")
    return d


@diagram("01-computer-git-github.svg", "Схема: как связаны вы, Git на компьютере и GitHub")
def computer_git_github():
    d = D(960, 470, "Как связаны вы, Git и GitHub",
          "Вы меняете файлы, Git сохраняет версии, GitHub хранит копию в интернете.")
    d.rect(30, 118, 580, 262, "none", LINE, 16, sw=1.5, dash="6 6")
    d.label(52, 146, "Ваш компьютер")
    d.rect(690, 118, 240, 262, "none", LINE, 16, sw=1.5, dash="6 6")
    d.label(712, 146, "Интернет")
    d.card(52, 166, 210, 190, "yellow", "Рабочая папка", None,
           "Обычная папка с файлами. Вы редактируете их сами или с помощью AI.")
    d.card(380, 166, 210, 190, "blue", "Локальный репозиторий", "папка .git",
           "Хранит историю всех сохранённых версий.")
    d.card(710, 166, 200, 190, "green", "GitHub", "удалённый репозиторий",
           "Копия проекта в интернете. Доступна вам и команде.")
    d.text(321, 226, "git add", 14, C["blue"][2], anchor="middle", mono=True)
    d.text(321, 246, "git commit", 14, C["blue"][2], anchor="middle", mono=True)
    d.arrow(266, 262, 374, 262, C["blue"][0])
    d.text(321, 286, "сохранить версию", 12.5, MUTED, anchor="middle")
    d.arrow(594, 236, 704, 236, C["blue"][0])
    d.pill(649, 236, "git push", "blue")
    d.arrow(704, 300, 594, 300, C["green"][0])
    d.pill(649, 300, "git pull", "green")
    d.text(480, 424, "Всё, что слева, работает без интернета. Интернет нужен только для обмена с GitHub.",
           14, MUTED, anchor="middle")
    return d


@diagram("03-three-areas.svg", "Схема трёх зон Git: рабочая папка, staging area, история коммитов")
def three_areas():
    d = D(960, 560, "Три зоны Git",
          "Изменение проходит путь: рабочая папка → staging area → история коммитов.")
    cards = [
        (40, "yellow", "Рабочая папка", "working directory",
         "Файлы, которые вы видите и редактируете.", "Как рабочий стол"),
        (370, "blue", "Staging area", "индекс",
         "Изменения, отобранные для следующего коммита.", "Как коробка перед отправкой"),
        (700, "green", "История коммитов", "репозиторий .git",
         "Сохранённые снимки проекта.", "Как фотоальбом версий"),
    ]
    for x, col, t, sub, body, analog in cards:
        d.card(x, 116, 220, 190, col, t, sub, body)
        d.text(x + 18, 290, analog, 13, MUTED, italic=True)
    d.text(315, 176, "git add", 14, C["blue"][2], anchor="middle", mono=True)
    d.arrow(264, 196, 366, 196, C["blue"][0])
    d.text(645, 176, "git commit", 14, C["green"][2], anchor="middle", mono=True)
    d.arrow(594, 196, 696, 196, C["green"][0])
    d.path("M440,310 C440,372 150,372 150,314", C["yellow"][0])
    d.pill(295, 360, "git restore <файл>", "yellow")
    d.text(295, 392, "отменить правки в рабочей папке", 12.5, MUTED, anchor="middle")
    d.path("M810,310 C810,372 520,372 520,314", C["blue"][0])
    d.pill(665, 360, "git restore --staged <файл>", "blue")
    d.text(665, 392, "убрать из staging, правки сохранятся", 12.5, MUTED, anchor="middle")
    d.rect(40, 426, 880, 100, C["grey"][1], None, 12)
    d.text(64, 462, "`git status` — показывает, что лежит в каждой зоне", 14.5, INK)
    d.text(64, 494, "`git diff` — рабочая папка против staging   ·   `git diff --staged` — staging против последнего коммита",
           14.5, INK)
    return d


@diagram("03-file-lifecycle.svg", "Жизненный цикл файла в Git: untracked, staged, committed, modified")
def file_lifecycle():
    d = D(960, 490, "Жизненный цикл файла",
          "Git отслеживает состояние каждого файла. Команда git status показывает эти состояния.")
    xs = [40, 366, 692]
    data = [("grey", "Неотслеживаемый", "untracked", "Новый файл. Git за ним ещё не следит."),
            ("blue", "Подготовлен", "staged", "Войдёт в следующий коммит."),
            ("green", "Сохранён", "committed", "Версия записана в историю.")]
    for x, (col, t, s, b) in zip(xs, data):
        d.card(x, 124, 228, 120, col, t, s, b, body_size=14)
    d.text(317, 176, "git add", 14, C["blue"][2], anchor="middle", mono=True)
    d.arrow(272, 194, 362, 194, C["blue"][0])
    d.text(643, 176, "git commit", 14, C["green"][2], anchor="middle", mono=True)
    d.arrow(598, 194, 688, 194, C["green"][0])
    d.card(692, 334, 228, 124, "yellow", "Изменён", "modified", "Файл отредактирован после коммита.",
           body_size=14)
    d.arrow(806, 248, 806, 330, C["yellow"][0])
    d.text(794, 294, "вы меняете файл", 13, MUTED, anchor="end")
    d.path("M688,396 H480 V250", C["blue"][0])
    d.pill(585, 396, "git add", "blue")
    d.para(40, 300, "Пример: создали notes.txt — он неотслеживаемый. После git add — подготовлен. "
                    "После git commit — сохранён. Изменили снова — изменён.", 330, 14, MUTED)
    return d


@diagram("04-local-remote.svg", "Схема локального репозитория на компьютере и удалённого репозитория на GitHub")
def local_remote():
    d = D(960, 640, "Локальный и удалённый репозитории",
          "origin — стандартное имя удалённого репозитория, с которым связан ваш проект.")
    d.rect(30, 116, 520, 400, "none", LINE, 16, dash="6 6")
    d.label(52, 144, "Ваш компьютер")
    d.rect(640, 116, 290, 400, "none", LINE, 16, dash="6 6")
    d.label(662, 144, "GitHub")
    d.rect(60, 160, 300, 56, C["yellow"][1], None, 12)
    d.text(80, 194, "Рабочая папка", 16, C["yellow"][2], 600)
    d.rect(60, 252, 300, 56, C["blue"][1], None, 12)
    d.text(80, 286, "Staging area", 16, C["blue"][2], 600)
    d.arrow(210, 218, 210, 248, C["blue"][0])
    d.text(224, 238, "git add", 13, C["blue"][2], mono=True)
    d.arrow(210, 310, 210, 342, C["blue"][0])
    d.text(224, 331, "git commit", 13, C["blue"][2], mono=True)
    d.rect(60, 346, 460, 150, C["blue"][1], None, 12)
    d.text(80, 376, "Локальный репозиторий (.git)", 16, C["blue"][2], 600)
    d.rect(80, 394, 196, 84, "#FFFFFF", None, 10)
    d.text(96, 424, "main", 15, INK, 600, mono=True)
    d.text(96, 448, "ваша ветка", 13, MUTED)
    d.rect(296, 394, 204, 84, "#FFFFFF", None, 10)
    d.text(312, 424, "origin/main", 15, INK, 600, mono=True)
    d.text(312, 446, "состояние GitHub при", 12.5, MUTED)
    d.text(312, 464, "последней синхронизации", 12.5, MUTED)
    d.rect(660, 346, 250, 150, C["green"][1], None, 12)
    d.text(680, 376, "Удалённый", 16, C["green"][2], 600)
    d.text(680, 396, "репозиторий origin", 16, C["green"][2], 600)
    d.rect(680, 414, 210, 64, "#FFFFFF", None, 10)
    d.text(696, 452, "main", 15, INK, 600, mono=True)
    d.arrow(524, 392, 656, 392, C["blue"][0])
    d.pill(590, 392, "git push", "blue")
    d.arrow(656, 436, 524, 436, C["green"][0])
    d.pill(590, 436, "git fetch", "green")
    d.arrow(656, 480, 524, 480, C["green"][0])
    d.pill(590, 480, "git pull", "green")
    d.path("M785,342 V188 H366", C["grey"][0])
    d.pill(460, 188, "git clone", "grey")
    d.text(460, 216, "первое скачивание проекта", 12.5, MUTED, anchor="middle")
    d.text(40, 556, "`git push` — отправить ваши коммиты на GitHub.", 14.5)
    d.text(40, 584, "`git fetch` — скачать новости с GitHub в origin/main, не меняя ваши файлы.", 14.5)
    d.text(40, 612, "`git pull` — скачать и сразу объединить с вашей веткой (fetch + merge).", 14.5)
    return d


@diagram("05-branching.svg", "Диаграмма ветвления и слияния: ветка feature отходит от main и сливается обратно")
def branching():
    d = D(960, 480, "Ветвление и слияние",
          "Ветка — отдельная линия работы. Main остаётся стабильной, пока вы пробуете новое.")
    blue, green = C["blue"][0], C["green"][0]
    d.path("M90,196 H848", blue, sw=3, head=False)
    d.path("M230,196 C300,196 300,312 370,312 H520 C620,312 700,196 780,196", green, sw=3, head=False)
    for x, lab in [(110, "Начало"), (230, "Стабильная версия"), (580, "Исправление в main")]:
        d.circle(x, 196, 11, "#FFFFFF", blue, 3)
        d.text(x, 168, lab, 13.5, MUTED, anchor="middle")
    d.circle(780, 196, 13, blue)
    d.text(780, 168, "Слияние (merge)", 13.5, C["blue"][2], 600, "middle")
    for x, lab in [(390, "Коммит в ветке"), (510, "Ещё коммит")]:
        d.circle(x, 312, 11, "#FFFFFF", green, 3)
        d.text(x, 346, lab, 13.5, MUTED, anchor="middle")
    d.pill(888, 196, "main", "blue", filled=True)
    d.pill(450, 276, "feature/contacts", "green", filled=True)
    d.num(286, 246, 1, "grey", 11)
    d.num(450, 372, 2, "grey", 11)
    d.num(744, 258, 4, "grey", 11)
    steps = [(1, "`git switch -c feature/contacts` — создать ветку"),
             (2, "Коммиты в ветке: `git add`, `git commit`"),
             (3, "`git switch main` — вернуться в main"),
             (4, "`git merge feature/contacts` — влить в main")]
    for i, (n, t) in enumerate(steps):
        x = 40 + (i % 2) * 450
        y = 412 + (i // 2) * 34
        d.num(x + 11, y - 5, n, "grey", 11)
        d.text(x + 30, y, t, 13.5, INK)
    return d


@diagram("05-pr-flow.svg", "Схема работы через Pull Request: ветка, изменения, коммит, push, Pull Request, проверка, слияние")
def pr_flow():
    d = D(960, 480, "Путь изменения через Pull Request",
          "Pull Request — запрос на слияние. Изменения проверяют до того, как они попадут в main.")
    w, gap = 197, 30
    xs = [40 + i * (w + gap) for i in range(4)]
    row1 = [(1, "Новая ветка", "`git switch -c имя`", "blue"), (2, "Изменения", "правка файлов", "blue"),
            (3, "Коммит", "`git commit`", "blue"), (4, "Отправка", "`git push`", "blue")]
    row2 = [(5, "Pull Request", "открыть на GitHub", "green"), (6, "Проверка", "ревью и автопроверки", "green"),
            (7, "Слияние", "Merge pull request", "green"), (8, "Обновление", "`git pull` в main", "blue")]
    for x, (n, t, s, c) in zip(xs, row1):
        d.step(x, 124, w, 92, n, t, s, c)
    for x, (n, t, s, c) in zip(reversed(xs), row2):
        d.step(x, 290, w, 92, n, t, s, c)
    for i in range(3):
        d.arrow(xs[i] + w + 3, 170, xs[i + 1] - 3, 170, C["blue"][0])
        d.arrow(xs[i + 1] - 3, 336, xs[i] + w + 3, 336, C["green"][0])
    d.path(f"M{xs[3] + w / 2},220 V286", C["blue"][0])
    d.path(f"M{xs[2] + 60},288 C{xs[2] + 40},252 {xs[1] + 150},252 {xs[1] + 140},220",
           C["yellow"][0], dash="5 5")
    d.text(xs[2] + 66, 262, "нужны правки", 12.5, C["yellow"][2])
    d.rect(40, 418, 14, 14, C["blue"][1], C["blue"][0], 3, sw=1)
    d.text(62, 430, "на вашем компьютере", 13.5, MUTED)
    d.rect(250, 418, 14, 14, C["green"][1], C["green"][0], 3, sw=1)
    d.text(272, 430, "на сайте GitHub", 13.5, MUTED)
    return d


@diagram("06-conflict.svg", "Пример конфликта слияния с маркерами <<<<<<<, ======= и >>>>>>>")
def conflict():
    d = D(960, 540, "Как выглядит конфликт слияния",
          "Обе ветки изменили одну и ту же строку. Git не знает, какую версию оставить, и просит выбрать вас.")
    d.rect(40, 124, 480, 290, CODEBG, LINE, 12, sw=1)
    d.text(60, 152, "shopping.txt", 13, MUTED, mono=True)
    d.line(40, 166, 520, 166, LINE, 1)
    lines = [("Список покупок", None), ("<<<<<<< HEAD", "blue"), ("Молоко — 2 литра", "blue"),
             ("=======", "grey"), ("Молоко — 1 литр", "green"), (">>>>>>> feature/milk", "green"),
             ("Хлеб", None)]
    y = 200
    for txt, col in lines:
        if col:
            d.rect(41, y - 21, 478, 32, C[col][1], None, 0)
        color = C[col][2] if col else INK
        d.text(60, y, txt, 15.5, color, 600 if txt[:1] in "<=>" else 400, mono=True)
        y += 32
    notes = [(211, "blue", "Ваша версия", "из текущей ветки (HEAD)"),
             (275, "grey", "Разделитель", "между двумя версиями"),
             (339, "green", "Другая версия", "из ветки feature/milk")]
    for cy, col, t, s in notes:
        d.line(526, cy, 552, cy, C[col][0], 2)
        d.text(564, cy - 3, t, 16, C[col][2], 600)
        d.text(564, cy + 17, s, 13.5, MUTED)
    d.label(40, 452, "Как исправить")
    steps = ["Оставьте нужный текст", "Удалите строки-маркеры", "`git add shopping.txt`", "`git commit`"]
    for i, t in enumerate(steps):
        x = 40 + i * 225
        d.num(x + 13, 487, i + 1, "blue")
        d.text(x + 34, 492, t, 14, INK)
    return d


@diagram("06-recovery.svg", "Таблица выбора команды для отмены изменений с оценкой риска")
def recovery():
    d = D(960, 660, "Как отменить изменения",
          "Найдите свою ситуацию. Цвет показывает, насколько безопасна команда.")
    d.label(40, 132, "Ситуация")
    d.label(420, 132, "Команда")
    d.label(770, 132, "Риск")
    rows = [
        ("Изменили файл, git add не делали. Хотите вернуть как было.", "git restore <файл>",
         "правки в файле будут удалены", ("red", "Удаляет правки")),
        ("Сделали git add, но передумали.", "git restore --staged <файл>",
         "файл останется изменённым", ("green", "Безопасно")),
        ("Нужна версия файла из прошлого коммита.", "git restore --source=<коммит> <файл>",
         "текущее содержимое файла заменится", ("yellow", "Осторожно")),
        ("Ошибочный коммит уже отправлен на GitHub.", "git revert <коммит>",
         "создаёт новый коммит-отмену", ("green", "Безопасно")),
        ("Последний коммит ещё не отправлен. Хотите его переделать.", "git reset --soft HEAD~1",
         "коммит отменён, правки остаются", ("yellow", "Меняет историю")),
        ("Хотите удалить все незакоммиченные правки.", "git reset --hard",
         "вернуть правки будет нельзя", ("red", "Опасно")),
        ("Коммит «потерялся» после reset.", "git reflog",
         "журнал прошлых положений веток", ("green", "Безопасно")),
    ]
    y = 146
    for sit, cmd, note, (col, risk) in rows:
        d.line(40, y, 920, y, LINE, 1)
        d.para(40, y + 28, sit, 350, 14.5, INK)
        d.text(420, y + 28, cmd, 13.5, INK, mono=True)
        d.text(420, y + 50, note, 12.5, MUTED)
        stroke, tint, dark = C[col]
        bw = text_width(risk, 13) + 26
        d.rect(770, y + 13, bw, 26, tint, None, 13)
        d.text(770 + bw / 2, y + 30.5, risk, 13, dark, 600, "middle")
        y += 64
    d.line(40, y, 920, y, LINE, 1)
    legend = [("green", "данные не теряются"), ("yellow", "меняет файл или историю"),
              ("red", "изменения можно потерять навсегда")]
    x = 40
    for col, t in legend:
        d.circle(x + 6, y + 37, 6, C[col][0])
        d.text(x + 20, y + 42, t, 13.5, MUTED)
        x += text_width(t, 13.5) + 60
    return d


@diagram("06-restore-revert-reset.svg", "Сравнение команд git restore, git revert и git reset")
def restore_revert_reset():
    d = D(960, 560, "restore, revert и reset: в чём разница",
          "Три команды отменяют разное. Перед выбором ответьте: изменения уже в коммите? Коммит уже на GitHub?")
    cols = [
        (40, "blue", "git restore", "Отменяет правки в файлах",
         [("Что меняет", "файлы в рабочей папке или staging"), ("История", "не меняется"),
          ("Когда", "правки ещё не закоммичены")], None),
        (340, "green", "git revert", "Отменяет коммит новым коммитом",
         [("Что меняет", "добавляет коммит, обратный старому"), ("История", "дополняется, ничего не стирается"),
          ("Когда", "коммит уже на GitHub")], None),
        (640, "red", "git reset", "Переносит ветку назад",
         [("Что меняет", "положение ветки, иногда файлы"), ("История", "переписывается"),
          ("Когда", "только неотправленные коммиты")], "`--hard` удаляет незакоммиченные правки"),
    ]
    for x, col, cmd, sub, rows, warn in cols:
        stroke, tint, dark = C[col]
        d.rect(x, 124, 280, 410, tint, None, 14)
        d.text(x + 20, 160, cmd, 20, dark, 600, mono=True)
        d.text(x + 20, 186, sub, 14, INK, 500)
        d.rect(x + 16, 202, 248, 90, "#FFFFFF", None, 10)
        y = 322
        for k, v in rows:
            d.text(x + 20, y, k, 12.5, MUTED, 500)
            y = d.para(x + 20, y + 20, v, 240, 14, INK) + 14
        if warn:
            d.para(x + 20, y + 4, "⚠ " + warn, 240, 13, C["red"][2])
    # мини-схема restore: файл сейчас <- версия из коммита
    for fx, lab, col in [(70, "сейчас", "yellow"), (200, "в коммите", "green")]:
        d.rect(fx, 218, 44, 54, "#FFFFFF", C[col][0], 4, sw=1.5)
        for k in range(3):
            d.line(fx + 9, 234 + k * 10, fx + 35, 234 + k * 10, LINE, 2)
        d.text(fx + 22, 286, lab, 11.5, MUTED, anchor="middle")
    d.arrow(196, 245, 120, 245, C["blue"][0])
    # revert: A-B-C-C'
    gx = [370, 430, 490, 556]
    d.line(370, 246, 556, 246, C["green"][0], 2.5)
    for i, x in enumerate(gx):
        last = i == 3
        d.circle(x, 246, 10 if not last else 11, C["green"][0] if last else "#FFFFFF", C["green"][0], 2.5)
        d.text(x, 228, ["A", "B", "C", "−C"][i], 12.5, INK if not last else C["green"][2], 600, "middle")
    d.text(556, 280, "отмена C", 11.5, C["green"][2], anchor="middle")
    # reset: A-B (C)
    d.line(670, 246, 790, 246, C["red"][0], 2.5)
    d.line(790, 246, 850, 246, LINE, 2.5, dash="4 4")
    for i, x in enumerate([670, 730, 790, 850]):
        faded = i == 3
        d.circle(x, 246, 10, "#FFFFFF", LINE if faded else C["red"][0], 2.5)
        d.text(x, 228, "ABC"[i] if i < 3 else "", 12.5, INK, 600, "middle")
    d.text(850, 228, "D", 12.5, "#9AA0A6", 600, "middle")
    d.path("M790,284 L790,262", C["red"][0])
    d.text(808, 282, "main", 12, C["red"][2], 600, mono=True)
    return d


@diagram("07-ai-workflow.svg", "Рабочий цикл с Claude Code и Git: проверка, задача, просмотр, тесты, diff, коммит, push")
def ai_workflow():
    d = D(960, 560, "Рабочий цикл с Claude Code и Git",
          "Каждая задача для AI начинается и заканчивается проверенной версией, сохранённой в Git.")
    w, gap = 197, 30
    xs = [40 + i * (w + gap) for i in range(4)]
    row1 = [(1, "Состояние", "`git status`"), (2, "Задача для AI", "цель и критерии"),
            (3, "Просмотр", "что изменил AI"), (4, "Тесты", "программа работает?")]
    row2 = [(5, "Проверка diff", "`git diff`"), (6, "Коммит", "`git commit`"), (7, "Отправка", "`git push`")]
    for x, (n, t, s) in zip(xs, row1):
        d.step(x, 124, w, 92, n, t, s, "blue")
    for x, (n, t, s) in zip(reversed(xs[1:]), row2):
        d.step(x, 290, w, 92, n, t, s, "green" if n >= 6 else "blue")
    for i in range(3):
        d.arrow(xs[i] + w + 3, 170, xs[i + 1] - 3, 170, C["blue"][0])
    d.arrow(xs[3] - 3, 336, xs[2] + w + 3, 336, C["green"][0])
    d.arrow(xs[2] - 3, 336, xs[1] + w + 3, 336, C["green"][0])
    d.path(f"M{xs[3] + w / 2},220 V286", C["blue"][0])
    d.path(f"M{xs[1] - 4},336 H{xs[0] + w / 2} V220", C["grey"][0])
    d.text(xs[0] + w / 2 + 12, 270, "следующая", 12.5, MUTED)
    d.text(xs[0] + w / 2 + 12, 288, "задача", 12.5, MUTED)
    d.rect(xs[2], 430, w * 2 + gap, 94, C["red"][1], None, 12)
    d.text(xs[2] + 20, 462, "Результат не устроил?", 15.5, C["red"][2], 600)
    d.para(xs[2] + 20, 486, "Не коммитьте. Верните файлы к последнему коммиту (глава 6) и уточните задачу.",
           w * 2 + gap - 40, 13.5, INK)
    d.path(f"M{xs[3] + w / 2},386 V426", C["red"][0], dash="5 5")
    d.para(40, 450, "Главное правило: коммит делаете вы, после проверки. Git хранит только то, что вы закоммитили.",
           370, 14, MUTED)
    return d


# ===========================================================================
# Схемы интерфейса GitHub (не скриншоты)
# ===========================================================================

UI_BADGE = "Схема интерфейса · не скриншот"
GH_GREEN = "#1F883D"


def browser(d: D, x, y, w, h, url):
    d.rect(x, y, w, h, "#FFFFFF", LINE, 12, sw=1.2)
    d.rect(x + 0.6, y + 0.6, w - 1.2, 36, "#F1F3F4", None, 11.5)
    d.rect(x + 0.6, y + 24, w - 1.2, 13, "#F1F3F4", None, 0)
    for i, col in enumerate(["#DADCE0", "#DADCE0", "#DADCE0"]):
        d.circle(x + 18 + i * 14, y + 18, 4.5, col)
    d.rect(x + 70, y + 8, w - 90, 20, "#FFFFFF", None, 10)
    d.text(x + 84, y + 22.5, url, 12, MUTED)


def button(d: D, x, y, w, label, primary=False, h=30):
    if primary:
        d.rect(x, y, w, h, GH_GREEN, None, 6)
        d.text(x + w / 2, y + h / 2 + 4.5, label, 13, "#FFFFFF", 600, "middle")
    else:
        d.rect(x, y, w, h, "#F6F8FA", "#D0D7DE", 6, sw=1)
        d.text(x + w / 2, y + h / 2 + 4.5, label, 13, INK, 500, "middle")


def field(d: D, x, y, w, value, placeholder=False, h=30):
    d.rect(x, y, w, h, "#FFFFFF", "#D0D7DE", 6, sw=1)
    d.text(x + 10, y + h / 2 + 4.5, value, 13, "#8C959F" if placeholder else INK)


def callout(d: D, x, y, n):
    d.circle(x, y, 11, C["blue"][0])
    d.text(x, y + 4.5, str(n), 12.5, "#FFFFFF", 600, "middle")


def legend(d: D, x, y, items, width=280):
    for i, t in enumerate(items):
        callout(d, x + 11, y - 5, i + 1)
        y = d.para(x + 32, y, t, width - 32, 14, INK) + 14
    return y


@diagram("ui-new-repo.svg", "Схема формы создания репозитория на GitHub (не скриншот)")
def ui_new_repo():
    d = D(960, 640, "Создание репозитория на GitHub", "Кнопка + в правом верхнем углу → New repository.",
          badge=UI_BADGE)
    browser(d, 40, 112, 560, 500, "github.com/new")
    x0 = 64
    d.text(x0, 184, "Create a new repository", 18, INK, 600)
    d.text(x0, 214, "Owner", 12.5, MUTED, 500)
    field(d, x0, 222, 160, "ivan-petrov  ▾")
    d.text(x0 + 172, 243, "/", 18, MUTED)
    d.text(x0 + 192, 214, "Repository name", 12.5, MUTED, 500)
    field(d, x0 + 192, 222, 300, "my-first-repo")
    callout(d, 578, 237, 1)
    d.text(x0, 280, "Description (optional)", 12.5, MUTED, 500)
    field(d, x0, 288, 492, "Мой первый репозиторий")
    callout(d, 578, 303, 2)
    d.text(x0, 346, "Visibility", 12.5, MUTED, 500)
    d.circle(x0 + 8, 370, 6.5, "#FFFFFF", C["blue"][0], 4.5)
    d.text(x0 + 22, 375, "Public", 13.5, INK, 500)
    d.circle(x0 + 108, 370, 6.5, "#FFFFFF", "#8C959F", 1.2)
    d.text(x0 + 122, 375, "Private", 13.5, INK)
    callout(d, 578, 370, 3)
    rows = [("README", None), (".gitignore", "None  ▾"), ("License", "None  ▾")]
    y = 404
    for label, val in rows:
        d.line(x0, y, x0 + 492, y, "#EAEEF2", 1)
        d.text(x0, y + 26, label, 13.5, INK, 500)
        if val:
            field(d, x0 + 352, y + 8, 140, val, h=28)
        else:
            d.rect(x0 + 452, y + 12, 40, 20, "#D0D7DE", None, 10)
            d.circle(x0 + 463, y + 22, 7, "#FFFFFF")
        y += 42
    callout(d, 578, 467, 4)
    button(d, x0, 552, 170, "Create repository", primary=True, h=34)
    callout(d, 254, 569, 5)
    legend(d, 636, 150, [
        "Владелец и имя репозитория. Имя — латиницей, без пробелов.",
        "Описание — по желанию, одна строка о проекте.",
        "Public — видят все. Private — только вы и приглашённые люди.",
        "README, .gitignore и лицензия. Для нового проекта их можно добавить. "
        "Если загружаете готовый проект с компьютера — оставьте выключенными.",
        "Создать репозиторий.",
    ])
    return d


@diagram("ui-repo-page.svg", "Схема страницы репозитория на GitHub (не скриншот)")
def ui_repo_page():
    d = D(960, 620, "Страница репозитория", "Главные элементы, которые понадобятся новичку.", badge=UI_BADGE)
    browser(d, 40, 112, 560, 480, "github.com/ivan-petrov/my-first-repo")
    x0 = 64
    d.text(x0, 184, "ivan-petrov / my-first-repo", 17, INK, 600)
    d.rect(x0 + 238, 170, 52, 20, "#FFFFFF", "#D0D7DE", 10, sw=1)
    d.text(x0 + 264, 184, "Public", 11.5, MUTED, 500, "middle")
    tabs = ["Code", "Issues", "Pull requests", "Actions", "Settings"]
    tx = x0
    for i, t in enumerate(tabs):
        d.text(tx, 220, t, 13, INK, 600 if i == 0 else 400)
        if i == 0:
            d.rect(tx - 4, 228, text_width(t, 13) + 8, 3, "#FD8C73", None, 1.5)
        tx += text_width(t, 13) + 26
    d.line(40, 232, 600, 232, "#D8DEE4", 1)
    callout(d, 578, 216, 1)
    button(d, x0, 246, 82, "main  ▾")
    callout(d, x0 + 96, 261, 2)
    button(d, 362, 246, 86, "Add file  ▾")
    button(d, 456, 246, 92, "Code  ▾", primary=True)
    callout(d, 362, 292, 3)
    callout(d, 548, 292, 4)
    d.rect(x0, 306, 492, 34, "#F6F8FA", "#D0D7DE", 6, sw=1)
    d.text(x0 + 12, 328, "ivan-petrov  Добавить файл hello.txt", 12.5, INK)
    d.text(x0 + 480, 328, "⟲ 3 Commits", 12.5, INK, 600, "end")
    callout(d, 578, 323, 5)
    for i, (f, m) in enumerate([("README.md", "Initial commit"), ("hello.txt", "Добавить файл hello.txt")]):
        y = 340 + i * 32
        d.rect(x0, y, 492, 32, "#FFFFFF", "#D0D7DE", 0, sw=1)
        d.text(x0 + 12, y + 21, "▤  " + f, 12.5, INK)
        d.text(x0 + 220, y + 21, m, 12.5, MUTED)
    d.rect(x0, 420, 492, 150, "#FFFFFF", "#D0D7DE", 6, sw=1)
    d.text(x0 + 12, 442, "README", 12.5, MUTED, 600)
    d.line(x0, 452, x0 + 492, 452, "#D8DEE4", 1)
    d.text(x0 + 16, 494, "my-first-repo", 22, INK, 600)
    d.line(x0 + 16, 506, x0 + 476, 506, "#D8DEE4", 1)
    d.text(x0 + 16, 534, "Мой первый репозиторий.", 13.5, INK)
    legend(d, 636, 150, [
        "Вкладки: код, задачи (Issues), Pull Request, автоматизация (Actions), настройки.",
        "Текущая ветка. Нажмите, чтобы переключиться на другую.",
        "Add file: создать новый файл или загрузить файлы с компьютера.",
        "Code: адрес для git clone и скачивание архива (Download ZIP).",
        "Число коммитов. Ссылка ведёт в историю изменений.",
    ])
    return d


@diagram("ui-commit-dialog.svg", "Схема окна сохранения изменений на сайте GitHub (не скриншот)")
def ui_commit_dialog():
    d = D(960, 520, "Сохранение изменений на сайте", "Окно открывается кнопкой Commit changes... после правки файла.",
          badge=UI_BADGE)
    x, y, w = 40, 116, 560
    d.rect(x, y, w, 370, "#FFFFFF", LINE, 12, sw=1.2)
    d.text(x + 24, y + 38, "Commit changes", 17, INK, 600)
    d.text(x + w - 26, y + 38, "×", 20, MUTED, anchor="middle")
    d.line(x, y + 56, x + w, y + 56, "#D8DEE4", 1)
    d.text(x + 24, y + 86, "Commit message", 12.5, MUTED, 500)
    field(d, x + 24, y + 94, w - 70, "Update README.md")
    callout(d, x + w - 22, y + 109, 1)
    d.text(x + 24, y + 150, "Extended description", 12.5, MUTED, 500)
    d.rect(x + 24, y + 158, w - 70, 56, "#FFFFFF", "#D0D7DE", 6, sw=1)
    d.text(x + 34, y + 180, "Add an optional extended description...", 13, "#8C959F")
    callout(d, x + w - 22, y + 186, 2)
    d.circle(x + 32, y + 242, 6.5, "#FFFFFF", C["blue"][0], 4.5)
    d.text(x + 46, y + 247, "Commit directly to the main branch", 13.5, INK)
    callout(d, x + w - 22, y + 242, 3)
    d.circle(x + 32, y + 274, 6.5, "#FFFFFF", "#8C959F", 1.2)
    d.text(x + 46, y + 279, "Create a new branch for this commit and start a pull request", 13.5, INK)
    callout(d, x + w - 22, y + 274, 4)
    d.line(x, y + 304, x + w, y + 304, "#D8DEE4", 1)
    button(d, x + w - 306, y + 320, 90, "Cancel")
    button(d, x + w - 206, y + 320, 146, "Commit changes", primary=True)
    callout(d, x + w - 34, y + 335, 5)
    legend(d, 636, 150, [
        "Короткое сообщение: что изменено.",
        "Подробности — по желанию.",
        "Сохранить прямо в main. Подходит для личного учебного проекта.",
        "Создать ветку и Pull Request. Так работают в команде.",
        "Сохранить коммит.",
    ])
    return d


@diagram("ui-pull-request.svg", "Схема страницы Pull Request на GitHub (не скриншот)")
def ui_pull_request():
    d = D(960, 620, "Страница Pull Request", "Что где находится на странице запроса на слияние.", badge=UI_BADGE)
    browser(d, 40, 112, 560, 480, "github.com/ivan-petrov/my-site/pull/1")
    x0 = 64
    d.text(x0, 184, "Добавить страницу контактов #1", 18, INK, 600)
    d.rect(x0, 198, 58, 24, GH_GREEN, None, 12)
    d.text(x0 + 29, 214.5, "Open", 12, "#FFFFFF", 600, "middle")
    d.text(x0 + 68, 214.5, "ivan-petrov wants to merge 1 commit into", 12, MUTED)
    d.text(x0 + 68, 232, "main from feature/contacts", 12, INK, 500, mono=True)
    callout(d, 578, 216, 1)
    tabs = ["Conversation", "Commits 1", "Checks 1", "Files changed 1"]
    tx = x0
    for i, t in enumerate(tabs):
        d.text(tx, 266, t, 12.5, INK, 600 if i == 0 else 400)
        tx += text_width(t, 12.5) + 24
    d.rect(x0 - 4, 274, text_width(tabs[0], 12.5) + 8, 3, "#FD8C73", None, 1.5)
    d.line(40, 278, 600, 278, "#D8DEE4", 1)
    callout(d, tx - 8, 262, 2)
    d.circle(x0 + 14, 310, 14, "#D0D7DE")
    d.rect(x0 + 38, 294, 454, 70, "#FFFFFF", "#D0D7DE", 6, sw=1)
    d.text(x0 + 50, 318, "Что сделано: добавлена страница контактов.", 12.5, INK)
    d.text(x0 + 50, 342, "Как проверить: открыть contacts.html в браузере.", 12.5, INK)
    d.rect(x0 + 38, 380, 454, 40, "#FFFFFF", "#D0D7DE", 6, sw=1)
    d.circle(x0 + 58, 400, 9, GH_GREEN)
    d.text(x0 + 58, 404.5, "✓", 11, "#FFFFFF", 700, "middle")
    d.text(x0 + 76, 405, "All checks have passed", 13, INK, 600)
    callout(d, 578, 400, 3)
    d.rect(x0 + 38, 436, 454, 120, "#FFFFFF", "#D0D7DE", 6, sw=1)
    d.circle(x0 + 58, 458, 9, GH_GREEN)
    d.text(x0 + 58, 462.5, "✓", 11, "#FFFFFF", 700, "middle")
    d.text(x0 + 76, 463, "This branch has no conflicts with the base branch", 12.5, INK, 600)
    button(d, x0 + 54, 498, 168, "Merge pull request  ▾", primary=True, h=34)
    callout(d, x0 + 238, 515, 4)
    legend(d, 636, 150, [
        "Откуда и куда: из ветки feature/contacts в main.",
        "Files changed — построчные изменения. Здесь проходит ревью.",
        "Результат автоматических проверок, если они настроены.",
        "Слияние. Стрелка рядом с кнопкой — выбор способа слияния.",
    ])
    return d


# ===========================================================================
# Часть II
# ===========================================================================

@diagram("09-repo-structure.svg", "Структура профессионального репозитория с пометками, какие файлы нужны")
def repo_structure():
    rows = [
        ("my-project/", None, ""),
        ("├── README.md", "green", "главная страница проекта"),
        ("├── LICENSE", "green", "условия использования кода"),
        ("├── .gitignore", "green", "что Git не должен сохранять"),
        ("├── src/", "green", "исходный код"),
        ("├── tests/", "blue", "автоматические тесты"),
        ("├── CHANGELOG.md", "blue", "журнал изменений по версиям"),
        ("├── .editorconfig", "blue", "единые отступы и кодировка"),
        ("├── .gitattributes", "blue", "правила для концов строк"),
        ("├── docs/", "blue", "подробная документация"),
        ("├── CONTRIBUTING.md", "purple", "как предложить изменение"),
        ("├── CODE_OF_CONDUCT.md", "purple", "правила общения участников"),
        ("├── SECURITY.md", "blue", "как сообщить об уязвимости"),
        ("├── .env.example", "grey", "образец настроек без секретов"),
        ("├── CITATION.cff", "grey", "как цитировать научное ПО"),
        ("├── examples/", "grey", "примеры использования"),
        ("├── scripts/", "grey", "служебные скрипты"),
        ("└── .github/", None, "настройки GitHub"),
        ("    ├── workflows/", "blue", "автоматические проверки (CI)"),
        ("    ├── dependabot.yml", "blue", "обновление зависимостей"),
        ("    ├── pull_request_template.md", "blue", "шаблон описания PR"),
        ("    └── ISSUE_TEMPLATE/", "purple", "шаблоны сообщений об ошибках"),
    ]
    h = 150 + len(rows) * 26 + 70
    d = D(960, h, "Структура профессионального репозитория",
          "Цвет показывает, на каком уровне зрелости проекта элемент обычно нужен.")
    y = 140
    for path, col, note in rows:
        d.text(56, y, path.replace(" ", " "), 14.5, INK, 600 if col is None else 400, mono=True)
        if col:
            d.circle(430, y - 5, 6, C[col][0])
        if note:
            d.text(450, y, note, 14.5, MUTED)
        y += 26
    y += 22
    d.line(40, y - 22, 920, y - 22, LINE, 1)
    legend = [("green", "базовый: почти любой проект"), ("blue", "профессиональный"),
              ("purple", "публичный open-source"), ("grey", "по ситуации")]
    x = 56
    for col, t in legend:
        d.circle(x, y + 8, 6, C[col][0])
        d.text(x + 14, y + 13, t, 13.5, MUTED)
        x += text_width(t, 13.5) + 52
    return d


@diagram("09-product-lifecycle.svg", "Упрощённый жизненный цикл программного продукта")
def product_lifecycle():
    d = D(960, 640, "Жизненный цикл программного продукта",
          "Упрощённая учебная схема. ISO/IEC/IEEE 12207 описывает процессы, а не обязательный порядок шагов.")
    cx, cy, rx, ry = 480, 370, 300, 170
    stages = [
        ("Требования", "что и для кого делаем", "docs/, Issues"),
        ("Проектирование", "как устроена система", "docs/architecture.md"),
        ("Разработка", "ветки, коммиты, PR", "src/, GitHub Flow"),
        ("Проверка", "тесты, ревью, CI", "tests/, Actions"),
        ("Выпуск", "версия и релиз", "SemVer, CHANGELOG"),
        ("Сопровождение", "ошибки, обновления", "SECURITY.md, Dependabot"),
    ]
    pts = []
    for i in range(6):
        ang = math.radians(-90 + i * 60)
        pts.append((cx + rx * math.cos(ang), cy + ry * math.sin(ang)))
    cw, ch = 220, 92
    # кольцо цикла и стрелки по часовой стрелке между этапами
    d.el.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#BDC1C6" stroke-width="2"/>')
    for i in range(6):
        t = math.radians(-60 + i * 60)
        px, py = cx + rx * math.cos(t), cy + ry * math.sin(t)
        tx, ty = -rx * math.sin(t), ry * math.cos(t)
        n = math.hypot(tx, ty)
        tx, ty = tx / n, ty / n
        nx, ny = -ty, tx
        tip = (px + tx * 8, py + ty * 8)
        b1 = (px - tx * 6 + nx * 6, py - ty * 6 + ny * 6)
        b2 = (px - tx * 6 - nx * 6, py - ty * 6 - ny * 6)
        d.el.append(f'<path d="M{tip[0]:.1f},{tip[1]:.1f} L{b1[0]:.1f},{b1[1]:.1f} L{b2[0]:.1f},{b2[1]:.1f} z" '
                    f'fill="{C["grey"][0]}"/>')
    cols = ["blue", "blue", "green", "green", "yellow", "purple"]
    for (x, y), (t, s, a), col in zip(pts, stages, cols):
        stroke, tint, dark = C[col]
        d.rect(x - cw / 2, y - ch / 2, cw, ch, tint, None, 12)
        d.text(x, y - 14, t, 16.5, dark, 600, "middle")
        d.text(x, y + 8, s, 13.5, INK, anchor="middle")
        d.text(x, y + 30, a, 12.5, MUTED, anchor="middle", mono=True)
    d.circle(cx, cy, 64, "#FFFFFF", LINE, 1.5)
    d.text(cx, cy - 4, "Продукт", 17, INK, 600, "middle")
    d.text(cx, cy + 18, "и его версии", 13, MUTED, anchor="middle")
    return d


@diagram("09-semver.svg", "Семантическое версионирование MAJOR.MINOR.PATCH с примерами")
def semver():
    d = D(960, 470, "Семантическое версионирование",
          "Номер версии MAJOR.MINOR.PATCH сообщает пользователю, насколько рискованно обновление.")
    parts = [("2", "red", "MAJOR", "несовместимые изменения"), ("4", "blue", "MINOR", "новые возможности"),
             ("1", "green", "PATCH", "исправления ошибок")]
    xs = [250, 480, 710]
    for (n, col, name, desc), x in zip(parts, xs):
        d.text(x, 196, n, 72, C[col][0], 400, "middle")
        d.text(x, 232, name, 14, C[col][2], 600, "middle", spacing=1.5)
        d.text(x, 254, desc, 14, MUTED, anchor="middle")
    d.text(365, 190, ".", 60, "#9AA0A6", 400, "middle")
    d.text(595, 190, ".", 60, "#9AA0A6", 400, "middle")
    ex = [("1.4.2 → 1.4.3", "исправили ошибку", "green"), ("1.4.2 → 1.5.0", "добавили функцию", "blue"),
          ("1.4.2 → 2.0.0", "старый код может сломаться", "red")]
    for i, (v, t, col) in enumerate(ex):
        x = 40 + i * 300
        d.rect(x, 296, 280, 74, C[col][1], None, 12)
        d.text(x + 20, 326, v, 16, C[col][2], 600, mono=True)
        d.text(x + 20, 352, t, 14, INK)
    d.text(40, 412, "`0.y.z` — начальная разработка: что угодно может измениться.  `1.0.0` — первая стабильная версия.",
           14, INK)
    d.text(40, 440, "В Git версию отмечают тегом: `v1.4.3`. Буква v — соглашение, а не часть номера версии.",
           14, MUTED)
    return d


@diagram("09-maturity-levels.svg", "Инфографика трёх уровней зрелости репозитория")
def maturity_levels():
    d = D(960, 620, "Уровни зрелости репозитория",
          "Каждый уровень включает требования предыдущего. Выберите уровень по назначению проекта.")
    levels = [
        ("green", "Базовый", "личный или учебный проект",
         ["README.md", ".gitignore", "LICENSE, если код публичный", "Понятные коммиты", "Нет секретов в коде"], 230),
        ("blue", "Профессиональный", "проект для работы и заказчиков",
         ["Тесты и CI", "CHANGELOG и теги версий", ".editorconfig, .gitattributes", "Защита ветки main",
          "Dependabot", "CONTRIBUTING, SECURITY", "Лицензии зависимостей"], 350),
        ("purple", "Open-source", "публичный проект для сообщества",
         ["CODE_OF_CONDUCT.md", "Шаблоны Issue", "Закрытые сообщения", "об уязвимостях",
          "Secret scanning, CodeQL", "Проверка Scorecard", "SPDX, сторонние компоненты"], 450),
    ]
    base = 580
    w = 280
    for i, (col, name, sub, items, hgt) in enumerate(levels):
        x = 40 + i * (w + 20)
        top = base - hgt
        stroke, tint, dark = C[col]
        d.rect(x, top, w, hgt, tint, None, 14)
        d.text(x + 20, top + 36, f"{i + 1}. {name}", 18, dark, 600)
        d.text(x + 20, top + 58, sub, 13, MUTED)
        y = top + 92
        if i > 0:
            d.text(x + 20, y, "+ всё с уровня " + str(i), 13, dark, 500)
            y += 28
        for it in items:
            if it != "об уязвимостях":  # продолжение предыдущего пункта
                d.text(x + 20, y, "✓", 14, stroke, 600)
            d.text(x + 40, y, it, 14, INK)
            y += 26
    return d


@diagram("10-license-spectrum.svg", "Спектр лицензий от разрешительных до сильного copyleft")
def license_spectrum():
    d = D(960, 470, "От разрешительных лицензий к copyleft",
          "Чем правее лицензия, тем больше условий при распространении изменённых версий.")
    groups = [
        ("green", "Разрешительные", "permissive", 40, 360,
         [("MIT", ""), ("BSD-2-Clause", ""), ("BSD-3-Clause", ""), ("Apache-2.0", "+ явная патентная лицензия")]),
        ("blue", "Слабый copyleft", "weak copyleft", 410, 240,
         [("MPL-2.0", "условия — на уровне файла"), ("LGPL-3.0", "на уровне библиотеки")]),
        ("purple", "Сильный copyleft", "strong copyleft", 660, 260,
         [("GPL-3.0", "вся программа при распространении"), ("AGPL-3.0", "+ при работе по сети")]),
    ]
    for col, name, en, x, w, items in groups:
        stroke, tint, dark = C[col]
        d.rect(x, 122, w, 8, stroke, None, 4)
        d.text(x, 160, name, 17, dark, 600)
        d.text(x, 182, en, 12.5, MUTED, mono=True)
        y = 214
        for lic, note in items:
            d.rect(x, y, w, 50 if note else 40, tint, None, 10)
            d.text(x + 16, y + 25, lic, 15, INK, 600, mono=True)
            if note:
                d.text(x + 16, y + 42, note, 12.5, MUTED)
            y += (50 if note else 40) + 10
    d.line(40, 418, 920, 418, LINE, 1)
    d.text(40, 444, "Меньше условий для получателя кода", 13.5, MUTED)
    d.text(920, 444, "Больше условий для производных версий", 13.5, MUTED, anchor="end")
    d.arrow(320, 440, 640, 440, C["grey"][0])
    return d


@diagram("10-license-choice.svg", "Схема выбора лицензии для проекта")
def license_choice():
    d = D(960, 760, "Как выбрать лицензию",
          "Схема помогает сузить выбор. Это учебный материал, а не юридическая консультация.")
    d.card(300, 120, 360, 70, "grey", "Права на весь код принадлежат вам?", None,
           "свой код, договор с работодателем, соавторы", title_size=15.5, body_size=13, center=True, pad=14)
    d.card(720, 120, 200, 110, "red", "Сначала выясните права", None,
           "Работодатель, соавторы, чужой код и зависимости.", title_size=14.5, body_size=13, pad=14)
    d.arrow(664, 150, 716, 150, C["red"][0])
    d.text(690, 140, "нет", 12.5, C["red"][2], anchor="middle")
    d.arrow(480, 194, 480, 236, C["grey"][0])
    d.text(492, 220, "да", 12.5, MUTED)
    d.card(330, 240, 300, 52, "grey", "Чего вы хотите от лицензии?", None, None, title_size=15.5, center=True,
           pad=14)
    goals = [
        (40, "green", "Чтобы кодом пользовались максимально широко"),
        (340, "blue", "Чтобы изменённые версии тоже оставались открытыми"),
        (640, "yellow", "Чтобы мой код без разрешения не использовали"),
    ]
    for x, col, t in goals:
        d.card(x, 340, 280, 70, col, None, None, t, body_size=14.5, pad=16, body_color=C[col][2])
    d.path("M400,296 C400,318 180,318 180,336", C["grey"][0])
    d.arrow(480, 296, 480, 336, C["grey"][0])
    d.path("M560,296 C560,318 780,318 780,336", C["grey"][0])
    for x in (180, 480, 780):
        d.arrow(x, 414, x, 446, C["grey"][0])
    # результаты
    d.rect(40, 450, 280, 210, C["green"][1], None, 12)
    d.text(58, 480, "Разрешительные лицензии", 15, C["green"][2], 600)
    yy = 510
    for lic, note in [("MIT", "короткая и простая"), ("BSD-2/3-Clause", "похожа на MIT"),
                      ("Apache-2.0", "явная патентная лицензия, NOTICE")]:
        d.text(58, yy, lic, 14, INK, 600, mono=True)
        d.text(58, yy + 20, note, 13, MUTED)
        yy += 48
    d.rect(340, 450, 280, 210, C["blue"][1], None, 12)
    d.text(358, 480, "Copyleft-лицензии", 15, C["blue"][2], 600)
    yy = 510
    for lic, note in [("MPL-2.0", "открывать изменённые файлы"), ("LGPL-3.0", "для библиотек"),
                      ("GPL-3.0", "вся программа при распространении"), ("AGPL-3.0", "+ пользователи сетевого сервиса")]:
        d.text(358, yy, lic, 14, INK, 600, mono=True)
        d.text(358, yy + 18, note, 12.5, MUTED)
        yy += 38
    d.rect(640, 450, 280, 210, C["yellow"][1], None, 12)
    d.text(658, 480, "Открытая лицензия не подходит", 15, C["yellow"][2], 600)
    d.para(658, 510, "Не публикуйте код или обсудите модель лицензирования с юристом. "
                     "Отсутствие лицензии в публичном репозитории — не стратегия защиты.", 246, 13.5, INK)
    d.text(40, 700, "Перед выбором проверьте лицензии зависимостей: они могут ограничить ваш выбор.", 14, INK)
    d.text(40, 726, "Подробности и сравнение — в главе 10 и в templates/LICENSE_SELECTION_GUIDE.md.", 13.5, MUTED)
    return d


@diagram("11-ci-pipeline.svg", "Диаграмма автоматических проверок CI в GitHub Actions")
def ci_pipeline():
    d = D(960, 560, "Автоматические проверки (CI)",
          "GitHub Actions запускает проверки при каждом push и Pull Request и показывает результат в PR.")
    d.label(40, 136, "Событие")
    d.card(40, 150, 170, 60, "grey", "push", None, None, title_size=15, center=True)
    d.card(40, 226, 170, 60, "grey", "Pull Request", None, None, title_size=15, center=True)
    d.path("M214,180 C250,180 250,218 282,218", C["grey"][0])
    d.path("M214,256 C250,256 250,226 282,226", C["grey"][0])
    d.label(290, 136, "Workflow .github/workflows/ci.yml")
    d.rect(286, 150, 634, 136, C["blue"][1], None, 14)
    steps = ["Скачать код", "Установить Python", "Линтер", "Тесты"]
    subs = ["checkout", "setup-python", "ruff check", "unittest"]
    sw = 136
    for i, (s, sub) in enumerate(zip(steps, subs)):
        x = 304 + i * (sw + 12)
        d.rect(x, 172, sw, 92, "#FFFFFF", None, 10)
        d.text(x + sw / 2, 210, s, 14, INK, 600, "middle")
        d.text(x + sw / 2, 236, sub, 12.5, MUTED, anchor="middle", mono=True)
        if i < 3:
            d.arrow(x + sw + 1, 218, x + sw + 11, 218, C["blue"][0])
    d.path("M603,290 V318 H330 V344", C["green"][0])
    d.path("M603,318 H770 V344", C["red"][0])
    d.card(200, 348, 260, 76, "green", "✓ Все проверки пройдены", None, "PR можно сливать", title_size=15,
           body_size=13.5)
    d.card(640, 348, 260, 76, "red", "✗ Проверка не прошла", None, "откройте лог и исправьте", title_size=15,
           body_size=13.5)
    d.label(40, 462, "Встроенные функции GitHub · включаются в настройках")
    extras = [("Dependabot", "обновления и уязвимые зависимости"), ("Secret scanning", "поиск ключей и токенов"),
              ("CodeQL", "анализ кода на уязвимости")]
    for i, (t, s) in enumerate(extras):
        x = 40 + i * 300
        d.rect(x, 476, 280, 60, C["grey"][1], None, 12)
        d.text(x + 18, 501, t, 14.5, INK, 600)
        d.text(x + 18, 523, s, 13, MUTED)
    return d


@diagram("11-pr-review.svg", "Процесс Pull Request и проверки кода с правилами защиты ветки")
def pr_review():
    d = D(960, 600, "Pull Request и проверка кода",
          "Правила ветки main не дают слить изменения, пока не пройдены проверки и не получено одобрение.")
    top = 184
    nodes = [
        (40, "blue", "Автор", "ветка, коммиты, push"),
        (270, "blue", "Pull Request", "описание по шаблону"),
        (500, "grey", "CI", "автоматические проверки"),
        (730, "purple", "Ревьюер", "читает Files changed"),
    ]
    for x, col, t, s in nodes:
        d.card(x, top, 190, 84, col, t, None, s, title_size=16, body_size=13.5)
    for i in range(3):
        d.arrow(nodes[i][0] + 194, top + 42, nodes[i + 1][0] - 4, top + 42, C["grey"][0])
    d.path(f"M790,{top} C790,{top - 52} 135,{top - 52} 135,{top - 4}", C["yellow"][0], dash="5 5")
    d.text(462, top - 50, "Request changes → новые коммиты в ту же ветку", 13.5, C["yellow"][2], anchor="middle")
    d.path(f"M595,{top + 88} C595,{top + 140} 135,{top + 140} 135,{top + 92}", C["red"][0], dash="5 5")
    d.text(365, top + 146, "проверка не прошла → исправить", 13, C["red"][2], anchor="middle")
    d.path(f"M825,{top + 88} V{top + 150}", C["green"][0])
    d.text(838, top + 124, "Approve", 13.5, C["green"][2], 600)
    y0 = top + 154
    d.rect(560, y0, 360, 120, C["green"][1], None, 14)
    d.text(580, y0 + 32, "Правила ветки main", 16, C["green"][2], 600)
    for i, t in enumerate(["✓ обязательные проверки пройдены", "✓ есть одобрение ревьюера",
                           "✓ нет конфликтов с main"]):
        d.text(580, y0 + 60 + i * 22, t, 14, INK)
    d.path(f"M740,{y0 + 124} V{y0 + 156}", C["green"][0])
    d.card(560, y0 + 160, 360, 60, "green", "Merge → удалить ветку", None, None, title_size=16, center=True,
           outline=True)
    d.para(40, y0 + 60, "Ревью — это чтение изменений другим человеком. Он задаёт вопросы, находит ошибки и "
                        "одобряет (Approve) или просит доработать (Request changes).", 440, 14, MUTED)
    return d


@diagram("11-secret-leak.svg", "Порядок действий, если секрет попал в Git-репозиторий")
def secret_leak():
    d = D(960, 600, "Секрет попал в репозиторий: что делать",
          "Сначала обезвредьте секрет, потом чистите историю. Порядок важен.")
    steps = [
        ("red", "Отзовите или замените секрет", "Смените ключ, токен или пароль у поставщика. Это главное действие."),
        ("red", "Оцените последствия", "Проверьте журналы доступа: пользовался ли кто-то ключом."),
        ("yellow", "Уберите секрет из кода", "Перенесите его в .env или секреты GitHub, добавьте .env в .gitignore."),
        ("yellow", "Решите, чистить ли историю", "git filter-repo переписывает историю. Согласуйте с командой."),
        ("grey", "Обратитесь в поддержку GitHub", "Если нужно убрать кэшированные представления и ссылки PR."),
        ("green", "Предотвратите повтор", "Push protection, проверка diff, .env.example вместо .env."),
    ]
    y = 128
    for i, (col, t, s) in enumerate(steps):
        d.num(58, y + 22, i + 1, col, 15)
        d.text(88, y + 20, t, 16, INK, 600)
        d.text(88, y + 44, s, 13.5, MUTED)
        if i < len(steps) - 1:
            d.line(58, y + 40, 58, y + 66, LINE, 2)
        y += 72
    d.rect(620, 128, 300, 250, C["red"][1], None, 14)
    d.text(642, 162, "Важно", 16, C["red"][2], 600)
    d.para(642, 192, "Удаление файла новым коммитом не убирает секрет из истории. Его можно найти в "
                     "старых коммитах, клонах и форках.", 256, 14, INK)
    d.para(642, 300, "Считайте опубликованный секрет скомпрометированным, даже если удалили его быстро.",
           256, 14, C["red"][2])
    return d


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (fn, desc) in DIAGRAMS.items():
        (OUT / name).write_text(fn().svg(desc), encoding="utf-8", newline="\n")
        print("ok", name)


if __name__ == "__main__":
    main()
