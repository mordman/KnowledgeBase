# Sphinx — Генератор документации Python проектов

Sphinx — это мощный генератор документации, который преобразует исходные файлы (RST, Markdown) в различные форматы (HTML, PDF, ePub и т.д.). Широко используется в Python сообществе.

## Official

| Ресурс | Ссылка | Описание |
|--------|--------|---------|
| Официальный сайт | https://www.sphinx-doc.org/ | Полная документация и гайды |
| GitHub | https://github.com/sphinx-doc/sphinx | Исходный код проекта |
| PyPI | https://pypi.org/project/Sphinx/ | Пакет для установки |
| ReadTheDocs | https://docs.readthedocs.io/ | Платформа для хостинга документации |

## Docker

### Использование Sphinx в контейнере

```dockerfile
FROM python:3.11-slim

WORKDIR /docs

RUN pip install sphinx sphinx-rtd-theme

COPY . .

CMD ["sphinx-build", "-b", "html", "source", "build/html"]
```

### Команды Docker

```bash
# Сборка образа
docker build -t sphinx-builder .

# Запуск генерации документации
docker run --rm -v $(pwd):/docs sphinx-builder

# Интерактивная работа
docker run -it --rm -v $(pwd):/docs sphinx-builder bash
```

## Git

### Рекомендации для версионирования

```bash
# Игнорировать артефакты сборки
echo "build/" >> .gitignore
echo "_build/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".doctrees/" >> .gitignore
```

### Типичная структура в Git

```
docs/
├── source/
│   ├── conf.py
│   ├── index.rst
│   └── modules/
├── build/          # Не коммитить
├── Makefile
└── requirements.txt
```

## Documentation

### Структура проекта Sphinx

```
docs/
├── source/
│   ├── conf.py                 # Конфигурация Sphinx
│   ├── index.rst               # Главная страница
│   ├── getting_started.rst     # Руководство начинающих
│   ├── api/
│   │   └── modules.rst
│   └── _static/
│       └── custom.css
├── build/                      # Генерируемые файлы
├── Makefile                    # Команды сборки (Unix)
└── make.bat                    # Команды сборки (Windows)
```

### Быстрый старт

```bash
# 1. Установка
pip install sphinx

# 2. Инициализация проекта
sphinx-quickstart docs

# 3. Добавление контента в source/index.rst
# 4. Сборка HTML
cd docs
make html

# 5. Просмотр результата
open build/html/index.html  # macOS
# или
xdg-open build/html/index.html  # Linux
# или
start build\html\index.html  # Windows
```

### Основной синтаксис reStructuredText (RST)

```rst
Заголовок секции
================

Подзаголовок
------------

Абзац с **жирным** и *курсивом*.

Список:

- Пункт 1
- Пункт 2
- Вложенный пункт

Нумерованный список:

1. Первый
2. Второй

Код:

.. code-block:: python

    def hello():
        print("Hello, Sphinx!")

Ссылка на другую страницу:

:doc:`getting_started`

Внешняя ссылка:

`Python <https://python.org>`_
```

### Конфигурация (conf.py)

```python
project = 'My Project'
copyright = '2026, Автор'
author = 'Автор'

extensions = [
    'sphinx.ext.autodoc',      # Автогенерация из docstrings
    'sphinx.ext.viewcode',     # Ссылки на исходный код
    'sphinx_rtd_theme',        # Read the Docs тема
]

html_theme = 'sphinx_rtd_theme'

html_static_path = ['_static']
```

### Темы оформления

| Тема | Установка | Описание |
|------|-----------|---------|
| sphinx_rtd_theme | `pip install sphinx-rtd-theme` | Профессиональный вид, используется ReadTheDocs |
| pydata-sphinx-theme | `pip install pydata-sphinx-theme` | Современная тема для научных проектов |
| furo | `pip install furo` | Минималистичная, быстрая тема |
| alabaster | встроена | Простая тема по умолчанию |

### Автогенерация документации из кода

```python
# conf.py
extensions = ['sphinx.ext.autodoc']

# Пример в RST файле:
# automodule:: mypackage.mymodule
#    :members:
#    :undoc-members:
```

## Files

### Полезные файлы проекта

```
docs/
├── source/
│   ├── conf.py              # Основная конфигурация
│   ├── index.rst            # Главная страница
│   └── requirements.txt     # Зависимости (если нужны)
├── Makefile                 # Автоматизация сборки (Unix)
├── make.bat                 # Автоматизация сборки (Windows)
└── .readthedocs.yaml        # Конфиг для ReadTheDocs
```

### Readthedocs конфиг (.readthedocs.yaml)

```yaml
version: 2

build:
  os: ubuntu-20.04
  tools:
    python: "3.11"

python:
  install:
    - requirements: docs/requirements.txt

sphinx:
  configuration: docs/source/conf.py

formats:
  - pdf
  - epub
```

### Tipы файлов

- `.rst` — reStructuredText (рекомендуется для Sphinx)
- `.md` — Markdown (нужно расширение myst-parser)
- `.py` — Python модули (для autodoc)

---

**Дополнительные ресурсы:**
- [Sphinx Tutorial](https://www.sphinx-doc.org/en/master/tutorial/)
- [reStructuredText Primer](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
- [Sphinx Extensions](https://www.sphinx-doc.org/en/master/usage/extensions/)