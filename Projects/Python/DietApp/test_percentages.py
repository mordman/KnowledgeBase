"""Тесты для функциональности процентов БЖУ"""
import unittest
from models.dish import DietTarget


class TestDietTargetPercentages(unittest.TestCase):
    """Тесты для DietTarget.resolve_macros()"""

    def test_no_percentages(self):
        """Если проценты не указаны, значения должны остаться прежними"""
        target = DietTarget(
            calories=2000,
            proteins=100,
            fats=80,
            carbs=250
        )
        resolved = target.resolve_macros()
        
        self.assertEqual(resolved.proteins, 100)
        self.assertEqual(resolved.fats, 80)
        self.assertEqual(resolved.carbs, 250)

    def test_proteins_percentage(self):
        """Тест конвертации процентов белков в граммы"""
        # 30% от 2000 ккал = 600 ккал / 4 ккал/г = 150г
        target = DietTarget(
            calories=2000,
            proteins=100,
            proteins_pct=30
        )
        resolved = target.resolve_macros()
        
        self.assertAlmostEqual(resolved.proteins, 150, places=2)

    def test_fats_percentage(self):
        """Тест конвертации процентов жиров в граммы"""
        # 25% от 2000 ккал = 500 ккал / 9 ккал/г = 55.56г
        target = DietTarget(
            calories=2000,
            fats=80,
            fats_pct=25
        )
        resolved = target.resolve_macros()
        
        self.assertAlmostEqual(resolved.fats, 55.56, places=2)

    def test_carbs_percentage(self):
        """Тест конвертации процентов углеводов в граммы"""
        # 50% от 2000 ккал = 1000 ккал / 4 ккал/г = 250г
        target = DietTarget(
            calories=2000,
            carbs=250,
            carbs_pct=50
        )
        resolved = target.resolve_macros()
        
        self.assertAlmostEqual(resolved.carbs, 250, places=2)

    def test_all_percentages(self):
        """Тест конвертации всех процентов одновременно"""
        target = DietTarget(
            calories=2000,
            proteins=100,
            fats=80,
            carbs=250,
            proteins_pct=30,  # 150г
            fats_pct=25,      # 55.56г
            carbs_pct=45      # 225г
        )
        resolved = target.resolve_macros()
        
        self.assertAlmostEqual(resolved.proteins, 150, places=2)
        self.assertAlmostEqual(resolved.fats, 55.56, places=2)
        self.assertAlmostEqual(resolved.carbs, 225, places=2)

    def test_percentage_zero_calories(self):
        """Тест с нулевой калорийностью"""
        target = DietTarget(
            calories=0,
            proteins_pct=30
        )
        resolved = target.resolve_macros()
        
        self.assertEqual(resolved.proteins, 0)

    def test_percentage_negative_values(self):
        """Тест с отрицательными процентами (должны игнорироваться)"""
        target = DietTarget(
            calories=2000,
            proteins=100,
            proteins_pct=-10
        )
        resolved = target.resolve_macros()
        
        # Отрицательный процент должен быть проигнорирован
        self.assertEqual(resolved.proteins, 100)

    def test_to_dict_preserves_values(self):
        """to_dict должен возвращать пересчитанные значения"""
        target = DietTarget(
            calories=2000,
            proteins=100,
            proteins_pct=30
        )
        resolved = target.resolve_macros()
        d = resolved.to_dict()
        
        self.assertAlmostEqual(d['proteins'], 150, places=2)


if __name__ == '__main__':
    unittest.main()
