from typing import List, Dict, Any, Optional, Tuple
from models.dish import Dish, Meal, DietTarget, DietTolerance, MealStructure

try:
    from pulp import (
        LpProblem, LpMinimize, LpVariable, lpSum, LpBinary,
        LpStatusOptimal, value, LpStatus
    )
    PULP_AVAILABLE = True
except ImportError:
    PULP_AVAILABLE = False


class PulpDietSolver:
    """Решатель задачи оптимальной диеты на основе PuLP"""

    def __init__(self, dishes: List[Dish]):
        self.dishes = dishes
        self.n_dishes = len(dishes)

    def solve(self, target: DietTarget, tolerance: DietTolerance,
              structure: MealStructure) -> Dict[str, Any]:
        """
        Решает задачу оптимизации с помощью PuLP.
        
        Формулировка задачи:
        - Переменные: x_i = 1 если блюдо i выбрано, 0 иначе
        - Ограничения: 
          * БЖУ и калории в пределах допуска
          * Количество блюд в пределах структуры
        - Цель: минимизировать отклонение от целевых значений + цена
        """
        
        if not PULP_AVAILABLE:
            return {"status": "error", "message": "PuLP не установлен"}
        
        if not self.dishes:
            return {"status": "error", "message": "Список блюд пуст"}

        # Создаём задачу оптимизации
        prob = LpProblem("Optimal_Diet", LpMinimize)

        # Переменные решения: x_i = 1 если блюдо i выбрано
        x = [LpVariable(f"dish_{i}", cat=LpBinary) for i in range(self.n_dishes)]

        # Целевая функция: минимизировать отклонения + цена
        # Используем вспомогательные переменные для отклонений
        dev_calories_pos = LpVariable("dev_calories_pos", lowBound=0)
        dev_calories_neg = LpVariable("dev_calories_neg", lowBound=0)
        dev_proteins_pos = LpVariable("dev_proteins_pos", lowBound=0)
        dev_proteins_neg = LpVariable("dev_proteins_neg", lowBound=0)
        dev_fats_pos = LpVariable("dev_fats_pos", lowBound=0)
        dev_fats_neg = LpVariable("dev_fats_neg", lowBound=0)
        dev_carbs_pos = LpVariable("dev_carbs_pos", lowBound=0)
        dev_carbs_neg = LpVariable("dev_carbs_neg", lowBound=0)

        # Минимизируем сумму отклонений (нормированных) + цена
        prob += (
            dev_calories_pos + dev_calories_neg +
            dev_proteins_pos + dev_proteins_neg +
            dev_fats_pos + dev_fats_neg +
            dev_carbs_pos + dev_carbs_neg +
            lpSum([self.dishes[i].price * x[i] for i in range(self.n_dishes)]) * 0.01
        ), "Objective"

        # Ограничения на БЖУ и калории с допуском
        tol = tolerance.to_dict()
        tgt = target.to_dict()

        # Калории
        prob += lpSum([self.dishes[i].calories * x[i] for i in range(self.n_dishes)]) - dev_calories_pos + dev_calories_neg == tgt['calories']
        
        # Белки
        prob += lpSum([self.dishes[i].proteins * x[i] for i in range(self.n_dishes)]) - dev_proteins_pos + dev_proteins_neg == tgt['proteins']
        
        # Жиры
        prob += lpSum([self.dishes[i].fats * x[i] for i in range(self.n_dishes)]) - dev_fats_pos + dev_fats_neg == tgt['fats']
        
        # Углеводы
        prob += lpSum([self.dishes[i].carbs * x[i] for i in range(self.n_dishes)]) - dev_carbs_pos + dev_carbs_neg == tgt['carbs']

        # Ограничения на количество блюд (структура питания)
        # Для упрощения считаем общее количество блюд за день
        total_dishes = lpSum(x)
        min_total = structure.min_dishes_per_meal * structure.num_meals
        max_total = structure.max_dishes_per_meal * structure.num_meals
        
        prob += total_dishes >= min_total, "MinDishes"
        prob += total_dishes <= max_total, "MaxDishes"

        # Ограничение на цену (опционально, с допуском)
        max_price = tgt['price'] * (1 + tol['price'] / 100)
        prob += lpSum([self.dishes[i].price * x[i] for i in range(self.n_dishes)]) <= max_price, "MaxPrice"

        # Решаем задачу
        prob.solve()

        # Проверяем статус решения
        if LpStatusOptimal != 1 and prob.status != LpStatusOptimal:
            return {
                "status": "error",
                "message": f"Не удалось найти оптимальное решение. Статус: {LpStatus[prob.status]}",
                "method": "PuLP"
            }

        # Извлекаем решение
        selected_dishes = []
        for i in range(self.n_dishes):
            if value(x[i]) == 1:
                selected_dishes.append(self.dishes[i])

        # Формируем план питания (распределяем по приёмам пищи)
        meals_plan = self._distribute_meals(selected_dishes, structure.num_meals)

        # Считаем итоги
        totals = {
            'calories': sum(d.calories for d in selected_dishes),
            'proteins': sum(d.proteins for d in selected_dishes),
            'fats': sum(d.fats for d in selected_dishes),
            'carbs': sum(d.carbs for d in selected_dishes),
            'price': sum(d.price for d in selected_dishes),
            'weight': sum(d.weight for d in selected_dishes)
        }

        return self._format_result(meals_plan, totals, target, tolerance, "PuLP")

    def _distribute_meals(self, dishes: List[Dish], num_meals: int) -> List[List[Dish]]:
        """Распределяет блюда по приёмам пищи"""
        if num_meals <= 0:
            return []
        
        # Простое равномерное распределение
        meals = [[] for _ in range(num_meals)]
        for i, dish in enumerate(dishes):
            meals[i % num_meals].append(dish)
        
        # Удаляем пустые приёмы пищи
        meals = [m for m in meals if m]
        
        return meals if meals else [[]]

    def _format_result(self, meals_plan: List[List[Dish]], totals: Dict[str, float],
                       target: DietTarget, tolerance: DietTolerance, 
                       method: str = "PuLP") -> Dict[str, Any]:
        """Форматирует результат для вывода"""
        
        output_meals = []
        for i, meal_dishes in enumerate(meals_plan):
            dish_list = []
            meal_totals = {
                'calories': 0, 'proteins': 0, 'fats': 0,
                'carbs': 0, 'price': 0, 'weight': 0
            }
            
            for d in meal_dishes:
                dish_list.append({
                    "name": d.name,
                    "calories": d.calories,
                    "price": d.price,
                    "weight": d.weight,
                    "recipe": d.recipe
                })
                meal_totals['calories'] += d.calories
                meal_totals['proteins'] += d.proteins
                meal_totals['fats'] += d.fats
                meal_totals['carbs'] += d.carbs
                meal_totals['price'] += d.price
                meal_totals['weight'] += d.weight
            
            output_meals.append({
                "meal_number": i + 1,
                "dishes": dish_list,
                "meal_totals": meal_totals
            })

        # Расчёт отклонений
        report_totals = {}
        target_dict = target.to_dict()
        tolerance_dict = tolerance.to_dict()
        
        for key in target_dict:
            actual = totals[key]
            target_val = target_dict[key]
            tol = tolerance_dict[key]
            diff = actual - target_val
            pct = (diff / target_val * 100) if target_val != 0 else 0
            status = "OK" if abs(pct) <= tol else "OUT"
            
            report_totals[key] = {
                "target": target_val,
                "actual": round(actual, 2),
                "deviation_pct": round(pct, 2),
                "status": status
            }

        return {
            "status": "success",
            "method": method,
            "daily_totals": report_totals,
            "total_price": round(totals['price'], 2),
            "total_weight": round(totals['weight'], 2),
            "plan": output_meals
        }