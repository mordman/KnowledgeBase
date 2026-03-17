"""Вспомогательные функции."""

def get_font_tuple(font_dict):
    """Преобразует словарь шрифта в кортеж для tkinter."""
    if not font_dict:
        return ("Arial", 11, "")
    
    weight = font_dict.get("weight", "normal")
    return (
        font_dict.get("family", "Arial"),
        font_dict.get("size", 11),
        "bold" if weight == "bold" else ""
    )

def load_json_file(filename, default_data=None):
    """Загружает данные из JSON файла."""
    import os, json
    
    if default_data is None:
        default_data = {}
    
    if not os.path.exists(filename):
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(default_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка создания файла {filename}: {e}")
        return default_data
    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка чтения {filename}: {e}")
        return default_data

def save_json_file(filename, data):
    """Сохраняет данные в JSON файл."""
    import json
    
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Ошибка сохранения {filename}: {e}")
        return False

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius, **kwargs):
    """Рисует прямоугольник со скругленными углами."""
    points = [
        x1 + radius, y1, x2 - radius, y1, x2, y1, x2, y1 + radius,
        x2, y2 - radius, x2, y2, x2 - radius, y2, x1 + radius, y2,
        x1, y2, x1, y2 - radius, x1, y1 + radius, x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)