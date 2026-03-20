from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class Dish:
    """Модель блюда"""
    name: str
    calories: float
    proteins: float
    fats: float
    carbs: float
    price: float
    weight: float = 0.0          # Вес в граммах
    recipe: str = ""             # Рецепт приготовления

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Dish':
        """Создание объекта из словаря"""
        return cls(
            name=data.get('name', 'Без названия'),
            calories=float(data.get('calories', 0)),
            proteins=float(data.get('proteins', 0)),
            fats=float(data.get('fats', 0)),
            carbs=float(data.get('carbs', 0)),
            price=float(data.get('price', 0)),
            weight=float(data.get('weight', 0)),
            recipe=data.get('recipe', '')
        )

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь"""
        return {
            'name': self.name,
            'calories': self.calories,
            'proteins': self.proteins,
            'fats': self.fats,
            'carbs': self.carbs,
            'price': self.price,
            'weight': self.weight,
            'recipe': self.recipe
        }


@dataclass
class Meal:
    """Модель приема пищи"""
    dishes: list
    totals: Dict[str, float]

    def to_dict(self) -> Dict[str, Any]:
        return {
            'dishes': [d.to_dict() for d in self.dishes],
            'totals': self.totals
        }


@dataclass
class DietTarget:
    """Целевые показатели диеты"""
    calories: float = 2000
    proteins: float = 100
    fats: float = 80
    carbs: float = 250
    price: float = 500

    def to_dict(self) -> Dict[str, float]:
        return {
            'calories': self.calories,
            'proteins': self.proteins,
            'fats': self.fats,
            'carbs': self.carbs,
            'price': self.price
        }


@dataclass
class DietTolerance:
    """Допустимые отклонения в процентах"""
    calories: float = 10
    proteins: float = 10
    fats: float = 10
    carbs: float = 10
    price: float = 20

    def to_dict(self) -> Dict[str, float]:
        return {
            'calories': self.calories,
            'proteins': self.proteins,
            'fats': self.fats,
            'carbs': self.carbs,
            'price': self.price
        }


@dataclass
class MealStructure:
    """Структура питания"""
    num_meals: int = 3
    min_dishes_per_meal: int = 1
    max_dishes_per_meal: int = 2