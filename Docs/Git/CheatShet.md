# Git Cheat Sheet 📘

Расширенная Markdown-версия [официальной шпаргалки Git](https://git-scm.com/cheat-sheet) с дополнительными полезными командами.

---

## 🚀 Начало работы

| Команда | Описание |
|---------|----------|
| `git init` | Создать новый репозиторий в текущей директории |
| `git clone <url>` | Клонировать существующий репозиторий |
| `git clone --depth 1 <url>` | Поверхностное клонирование (только последний коммит) |
| `git clone -b <branch> <url>` | Клонировать конкретную ветку |
| `git clone --recurse-submodules <url>` | Клонировать вместе с подмодулями |

---

## 📝 Подготовка к коммиту

| Команда | Описание |
|---------|----------|
| `git add <file>` | Добавить файл в индекс (staging) |
| `git add .` | Добавить все изменённые и новые файлы |
| `git add -u` | Добавить только изменённые/удалённые файлы (без новых) |
| `git add -A` | Добавить все изменения (эквивалент `git add .` + удалённые) |
| `git add -p` | Интерактивно выбирать части файла для индексации |
| `git mv <old> <new>` | Переименовать/переместить файл |
| `git rm <file>` | Удалить файл и отметить удаление в индексе |
| `git rm --cached <file>` | Убрать файл из индекса, оставив в рабочей директории |
| `git reset <file>` | Убрать файл из индекса (сохраняет изменения) |
| `git restore --staged <file>` | Современная альтернатива `git reset <file>` |
| `git restore --staged .` | Убрать все файлы из индекса |
| `git status` | Показать состояние рабочей директории и индекса |
| `git status -s` | Краткий формат статуса |

---

## 💾 Создание коммитов

| Команда | Описание |
|---------|----------|
| `git commit` | Создать коммит (откроет редактор для сообщения) |
| `git commit -m "message"` | Создать коммит с сообщением |
| `git commit -am "message"` | Проиндексировать изменённые файлы и закоммитить |
| `git commit --amend` | Изменить последний коммит (сообщение или добавить забытые файлы) |
| `git commit --amend --no-edit` | Изменить коммит без правки сообщения |
| `git commit --allow-empty -m "msg"` | Создать пустой коммит |
| `git commit -m "subject" -m "body"` | Коммит с заголовком и описанием |

---

## 🔀 Работа с ветками

| Команда | Описание |
|---------|----------|
| `git branch` | Список локальных веток |
| `git branch -r` | Список удалённых веток |
| `git branch -a` | Список всех веток (локальные + удалённые) |
| `git branch <name>` | Создать новую ветку |
| `git branch -d <name>` | Удалить смерженную ветку |
| `git branch -D <name>` | Принудительно удалить ветку |
| `git branch -m <new-name>` | Переименовать текущую ветку |
| `git branch --sort=-committerdate` | Сортировка веток по дате последнего коммита |
| `git switch <name>` | Переключиться на ветку (современный способ) |
| `git switch -c <name>` | Создать и переключиться на новую ветку |
| `git checkout <name>` | Переключиться на ветку (старый способ) |
| `git checkout -b <name>` | Создать и переключиться на ветку (старый способ) |

---

## 🔍 Diff — различия между файлами и коммитами

| Команда | Описание |
|---------|----------|
| `git diff` | Различия в unstaged файлах |
| `git diff --staged` | Различия в staged файлах |
| `git diff HEAD` | Все изменения относительно последнего коммита |
| `git diff <commit> <commit>` | Различия между двумя коммитами |
| `git diff <commit> <file>` | Изменения одного файла с момента коммита |
| `git diff <commit> --stat` | Краткая сводка изменений (какие файлы и сколько строк) |
| `git diff --word-diff` | Различия по словам, а не по строкам |
| `git diff --name-only` | Только имена изменённых файлов |
| `git diff --name-status` | Имена файлов и их статус (A/M/D) |
| `git show <commit>` | Показать содержимое коммита с diff |
| `git show <commit> --stat` | Сводка коммита |

### Способы ссылки на коммит
- Имя ветки: `main`, `feature/login`
- Тег: `v0.1`
- Hash коммита: `3e887ab`
- Удалённая ветка: `origin/main`
- Текущий коммит: `HEAD`
- Предыдущие коммиты: `HEAD^`, `HEAD~3`, `HEAD^^^`

---

## ❌ Отмена изменений

| Команда | Описание |
|---------|----------|
| `git restore <file>` | Отменить unstaged изменения в файле |
| `git checkout <file>` | Отменить unstaged изменения (старый способ) |
| `git restore --staged --worktree <file>` | Отменить все изменения (staged + unstaged) в файле |
| `git restore --staged --worktree .` | Отменить все изменения во всём проекте |
| `git reset --hard` | Откатить всё к последнему коммиту (опасно!) |
| `git reset --soft HEAD^` | Отменить коммит, сохранить изменения в индексе |
| `git reset --mixed HEAD^` | Отменить коммит, сохранить изменения в рабочей директории |
| `git reset HEAD^` | "Отменить" последний коммит (рабочая директория не меняется) |
| `git clean -fd` | Удалить неотслеживаемые файлы и директории |
| `git clean -n` | "Сушка" — показать, что удалит `git clean` |
| `git checkout --orphan <name>` | Создать ветку без истории |

---

## 📦 Stash (заначка)

| Команда | Описание |
|---------|----------|
| `git stash` | Спрятать все изменения |
| `git stash push -m "message"` | Спрятать изменения с описанием |
| `git stash -u` | Спрятать включая неотслеживаемые файлы |
| `git stash --keep-index` | Спрятать только unstaged изменения |
| `git stash list` | Список всех stash-ей |
| `git stash pop` | Применить и удалить последний stash |
| `git stash apply` | Применить stash без удаления |
| `git stash drop stash@{n}` | Удалить конкретный stash |
| `git stash show stash@{n}` | Показать изменения в stash |
| `git stash clear` | Удалить все stash-и |
| `git stash branch <name> stash@{n}` | Создать ветку из stash |

---

## 🛠 Редактирование истории

| Команда | Описание |
|---------|----------|
| `git rebase -i HEAD~5` | Интерактивный rebase последних 5 коммитов |
| `git rebase -i <commit>` | Интерактивный rebase начиная с коммита |
| `git reflog` | Журнал всех операций с HEAD (спасает после ошибок!) |
| `git reflog <branch>` | Reflog конкретной ветки |
| `git reset --hard <commit>` | Восстановиться к коммиту после неудачного rebase |
| `git rebase --abort` | Прервать текущий rebase |
| `git rebase --continue` | Продолжить rebase после разрешения конфликтов |
| `git rebase --skip` | Пропустить проблемный коммит при rebase |
| `git cherry-pick <commit>` | Скопировать один коммит в текущую ветку |
| `git cherry-pick -n <commit>` | Cherry-pick без авто-коммита |
| `git cherry-pick <commit1> <commit2>` | Скопировать несколько коммитов |

---

## 🏛 Археология кода (история)

| Команда | Описание |
|---------|----------|
| `git log` | Показать историю коммитов |
| `git log --oneline` | Компактная история (по коммиту на строку) |
| `git log --graph` | История с графом ветвления |
| `git log --oneline --graph --all` | Полная графическая история всех веток |
| `git log -n 5` | Последние 5 коммитов |
| `git log --author="name"` | Коммиты определённого автора |
| `git log --since="2024-01-01"` | Коммиты с указанной даты |
| `git log --until="2024-12-31"` | Коммиты до указанной даты |
| `git log --grep="keyword"` | Поиск по сообщению коммита |
| `git log -- <file>` | История изменений файла |
| `git log --follow <file>` | История файла с учётом переименований |
| `git log -G "pattern"` | Поиск по добавленному/удалённому тексту |
| `git log -S "string"` | Коммиты, в которых появилась/исчезла строка |
| `git log --diff-filter=A` | Только коммиты с добавлением файлов |
| `git blame <file>` | Кто последним изменил каждую строку |
| `git blame -L 10,20 <file>` | Blame для диапазона строк |
| `git shortlog` | Группировка коммитов по авторам |
| `git shortlog -sn` | Количество коммитов каждого автора |
| `git bisect start` | Бинарный поиск бага между коммитами |
| `git bisect bad` | Пометить текущий коммит как "с багом" |
| `git bisect good <commit>` | Пометить коммит как "без бага" |
| `git bisect reset` | Завершить bisect |

---

## 🔗 Объединение расходящихся веток

| Команда | Описание |
|---------|----------|
| `git rebase main` (на `banana`) | Перенести `banana` поверх `main` |
| `git merge banana` (на `main`) | Слить `banana` в `main` (merge commit) |
| `git merge --no-ff banana` | Всегда создавать merge commit |
| `git merge --squash banana` | Squash merge (все коммиты в один, требует commit) |
| `git merge --ff-only banana` | Fast-forward merge (ошибка, если невозможен) |
| `git pull --rebase` | Fetch + rebase вместо merge |
| `git pull --ff-only` | Fetch + fast-forward |
| `git merge --abort` | Отменить незавершённый merge |

### Решение конфликтов
1. `git status` — посмотреть конфликтующие файлы
2. Вручную отредактировать файлы (разметка `<<<<<<<`, `=======`, `>>>>>>>`)
3. `git add <file>` — пометить как решённый
4. `git commit` или `git rebase --continue`

---

## 🌐 Работа с удалёнными репозиториями

| Команда | Описание |
|---------|----------|
| `git remote` | Список удалённых репозиториев |
| `git remote -v` | Список с URL |
| `git remote add <name> <url>` | Добавить удалённый репозиторий |
| `git remote remove <name>` | Удалить remote |
| `git remote rename <old> <new>` | Переименовать remote |
| `git remote set-url <name> <new-url>` | Изменить URL remote |
| `git fetch <remote>` | Получить изменения без merge |
| `git fetch origin main` | Fetch конкретной ветки |
| `git fetch --all` | Fetch всех remote |
| `git fetch --prune` | Удалить ссылки на несуществующие ветки |
| `git pull` | Fetch + merge |
| `git pull origin main` | Pull конкретной ветки |
| `git push` | Push текущей ветки в tracking branch |
| `git push origin main` | Push конкретной ветки |
| `git push -u origin <name>` | Push новой ветки с установкой upstream |
| `git push --all` | Push всех веток |
| `git push --force-with-lease` | Безопасный force push (проверяет, что remote не обновился) |
| `git push --force` | Принудительный push (ОПАСНО!) |
| `git push origin --delete <branch>` | Удалить ветку на remote |
| `git push origin :<branch>` | Альтернативный способ удаления ветки на remote |

---

## 🏷 Теги

| Команда | Описание |
|---------|----------|
| `git tag` | Список всех тегов |
| `git tag <name>` | Создать lightweight тег |
| `git tag -a <name> -m "msg"` | Создать annotated тег |
| `git tag -a <name> <commit>` | Создать тег на конкретный коммит |
| `git tag -d <name>` | Удалить локальный тег |
| `git push origin <tag>` | Push одного тега |
| `git push --tags` | Push всех тегов |
| `git push origin --delete <tag>` | Удалить тег на remote |
| `git tag -f <name> <commit>` | Перезаписать существующий тег |
| `git show <tag>` | Показать информацию о теге |

---

## 🔄 Восстановление файлов

| Команда | Описание |
|---------|----------|
| `git checkout <commit> <file>` | Получить версию файла из коммита |
| `git restore <file> --source <commit>` | Современный способ восстановления |
| `git restore --staged <file> --source <commit>` | Восстановить с индексацией |
| `git checkout HEAD^ -- <file>` | Получить версию из предыдущего коммита |

---

## ⚙️ Конфигурация Git

| Команда | Описание |
|---------|----------|
| `git config user.name "Your Name"` | Установить имя (локально) |
| `git config user.email "you@example.com"` | Установить email (локально) |
| `git config --global user.name "Your Name"` | Установить имя глобально |
| `git config --global user.email "you@example.com"` | Установить email глобально |
| `git config --global core.editor "code --wait"` | Установить редактор (VSCode) |
| `git config --global init.defaultBranch main` | Имя ветки по умолчанию |
| `git config alias.st status` | Создать алиас `git st` |
| `git config alias.co checkout` | Алиас для checkout |
| `git config alias.br branch` | Алиас для branch |
| `git config alias.lg "log --oneline --graph --all"` | Красивый log |
| `git config --global --unset credential.helper` | ❗ **Убрать помощника учётных данных** |
| `git config --global --unset-all credential.helper` | Удалить все значения `credential.helper` |
| `git config --global credential.helper store` | Хранить пароли в открытом виде |
| `git config --global credential.helper cache` | Кэшировать учётные данные в памяти |
| `git config --global credential.helper 'cache --timeout=3600'` | Кэш с таймаутом 1 час |
| `git config --list` | Показать все настройки |
| `git config --global --list` | Показать глобальные настройки |
| `git config --system --list` | Показать системные настройки |
| `git config --get <key>` | Получить значение конкретной опции |
| `man git-config` | Полная документация по конфигурации |

---

## 🔐 Credential Helper (управление учётными данными)

| Команда | Описание |
|---------|----------|
| `git config --global credential.helper` | Посмотреть текущий helper |
| `git config --global credential.helper manager` | Использовать Git Credential Manager |
| `git config --global credential.helper osxkeychain` | Keychain на macOS |
| `git config --global credential.helper wincred` | Credential Manager на Windows |
| `git config --global --unset credential.helper` | ❗ **Отключить helper (запросит пароль снова)** |
| `git credential reject <url>` | Удалить сохранённый пароль для URL |
| `git credential approve` | Сохранить учётные данные вручную |

> **💡 Совет:** Если `git push` не запрашивает пароль и вы не знаете, куда он сохраняется, выполните `git config --global --unset credential.helper` и повторите push.

---

## 📂 Подмодули (submodules)

| Команда | Описание |
|---------|----------|
| `git submodule add <url>` | Добавить подмодуль |
| `git submodule add <url> <path>` | Добавить подмодуль в конкретную директорию |
| `git submodule update --init` | Инициализировать подмодули после clone |
| `git submodule update --init --recursive` | Инициализировать все подмодули рекурсивно |
| `git submodule update --remote` | Обновить подмодули до последних коммитов |
| `git submodule foreach <cmd>` | Выполнить команду во всех подмодулях |
| `git submodule deinit <path>` | Удалить подмодуль |

---

## 🌳 Worktree (рабочие директории)

| Команда | Описание |
|---------|----------|
| `git worktree add <path> <branch>` | Создать новую рабочую директорию для ветки |
| `git worktree list` | Список всех worktree |
| `git worktree remove <path>` | Удалить worktree |
| `git worktree prune` | Очистить битые ссылки worktree |

---

## 🧰 Полезные утилиты

| Команда | Описание |
|---------|----------|
| `git grep "pattern"` | Поиск текста в репозитории |
| `git grep -n "pattern"` | Поиск с номерами строк |
| `git grep -i "pattern"` | Поиск без учёта регистра |
| `git grep -E "regex"` | Поиск с регулярными выражениями |
| `git archive --format=zip HEAD > source.zip` | Экспорт репозитория в архив |
| `git archive --format=tar HEAD \| gzip > source.tar.gz` | Экспорт в tar.gz |
| `git gc` | Очистка и оптимизация репозитория |
| `git gc --aggressive` | Агрессивная оптимизация |
| `git fsck` | Проверка целостности репозитория |
| `git bundle create repo.bundle --all` | Упаковать репозиторий в один файл |
| `git bundle verify repo.bundle` | Проверить bundle |
| `git clone repo.bundle` | Клонировать из bundle |
| `git count-objects -v` | Статистика объектов в репозитории |
| `git show-ref` | Показать все ссылки (ветки, теги) |

---

## 🎯 Алиасы для `.gitconfig`

Добавьте в секцию `[alias]`:

```ini
[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    ca = commit --amend
    lg = log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
    unstage = reset HEAD --
    last = log -1 HEAD
    visual = !gitk
    undo = reset --hard HEAD~1
    aliases = config --get-regexp alias
    branches = branch -a
    remotes = remote -v
```

---

## 🆘 Восстановление удалённых данных

| Команда | Описание |
|---------|----------|
| `git reflog` | Посмотреть историю HEAD |
| `git fsck --lost-found` | Найти "потерянные" коммиты |
| `git show <commit-from-reflog>` | Показать коммит из reflog |
| `git reset --hard <commit-from-reflog>` | Восстановить потерянную ветку |

---

## ⚠️ Опасные команды (использовать с осторожностью!)

- `git reset --hard` — удалит все изменения
- `git push --force` — перезапишет историю на remote
- `git clean -fd` — удалит неотслеживаемые файлы безвозвратно
- `git branch -D` — удалит ветку без проверки на merge
- `rm -rf .git` — удалит репозиторий полностью

**Всегда делайте `git reflog` перед опасными операциями!**

---

> 📖 Официальная документация: [git-scm.com/doc](https://git-scm.com/doc)
> 
> 💬 Быстрая помощь: `git help <command>` или `git <command> --help`