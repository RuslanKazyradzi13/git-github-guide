# Источники и полезные ссылки

**Дата проверки всех источников: 11 октября 2026 года.**

Основные источники — официальная документация. Вторичные источники использованы только там, где первоисточник платный или недоступен, и отмечены отдельно. Сайты и интерфейсы меняются: если ссылка не открывается или описание расходится с сайтом, ориентируйтесь на актуальную официальную документацию.

## Версии, на которые опирается методичка

| Компонент | Версия на дату проверки | Источник |
| --- | --- | --- |
| Git | 2.56.0 (28 сентября 2026) | [git-scm.com](https://git-scm.com/) |
| Git для Windows | 2.56.0(2) (5 октября 2026) | [gitforwindows.org](https://gitforwindows.org/) |
| Git 3.0 | Не выпущен, дата не объявлена | [BreakingChanges](https://git-scm.com/docs/BreakingChanges) |
| `actions/checkout` | v7.0.1 | [github.com/actions/checkout](https://github.com/actions/checkout) |
| `actions/setup-python` | v7.0.0 | [github.com/actions/setup-python](https://github.com/actions/setup-python) |
| `actions/setup-node` | v7.1.0 | [github.com/actions/setup-node](https://github.com/actions/setup-node) |
| `actions/dependency-review-action` | v5.0.0 | [github.com/actions/dependency-review-action](https://github.com/actions/dependency-review-action) |
| Python | 3.15 — новейшая; 3.11–3.14 поддерживаются; 3.10 — окончание поддержки 1 октября 2026 | [Status of Python versions](https://devguide.python.org/versions/) |
| Ruff | 0.17.0 | [pypi.org/project/ruff](https://pypi.org/project/ruff/) |

Примеры вывода команд Git получены в Git для Windows 2.55 в октябре 2026 года. В версии 2.56 формулировки могут незначительно отличаться.

## Git

- [Документация Git](https://git-scm.com/doc) — справочник команд, книга, видео.
- [Справочник команд](https://git-scm.com/docs): [git-init](https://git-scm.com/docs/git-init), [git-status](https://git-scm.com/docs/git-status), [git-add](https://git-scm.com/docs/git-add), [git-commit](https://git-scm.com/docs/git-commit), [git-log](https://git-scm.com/docs/git-log), [git-diff](https://git-scm.com/docs/git-diff), [git-clone](https://git-scm.com/docs/git-clone), [git-push](https://git-scm.com/docs/git-push), [git-pull](https://git-scm.com/docs/git-pull), [git-fetch](https://git-scm.com/docs/git-fetch), [git-remote](https://git-scm.com/docs/git-remote), [git-branch](https://git-scm.com/docs/git-branch), [git-switch](https://git-scm.com/docs/git-switch), [git-merge](https://git-scm.com/docs/git-merge), [git-restore](https://git-scm.com/docs/git-restore), [git-revert](https://git-scm.com/docs/git-revert), [git-reset](https://git-scm.com/docs/git-reset), [git-reflog](https://git-scm.com/docs/git-reflog), [git-stash](https://git-scm.com/docs/git-stash), [git-clean](https://git-scm.com/docs/git-clean), [git-tag](https://git-scm.com/docs/git-tag), [git-config](https://git-scm.com/docs/git-config), [gitignore](https://git-scm.com/docs/gitignore), [gitattributes](https://git-scm.com/docs/gitattributes), [git-filter-branch](https://git-scm.com/docs/git-filter-branch) (предупреждение о рисках и рекомендация git filter-repo).
- [Установка Git для Windows](https://git-scm.com/install/windows), [Git for Windows](https://gitforwindows.org/), [параметры установщика (исходный код)](https://github.com/git-for-windows/build-extra/blob/main/installer/install.iss).
- [Release notes Git 2.51.0](https://github.com/git/git/blob/master/Documentation/RelNotes/2.51.0.adoc) — `git switch` и `git restore` больше не экспериментальные.
- [git filter-repo](https://github.com/newren/git-filter-repo) — инструмент для переписывания истории.

### Книга Pro Git на русском языке

- [Pro Git, 2-е издание](https://git-scm.com/book/ru/v2)
- [О системе контроля версий](https://git-scm.com/book/ru/v2/Введение-О-системе-контроля-версий)
- [Установка Git](https://git-scm.com/book/ru/v2/Введение-Установка-Git)
- [Первоначальная настройка Git](https://git-scm.com/book/ru/v2/Введение-Первоначальная-настройка-Git)
- [Создание Git-репозитория](https://git-scm.com/book/ru/v2/Основы-Git-Создание-Git-репозитория)
- [Запись изменений в репозиторий](https://git-scm.com/book/ru/v2/Основы-Git-Запись-изменений-в-репозиторий)
- [Просмотр истории коммитов](https://git-scm.com/book/ru/v2/Основы-Git-Просмотр-истории-коммитов)
- [Операции отмены](https://git-scm.com/book/ru/v2/Основы-Git-Операции-отмены)
- [Работа с удалёнными репозиториями](https://git-scm.com/book/ru/v2/Основы-Git-Работа-с-удалёнными-репозиториями)
- [Работа с тегами](https://git-scm.com/book/ru/v2/Основы-Git-Работа-с-тегами)
- [О ветвлении в двух словах](https://git-scm.com/book/ru/v2/Ветвление-в-Git-О-ветвлении-в-двух-словах)
- [Основы ветвления и слияния](https://git-scm.com/book/ru/v2/Ветвление-в-Git-Основы-ветвления-и-слияния)
- [Припрятывание и очистка](https://git-scm.com/book/ru/v2/Инструменты-Git-Припрятывание-и-очистка)
- [Раскрытие тайн reset](https://git-scm.com/book/ru/v2/Инструменты-Git-Раскрытие-тайн-reset)
- [GitHub: внесение собственного вклада в проекты](https://git-scm.com/book/ru/v2/GitHub-Внесение-собственного-вклада-в-проекты)

## GitHub

### Начало работы и аккаунт

- [GitHub Docs](https://docs.github.com/)
- [What is GitHub?](https://docs.github.com/en/get-started/start-your-journey/what-is-github)
- [Creating an account on GitHub](https://docs.github.com/en/account-and-profile/how-tos/account-management/creating-an-account-on-github)
- [About mandatory two-factor authentication](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/about-mandatory-two-factor-authentication)
- [Email addresses reference](https://docs.github.com/en/account-and-profile/reference/email-addresses-reference)
- [Blocking command line pushes that expose your personal email address](https://docs.github.com/en/account-and-profile/how-tos/email-preferences/blocking-command-line-pushes-that-expose-your-personal-email-address)
- [Git and GitHub learning resources](https://docs.github.com/en/get-started/start-your-journey/git-and-github-learning-resources)

### Вход из терминала

- [Caching your GitHub credentials in Git](https://docs.github.com/en/get-started/git-basics/caching-your-github-credentials-in-git)
- [Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- [Token authentication requirements for Git operations](https://github.blog/security/application-security/token-authentication-requirements-for-git-operations/) — отказ от паролей с 13 августа 2021 года.
- [Connecting to GitHub with SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [gh auth login](https://cli.github.com/manual/gh_auth_login)

### Репозитории и файлы

- [Creating a new repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository)
- [About repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories)
- [Adding locally hosted code to GitHub](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github)
- [Creating new files](https://docs.github.com/en/repositories/working-with-files/managing-files/creating-new-files)
- [Adding a file to a repository](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository)
- [Editing files](https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files)
- [Deleting files in a repository](https://docs.github.com/en/repositories/working-with-files/managing-files/deleting-files-in-a-repository)
- [Downloading source code archives](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives)
- [Cloning a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
- [About large files on GitHub](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)
- [github/gitignore — шаблоны .gitignore](https://github.com/github/gitignore)

### Ветки, Pull Request, совместная работа

- [GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [Creating a pull request](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-a-pull-request)
- [Pull request reviews](https://docs.github.com/en/pull-requests/reference/pull-request-reviews)
- [Pull request merges](https://docs.github.com/en/pull-requests/reference/pull-request-merges)
- [Resolving a merge conflict on GitHub](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/resolving-a-merge-conflict-on-github)
- [About rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)

### Файлы сообщества, лицензии, релизы

- [Creating a default community health file](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file)
- [Adding a license to a repository](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-license-to-a-repository)
- [Licensing a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)
- [Adding a code of conduct to your project](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-code-of-conduct-to-your-project)
- [Configuring issue templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)
- [Creating a pull request template](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository)
- [About CITATION files](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files)
- [About community profiles for public repositories](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories)
- [Syntax for issue forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)
- [Customizing your repository's social media preview](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview)
- [Basic writing and formatting syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) — элемент `<picture>` для картинок под светлую и тёмную тему
- [Managing releases in a repository](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
- [Automatically generated release notes](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes)
- [GitHub Terms of Service](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service) — раздел D.5 «License Grant to Other Users» (редакция от 27 апреля 2026 года).

### Безопасность и автоматизация

- [GitHub Actions documentation](https://docs.github.com/en/actions)
- [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- [Securely using pull_request_target](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target)
- [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
- [About secret scanning](https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning)
- [About push protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection)
- [Managing user push protection](https://docs.github.com/en/code-security/how-tos/secure-your-secrets/prevent-future-leaks/manage-user-push-protection)
- [About Dependabot alerts](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-alerts)
- [Configuring Dependabot version updates](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/configure-version-updates)
- [Dependabot options reference](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference)
- [About dependency review](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review)
- [About code scanning with CodeQL](https://docs.github.com/en/code-security/concepts/code-scanning/codeql/codeql-code-scanning)
- [Configuring private vulnerability reporting](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository)
- [Adding a security policy](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/add-security-policy)
- [Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [Artifact attestations](https://docs.github.com/en/actions/concepts/security/artifact-attestations)
- [About GitHub Advanced Security](https://docs.github.com/en/get-started/learning-about-github/about-github-advanced-security)

### Обучение

- [GitHub Skills](https://learn.github.com/skills) (адрес skills.github.com перенаправляет сюда): [Introduction to GitHub](https://github.com/skills/introduction-to-github), [Communicate using Markdown](https://github.com/skills/communicate-using-markdown), [Review pull requests](https://github.com/skills/review-pull-requests), [Resolve merge conflicts](https://github.com/skills/resolve-merge-conflicts), [Hello GitHub Actions](https://github.com/skills/hello-github-actions), [Secure your repository's supply chain](https://github.com/skills/secure-repository-supply-chain), [Introduction to Repository Management](https://github.com/skills/introduction-to-repository-management).
- [GitHub Desktop](https://github.com/apps/desktop) — приложение с графическим интерфейсом для Git и GitHub.

## Claude Code

- [Set up Claude Code](https://code.claude.com/docs/en/setup)
- [Best practices](https://code.claude.com/docs/en/best-practices)
- [Memory (CLAUDE.md)](https://code.claude.com/docs/en/memory)
- [Checkpointing](https://code.claude.com/docs/en/checkpointing)
- [Permission modes](https://code.claude.com/docs/en/permission-modes)
- [Settings](https://code.claude.com/docs/en/settings)
- [Worktrees](https://code.claude.com/docs/en/worktrees)
- [Commands](https://code.claude.com/docs/en/commands)
- [Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)

## Лицензии и авторское право

- [Choose a License](https://choosealicense.com/), [сравнительная таблица](https://choosealicense.com/appendix/), [No License](https://choosealicense.com/no-permission/)
- [SPDX License List](https://spdx.org/licenses/) (версия 3.29.0), [SPDX License Expressions](https://spdx.github.io/spdx-spec/v3.0.1/annexes/spdx-license-expressions/), [спецификация SPDX 3.0.1](https://spdx.github.io/spdx-spec/)
- [Open Source Initiative — лицензии](https://opensource.org/licenses), [OSI FAQ](https://opensource.org/faq)
- [GNU: Various Licenses and Comments about Them](https://www.gnu.org/licenses/license-list.html), [GPL FAQ](https://www.gnu.org/licenses/gpl-faq.html)
- [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.html), [GNU LGPL v3](https://www.gnu.org/licenses/lgpl-3.0.html), [GNU AGPL v3](https://www.gnu.org/licenses/agpl-3.0.html)
- [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0), [ASF: Licensing howto (NOTICE)](https://infra.apache.org/licensing-howto.html)
- [Mozilla Public License 2.0](https://www.mozilla.org/en-US/MPL/2.0/), [MPL 2.0 FAQ](https://www.mozilla.org/en-US/MPL/2.0/FAQ/)
- [MIT License](https://opensource.org/license/mit), [BSD 2-Clause](https://opensource.org/license/bsd-2-clause), [BSD 3-Clause](https://opensource.org/license/bsd-3-clause)
- [The Unlicense](https://unlicense.org/), [OSI: The Unlicense](https://opensource.org/license/unlicense)
- [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)
- [REUSE](https://reuse.software/), [спецификация REUSE 3.3](https://reuse.software/spec-3.3/), [руководство](https://reuse.software/tutorial/)
- [Contributor Covenant](https://www.contributor-covenant.org/) (версия 3.0); [официальный перевод версии 2.1 на русский](https://www.contributor-covenant.org/ru/version/2/1/code_of_conduct/)
- [Citation File Format](https://citation-file-format.github.io/), [cffinit](https://citation-file-format.github.io/cff-initializer-javascript/)
- [Developer Certificate of Origin](https://developercertificate.org/)
- [U.S. Copyright Office: Copyright and Artificial Intelligence](https://www.copyright.gov/ai/), [Registration Guidance (2023)](https://www.copyright.gov/ai/ai_policy_guidance.pdf), [Part 2: Copyrightability (2025)](https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf)
- [Гражданский кодекс РФ, часть четвёртая](https://www.consultant.ru/document/cons_doc_LAW_64629/) — ст. 1228, 1259, 1261, 1265, 1286.1, 1295.
- [Urheberrechtsgesetz (Германия), § 29](https://www.gesetze-im-internet.de/urhg/__29.html)
- [Regulation (EU) 2024/2847 — Cyber Resilience Act](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R2847)
- [OpenChain Project](https://www.openchainproject.org/)

## Международные стандарты

Тексты стандартов ISO, как правило, платные. Перечни характеристик и процессов в методичке даны по общедоступным описаниям на iso.org и по вторичным источникам, указанным ниже.

- [ISO/IEC/IEEE 12207:2026 — Software life cycle processes](https://www.iso.org/standard/90219.html) (редакция 2017 года отменена: [iso.org/standard/63712.html](https://www.iso.org/standard/63712.html))
- [ISO/IEC 25010:2023 — Product quality model](https://www.iso.org/standard/78176.html)
- [ISO/IEC 25019:2023 — Quality-in-use model](https://www.iso.org/standard/78177.html)
- [ISO/IEC/IEEE 29148:2018 — Requirements engineering](https://www.iso.org/standard/72089.html)
- [ISO/IEC 5962:2021 — SPDX Specification V2.2.1](https://www.iso.org/standard/81870.html)
- [ISO/IEC 5230:2020 — OpenChain Specification](https://www.iso.org/standard/81039.html)
- [ISO/IEC 18974:2023 — OpenChain security assurance specification](https://www.iso.org/standard/86450.html)
- [ISO: сертификация](https://www.iso.org/certification.html) — ISO не выдаёт сертификаты.
- Вторичные источники: [ANSI blog о редакции 12207:2026](https://blog.ansi.org/ansi/iso-iec-ieee-12207-2026-software-life-cycle/), [arc42 Quality Model: ISO 25010](https://quality.arc42.org/standards/iso-25010).

## Практики и спецификации сообщества

- [Semantic Versioning 2.0.0](https://semver.org/lang/ru/)
- [Keep a Changelog 1.1.0](https://keepachangelog.com/ru/1.1.0/)
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/ru/v1.0.0/)
- [commitlint config-conventional](https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional)
- [EditorConfig](https://editorconfig.org/)
- [Mermaid](https://mermaid.js.org/)

## Безопасность ПО

- [OpenSSF Scorecard](https://scorecard.dev/), [репозиторий и список проверок](https://github.com/ossf/scorecard), [scorecard-action](https://github.com/ossf/scorecard-action)
- [OpenSSF Best Practices Badge](https://www.bestpractices.dev/)
- [OpenSSF OSPS Baseline](https://baseline.openssf.org/)
- [SLSA](https://slsa.dev/), [SLSA v1.2](https://slsa.dev/spec/v1.2/)
- [OWASP SAMM](https://owaspsamm.org/), [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/), [ASVS на GitHub](https://github.com/OWASP/ASVS), [OWASP Top 10:2025](https://owasp.org/Top10/)
- [NIST SP 800-218 (SSDF)](https://csrc.nist.gov/pubs/sp/800/218/final)
- [pip-audit](https://pypi.org/project/pip-audit/)
