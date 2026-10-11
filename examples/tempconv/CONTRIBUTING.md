# Как участвовать в проекте

Спасибо, что хотите помочь! Этот документ описывает, как предложить изменение.

## Перед началом

- Ошибку или идею сначала обсудите в [Issue](https://github.com/OWNER/tempconv/issues): возможно, над ней уже работают.
- Об уязвимостях сообщайте не в Issue, а по правилам [SECURITY.md](SECURITY.md).

## Подготовка окружения

```powershell
git clone https://github.com/OWNER/tempconv.git
cd tempconv
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e . -r requirements-dev.txt
```

Если PowerShell запрещает запуск `Activate.ps1`, выполните один раз `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

## Как внести изменение

1. Создайте ветку от `main`: `git switch -c fix/short-description`.
2. Внесите изменения и добавьте тесты на новое поведение.
3. Запустите проверки:

   ```powershell
   ruff check .
   python -m unittest discover -s tests -v
   ```

4. Обновите `README.md`, если изменилось использование, и добавьте запись в раздел `[Unreleased]` файла `CHANGELOG.md`.
5. Сделайте коммит. Сообщение — по [Conventional Commits](https://www.conventionalcommits.org/ru/v1.0.0/): `fix: ...`, `feat: ...`, `docs: ...`.
6. Отправьте ветку и откройте Pull Request. Заполните шаблон описания.

## Правила оформления кода

- Стиль проверяет `ruff`; настройки — в `pyproject.toml`.
- Отступ — 4 пробела, кодировка UTF-8, концы строк LF (см. `.editorconfig`).
- Только стандартная библиотека Python. Новую зависимость сначала обсудите в Issue.

## Ревью

Pull Request сливается после того, как прошли автоматические проверки и изменения одобрил сопровождающий проекта. Ответ может занять несколько дней.

## Лицензия вклада

Отправляя изменения, вы соглашаетесь, что они распространяются на условиях лицензии проекта ([LICENSE](LICENSE)).
