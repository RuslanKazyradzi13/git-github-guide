"""Перевод температур между шкалами Цельсия, Фаренгейта и Кельвина."""

__version__ = "1.0.0"

SCALES = ("C", "F", "K")
ABSOLUTE_ZERO_C = -273.15


def normalize_scale(scale: str) -> str:
    """Возвращает обозначение шкалы заглавной буквой или вызывает ValueError."""
    name = scale.strip().upper()
    if name not in SCALES:
        raise ValueError(f"неизвестная шкала {scale!r}, допустимо: C, F, K")
    return name


def to_celsius(value: float, scale: str) -> float:
    """Переводит значение из указанной шкалы в градусы Цельсия."""
    name = normalize_scale(scale)
    if name == "C":
        celsius = value
    elif name == "F":
        celsius = (value - 32) * 5 / 9
    else:
        celsius = value + ABSOLUTE_ZERO_C
    if celsius < ABSOLUTE_ZERO_C - 1e-9:
        raise ValueError("температура ниже абсолютного нуля")
    return celsius


def from_celsius(celsius: float, scale: str) -> float:
    """Переводит градусы Цельсия в указанную шкалу."""
    name = normalize_scale(scale)
    if name == "C":
        return celsius
    if name == "F":
        return celsius * 9 / 5 + 32
    return celsius - ABSOLUTE_ZERO_C


def convert(value: float, source: str, target: str) -> float:
    """Переводит значение из шкалы source в шкалу target."""
    return from_celsius(to_celsius(value, source), target)
