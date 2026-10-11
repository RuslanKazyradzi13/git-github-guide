"""Склеивает PNG-кадры в зацикленный GIF с общей палитрой.

    python tools/frames_to_gif.py <папка с кадрами> <файл.gif> <кадров в секунду> <#цвет,#цвет>

Перечисленные цвета попадают в палитру без искажений: так фон GIF точно
совпадает с фоном страницы GitHub. Остальные цвета подбираются по кадрам.
Вызывается из tools/make_hero.mjs. Нужен пакет Pillow.
"""

from __future__ import annotations

import pathlib
import sys

from PIL import Image


def main() -> None:
    src, out, fps, keep = sys.argv[1:5]
    files = sorted(pathlib.Path(src).glob("*.png"))
    keys = [tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) for c in keep.split(",")]

    # Палитра: заданные цвета + 256 - n самых частых по выборке кадров.
    sample = files[:: max(1, len(files) // 16)]
    w, h = Image.open(files[0]).size
    strip = Image.new("RGB", (w, h * len(sample)))
    for i, f in enumerate(sample):
        strip.paste(Image.open(f).convert("RGB"), (0, h * i))
    q = strip.quantize(colors=256 - len(keys), method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    qp = q.getpalette()[: 3 * (256 - len(keys))]
    found = [tuple(qp[i:i + 3]) for i in range(0, len(qp), 3)]
    # Pillow сопоставляет цвета приближённо (по 6 бит на канал). Близкие к заданным
    # цвета убираем, иначе фон может стать «почти белым» и выделиться на странице.
    found = [c for c in found if all(max(abs(a - b) for a, b in zip(c, k)) > 6 for k in keys)]
    colors = keys + found
    colors += [keys[0]] * (256 - len(colors))
    flat = [v for rgb in colors for v in rgb]
    pal = Image.new("P", (1, 1))
    pal.putpalette(flat)

    frames = [Image.open(f).convert("RGB").quantize(palette=pal, dither=Image.Dither.NONE) for f in files]
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=round(1000 / float(fps)),
                   loop=0, optimize=False, palette=bytes(flat), disposal=1)
    size = pathlib.Path(out).stat().st_size
    print(f"{out}: {len(frames)} кадров, {size / 1024 / 1024:.1f} МБ")


if __name__ == "__main__":
    main()
