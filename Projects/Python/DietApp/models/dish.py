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
    
    # Проценты от общей калорийности (если указаны, имеют приоритет над абсолютными значениями)
    proteins_pct: float = 0.0
    fats_pct: float = 0.0
    carbs_pct: float = 0.0

    def to_dict(self) -> Dict[str, float]:
        return {
            'calories': self.calories,
            'proteins': self.proteins,
            'fats': self.fats,
            'carbs': self.carbs,
            'price': self.price
        }
    
    def resolve_macros(self) -> 'DietTarget':
        """
        Если проценты указаны, конвертирует их в граммы на основе калорийности.
        Калорийность макронутриентов:
        - Белки: 4 ккал/г
        - Жиры: 9 ккал/г
        - Углеводы: 4 ккал/г
        
        Returns: новый объект DietTarget с пересчитанными значениями
        """
        new_proteins = self.proteins
        new_fats = self.fats
        new_carbs = self.carbs
        
        # Если указан процент для белков, пересчитываем
        if self.proteins_pct > 0:
            new_proteins = (self.calories * self.proteins_pct / 100) / 4
        
        # Если указан процент для жиров, пересчитываем
        if self.fats_pct > 0:
            new_fats = (self.calories * self.fats_pct / 100) / 9
        
        # Если указан процент для углеводов, пересчитываем
        if self.carbs_pct > 0:
            new_carbs = (self.calories * self.carbs_pct / 100) / 4
        
        return DietTarget(
            calories=self.calories,
            proteins=new_proteins,
            fats=new_fats,
            carbs=new_carbs,
            price=self.price,
            proteins_pct=self.proteins_pct,
            fats_pct=self.fats_pct,
            carbs_pct=self.carbs_pct
        )


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