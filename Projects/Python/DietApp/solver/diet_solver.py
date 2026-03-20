import itertools
import random
from typing import List, Dict, Any, Optional
from models.dish import Dish, Meal, DietTarget, DietTolerance, MealStructure


class DietSolver:
    """Решатель задачи оптимальной диеты"""

    def __init__(self, dishes: List[Dish]):
        self.dishes = dishes
        self.possible_meals: List[Meal] = []

    def _calculate_totals(self, dishes: List[Dish]) -> Dict[str, float]:
        """Считает суммарные показатели для списка блюд"""
        totals = {
            'calories': 0,
            'price': 0,
            'proteins': 0,
            'fats': 0,
            'carbs': 0,
            'weight': 0  # Добавлен подсчет общего веса
        }
        for dish in dishes:
            totals['calories'] += dish.calories
            totals['price'] += dish.price
            totals['proteins'] += dish.proteins
            totals['fats'] += dish.fats
            totals['carbs'] += dish.carbs
            totals['weight'] += dish.weight
        return totals

    def _generate_possible_meals(self, structure: MealStructure) -> List[Meal]:
        """Генерирует все возможные варианты одного приема пищи"""
        possible_meals = []
        
        for r in range(structure.min_dishes_per_meal, structure.max_dishes_per_meal + 1):
            for combo in itertools.combinations(self.dishes, r):
                totals = self._calculate_totals(list(combo))
                meal = Meal(dishes=list(combo), totals=totals)
                possible_meals.append(meal)
        
        return possible_meals

    def _get_deviation_score(self, actual: float, target: float, tolerance_pct: float) -> float:
        """
        Возвращает 'штраф' за отклонение.
        Если в пределах допуска - штраф 0.
        Если вне - штраф равен проценту превышения границы.
        """
        if target == 0:
            return 0 if actual == 0 else 100
        
        lower_bound = target * (1 - tolerance_pct / 100)
        upper_bound = target * (1 + tolerance_pct / 100)

        if lower_bound <= actual <= upper_bound:
            return 0
        else:
            if actual < lower_bound:
                return (lower_bound - actual) / target * 100
            else:
                return (actual - upper_bound) / target * 100

    def _meal_score(self, meal: Meal, ideal_per_meal: Dict[str, float]) -> float:
        """Оценивает близость приема пищи к идеалу"""
        score = 0
        for key in ['calories', 'proteins', 'fats', 'carbs']:
            if ideal_per_meal.get(key, 0) > 0:
                score += abs(meal.totals[key] - ideal_per_meal[key]) / ideal_per_meal[key]
        return score

    def solve(self, target: DietTarget, tolerance: DietTolerance, 
              structure: MealStructure) -> Dict[str, Any]:
        """
        Основной алгоритм подбора диеты.
        
        Returns:
            Dict с результатами или ошибкой
        """
        if not self.dishes:
            return {"status": "error", "message": "Список блюд пуст"}

        # 1. Генерация всех возможных вариантов одного приема пищи
        self.possible_meals = self._generate_possible_meals(structure)
        
        if not self.possible_meals:
            return {"status": "error", "message": "Не удалось сгенерировать варианты приемов пищи"}

        # 2. Оптимизация: сортировка по близости к идеалу
        ideal_per_meal = {k: v / structure.num_meals for k, v in target.to_dict().items()}
        self.possible_meals.sort(key=lambda m: self._meal_score(m, ideal_per_meal))
        
        # Оставляем топ вариантов для ускорения
        limit = 2000
        if len(self.possible_meals) > limit:
            self.possible_meals = self.possible_meals[:limit]

        # 3. Сборка дня из приемов пищи (Монте-Карло)
        best_day = None
        best_total_score = float('inf')
        max_iterations = 50000

        for _ in range(max_iterations):
            day_plan = random.choices(self.possible_meals, k=structure.num_meals)
            
            # Суммируем показатели за день
            day_totals = {
                'calories': 0, 'price': 0, 'proteins': 0, 
                'fats': 0, 'carbs': 0, 'weight': 0
            }
            for meal in day_plan:
                for k, v in meal.totals.items():
                    day_totals[k] += v
            
            # Считаем общий штраф
            current_score = 0
            tolerance_dict = tolerance.to_dict()
            target_dict = target.to_dict()
            
            for key in ['calories', 'proteins', 'fats', 'carbs', 'price']:
                dev = self._get_deviation_score(
                    day_totals[key], 
                    target_dict[key], 
                    tolerance_dict[key]
                )
                current_score += dev
            
            if current_score < best_total_score:
                best_total_score = current_score
                best_day = {
                    'meals': day_plan,
                    'totals': day_totals,
                    'score': current_score
                }
                
                if current_score == 0:
                    break

        return self._format_result(best_day, target, tolerance)

    def _format_result(self, result: Optional[Dict], target: DietTarget, 
                       tolerance: DietTolerance) -> Dict[str, Any]:
        """Форматирует результат для вывода"""
        if not result:
            return {"status": "error", "message": "Не удалось найти решение"}
        
        output_meals = []
        for i, meal in enumerate(result['meals']):
            dish_list = []
            for d in meal.dishes:
                dish_list.append({
                    "name": d.name,
                    "calories": d.calories,
                    "price": d.price,
                    "weight": d.weight,       # Добавлен вес
                    "recipe": d.recipe        # Добавлен рецепт
                })
            output_meals.append({
                "meal_number": i + 1,
                "dishes": dish_list,
                "meal_totals": meal.totals
            })

        # Расчет процентов отклонения для отчета
        report_totals = {}
        target_dict = target.to_dict()
        tolerance_dict = tolerance.to_dict()
        
        for key in target_dict:
            actual = result['totals'][key]
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
            "daily_totals": report_totals,
            "total_price": round(result['totals']['price'], 2),
            "total_weight": round(result['totals']['weight'], 2),  # Общий вес за день
            "plan": output_meals
        }