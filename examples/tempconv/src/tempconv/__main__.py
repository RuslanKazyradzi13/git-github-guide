"""Командная строка: python -m tempconv 100 C F"""

import argparse
import os
import sys

from tempconv import __version__, convert, normalize_scale

SYMBOLS = {"C": "°C", "F": "°F", "K": "K"}
DEFAULT_PRECISION = 2


def precision_from_env() -> int:
    """Число знаков после запятой из переменной окружения TEMPCONV_PRECISION (0–6)."""
    raw = os.environ.get("TEMPCONV_PRECISION", str(DEFAULT_PRECISION))
    try:
        value = int(raw)
    except ValueError:
        return DEFAULT_PRECISION
    return min(max(value, 0), 6)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="tempconv",
        description="Перевод температур между шкалами C (Цельсий), F (Фаренгейт) и K (Кельвин).",
    )
    parser.add_argument("value", type=float, help="значение температуры, например 36.6")
    parser.add_argument("source", help="исходная шкала: C, F или K")
    parser.add_argument("target", help="целевая шкала: C, F или K")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args(argv)

    try:
        result = convert(args.value, args.source, args.target)
        source, target = normalize_scale(args.source), normalize_scale(args.target)
    except ValueError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 2

    digits = precision_from_env()
    print(f"{args.value:g} {SYMBOLS[source]} = {result:.{digits}f} {SYMBOLS[target]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
