# Глава 8. Практика и итоговые проекты

Знания закрепляются только руками. В этой главе — короткие упражнения по каждой главе и два итоговых проекта: первый репозиторий от папки до отмены изменений и профессионально оформленный репозиторий с лицензией, CI и релизом.

**Как работать с главой:**

- выполняйте шаги по порядку и сверяйтесь с ожидаемым результатом;
- если результат отличается — остановитесь, выполните `git status` и найдите причину в [главе 6](06_oshibki_i_vosstanovlenie.md);
- хеши коммитов, даты и логин у вас будут свои — это нормально.

**Время:** проект 1 — 1,5 часа, проект 2 — 3–4 часа.

**Когда выполнять:** упражнения и проект 1 — сразу после глав 1–7. Проект 2 опирается на часть II — выполняйте его после глав 9–11.

<!-- toc -->
**Содержание главы**

- [8.1. Упражнения по главам](#81-упражнения-по-главам)
- [8.2. Проект 1. «Мой первый репозиторий»](#82-проект-1-мой-первый-репозиторий)
- [8.3. Проект 2. «Профессионально оформленный репозиторий»](#83-проект-2-профессионально-оформленный-репозиторий)
- [8.4. Чек-лист готовности репозитория к публикации](#84-чек-лист-готовности-репозитория-к-публикации)
- [8.5. Контрольный список навыков](#85-контрольный-список-навыков)
- [8.6. Что изучать дальше](#86-что-изучать-дальше)
<!-- /toc -->

## 8.1. Упражнения по главам

| Глава | Задание | Ожидаемый результат |
| --- | --- | --- |
| 1. Основы | Объясните своими словами разницу между Git и GitHub, коммитом и веткой | Git — программа на компьютере, GitHub — сервис в интернете; коммит — сохранённая версия, ветка — линия работы |
| 2. Установка | Выполните `git --version` и `git config --global --list` | Версия Git; `user.name`, `user.email`, `init.defaultbranch=main` |
| 3. Команды | Создайте репозиторий, сделайте три коммита, найдите в `git log` второй и посмотрите его изменения через `git show <хеш>` | Три строки в `git log --oneline`; `git show` выводит сообщение и diff коммита |
| 3. Команды | Измените файл, подготовьте его, затем измените снова. Сравните `git diff` и `git diff --staged` | Первая правка видна в `--staged`, вторая — в `git diff` |
| 4. GitHub | Создайте файл через сайт, затем получите его командой `git pull` | Файл появился в папке, `git log` показывает коммит с сайта |
| 5. Ветки | Создайте две ветки, в каждой по коммиту, влейте обе в `main` | `git log --oneline --graph --all` показывает слияние |
| 5. Pull Request | Откройте PR из ветки, оставьте комментарий к строке во **Files changed**, слейте PR | PR в статусе **Merged**, ветка удалена |
| 6. Восстановление | Создайте конфликт и решите его; затем отмените коммит через `git revert` | В истории коммит слияния и коммит `Revert "..."` |
| 6. Безопасность | Создайте `.env` и убедитесь, что Git его игнорирует | `git check-ignore -v .env` показывает правило из `.gitignore` |
| 7. AI | Поручите Claude Code маленькую правку в отдельной ветке, просмотрите `git diff`, закоммитьте или откатите | Чистый `git status` в конце; осознанное решение по каждому изменению |

## 8.2. Проект 1. «Мой первый репозиторий»

Цель: пройти полный путь от пустой папки до отмены изменения. Понадобятся главы 2–6.

### Шаг 1. Создайте папку проекта

```powershell
mkdir ~\projects\my-first-repo
cd ~\projects\my-first-repo
pwd
```

**Ожидается:** `pwd` показывает `C:\Users\<вы>\projects\my-first-repo`.

### Шаг 2. Создайте простой файл

```powershell
notepad README.md
```

Нажмите **Да** в вопросе о создании файла и напишите:

```markdown
# Мой первый репозиторий

Учусь работать с Git и GitHub.
```

Сохраните и закройте Блокнот.

**Ожидается:** `ls` показывает `README.md`.

### Шаг 3. Инициализируйте Git

```powershell
git init
git status
```

**Ожидается:**

```text
Initialized empty Git repository in C:/Users/<вы>/projects/my-first-repo/.git/
```

```text
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	README.md
```

Если вместо `main` написано `master` — выполните `git branch -M main` и проверьте настройку `init.defaultBranch` ([глава 2](02_ustanovka_i_nastroyka.md#24-первая-настройка-git)).

### Шаг 4. Создайте первый коммит

```powershell
git add README.md
git status
git commit -m "Добавить README"
```

**Ожидается:** `git status` показывает `new file: README.md` в разделе `Changes to be committed`, коммит выводит строку `[main (root-commit) ...] Добавить README`.

### Шаг 5. Создайте репозиторий на GitHub

1. **+** → **New repository**.
2. Имя: `my-first-repo`. Видимость: **Public** или **Private**.
3. README, .gitignore и лицензию **не добавляйте**.
4. **Create repository** → скопируйте HTTPS-адрес со страницы **Quick setup**.

**Ожидается:** пустой репозиторий с инструкциями Quick setup.

### Шаг 6. Свяжите локальный проект с GitHub

```powershell
git remote add origin https://github.com/<логин>/my-first-repo.git
git remote -v
```

**Ожидается:** две строки с вашим адресом — `(fetch)` и `(push)`.

### Шаг 7. Отправьте изменения

```powershell
git push -u origin main
```

При первом push войдите в GitHub через браузер ([глава 4](04_rabota_s_github.md#48-вход-в-github-из-терминала)).

**Ожидается:** `* [new branch] main -> main` и `branch 'main' set up to track 'origin/main'`. На сайте виден `README.md` с оформленным заголовком.

### Шаг 8. Создайте отдельную ветку

```powershell
git switch -c feature/about
git branch
```

**Ожидается:** `Switched to a new branch 'feature/about'`; в списке веток звёздочка у `feature/about`.

### Шаг 9. Измените файл и сделайте коммит

Откройте `README.md` (`notepad README.md`) и добавьте в конец:

```markdown
## Обо мне

Начинающий разработчик. Изучаю Git, GitHub и работу с AI-ассистентами.
```

```powershell
git diff
git add README.md
git commit -m "Добавить раздел «Обо мне»"
```

**Ожидается:** `git diff` показывает добавленные строки со знаком `+`; коммит создан в ветке `feature/about`.

### Шаг 10. Объедините изменения

**Вариант А — через Pull Request (рекомендуется):**

```powershell
git push -u origin feature/about
```

На GitHub: **Compare & pull request** → проверьте **base: main ← compare: feature/about** → **Create pull request** → вкладка **Files changed** → **Merge pull request** → **Confirm merge** → **Delete branch**. Затем на компьютере:

```powershell
git switch main
git pull
git branch -d feature/about
```

**Вариант Б — локально:**

```powershell
git switch main
git merge feature/about
git push
git branch -d feature/about
```

**Ожидается:** в `main` есть раздел «Обо мне». При локальном слиянии Git пишет `Fast-forward`.

### Шаг 11. Посмотрите историю

```powershell
git log --oneline --graph --all
```

**Ожидается** (вариант Б):

```text
* 4c1d2e9 (HEAD -> main, origin/main) Добавить раздел «Обо мне»
* 9a8b7c6 Добавить README
```

При варианте А появится ещё коммит слияния `Merge pull request #1 ...`, а у удалённой ветки, которую вы удалили на сайте, может остаться локальная «закладка» `origin/feature/about`. Уберите её командой `git fetch --prune`. На GitHub откройте список коммитов (ссылка с числом коммитов) — он совпадает с выводом `git log`.

### Шаг 12. Внесите тестовое изменение и отмените его

**12.1. Отмена незакоммиченной правки.** Допишите в `README.md` строку `Ошибочная строка` и сохраните. Затем:

```powershell
git status
git diff
git restore README.md
git status
```

**Ожидается:** сначала `modified: README.md` и строка `+Ошибочная строка` в diff; после `git restore` — `nothing to commit, working tree clean`, строки в файле нет.

**12.2. Отмена отправленного коммита.** Снова допишите `Ошибочная строка`, затем:

```powershell
git add README.md
git commit -m "Тестовое изменение"
git push
git revert --no-edit HEAD
git push
git log --oneline
```

**Ожидается** (вариант Б; при варианте А между коммитами будет ещё `Merge pull request #1 ...`):

```text
b3c4d5e (HEAD -> main, origin/main) Revert "Тестовое изменение"
a1b2c3d Тестовое изменение
4c1d2e9 Добавить раздел «Обо мне»
9a8b7c6 Добавить README
```

Строки нет в файле, а в истории видно и ошибку, и её отмену. Именно так безопасно отменяют коммиты, которые уже на GitHub.

### Проверка проекта 1

- [ ] На GitHub есть репозиторий `my-first-repo` с `README.md`.
- [ ] В истории не меньше четырёх коммитов, включая `Revert "Тестовое изменение"`.
- [ ] `git status` показывает `Your branch is up to date with 'origin/main'` и чистую рабочую папку.
- [ ] Ветка `feature/about` удалена локально и на GitHub.

## 8.3. Проект 2. «Профессионально оформленный репозиторий»

Цель: оформить небольшой программный проект так, как это делают в профессиональных командах. Понадобятся главы 9–11.

Эталонное решение — папка [examples/tempconv](examples/tempconv/): консольный конвертер температур на Python. Можно повторить его или оформить свой проект по тем же шагам.

> [!NOTE]
> Если вы не программировали на Python, это не страшно: код уже готов в примере. Задача проекта — **оформление репозитория**, а не написание программы. Для запуска проверок понадобится Python 3.11+ с [python.org](https://www.python.org/downloads/).

### Шаг 1. Создайте репозиторий

1. На GitHub: **New repository** → имя `tempconv` → **Public** → включите **README** → **Create repository**.
2. Склонируйте:

```powershell
cd ~\projects
git clone https://github.com/<логин>/tempconv.git
cd tempconv
```

3. Скопируйте в папку файлы `src/`, `tests/`, `pyproject.toml`, `requirements-dev.txt` из примера (через Проводник).
4. Ваш проект только начинается, поэтому задайте начальную версию: в `pyproject.toml` (строка `version = "1.0.0"`) и в `src/tempconv/__init__.py` (строка `__version__ = "1.0.0"`) замените `1.0.0` на `0.1.0`.
5. Первый коммит:

```powershell
git add .
git commit -m "feat: добавить конвертер температур"
git push
```

**Ожидается:** на GitHub видны папки `src` и `tests`.

### Шаг 2. Оформите README

Возьмите шаблон [templates/README.template.md](templates/README.template.md) и заполните разделы: описание, проблема, возможности, установка, быстрый старт, примеры, настройка, тестирование, статус, лицензия. Сверьтесь с [README примера](examples/tempconv/README.md).

```powershell
git add README.md
git commit -m "docs: описать установку и использование в README"
git push
```

**Ожидается:** на главной странице репозитория — оформленный README с содержанием и примерами команд.

### Шаг 3. Выберите лицензию по условиям

**Условия задачи:**

- весь код написан вами, чужих фрагментов нет, работодатель прав на код не имеет;
- вы хотите, чтобы код могли использовать кто угодно и где угодно, включая коммерческие продукты;
- вы не требуете открывать исходный код производных программ;
- достаточно, чтобы сохранялось уведомление о вашем авторстве;
- лицензия должна быть короткой и понятной.

**Решение.** Подходят разрешительные лицензии. Под условия «коротко и просто» лучше всего подходит **MIT**. Если бы для вас была важна явная патентная лицензия — стоило бы рассмотреть **Apache-2.0** ([глава 10](10_litsenzii_i_avtorskie_prava.md)).

**Как добавить:**

1. На GitHub: **Add file** → **Create new file** → имя `LICENSE` → **Choose a license template** → **MIT License** → **Review and submit**.
2. Проверьте строку `Copyright (c) <год> <имя>`: год и **ваше** имя или имя правообладателя.
3. **Commit changes**, затем получите новый коммит на компьютере: `git pull`. Так как все ваши коммиты уже отправлены, Git просто «перемотает» ветку вперёд (`Fast-forward`).

Проверьте, что в `pyproject.toml` есть строка `license = "MIT"` (SPDX-идентификатор; в файле из примера она уже есть), и добавьте в README раздел «Лицензия»:

```powershell
git add README.md pyproject.toml
git commit -m "docs: указать лицензию MIT в README"
git push
```

**Ожидается:** справа на странице репозитория появилась отметка **MIT license**.

### Шаг 4. Добавьте .gitignore, .editorconfig и .gitattributes

Скопируйте файлы из примера или создайте свои ([глава 9](09_standarty_i_oformlenie_proektov.md#92-структура-профессионального-репозитория)).

```powershell
git add .gitignore .editorconfig .gitattributes
git commit -m "chore: добавить .gitignore, .editorconfig и .gitattributes"
git push
```

**Ожидается:** `git status --ignored` показывает `.venv/` и `__pycache__/` в игнорируемых, если они есть.

### Шаг 5. Создайте CONTRIBUTING.md и SECURITY.md

Возьмите шаблоны [templates/CONTRIBUTING.template.md](templates/CONTRIBUTING.template.md) и [templates/SECURITY.template.md](templates/SECURITY.template.md). Заполните заполнители в квадратных скобках своими данными. Укажите реальный способ закрыто сообщить об уязвимости и включите **Private vulnerability reporting** ([глава 11](11_bezopasnost_i_avtomatizatsiya.md)).

```powershell
git add CONTRIBUTING.md SECURITY.md
git commit -m "docs: добавить CONTRIBUTING и SECURITY"
git push
```

**Ожидается:** при создании Issue GitHub показывает ссылку на правила участия; в разделе безопасности репозитория есть политика.

### Шаг 6. Ведите CHANGELOG.md

Создайте `CHANGELOG.md` по шаблону [templates/CHANGELOG.template.md](templates/CHANGELOG.template.md). Запишите изменения в раздел `## [Unreleased]`, а перед релизом перенесите их в раздел версии:

```markdown
## [0.1.0] - 2026-10-11

### Added

- Перевод температур между шкалами C, F и K.
```

```powershell
git add CHANGELOG.md
git commit -m "docs: добавить CHANGELOG"
git push
```

### Шаг 7. Пишите понятные сообщения коммитов

Используйте формат Conventional Commits ([глава 9](09_standarty_i_oformlenie_proektov.md#96-сообщения-коммитов-conventional-commits)):

| Тип | Когда | Пример |
| --- | --- | --- |
| `feat` | Новая возможность | `feat: добавить шкалу Ранкина` |
| `fix` | Исправление ошибки | `fix: принимать шкалу с пробелами` |
| `docs` | Документация | `docs: добавить пример в README` |
| `test` | Тесты | `test: проверить отрицательные значения` |
| `ci` | Автоматические проверки | `ci: добавить Python 3.15 в матрицу` |
| `chore` | Служебное | `chore: обновить .gitignore` |

**Ожидается:** `git log --oneline` читается как список понятных изменений.

### Шаг 8. Настройте базовый workflow проверки

1. Скопируйте `.github/workflows/ci.yml` и `.github/dependabot.yml` из примера.
2. Отправьте их через ветку и Pull Request:

```powershell
git switch -c ci/add-checks
git add .github
git commit -m "ci: добавить проверку стиля и тесты"
git push -u origin ci/add-checks
```

3. Откройте PR. Через минуту во вкладке **Checks** появятся проверки для четырёх версий Python.
4. Когда они станут зелёными, слейте PR и обновите `main` у себя (`git switch main`, `git pull`).

**Ожидается:** во вкладке **Actions** — успешный запуск workflow **CI**; в README можно добавить значок CI.

### Шаг 9. Создайте тег и релиз

```powershell
git switch main
git pull
git tag -a v0.1.0 -m "Версия 0.1.0"
git push origin v0.1.0
```

> **Тег** (*tag*) — постоянная метка на коммите, обычно номер версии. Аннотированный тег (`-a`) хранит автора, дату и сообщение — такие используют для релизов.

На GitHub: **Releases** → **Draft a new release** → **Choose a tag**: `v0.1.0` → заголовок `v0.1.0` → вставьте раздел версии из `CHANGELOG.md` или нажмите **Generate release notes** → **Publish release**.

**Ожидается:** на странице репозитория справа появился блок **Releases** с версией `v0.1.0`; к релизу автоматически приложены архивы исходного кода.

### Шаг 10. Проверьте безопасность и готовность к публикации

1. Включите защиту ветки `main`: обязательный Pull Request и успешные проверки ([глава 11](11_bezopasnost_i_avtomatizatsiya.md#114-защита-основной-ветки)).
2. Проверьте, что включены Dependabot alerts и secret scanning ([глава 11](11_bezopasnost_i_avtomatizatsiya.md)).
3. Просмотрите историю на секреты: `git log -p -i -G "password|token|secret|key"` покажет коммиты, где добавлялись или удалялись строки с этими словами.
4. Пройдите чек-лист [templates/PROJECT_RELEASE_CHECKLIST.md](templates/PROJECT_RELEASE_CHECKLIST.md) — уровни «Базовый» и «Профессиональный».

**Ожидается:** все пункты базового и профессионального уровня отмечены или осознанно пропущены с пояснением.

### Проверка проекта 2

- [ ] README с установкой, примерами, настройкой, тестированием и лицензией.
- [ ] `LICENSE` с годом и именем правообладателя; GitHub распознаёт лицензию.
- [ ] `.gitignore`, `.editorconfig`, `.gitattributes`.
- [ ] `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`.
- [ ] Сообщения коммитов по Conventional Commits.
- [ ] Workflow CI проходит в Pull Request.
- [ ] Тег `v0.1.0` и релиз на GitHub.
- [ ] Защита `main`, Dependabot и secret scanning включены.

## 8.4. Чек-лист готовности репозитория к публикации

Краткая версия. Полная, с пунктами для отметки и итоговой таблицей, — [templates/PROJECT_RELEASE_CHECKLIST.md](templates/PROJECT_RELEASE_CHECKLIST.md). Уровни накопительные.

**Уровень 1. Базовый — небольшой личный проект**

- [ ] README: что это, как установить и запустить; команды работают.
- [ ] `.gitignore`; в репозитории нет временных и служебных файлов.
- [ ] В коде и истории нет паролей, токенов, ключей и личных данных.
- [ ] У вас есть право публиковать весь код.
- [ ] Для публичного кода — файл `LICENSE` с правообладателем.
- [ ] Понятные сообщения коммитов; всё отправлено на GitHub.

**Уровень 2. Профессиональный — документация, тесты, контроль качества, сопровождение**

- [ ] README с требованиями, настройкой, тестированием, статусом и ограничениями.
- [ ] Тесты и линтер запускаются в CI для каждого Pull Request.
- [ ] `CHANGELOG.md`, версия по SemVer, тег `vX.Y.Z` и релиз.
- [ ] `CONTRIBUTING.md`, `SECURITY.md`, шаблон Pull Request.
- [ ] `.editorconfig`, `.gitattributes`.
- [ ] Ветка `main` защищена; Dependabot включён; действия в workflow закреплены хешами.
- [ ] Лицензии зависимостей проверены.

**Уровень 3. Публичный open-source — сообщество, безопасность, лицензирование, релизы**

- [ ] `CODE_OF_CONDUCT.md` с реальным контактом для жалоб.
- [ ] Шаблоны Issue; условия приёма вклада (лицензия проекта, DCO или CLA).
- [ ] Закрытые сообщения об уязвимостях, secret scanning, push protection, CodeQL.
- [ ] Проверка OpenSSF Scorecard.
- [ ] SPDX-идентификатор лицензии; `THIRD_PARTY_NOTICES.md` или `NOTICE` для встроенных компонентов.
- [ ] Релизы собираются в CI, заметки о выпуске перечисляют несовместимые изменения и исправления безопасности.

## 8.5. Контрольный список навыков

Отметьте, что умеете делать самостоятельно, без подсказок.

**Основы и настройка**

- [ ] Объяснить разницу между Git и GitHub, коммитом, веткой и репозиторием.
- [ ] Открыть терминал в нужной папке и перемещаться по папкам.
- [ ] Установить Git и настроить имя, почту, ветку `main`, редактор.

**Ежедневная работа**

- [ ] Создать репозиторий (`git init`) или склонировать его (`git clone`).
- [ ] Проверить состояние (`git status`) и изменения (`git diff`, `git diff --staged`).
- [ ] Подготовить и сохранить изменения (`git add`, `git commit`) с понятным сообщением.
- [ ] Посмотреть историю (`git log --oneline --graph --all`).
- [ ] Отправить и получить изменения (`git push`, `git pull`, `git fetch`).

**GitHub**

- [ ] Создать репозиторий и выбрать Public или Private.
- [ ] Добавить, изменить и удалить файл через сайт.
- [ ] Отправить существующий проект на GitHub, в том числе в репозиторий с README.
- [ ] Войти в GitHub из терминала без пароля от аккаунта.

**Ветки и командная работа**

- [ ] Создать ветку, переключиться, слить и удалить её.
- [ ] Открыть Pull Request, просмотреть **Files changed**, слить PR.
- [ ] Решить конфликт слияния.

**Восстановление и безопасность**

- [ ] Отменить незакоммиченные правки (`git restore`, `git stash`).
- [ ] Отменить отправленный коммит (`git revert`).
- [ ] Восстановить старую версию файла (`git restore --source`).
- [ ] Объяснить разницу между `restore`, `revert` и `reset` и риски `reset --hard` и `push --force`.
- [ ] Найти «потерянный» коммит через `git reflog`.
- [ ] Настроить `.gitignore` и не допустить секреты в репозиторий.

**Работа с AI**

- [ ] Начинать задачу для AI с чистого `git status` и отдельной ветки.
- [ ] Проверять изменения AI через `git diff` и тесты перед коммитом.
- [ ] Откатывать неудачные изменения AI.

**Оформление проектов**

- [ ] Оформить README, LICENSE, CHANGELOG, CONTRIBUTING, SECURITY.
- [ ] Выбрать лицензию по целям проекта и проверить лицензии зависимостей.
- [ ] Настроить базовый CI и Dependabot.
- [ ] Выпустить версию: тег и релиз на GitHub.

## 8.6. Что изучать дальше

- **GitHub Skills** — бесплатные интерактивные курсы прямо в GitHub: [learn.github.com/skills](https://learn.github.com/skills). Начните с [Introduction to GitHub](https://github.com/skills/introduction-to-github), затем [Review pull requests](https://github.com/skills/review-pull-requests), [Resolve merge conflicts](https://github.com/skills/resolve-merge-conflicts), [Hello GitHub Actions](https://github.com/skills/hello-github-actions) и [Secure your repository's supply chain](https://github.com/skills/secure-repository-supply-chain).
- **Книга Pro Git на русском** — бесплатно на [git-scm.com/book/ru/v2](https://git-scm.com/book/ru/v2). Главы 1–3 повторяют и углубляют эту методичку.
- **Темы следующего уровня:** `git rebase`, подписание коммитов, Git LFS, GitHub Pages, GitHub Projects.

Все источники — в файле [sources.md](sources.md).
