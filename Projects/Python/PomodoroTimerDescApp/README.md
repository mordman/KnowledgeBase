# Pomodoro Timer

## Обзор

**Pomodoro Widget** — это компактный настольный таймер, реализованный на Python с GUI на `tkinter`. Приложение работает в режиме "поверх всех окон", сохраняет настройки и историю работы в JSON, поддерживает темы, уведомления и расширенный режим расписания.

## Стек технологий

- Python 3.6+
- `tkinter` — графический интерфейс
- `json` — конфигурация и история
- `os`, `platform` — работа с файловой системой и платформо-зависимые проверки
- `datetime` — временные метки и длительность сессий
- `subprocess` — воспроизведение аудио на macOS/Linux

## Структура проекта

```text
Projects/Python/PomodoroTimerDescApp/
├── PomodoroPy.py
├── README.md
├── config.json
├── pomodoro_history.json
└── themes/
    ├── dark.json
    ├── light.json
    └── blue.json
```

## Основные возможности

- Работа и отдых с настраиваемыми интервалами
- Автозапуск следующего шага
- Сохранение позиции и размеров окна
- Поддержка зонального режима расписания
- Сохранение истории сессий в `pomodoro_history.json`
- Окно статистики с итогами и последними записями
- Всплывающие уведомления и звуковые сигналы
- Три встроенные темы и загрузка пользовательских тем

## Архитектура класса

```mermaid
classDiagram
    class Pomodoro {
        +Tk root
        +dict config
        +dict themes
        +dict theme
        +list history
        +int time
        +int max_time
        +bool running
        +bool work_mode
        +bool schedule_active
        +list schedule
        +int schedule_index
        +str schedule_name
        +datetime start_time
        +datetime app_start_time
        +__init__()
        +load_config()
        +load_themes()
        +load_json(path, default)
        +save_json(path, data)
        +setup_window()
        +setup_ui()
        +setup_bindings()
        +toggle()
        +countdown()
        +switch_mode()
        +reset()
        +save_session()
        +show_notification(title, message)
        +open_schedule_menu()
        +activate_schedule(name, steps)
        +activate_schedule_step(index)
        +advance_schedule()
        +open_settings()
        +open_stats()
        +apply_theme(key)
        +close_app()
        +run()
    }
```

## Поток выполнения приложения

```mermaid
flowchart TD
    Start[Start Application] --> Init[Pomodoro.__init__()]
    Init --> LoadConfig[load_config()]
    Init --> LoadThemes[load_themes()]
    Init --> LoadHistory[load_json(pomodoro_history.json)]
    Init --> SetupWindow[setup_window()]
    Init --> SetupUI[setup_ui()]
    Init --> SetupBindings[setup_bindings()]
    Init --> UpdateDisplay[update_display()]
    Init --> UpdateUptime[update_uptime()]
    UpdateUptime --> Mainloop[root.mainloop()]
```

## Основные сценарии вызовов

```mermaid
sequenceDiagram
    participant User
    participant App as Pomodoro
    participant UI as Tkinter

    User->>App: нажимает таймер / кнопку пропуска
    App->>App: toggle() / skip_step()
    App->>UI: обновляет метки и цвета
    App->>App: if running then countdown()
    App->>App: if time == 0 then save_session()
    alt schedule active
        App->>App: advance_schedule()
    else
        App->>App: switch_mode()
    end
    App->>UI: show_notification()
```

## Режимы работы

- Обычный режим Pomodoro: циклы `work_time` / `break_time`
- Расписание: шаги из JSON с каждой длительностью и меткой
- Пропуск шага: кнопка `⏭` или пробел
- Сброс: правый клик мыши
- Закрытие: двойной клик или кнопка `✕`

## Схема логики таймера

```mermaid
flowchart LR
    A[Пользователь запускает таймер] --> B{running?}
    B -- Да --> C[Остановить таймер]
    B -- Нет --> D[Начать отсчет]
    D --> E[countdown()]
    E --> F{time > 0}
    F -- Да --> E
    F -- Нет --> G[save_session()]
    G --> H{schedule_active?}
    H -- Да --> I[advance_schedule()]
    H -- Нет --> J[switch_mode()]
    I --> E
    J --> E
```

## Файловая схема данных

```mermaid
flowchart TD
    Config[config.json] -->|read/write| App
    History[pomodoro_history.json] -->|append| App
    Themes[themes/*.json] -->|load| App
```

## Формат расписания

JSON-расписание поддерживает два формата:

- объект с ключом `steps`
- список шагов напрямую

Пример шага:

```json
{
  "duration": 1500,
  "label": "🍅 Помидор №1",
  "type": "work",
  "sound": ""
}
```

## Стек и зависимости

- Python 3.6+
- Стандартная библиотека:
  - `tkinter`
  - `json`
  - `os`
  - `platform`
  - `datetime`
  - `subprocess`
- Опционально:
  - `winsound` на Windows
  - `paplay`, `aplay`, `mpv`, `vlc`, `ffplay` или `xdg-open` на Linux/macOS

## Запуск

```bash
cd Projects/Python/PomodoroTimerDescApp
python PomodoroPy.py
```

> На Linux/macOS убедитесь, что установлен один из проигрывателей `paplay`, `aplay`, `mpv`, `vlc`, `ffplay` или доступна команда `xdg-open`.

## Как изменить тему

1. Скопируйте файл темы из `themes/`
2. Переименуйте его в `my_theme.json`
3. Отредактируйте цвета и шрифты
4. Перезапустите приложение

## Как добавить настройку

1. Добавьте новый ключ в `DEFAULTS`
2. Создайте поле ввода в `open_settings()`
3. Сохраните значение в `self.config`
4. Обновите `save_json()` и UI при необходимости

## Особенности реализации

- Окно всегда поверх всех остальных благодаря `-topmost`
- Позиция и размер окна сохраняются при выходе
- История сессий хранится в JSON
- Всплывающие уведомления рисуются собственным окном `Toplevel`
- Кроссплатформенный звук с несколькими fallback-вариантами
- Расписание может быть отключено в любой момент
