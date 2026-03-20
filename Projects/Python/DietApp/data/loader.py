import json
from typing import List, Tuple, Optional
from models.dish import Dish


class DataLoader:
    """Класс для загрузки и валидации данных"""

    @staticmethod
    def load_dishes_from_json(json_str: str) -> Tuple[Optional[List[Dish]], Optional[str]]:
        """
        Загружает список блюд из JSON строки.
        
        Returns:
            Tuple[List[Dish], None] при успехе
            Tuple[None, str] при ошибке (сообщение об ошибке)
        """
        try:
            data = json.loads(json_str)
            
            if not isinstance(data, list):
                return None, "JSON должен содержать список блюд"
            
            dishes = []
            for i, item in enumerate(data):
                if not isinstance(item, dict):
                    return None, f"Элемент {i} не является объектом"
                
                # Проверка обязательных полей
                required_fields = ['name', 'calories']
                for field in required_fields:
                    if field not in item:
                        return None, f"В элементе {i} отсутствует поле '{field}'"
                
                try:
                    dish = Dish.from_dict(item)
                    dishes.append(dish)
                except (ValueError, TypeError) as e:
                    return None, f"Ошибка в элементе {i}: {str(e)}"
            
            if not dishes:
                return None, "Список блюд пуст"
            
            return dishes, None
            
        except json.JSONDecodeError as e:
            return None, f"Ошибка парсинга JSON: {str(e)}"
        except Exception as e:
            return None, f"Неизвестная ошибка: {str(e)}"

    @staticmethod
    def get_sample_json() -> str:
        """Возвращает пример JSON для заполнения"""
        sample_data = [
            {
                "name": "Овсянка на воде",
                "calories": 350,
                "proteins": 12,
                "fats": 6,
                "carbs": 60,
                "price": 50,
                "weight": 250,
                "recipe": "1. Залить овсяные хлопья водой в пропорции 1:2.\n2. Довести до кипения.\n3. Варить на медленном огне 10-15 минут, помешивая.\n4. Добавить соль по вкусу."
            },
            {
                "name": "Яйцо вареное",
                "calories": 155,
                "proteins": 13,
                "fats": 11,
                "carbs": 1,
                "price": 20,
                "weight": 60,
                "recipe": "1. Положить яйца в холодную воду.\n2. Довести до кипения.\n3. Варить 8-10 минут для вкрутую.\n4. Охладить в холодной воде."
            },
            {
                "name": "Куриная грудка гриль",
                "calories": 165,
                "proteins": 31,
                "fats": 3.6,
                "carbs": 0,
                "price": 150,
                "weight": 150,
                "recipe": "1. Замариновать грудку в специях на 30 мин.\n2. Разогреть гриль или сковороду.\n3. Жарить по 6-7 минут с каждой стороны.\n4. Дать отдохнуть 5 минут перед нарезкой."
            },
            {
                "name": "Рис отварной",
                "calories": 130,
                "proteins": 2.7,
                "fats": 0.3,
                "carbs": 28,
                "price": 30,
                "weight": 200,
                "recipe": "1. Промыть рис до прозрачной воды.\n2. Залить водой в пропорции 1:2.\n3. Довести до кипения, убавить огонь.\n4. Варить под крышкой 15-20 минут."
            },
            {
                "name": "Брокколи на пару",
                "calories": 35,
                "proteins": 2.4,
                "fats": 0.4,
                "carbs": 7,
                "price": 40,
                "weight": 150,
                "recipe": "1. Разобрать брокколи на соцветия.\n2. Положить в пароварку.\n3. Готовить 5-7 минут до мягкости.\n4. Посолить по вкусу."
            },
            {
                "name": "Творог 5%",
                "calories": 120,
                "proteins": 17,
                "fats": 5,
                "carbs": 1.8,
                "price": 80,
                "weight": 180,
                "recipe": "Готовый продукт. Можно добавить мед, фрукты или зелень по вкусу."
            },
            {
                "name": "Яблоко свежее",
                "calories": 52,
                "proteins": 0.3,
                "fats": 0.2,
                "carbs": 14,
                "price": 25,
                "weight": 150,
                "recipe": "Вымыть, при желании очистить от кожуры. Употреблять свежим."
            },
            {
                "name": "Гречка отварная",
                "calories": 110,
                "proteins": 4,
                "fats": 1,
                "carbs": 20,
                "price": 35,
                "weight": 200,
                "recipe": "1. Перебрать и промыть гречку.\n2. Залить водой 1:2.\n3. Довести до кипения, варить 15-20 минут.\n4. Добавить масло по желанию."
            },
            {
                "name": "Лосось на пару",
                "calories": 208,
                "proteins": 20,
                "fats": 13,
                "carbs": 0,
                "price": 300,
                "weight": 150,
                "recipe": "1. Посолить и поперчить филе.\n2. Положить в пароварку кожей вниз.\n3. Готовить 12-15 минут.\n4. Подавать с лимоном."
            },
            {
                "name": "Оливковое масло",
                "calories": 884,
                "proteins": 0,
                "fats": 100,
                "carbs": 0,
                "price": 10,
                "weight": 10,
                "recipe": "Использовать как заправку для салатов или добавлять в готовые блюда. 1 ст. ложка = 10г."
            }
        ]
        return json.dumps(sample_data, ensure_ascii=False, indent=4)