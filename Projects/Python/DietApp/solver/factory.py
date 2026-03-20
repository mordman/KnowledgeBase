from typing import List, Optional
from models.dish import Dish
from .diet_solver import HeuristicDietSolver
from .pulp_solver import PulpDietSolver, PULP_AVAILABLE


class SolverFactory:
    """Фабрика для создания подходящего решателя"""

    @staticmethod
    def create(dishes: List[Dish], prefer_pulp: bool = True) -> Optional[object]:
        """
        Создаёт решатель в зависимости от доступности PuLP.
        
        Args:
            dishes: Список блюд
            prefer_pulp: Предпочитать PuLP если доступен
        
        Returns:
            Экземпляр решателя или None
        """
        if prefer_pulp and PULP_AVAILABLE:
            return PulpDietSolver(dishes)
        else:
            return HeuristicDietSolver(dishes)

    @staticmethod
    def get_method_name() -> str:
        """Возвращает название используемого метода"""
        if PULP_AVAILABLE:
            return "PuLP (Линейное программирование)"
        else:
            return "Эвристический (Монте-Карло)"

    @staticmethod
    def is_pulp_available() -> bool:
        """Проверяет доступность PuLP"""
        return PULP_AVAILABLE