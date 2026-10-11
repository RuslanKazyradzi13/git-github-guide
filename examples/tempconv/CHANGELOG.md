# Журнал изменений

Все заметные изменения проекта записываются в этот файл.

Формат основан на [Keep a Changelog 1.1.0](https://keepachangelog.com/ru/1.1.0/), проект следует [Semantic Versioning 2.0.0](https://semver.org/lang/ru/).

## [Unreleased]

## [1.0.0] - 2026-10-11

### Added

- Переменная окружения `TEMPCONV_PRECISION` для выбора числа знаков после запятой.
- Команда `tempconv` после установки пакета.
- Автоматические проверки в GitHub Actions: стиль кода и тесты.

### Changed

- Сообщения об ошибках выводятся в поток ошибок, код выхода при ошибке — `2`.

### Fixed

- Шкала с пробелами, например `" f "`, больше не вызывает ошибку.

## [0.1.0] - 2026-10-04

### Added

- Перевод температур между шкалами C, F и K.
- Проверка значений ниже абсолютного нуля.

[Unreleased]: https://github.com/OWNER/tempconv/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/OWNER/tempconv/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/OWNER/tempconv/releases/tag/v0.1.0
