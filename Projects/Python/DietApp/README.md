# 🥗 Оптимальная Диета v1.1

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PuLP Support](https://img.shields.io/badge/PuLP-optional-green.svg)](https://pypi.org/project/pulp/)

Приложение для автоматического составления оптимального рациона питания на один день с использованием методов линейного программирования (PuLP) или эвристического поиска (Монте-Карло).

---

## 📖 Оглавление

1. [Назначение](#-назначение)
2. [Возможности](#-возможности)
3. [Архитектура](#-архитектура)
4. [Установка](#-установка)
5. [Запуск](#-запуск)
6. [Интерфейс](#-интерфейс)
7. [Методы расчёта](#-методы-расчёта)
8. [Форматы данных](#-форматы-данных)
9. [API](#-api)
10. [Примеры](#-примеры)
11. [Troubleshooting](#-troubleshooting)
12. [Планы развития](#-планы-развития)

---

## 🎯 Назначение

Приложение решает задачу оптимизации рациона питания с учётом:

| Параметр | Описание |
|----------|----------|
| 📊 **Калорийность** | Целевое количество калорий за день |
| 🥩 **БЖУ** | Баланс белков, жиров, углеводов |
| 💰 **Бюджет** | Максимальная стоимость продуктов |
| 🍽 **Структура** | Количество приёмов пищи и блюд в каждом |
| ⚖️ **Вес** | Общий вес пищи за день |
| 📝 **Рецепты** | Подробные инструкции приготовления |

---

## ✨ Возможности

### Основные функции

| Функция | Описание | Статус |
|---------|----------|--------|
| 🎲 **Автоподбор диеты** | Алгоритм подбирает комбинации блюд | ✅ |
| 📊 **Гибкие ограничения** | Настройка допустимых отклонений % | ✅ |
| 🍽 **Структура питания** | Настройка приёмов пищи и блюд | ✅ |
| 📝 **Рецепты блюд** | Подробное описание приготовления | ✅ |
| ⚖️ **Вес порций** | Учёт веса каждого блюда | ✅ |
| 💰 **Контроль бюджета** | Расчёт стоимости рациона | ✅ |
| 📥 **Загрузка JSON** | Импорт списка блюд | ✅ |
| 💾 **Экспорт результата** | Сохранение плана в файл | ✅ |
| 🔀 **Два метода расчёта** | PuLP или эвристика | ✅ v1.1 |
| 📊 **Статус решателя** | Отображение доступного метода | ✅ v1.1 |

### Новое в версии 1.1

| Функция | Описание |
|---------|----------|
| 🧮 **PuLP интеграция** | Поддержка линейного программирования |
| 🔄 **Автопереключение** | Автоматический выбор доступного метода |
| ⚙️ **Ручной выбор** | Возможность принудительного выбора метода |
| 📋 **Информирование** | Отображение использованного метода в результате |

---

## 🏗 Архитектура

### Структура проекта

```
DietApp/
├── main.py                 # Точка входа
├── requirements.txt        # Зависимости
├── README.md              # Документация
├── gui/
│   ├── __init__.py
│   └── app.py             # Пользовательский интерфейс
├── solver/
│   ├── __init__.py
│   ├── factory.py         # Фабрика решателей
│   ├── diet_solver.py     # Эвристический решатель
│   └── pulp_solver.py     # PuLP решатель
├── data/
│   ├── __init__.py
│   └── loader.py          # Загрузка данных
└── models/
    ├── __init__.py
    └── dish.py            # Модели данных
```

### Диаграмма компонентов

```
┌─────────────────────────────────────────────────────────────────┐
│                         main.py                                 │
│                    (Точка входа)                                │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      gui/app.py                                 │
│                  (Пользовательский интерфейс)                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │ Параметры   │  │  Данные     │  │    Результат            │ │
│  │ - Цели      │  │  - JSON     │  │    - План питания       │ │
│  │ - Структура │  │  - Блюда    │  │    - Итоги              │ │
│  │ - Метод     │  │  - Валидация│  │    - Экспорт            │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   solver/factory.py                             │
│                   (Фабрика решателей)                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Проверка доступности PuLP                              │   │
│  │  ↓                                                      │   │
│  │  PuLP доступен? ──ДА──> PulpDietSolver                  │   │
│  │       │                                                 │   │
│  │       НЕТ                                               │   │
│  │       ↓                                                 │   │
│  │  HeuristicDietSolver                                    │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┴───────────────┐
                ▼                               ▼
┌───────────────────────────┐   ┌───────────────────────────┐
│  solver/pulp_solver.py    │   │  solver/diet_solver.py    │
│  (Линейное программирование)  │  │  (Эвристика/Монте-Карло)    │
│  - Точное решение         │   │  - Приближённое решение   │
│  - Быстро                 │   │  - Гибко                  │
│  - Требует pulp           │   │  - Без зависимостей       │
└───────────────────────────┘   └───────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      models/dish.py                             │
│                    (Модели данных)                              │
│  Dish | Meal | DietTarget | DietTolerance | MealStructure      │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                       data/loader.py                            │
│                   (Загрузка данных)                             │
│  - JSON парсинг | Валидация | Примеры данных                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 Установка

### Системные требования

| Требование | Минимум | Рекомендуется |
|------------|---------|---------------|
| Python | 3.7+ | 3.9+ |
| ОЗУ | 512 MB | 1 GB |
| Место на диске | 10 MB | 50 MB |
| Экран | 1024x768 | 1920x1080 |

### Вариант 1: Базовая установка (без PuLP)

```bash
# Клонируйте или скачайте проект
cd DietApp

# Запуск без дополнительных зависимостей
python main.py
```

**Плюсы:**
- ✅ Никаких внешних зависимостей
- ✅ Работает из коробки
- ✅ Подходит для обучения

**Минусы:**
- ⚠️ Менее точные расчёты
- ⚠️ Медленнее на больших наборах данных

### Вариант 2: Полная установка (с PuLP)

```bash
# Установка PuLP
pip install pulp>=2.7.0

# Или через requirements.txt
pip install -r requirements.txt

# Запуск приложения
python main.py
```

**Плюсы:**
- ✅ Точные оптимальные решения
- ✅ Быстрые расчёты
- ✅ Гарантии сходимости

**Минусы:**
- ⚠️ Требует установку дополнительной библиотеки

### Проверка установки PuLP

```python
# В Python консоли
>>> import pulp
>>> pulp.__version__
'2.7.0'
>>> pulp.pulpTestAll()
OK
```

---

## 🚀 Запуск

### Команды запуска

| Команда | Описание |
|---------|----------|
| `python main.py` | Запуск приложения |
| `python -m gui.app` | Альтернативный запуск |
| `python -c "import pulp; print(pulp.__version__)"` | Проверка PuLP |

### Аргументы командной строки (планируется)

```bash
# Будущая функциональность
python main.py --input dishes.json --output result.json --method pulp
```

---

## 🖥 Интерфейс

### Главная панель

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Оптимальная Диета v1.1                           │
├─────────────────────────────────┬───────────────────────────────────┤
│  ПАРАМЕТРЫ И ЦЕЛИ             │  ДАННЫЕ И РЕЗУЛЬТАТ               │
│                                 │                                   │
│  Метод решения:                │  📋 JSON список блюд:             │
│  ✅ PuLP доступен              │  ┌─────────────────────────────┐  │
│  ☐ Использовать PuLP           │  │ [{"name": "Овсянка", ...}]  │  │
│                                 │  └─────────────────────────────┘  │
│  ┌───────────────────────────┐  │  [📥 Загрузить] [✓ Проверить]    │
│  │ Ккал      [2000] [%] 10   │  │                                   │
│  │ Белки     [100]  [%] 10   │  │  📊 Результат (JSON):           │
│  │ Жиры      [80]   [%] 10   │  │  ┌─────────────────────────────┐  │
│  │ Углеводы  [250]  [%] 10   │  │  │ {"status": "success", ...}  │  │
│  │ Цена      [500]  [%] 20   │  │  └─────────────────────────────┘  │
│  └───────────────────────────┘  │  [💾 Сохранить в файл]           │
│                                 │                                   │
│  Структура питания:             │                                   │
│  Приёмов пищи: [3]              │                                   │
│  Блюд (мин): [1] (макс): [2]    │                                   │
│                                 │                                   │
│  [🔢 Рассчитать диету]          │                                   │
│  [🗑 Очистить результат]        │                                   │
└─────────────────────────────────┴───────────────────────────────────┘
```

### Элементы интерфейса

| Элемент | Назначение |
|---------|------------|
| **Статус решателя** | Показывает доступный метод расчёта |
| **Чекбокс PuLP** | Включение/выключение использования PuLP |
| **Поля целей** | Целевые значения БЖУ, калорий, цены |
| **Поля отклонений** | Допустимый процент отклонения |
| **Структура питания** | Количество приёмов и блюд |
| **JSON ввод** | Список доступных блюд |
| **JSON вывод** | Результат расчёта |
| **Кнопки** | Действия (расчёт, сохранение, проверка) |

### Индикаторы статуса

| Статус | Значение | Цвет |
|--------|----------|------|
| ✅ PuLP доступен (будет использован) | PuLP установлен и включён | 🟢 Зелёный |
| ⚠️ PuLP доступен (используется эвристика) | PuLP установлен но отключён | 🟠 Оранжевый |
| ❌ PuLP не установлен (используется эвристика) | PuLP отсутствует | 🔴 Красный |

---

## 🔧 Методы расчёта

### Сравнение методов

| Критерий | PuLP | Эвристика |
|----------|------|-----------|
| **Алгоритм** | Линейное программирование | Монте-Карло + эвристика |
| **Точность** | ⭐⭐⭐⭐⭐ Глобальный оптимум | ⭐⭐⭐⭐ Локальный оптимум |
| **Скорость** | ⭐⭐⭐⭐⭐ < 1 секунды | ⭐⭐⭐ 1-5 секунд |
| **Гарантии** | ✅ Доказанная оптимальность | ⚠️ Приближённое решение |
| **Зависимости** | `pip install pulp` | Только стандартные библиотеки |
| **Ограничения** | Линейные ограничения | Гибкие правила |
| **Масштаб** | До 1000 блюд | До 200 блюд (рекомендуется) |
| **Память** | Низкое потребление | Среднее потребление |

### Когда использовать PuLP

✅ **Рекомендуется PuLP когда:**
- Нужна максимальная точность
- Большой список блюд (>50)
- Строгие ограничения по БЖУ
- Важна скорость расчёта
- Есть возможность установить зависимости

✅ **Рекомендуется Эвристика когда:**
- Нельзя устанавливать зависимости
- Маленький список блюд (<50)
- Допустимы приближённые решения
- Нужна максимальная совместимость
- Обучающие/демонстрационные цели

### Автоматический выбор метода

```python
# Логика фабрики решателей
if PULP_AVAILABLE and user_prefers_pulp:
    solver = PulpDietSolver(dishes)  # Точный метод
else:
    solver = HeuristicDietSolver(dishes)  # Эвристический метод
```

---

## 📊 Форматы данных

### Входной JSON (Список блюд)

```json
[
  {
    "name": "Овсянка на воде",
    "calories": 350,
    "proteins": 12,
    "fats": 6,
    "carbs": 60,
    "price": 50,
    "weight": 250,
    "recipe": "1. Залить овсяные хлопья водой в пропорции 1:2.\n2. Довести до кипения.\n3. Варить на медленном огне 10-15 минут."
  },
  {
    "name": "Куриная грудка гриль",
    "calories": 165,
    "proteins": 31,
    "fats": 3.6,
    "carbs": 0,
    "price": 150,
    "weight": 150,
    "recipe": "1. Замариновать грудку в специях.\n2. Жарить по 6-7 минут с каждой стороны."
  }
]
```

#### Поля входного JSON

| Поле | Тип | Обязательное | По умолчанию | Описание |
|------|-----|--------------|--------------|----------|
| `name` | string | ✅ Да | - | Название блюда |
| `calories` | number | ✅ Да | - | Калорийность (ккал) |
| `proteins` | number | ❌ Нет | 0 | Белки (г) |
| `fats` | number | ❌ Нет | 0 | Жиры (г) |
| `carbs` | number | ❌ Нет | 0 | Углеводы (г) |
| `price` | number | ❌ Нет | 0 | Цена (руб) |
| `weight` | number | ❌ Нет | 0 | Вес порции (г) |
| `recipe` | string | ❌ Нет | "" | Рецепт приготовления |

### Выходной JSON (Результат)

```json
{
  "status": "success",
  "method": "PuLP",
  "daily_totals": {
    "calories": {
      "target": 2000,
      "actual": 1985.5,
      "deviation_pct": -0.73,
      "status": "OK"
    },
    "proteins": {
      "target": 100,
      "actual": 102.3,
      "deviation_pct": 2.3,
      "status": "OK"
    },
    "fats": {
      "target": 80,
      "actual": 78.5,
      "deviation_pct": -1.88,
      "status": "OK"
    },
    "carbs": {
      "target": 250,
      "actual": 245.2,
      "deviation_pct": -1.92,
      "status": "OK"
    },
    "price": {
      "target": 500,
      "actual": 485.0,
      "deviation_pct": -3.0,
      "status": "OK"
    }
  },
  "total_price": 485.0,
  "total_weight": 1250.0,
  "plan": [
    {
      "meal_number": 1,
      "dishes": [
        {
          "name": "Овсянка на воде",
          "calories": 350,
          "price": 50,
          "weight": 250,
          "recipe": "1. Залить овсяные хлопья..."
        }
      ],
      "meal_totals": {
        "calories": 350,
        "proteins": 12,
        "fats": 6,
        "carbs": 60,
        "price": 50,
        "weight": 250
      }
    }
  ]
}
```

#### Поля выходного JSON

| Поле | Тип | Описание |
|------|-----|----------|
| `status` | string | "success" или "error" |
| `method` | string | "PuLP" или "Heuristic" |
| `daily_totals` | object | Итоговые показатели за день |
| `total_price` | number | Общая стоимость (руб) |
| `total_weight` | number | Общий вес (г) |
| `plan` | array | План питания по приёмам пищи |

---

## 🔌 API

### Модели данных (`models/dish.py`)

#### Класс `Dish`

```python
@dataclass
class Dish:
    name: str
    calories: float
    proteins: float
    fats: float
    carbs: float
    price: float
    weight: float = 0.0
    recipe: str = ""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Dish'
    def to_dict(self) -> Dict[str, Any]
```

#### Класс `DietTarget`

```python
@dataclass
class DietTarget:
    calories: float = 2000
    proteins: float = 100
    fats: float = 80
    carbs: float = 250
    price: float = 500
    
    def to_dict(self) -> Dict[str, float]
```

#### Класс `DietTolerance`

```python
@dataclass
class DietTolerance:
    calories: float = 10
    proteins: float = 10
    fats: float = 10
    carbs: float = 10
    price: float = 20
    
    def to_dict(self) -> Dict[str, float]
```

#### Класс `MealStructure`

```python
@dataclass
class MealStructure:
    num_meals: int = 3
    min_dishes_per_meal: int = 1
    max_dishes_per_meal: int = 2
```

### Загрузка данных (`data/loader.py`)

#### Класс `DataLoader`

```python
class DataLoader:
    @staticmethod
    def load_dishes_from_json(json_str: str) -> Tuple[Optional[List[Dish]], Optional[str]]
    @staticmethod
    def get_sample_json() -> str
```

**Пример использования:**

```python
from data.loader import DataLoader

loader = DataLoader()
dishes, error = loader.load_dishes_from_json(json_string)

if error:
    print(f"Ошибка: {error}")
else:
    print(f"Загружено {len(dishes)} блюд")
```

### Решатели (`solver/`)

#### Фабрика `SolverFactory`

```python
class SolverFactory:
    @staticmethod
    def create(dishes: List[Dish], prefer_pulp: bool = True) -> Optional[object]
    @staticmethod
    def get_method_name() -> str
    @staticmethod
    def is_pulp_available() -> bool
```

**Пример использования:**

```python
from solver.factory import SolverFactory

solver = SolverFactory.create(dishes, prefer_pulp=True)
method = SolverFactory.get_method_name()
print(f"Используемый метод: {method}")
```

#### PuLP решатель `PulpDietSolver`

```python
class PulpDietSolver:
    def __init__(self, dishes: List[Dish])
    def solve(self, target: DietTarget, tolerance: DietTolerance, 
              structure: MealStructure) -> Dict[str, Any]
```

#### Эвристический решатель `HeuristicDietSolver`

```python
class HeuristicDietSolver:
    def __init__(self, dishes: List[Dish])
    def solve(self, target: DietTarget, tolerance: DietTolerance, 
              structure: MealStructure) -> Dict[str, Any]
```

### Интерфейс (`gui/app.py`)

#### Класс `DietApp`

```python
class DietApp:
    def __init__(self, root: tk.Tk)
    def run_calculation(self)
    def export_result(self)
    def clear_output(self)
```

---

## 📝 Примеры

### Пример 1: Базовое использование

```python
from data.loader import DataLoader
from solver.factory import SolverFactory
from models.dish import DietTarget, DietTolerance, MealStructure

# Загрузка данных
loader = DataLoader()
json_data = loader.get_sample_json()
dishes, error = loader.load_dishes_from_json(json_data)

# Параметры
target = DietTarget(calories=2000, proteins=100, fats=80, carbs=250, price=500)
tolerance = DietTolerance(calories=10, proteins=10, fats=10, carbs=10, price=20)
structure = MealStructure(num_meals=3, min_dishes_per_meal=1, max_dishes_per_meal=2)

# Расчёт
solver = SolverFactory.create(dishes)
result = solver.solve(target, tolerance, structure)

print(f"Метод: {result.get('method')}")
print(f"Статус: {result.get('status')}")
print(f"Цена: {result.get('total_price')} руб.")
```

### Пример 2: Проверка доступности PuLP

```python
from solver.factory import SolverFactory

if SolverFactory.is_pulp_available():
    print("✅ PuLP доступен - будут точные расчёты")
else:
    print("⚠️ PuLP не установлен - используются эвристики")
    print("Установите: pip install pulp")
```

### Пример 3: Экспорт результата

```python
import json

# После расчёта
with open('diet_plan.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("Результат сохранён в diet_plan.json")
```

### Пример 4: Кастомный список блюд

```json
[
  {
    "name": "Завтрак: Омлет",
    "calories": 300,
    "proteins": 20,
    "fats": 22,
    "carbs": 2,
    "price": 80,
    "weight": 200,
    "recipe": "Взбить 3 яйца, жарить 5 минут"
  },
  {
    "name": "Обед: Паста",
    "calories": 500,
    "proteins": 15,
    "fats": 10,
    "carbs": 90,
    "price": 150,
    "weight": 400,
    "recipe": "Отварить пасту, добавить соус"
  }
]
```

---

## ⚠️ Troubleshooting

### Частые проблемы

| Проблема | Причина | Решение |
|----------|---------|---------|
| `NameError: ttk is not defined` | Не импортирован ttk | Добавить `from tkinter import ttk` |
| `ModuleNotFoundError: No module named 'pulp'` | PuLP не установлен | `pip install pulp` |
| `JSONDecodeError` | Неверный формат JSON | Проверить синтаксис JSON |
| `Список блюд пуст` | Нет блюд в JSON | Добавить хотя бы одно блюдо |
| `Не удалось найти решение` | Слишком строгие ограничения | Увеличить процент отклонения |
| `Медленный расчёт` | Много блюд (>200) | Использовать PuLP или уменьшить список |

### Диагностика

```python
# Проверка Python версии
import sys
print(f"Python {sys.version}")

# Проверка tkinter
import tkinter
print(f"tkinter: {tkinter.TkVersion}")

# Проверка PuLP
try:
    import pulp
    print(f"PuLP: {pulp.__version__}")
except ImportError:
    print("PuLP: не установлен")

# Проверка структуры проекта
import os
print(os.listdir('.'))
```

### Логи и отладка

Включите вывод отладочной информации:

```python
# В solver/factory.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 🔮 Планы развития

### Версия 1.2 (Планируется)

| Функция | Приоритет | Статус |
|---------|-----------|--------|
| Расчёт на неделю | Высокий | 📋 В плане |
| Учёт аллергенов | Высокий | 📋 В плане |
| Сохранение профилей | Средний | 📋 В плане |
| Экспорт в PDF | Средний | 📋 В плане |
| Графики и визуализация | Низкий | 📋 В плане |

### Версия 2.0 (Долгосрочно)

| Функция | Описание |
|---------|----------|
| 🌐 Веб-интерфейс | Доступ через браузер |
| 📝 ЧатБот | Доступ через месенджеры
| 📱  Мобильное приложение | iOS/Android версии |
| 🗄  База данных блюд | SQLite/PostgreSQL интеграция |
| 🤖 ML рекомендации | Персональные рекомендации на основе истории |
| 🤖 ML добавление блюда с фото | Персональные рекомендации на основе истории |
| 🛒 Интеграция с магазинами | Автоматический заказ продуктов |

---

## 📄 Лицензия

MIT License

```
Copyright (c) 2024 DietApp

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🤝 Авторы и контрибьюторы

| Роль | Описание |
|------|----------|
| 🐍 **Python** | 3.7+ |
| 🎨 **GUI** | tkinter (ttk) |
| 📊 **Оптимизация** | PuLP (опционально) |
| 📦 **Структура** | Модульная архитектура |
| 📝 **Документация** | Markdown |

### Используемые библиотеки

| Библиотека | Версия | Назначение | Обязательная |
|------------|--------|------------|--------------|
| `tkinter` | stdlib | GUI | ✅ Да |
| `json` | stdlib | Работа с данными | ✅ Да |
| `itertools` | stdlib | Комбинаторика | ✅ Да |
| `random` | stdlib | Эвристика | ✅ Да |
| `dataclasses` | stdlib | Модели данных | ✅ Да |
| `pulp` | 2.7.0+ | Линейное программирование | ❌ Нет |

---

## 📞 Поддержка

### При возникновении проблем

1. ✅ Проверьте версию Python (`python --version`)
2. ✅ Проверьте формат JSON (кнопка "Проверить JSON")
3. ✅ Убедитесь, что все числовые поля заполнены
4. ✅ Проверьте, что min блюд ≤ max блюд
5. ✅ Убедитесь, что список блюд не пуст
6. ✅ Проверьте доступность PuLP (если нужен точный расчёт)

### Контакты

- 📧 Email: support@dietapp.example
- 🐛 Issues: GitHub Issues
- 📖 Wiki: GitHub Wiki

---

**Версия:** 1.1  
**Дата обновления:** 2026  
**Язык:** Python 3.7+  
**Лицензия:** MIT

---

## 📊 История версий

| Версия | Дата | Изменения |
|--------|------|-----------|
| 1.0 | 2024 | Базовая версия с эвристическим методом |
| 1.1 | 2024 | Добавлена поддержка PuLP, фабрика решателей |
| 1.2 | TBD | Расчёт на неделю, аллергены |
| 2.0 | TBD | Веб-интерфейс, база данных |

---

**Спасибо за использование Оптимальная Диета v1.1! 🥗**