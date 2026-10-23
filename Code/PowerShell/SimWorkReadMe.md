# Simulate-Workday.ps1 — симулятор рабочего дня

`Simulate-Workday.ps1` — PowerShell-скрипт, который имитирует активность пользователя на компьютере в течение заданного времени.

Скрипт может автоматически выполнять сценарии в:

- Microsoft Excel;
- Microsoft Word;
- Microsoft Outlook;
- Microsoft PowerPoint;
- VS Code;
- Notepad++;
- CMD;
- PowerShell;
- Windows Terminal;
- Git;
- 7-Zip;
- браузере;
- Проводнике;
- Калькуляторе;
- Диспетчере задач;
- Просмотре событий;
- системных оснастках Windows.

Также поддерживается:

- симуляция движения мыши;
- плавное движение курсора;
- движение курсора к активному окну;
- опциональные клики мышью;
- опциональная отправка клавиш/текста;
- логирование действий в файл;
- воспроизводимость через `-Seed`;
- регулировка скорости через `-Speed`;
- отключение отдельных приложений.

---

## Содержание

- [Важное предупреждение](#важное-предупреждение)
- [Требования](#требования)
- [Быстрый старт](#быстрый-старт)
- [Файлы и логи](#файлы-и-логи)
- [Параметры запуска](#параметры-запуска)
- [Примеры вызова](#примеры-вызова)
- [Режимы мыши](#режимы-мыши)
- [Ввод с клавиатуры](#ввод-с-клавиатуры)
- [Поддерживаемые приложения](#поддерживаемые-приложения)
- [Сценарии](#сценарии)
- [Поведение при ошибках](#поведение-при-ошибках)
- [Диагностика и устранение проблем](#диагностика-и-устранение-проблем)
- [Рекомендуемые сценарии использования](#рекомендуемые-сценарии-использования)
- [Ограничения](#ограничения)

---

## Важное предупреждение

Скрипт управляет реальными приложениями, окнами, мышью и клавиатурой.

По умолчанию опасные режимы выключены:

- `-MouseClicks` — выключен;
- `-AllowSendKeys` — выключен.

Если включить:

```powershell
-MouseClicks
```

скрипт будет делать клики мышью.

Если включить:

```powershell
-AllowSendKeys
```

скрипт будет отправлять клавиши в активное окно.

Используйте эти режимы только на тестовой машине или когда понимаете, какое окно находится в фокусе.

Не рекомендуется запускать скрипт:

- на рабочем компьютере с открытыми важными документами;
- в чатах, мессенджерах, почте;
- в терминалах с доступом к продуктивным системам;
- на машинах, где нельзя случайно нажать или напечатать что-то.

---

## Требования

### Обязательное

- ОС Windows;
- PowerShell 5.1 или PowerShell 7;
- интерактивная сессия пользователя.

Для корректной работы с мышью, окнами и вводом скрипт должен выполняться в активной пользовательской сессии.

Он не будет полноценно работать:

- в заблокированной сессии;
- в фоновой службе без интерактивного рабочего стола;
- в некоторых headless-окружениях;
- в CI/CD-агентах без настроенного UI;
- в свернутой или отключенной RDP-сессии.

### Необязательные приложения

Скрипт автоматически определяет доступность приложений и отключает недоступные сценарии.

| Приложение / инструмент | Где ищется |
|---|---|
| Excel | COM-объект `Excel.Application` |
| Word | COM-объект `Word.Application` |
| Outlook | COM-объект `Outlook.Application` |
| PowerPoint | COM-объект `PowerPoint.Application` |
| VS Code | команда `code` в `PATH` |
| Notepad++ | команда `notepad++` или стандартные пути установки |
| Браузер | `msedge`, `chrome`, `firefox`, `brave` |
| Windows Terminal | команда `wt` |
| Git | команда `git` |
| 7-Zip | `7z`, `7zG` или стандартные пути установки |
| Калькулятор | `calc.exe` |
| Проводник | `explorer.exe` |
| Диспетчер задач | `taskmgr.exe` |
| Просмотр событий | `eventvwr.msc` |
| Системные оснастки | `control.exe`, `ms-settings:`, `msinfo32.exe`, `devmgmt.msc`, `services.msc` |

Если приложение не найдено, связанные с ним сценарии можно отключить вручную соответствующим ключом `-No...`.

---

## Быстрый старт

### 1. Открыть PowerShell

Желательно использовать обычное окно PowerShell от текущего пользователя.

### 2. Перейти в папку со скриптом

```powershell
cd C:\Scripts
```

### 3. Запустить скрипт на 60 секунд

```powershell
.\Simulate-Workday.ps1
```

По умолчанию:

- длительность — 60 секунд;
- скорость — обычная;
- мышь плавно двигается;
- клики выключены;
- ввод текста выключен.

---

### Запуск на 5 минут

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 5
```

---

### Запуск на 90 секунд

```powershell
.\Simulate-Workday.ps1 -DurationSeconds 90
```

> Если указан `-DurationSeconds` больше нуля, используется именно он.  
> Если `-DurationSeconds` равен нулю, используется `-DurationMinutes`.

---

### Запуск с воспроизводимостью

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 2 -Seed 42
```

Один и тот же `-Seed` даёт похожую последовательность случайных действий.

---

## Файлы и логи

По умолчанию скрипт использует рабочую папку:

```text
%TEMP%\SimWork
```

Пример:

```text
C:\Users\UserName\AppData\Local\Temp\SimWork
```

Там создаются:

- лог-файл выполнения;
- временные файлы;
- тестовые документы;
- HTML-страницы;
- файлы для Git;
- архивы 7-Zip;
- файлы Outlook;
- презентации PowerPoint;
- сохранённые книги Excel;
- сохранённые документы Word.

Основные результаты:

| Файл | Описание |
|---|---|
| `Simulate-Workday_yyyyMMdd_HHmmss.log` | лог выполнения |
| `Workbook.xlsx` | сохранённая книга Excel |
| `Document.docx` | сохранённый документ Word |
| `PPT_*.pptx` | созданные презентации PowerPoint |
| `OutlookItem_*.msg`, `.ics`, `.vcf` | созданные элементы Outlook |
| `GitDemo` | тестовый Git-репозиторий |
| `*.zip` | архивы 7-Zip |
| `page_*.html` | локальные страницы для браузера |

Чтобы использовать другую рабочую папку:

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 5 -WorkDirectory "C:\SimWork"
```

---

## Параметры запуска

### Основные параметры

| Параметр | Тип | По умолчанию | Описание |
|---|---:|---:|---|
| `-DurationMinutes` | `int` | `0` | Длительность симуляции в минутах |
| `-DurationSeconds` | `int` | `60` | Длительность симуляции в секундах |
| `-Seed` | `int` | `0` | Seed для генератора случайных действий |
| `-Speed` | `double` | `1.0` | Скорость симуляции |
| `-WorkDirectory` | `string` | `%TEMP%\SimWork` | Рабочая папка для файлов и логов |

### Управление приложениями

| Параметр | Что отключает |
|---|---|
| `-NoExcel` | Excel |
| `-NoWord` | Word |
| `-NoVSCode` | VS Code |
| `-NoNotepadPlus` | Notepad++ |
| `-NoCmd` | CMD |
| `-NoPowerShell` | PowerShell-сценарии |
| `-NoBrowser` | браузер |
| `-NoExplorer` | Проводник |
| `-NoOutlook` | Outlook |
| `-NoPowerPoint` | PowerPoint |
| `-NoTerminal` | Windows Terminal |
| `-NoGit` | Git |
| `-No7Zip` | 7-Zip |
| `-NoCalculator` | Калькулятор |
| `-NoTaskManager` | Диспетчер задач |
| `-NoEventViewer` | Просмотр событий |
| `-NoSystemTools` | системные оснастки |

### Параметры мыши

| Параметр | По умолчанию | Описание |
|---|---:|---|
| `-MouseMove` | `Smooth` | Режим движения мыши: `Off`, `Instant`, `Smooth` |
| `-MouseClicks` | выключено | Разрешить клики мышью |
| `-MouseSteps` | `16` | Количество шагов плавного движения |
| `-MouseStepDelayMs` | `18` | Задержка между шагами движения |

### Параметры ввода

| Параметр | По умолчанию | Описание |
|---|---:|---|
| `-AllowSendKeys` | выключено | Разрешить реальную отправку клавиш |

---

## Примеры вызова

### Пример 1. Запуск на 60 секунд

```powershell
.\Simulate-Workday.ps1
```

---

### Пример 2. Запуск на 5 минут

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 5
```

---

### Пример 3. Запуск на 2 минуты 30 секунд

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 2 -DurationSeconds 30
```

Так как `-DurationSeconds` больше нуля, будет использовано значение:

```text
30 секунд
```

Если нужно именно 2 минуты 30 секунд, лучше указать только секунды:

```powershell
.\Simulate-Workday.ps1 -DurationSeconds 150
```

---

### Пример 4. Быстрая симуляция

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 5 -Speed 2
```

Скрипт будет выполнять паузы примерно в 2 раза быстрее.

---

### Пример 5. Медленная симуляция

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 5 -Speed 0.5
```

---

### Пример 6. Очень быстрая симуляция

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 1 -Speed 5
```

---

### Пример 7. Воспроизводимый прогон

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 3 -Seed 123
```

---

### Пример 8. Другая рабочая папка

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 5 -WorkDirectory "D:\SimWork"
```

---

### Пример 9. Отключить мышь

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 5 -MouseMove Off
```

---

### Пример 10. Мгновенное перемещение мыши без плавности

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 5 -MouseMove Instant
```

---

### Пример 11. Плавная мышь с меньшим числом шагов

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 5 -MouseMove Smooth -MouseSteps 8
```

---

### Пример 12. Более плавная и медленная мышь

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 5 -MouseSteps 30 -MouseStepDelayMs 30
```

---

### Пример 13. Включить клики мышью

Осторожно: скрипт будет кликать.

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 1 -MouseClicks
```

---

### Пример 14. Включить ввод текста

Осторожно: скрипт будет печатать в активное окно.

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 1 -AllowSendKeys
```

---

### Пример 15. Полная интерактивная симуляция

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 5 -MouseMove Smooth -MouseClicks -AllowSendKeys
```

---

### Пример 16. Только Excel и Word

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 5 `
  -NoVSCode `
  -NoNotepadPlus `
  -NoCmd `
  -NoPowerShell `
  -NoBrowser `
  -NoExplorer `
  -NoOutlook `
  -NoPowerPoint `
  -NoTerminal `
  -NoGit `
  -No7Zip `
  -NoCalculator `
  -NoTaskManager `
  -NoEventViewer `
  -NoSystemTools
```

---

### Пример 17. Только браузер и Проводник

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 3 `
  -NoExcel `
  -NoWord `
  -NoVSCode `
  -NoNotepadPlus `
  -NoCmd `
  -NoPowerShell `
  -NoOutlook `
  -NoPowerPoint `
  -NoTerminal `
  -NoGit `
  -No7Zip `
  -NoCalculator `
  -NoTaskManager `
  -NoEventViewer `
  -NoSystemTools
```

---

### Пример 18. Только Git и Windows Terminal

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 3 `
  -NoExcel `
  -NoWord `
  -NoVSCode `
  -NoNotepadPlus `
  -NoCmd `
  -NoPowerShell `
  -NoBrowser `
  -NoExplorer `
  -NoOutlook `
  -NoPowerPoint `
  -No7Zip `
  -NoCalculator `
  -NoTaskManager `
  -NoEventViewer `
  -NoSystemTools
```

> Windows Terminal и Git должны быть установлены и доступны в `PATH`.

---

### Пример 19. Только Калькулятор

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 1 `
  -NoExcel `
  -NoWord `
  -NoVSCode `
  -NoNotepadPlus `
  -NoCmd `
  -NoPowerShell `
  -NoBrowser `
  -NoExplorer `
  -NoOutlook `
  -NoPowerPoint `
  -NoTerminal `
  -NoGit `
  -No7Zip `
  -NoTaskManager `
  -NoEventViewer `
  -NoSystemTools
```

---

### Пример 20. Калькулятор с реальным вводом

```powershell
.\Simulate-Workday.ps1 -DurationSeconds 30 `
  -AllowSendKeys `
  -NoExcel `
  -NoWord `
  -NoVSCode `
  -NoNotepadPlus `
  -NoCmd `
  -NoPowerShell `
  -NoBrowser `
  -NoExplorer `
  -NoOutlook `
  -NoPowerPoint `
  -NoTerminal `
  -NoGit `
  -No7Zip `
  -NoTaskManager `
  -NoEventViewer `
  -NoSystemTools
```

---

### Пример 21. Только системные оснастки

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 2 `
  -NoExcel `
  -NoWord `
  -NoVSCode `
  -NoNotepadPlus `
  -NoCmd `
  -NoPowerShell `
  -NoBrowser `
  -NoExplorer `
  -NoOutlook `
  -NoPowerPoint `
  -NoTerminal `
  -NoGit `
  -No7Zip `
  -NoCalculator `
  -NoTaskManager `
  -NoEventViewer
```

---

### Пример 22. Только Диспетчер задач и Просмотр событий

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 2 `
  -NoExcel `
  -NoWord `
  -NoVSCode `
  -NoNotepadPlus `
  -NoCmd `
  -NoPowerShell `
  -NoBrowser `
  -NoExplorer `
  -NoOutlook `
  -NoPowerPoint `
  -NoTerminal `
  -NoGit `
  -No7Zip `
  -NoCalculator `
  -NoSystemTools
```

---

### Пример 23. Запуск без офисных приложений

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 10 -NoExcel -NoWord -NoOutlook -NoPowerPoint
```

---

### Пример 24. Длительная фоновая симуляция без ввода

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 30 -MouseMove Smooth -Speed 1.5
```

---

### Пример 25. Тестовый прогон на 15 секунд

```powershell
.\Simulate-Workday.ps1 -DurationSeconds 15 -Speed 2
```

---

## Режимы мыши

Параметр:

```powershell
-MouseMove <Off|Instant|Smooth>
```

### Off

Мышь не двигается.

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 5 -MouseMove Off
```

---

### Instant

Курсор мгновенно перемещается в целевую точку.

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 5 -MouseMove Instant
```

---

### Smooth

Курсор плавно двигается к целевой точке.

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 5 -MouseMove Smooth
```

Дополнительно можно настроить плавность:

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 5 -MouseSteps 25 -MouseStepDelayMs 25
```

---

## Ввод с клавиатуры

По умолчанию скрипт не печатает текст.

Чтобы включить реальную отправку клавиш:

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 1 -AllowSendKeys
```

Ввод используется только в части сценариев, например:

- печать текста в активное окно;
- ввод команд в CMD;
- ввод выражений в Калькулятор;
- отправка специальных клавиш.

Без `-AllowSendKeys` такие сценарии либо выполняют безопасные действия, либо только логируют, что ввод не был выполнен.

---

## Поддерживаемые приложения

### Excel

Сценарии:

- создание книги;
- заполнение таблиц;
- формулы;
- диаграммы;
- автофильтр;
- комментарии;
- новые листы;
- числовые форматы;
- закрепление области;
- защита листа;
- сохранение в `Workbook.xlsx`.

---

### Word

Сценарии:

- создание документа;
- заголовки;
- таблицы;
- списки;
- поиск и замена;
- форматирование;
- гиперссылки;
- дата и время;
- ориентация страницы;
- колонтитулы;
- сохранение в `Document.docx`.

---

### Outlook

Сценарии:

- создание черновика письма;
- создание встречи;
- создание задачи;
- создание контакта.

Особенности:

- письма не отправляются;
- элементы сохраняются во временные файлы;
- используются форматы `.msg`, `.ics`, `.vcf`.

---

### PowerPoint

Сценарии:

- создание презентации;
- добавление слайдов;
- добавление текстовых блоков;
- заметки к слайдам;
- сохранение в `.pptx`.

---

### VS Code

Сценарии:

- открытие `Scratch.ps1`;
- добавление функций;
- добавление классов;
- TODO/FIXME комментарии;
- Markdown-заметки;
- JavaScript-фрагменты;
- Python-фрагменты;
- CSS-фрагменты;
- `.gitignore`;
- `Dockerfile`.

---

### Notepad++

Сценарии:

- TODO-файлы;
- CSV;
- JSON;
- лог-файлы;
- INI;
- XML;
- SQL;
- YAML;
- BAT;
- имитация печати текста при `-AllowSendKeys`.

---

### CMD

Сценарии:

- диагностика;
- просмотр временной папки;
- сетевые команды;
- batch-файлы;
- видимое окно CMD;
- переменные окружения;
- список процессов;
- циклы `echo`;
- `PATH`;
- `doskey`.

---

### PowerShell

Сценарии:

- сводка процессов;
- математические действия;
- тестирование модуля;
- информация о дисках;
- сводка служб;
- переменные окружения;
- `ping localhost`;
- региональные настройки.

---

### Браузер

Сценарии:

- локальные HTML-отчёты;
- страницы времени;
- списки задач;
- формы;
- CSS-карточки;
- JSON-просмотр;
- открытие нескольких страниц.

---

### Проводник

Сценарии:

- открытие рабочей папки;
- открытие «Этот компьютер»;
- открытие загрузок;
- создание папок;
- создание файлов;
- копирование файлов;
- поиск в папке;
- создание структуры папок;
- открытие папки шрифтов.

---

### Калькулятор

Сценарии:

- открытие калькулятора;
- простое вычисление;
- случайное умножение;
- очистка калькулятора.

Для реального ввода используйте:

```powershell
-AllowSendKeys
```

---

### Windows Terminal

Сценарии:

- открытие терминала;
- выполнение команды;
- открытие PowerShell в терминале.

Требуется команда:

```powershell
wt
```

---

### Git

Сценарии:

- `git init`;
- `git status`;
- `git add`;
- `git commit`;
- `git branch`;
- `git checkout`;
- `git log`.

Репозиторий создаётся в:

```text
%TEMP%\SimWork\GitDemo
```

---

### 7-Zip

Сценарии:

- создание архива;
- просмотр содержимого архива;
- тестирование архива.

Требуется один из вариантов:

- `7z` в `PATH`;
- `7zG` в `PATH`;
- установка 7-Zip в стандартный каталог.

---

### Диспетчер задач

Сценарии:

- открытие Диспетчера задач;
- движение курсора по окну.

---

### Просмотр событий

Сценарии:

- открытие `eventvwr.msc`;
- движение курсора по панелям.

---

### Системные оснастки

Сценарии:

- Панель управления;
- Параметры Windows;
- Сведения о системе;
- Диспетчер устройств;
- Службы.

---

## Сценарии

Скрипт выбирает приложения и сценарии случайно.

Если указан `-Seed`, выбор становится воспроизводимым.

Пример:

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 2 -Seed 777
```

---

## Поведение при ошибках

Скрипт старается не останавливаться из-за одного неудачного сценария.

Если сценарий завершается ошибкой:

1. Ошибка записывается в лог.
2. Скрипт пробует продолжить работу.
3. Если приложение недоступно, оно может быть автоматически отключено.

Некоторые ошибки всё равно останавливают скрипт, например:

- истекло время выполнения;
- остановка пользователем;
- нет ни одного доступного приложения;
- критическая ошибка среды выполнения.

---

## Диагностика и устранение проблем

### Скрипт не запускается из-за политики выполнения

Ошибка может выглядеть так:

```text
не может быть загружен, так как выполнение сценариев отключено
```

Решение для текущего пользователя:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Или разовый запуск с обходом политики:

```powershell
powershell -ExecutionPolicy Bypass -File .\Simulate-Workday.ps1 -DurationSeconds 30
```

---

### Excel или Word недоступны

Если офисные приложения не установлены, используйте:

```powershell
.\Simulate-Workday.ps1 -NoExcel -NoWord
```

Если они установлены, но возникают ошибки, попробуйте:

```powershell
.\Simulate-Workday.ps1 -Speed 0.8
```

или уменьшите нагрузку:

```powershell
.\Simulate-Workday.ps1 -DurationSeconds 30 -NoBrowser -NoVSCode
```

---

### VS Code не найден

Если `code` отсутствует в `PATH`, отключите сценарии VS Code:

```powershell
.\Simulate-Workday.ps1 -NoVSCode
```

Или добавьте VS Code в `PATH`.

---

### Notepad++ не найден

Если Notepad++ установлен в нестандартную папку, скрипт может его не найти.

Решение:

```powershell
.\Simulate-Workday.ps1 -NoNotepadPlus
```

---

### Браузер не найден

Скрипт ищет:

- `msedge`;
- `chrome`;
- `firefox`;
- `brave`.

Если браузер не найден:

```powershell
.\Simulate-Workday.ps1 -NoBrowser
```

---

### Git не найден

Если команда `git` недоступна:

```powershell
.\Simulate-Workday.ps1 -NoGit
```

---

### 7-Zip не найден

Если 7-Zip не установлен или не найден:

```powershell
.\Simulate-Workday.ps1 -No7Zip
```

---

### Windows Terminal не найден

Если команда `wt` недоступна:

```powershell
.\Simulate-Workday.ps1 -NoTerminal
```

---

### Калькулятор открывается, но ввод не работает

Современный калькулятор Windows может требовать активный фокус и интерактивную сессию.

Проверьте:

1. Запущен ли скрипт в активной сессии пользователя.
2. Включён ли ввод:

```powershell
.\Simulate-Workday.ps1 -AllowSendKeys
```

3. Не перекрыто ли окно калькулятора другим окном.

---

### Мышь не двигается

Возможные причины:

- скрипт работает в фоновой сессии;
- рабочий стол заблокирован;
- используется режим `-MouseMove Off`;
- нет интерактивного рабочего стола.

Проверьте запуск в обычном окне PowerShell на рабочем столе.

---

### Текст печатается не туда

Если включён `-AllowSendKeys`, скрипт печатает в активное окно.

Если фокус не был корректно установлен, текст может попасть в другое приложение.

Решение:

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 5
```

без:

```powershell
-AllowSendKeys
```

---

### После завершения остались процессы Excel или Word

Скрипт пытается корректно закрыть COM-объекты, но при аварийном завершении процессы могут остаться.

Проверить:

```powershell
Get-Process EXCEL, WINWORD -ErrorAction SilentlyContinue
```

Завершить:

```powershell
Stop-Process -Name EXCEL -Force -ErrorAction SilentlyContinue
Stop-Process -Name WINWORD -Force -ErrorAction SilentlyContinue
```

---

### Скрипт слишком активный

Уменьшите скорость:

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 5 -Speed 0.5
```

Или отключите мышь:

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 5 -MouseMove Off
```

---

## Рекомендуемые сценарии использования

### 1. Тест автоматизации

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 2 -Seed 42
```

---

### 2. Имитация активности пользователя

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 15 -Speed 1.2
```

---

### 3. Проверка работы с окнами и мышью

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 3 -MouseMove Smooth
```

---

### 4. Проверка клавиатурного ввода

```powershell
.\Simulate-Workday.ps1 -DurationSeconds 30 -AllowSendKeys
```

---

### 5. Тест только офисных приложений

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 5 `
  -NoVSCode `
  -NoNotepadPlus `
  -NoCmd `
  -NoPowerShell `
  -NoBrowser `
  -NoExplorer `
  -NoTerminal `
  -NoGit `
  -No7Zip `
  -NoCalculator `
  -NoTaskManager `
  -NoEventViewer `
  -NoSystemTools
```

---

### 6. Тест только инструментов разработчика

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 5 `
  -NoExcel `
  -NoWord `
  -NoOutlook `
  -NoPowerPoint `
  -NoNotepadPlus `
  -NoBrowser `
  -NoExplorer `
  -NoCalculator `
  -NoTaskManager `
  -NoEventViewer `
  -NoSystemTools
```

---

### 7. Демонстрация для мониторинга активности

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 10 -Speed 1.0 -Seed 1000
```

---

## Ограничения

### Нет точного позиционирования курсора в полях ввода

Скрипт двигает мышь в активное окно и использует приблизительные координаты:

- центр окна;
- рабочая область;
- область редактора;
- область терминала;
- область браузера.

Он не использует точные координаты конкретного текстового поля.

Для точного попадания в элементы нужны:

- UI Automation;
- Accessibility API;
- специализированные драйверы приложений;
- машинное зрение.

---

### Не работает в headless-режиме

Для движения мыши, фокусировки окон и ввода нужна активная пользовательская сессия.

---

### Ввод может попасть не в то окно

Если включён `-AllowSendKeys`, скрипт отправляет клавиши в активное окно.

Если фокус не удалось корректно переключить, ввод может уйти в другое приложение.

---

### Некоторые приложения зависят от языка интерфейса

Скрипт старается использовать нейтральные методы, но часть действий может зависеть от:

- языка Windows;
- языка Office;
- настроек приложения;
- версии приложения.

---

### Длительная работа может создавать много временных файлов

Рабочая папка:

```text
%TEMP%\SimWork
```

может постепенно заполняться:

- логами;
- HTML-файлами;
- архивами;
- презентациями;
- файлами Outlook;
- Git-репозиториями;
- временными скриптами.

Папку можно периодически очищать.

---

## Безопасная рекомендация по умолчанию

Если вы запускаете скрипт впервые, используйте:

```powershell
.\Simulate-Workday.ps1 -DurationSeconds 30 -Speed 1.0
```

Затем можно постепенно включать дополнительные режимы:

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 2 -MouseMove Smooth
```

и только после проверки:

```powershell
.\Simulate-Workday.ps1 -DurationMinutes 2 -MouseClicks -AllowSendKeys
```
