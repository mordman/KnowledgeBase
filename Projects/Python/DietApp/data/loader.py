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
            },
            {
                "name": "Миндаль",
                "calories": 579,
                "proteins": 21,
                "fats": 50,
                "carbs": 22,
                "price": 150,
                "weight": 100,
                "recipe": "Готовый продукт. Можно употреблять в сыром виде или слегка обжарить."
            },
            {
                "name": "Банан",
                "calories": 96,
                "proteins": 1.5,
                "fats": 0.5,
                "carbs": 21,
                "price": 20,
                "weight": 120,
                "recipe": "Очистить от кожуры. Употреблять свежим."
            },
            {
                "name": "Говядина тушеная",
                "calories": 180,
                "proteins": 26,
                "fats": 8,
                "carbs": 0,
                "price": 250,
                "weight": 150,
                "recipe": "1. Нарезать говядину кубиками.\n2. Обжарить до корочки.\n3. Добавить воду, накрыть крышкой.\n4. Тушить на медленном огне 1.5-2 часа."
            },
            {
                "name": "Салат Цезарь",
                "calories": 150,
                "proteins": 14,
                "fats": 8,
                "carbs": 6,
                "price": 180,
                "weight": 200,
                "recipe": "1. Нарезать салат романо.\n2. Добавить куриное филе гриль.\n3. Полить соусом Цезарь.\n4. Посыпать пармезаном и сухариками."
            },
            {
                "name": "Кефир 2.5%",
                "calories": 53,
                "proteins": 2.8,
                "fats": 2.5,
                "carbs": 4,
                "price": 40,
                "weight": 250,
                "recipe": "Готовый продукт. Подавать охлажденным."
            },
            {
                "name": "Индейка запеченная",
                "calories": 135,
                "proteins": 28,
                "fats": 2,
                "carbs": 0,
                "price": 200,
                "weight": 150,
                "recipe": "1. Замариновать филе в специях.\n2. Разогреть духовку до 180°C.\n3. Запекать 35-40 минут.\n4. Дать отдохнуть 5 минут."
            },
            {
                "name": "Картофель отварной",
                "calories": 82,
                "proteins": 2,
                "fats": 0.4,
                "carbs": 17,
                "price": 15,
                "weight": 200,
                "recipe": "1. Очистить картофель.\n2. Положить в кипящую подсоленную воду.\n3. Варить 20-25 минут до готовности.\n4. Слить воду, добавить масло."
            },
            {
                "name": "Авокадо",
                "calories": 160,
                "proteins": 2,
                "fats": 15,
                "carbs": 9,
                "price": 120,
                "weight": 150,
                "recipe": "1. Разрезать пополам, удалить косточку.\n2. Вынуть мякоть ложкой.\n3. Нарезать или размять в пюре.\n4. Посолить, полить лимонным соком."
            },
            {
                "name": "Паста с томатным соусом",
                "calories": 180,
                "proteins": 6,
                "fats": 3,
                "carbs": 35,
                "price": 70,
                "weight": 250,
                "recipe": "1. Отварить пасту аль денте.\n2. Приготовить соус из томатов с чесноком.\n3. Смешать пасту с соусом.\n4. Посыпать базиликом."
            },
            {
                "name": "Тунец консервированный",
                "calories": 116,
                "proteins": 26,
                "fats": 1,
                "carbs": 0,
                "price": 90,
                "weight": 130,
                "recipe": "Готовый продукт. Слить жидкость, использовать для салатов или бутербродов."
            },
            {
                "name": "Мед",
                "calories": 304,
                "proteins": 0.3,
                "fats": 0,
                "carbs": 82,
                "price": 50,
                "weight": 30,
                "recipe": "Использовать как натуральный подсластитель. 1 ст. ложка = 30г."
            },
            {
                "name": "Шпинат свежий",
                "calories": 23,
                "proteins": 2.9,
                "fats": 0.4,
                "carbs": 3.6,
                "price": 60,
                "weight": 100,
                "recipe": "Промыть листья. Использовать в салатах или как гарнир."
            },
            {
                "name": "Сыр твердый (Гауда)",
                "calories": 350,
                "proteins": 25,
                "fats": 27,
                "carbs": 2,
                "price": 80,
                "weight": 50,
                "recipe": "Нарезать ломтиками. Подавать с хлебом или использовать в бутербродах."
            },
            {
                "name": "Перловка отварная",
                "calories": 120,
                "proteins": 3.5,
                "fats": 0.7,
                "carbs": 25,
                "price": 20,
                "weight": 200,
                "recipe": "1. Замочить перловку на 2 часа.\n2. Промыть и залить свежей водой.\n3. Варить 40-50 минут.\n4. Добавить масло по вкусу."
            },
            {
                "name": "Апельсин",
                "calories": 47,
                "proteins": 0.9,
                "fats": 0.1,
                "carbs": 12,
                "price": 30,
                "weight": 200,
                "recipe": "Очистить от кожуры. Употреблять свежим."
            },
            {
                "name": "Хлеб цельнозерновой",
                "calories": 250,
                "proteins": 13,
                "fats": 3.5,
                "carbs": 41,
                "price": 15,
                "weight": 50,
                "recipe": "Готовый продукт. Нарезать ломтиками."
            },
            {
                "name": "Йогурт натуральный 3.2%",
                "calories": 66,
                "proteins": 5,
                "fats": 3.2,
                "carbs": 3.5,
                "price": 50,
                "weight": 200,
                "recipe": "Готовый продукт. Можно добавить фрукты, ягоды или мед."
            }
        ]
        return json.dumps(sample_data, ensure_ascii=False, indent=4)