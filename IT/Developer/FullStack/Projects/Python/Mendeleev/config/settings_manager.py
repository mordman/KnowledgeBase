"""Менеджер настроек приложения."""

import json
import os
import copy
from config.templates import TEMPLATES, SYSTEM_TEMPLATES

SETTINGS_FILE = "settings.json"

def get_default_settings():
    """Возвращает настройки по умолчанию."""
    return {
        "cell_width": 65,
        "cell_height": 75,
        "window_width": 1200,
        "window_height": 850,
        "category_colors": {
            "Щелочные металлы": "#FF6B6B",
            "Щелочноземельные металлы": "#FFE66D",
            "Переходные металлы": "#4ECDC4",
            "Постпереходные металлы": "#C7F464",
            "Полуметаллы": "#A8D8EA",
            "Неметаллы": "#F7FFF7",
            "Галогены": "#FF9F1C",
            "Благородные газы": "#D4A5A5",
            "Лантаноиды": "#9D8DF1",
            "Актиноиды": "#C77DFF",
            "Неизвестные свойства": "#808080"
        },
        "fonts": {
            "element_symbol": {"family": "Arial", "size": 16, "weight": "bold"},
            "element_number": {"family": "Arial", "size": 9, "weight": "normal"},
            "element_mass": {"family": "Arial", "size": 8, "weight": "normal"},
            "detail_title": {"family": "Arial", "size": 20, "weight": "bold"},
            "detail_info": {"family": "Arial", "size": 11, "weight": "normal"},
            "detail_description": {"family": "Arial", "size": 11, "weight": "normal"},
            "molecule_title": {"family": "Arial", "size": 16, "weight": "bold"},
            "molecule_name": {"family": "Arial", "size": 11, "weight": "normal"},
            "molecule_formula": {"family": "Arial", "size": 11, "weight": "normal"},
            "molecule_description": {"family": "Arial", "size": 10, "weight": "normal"},
            "legend_title": {"family": "Arial", "size": 16, "weight": "bold"},
            "legend_category": {"family": "Arial", "size": 10, "weight": "normal"},
            "button_text": {"family": "Arial", "size": 11, "weight": "bold"},
            "settings_label": {"family": "Arial", "size": 11, "weight": "normal"}
        },
        "colors": {
            "window_background": "#F0F0F0",
            "canvas_background": "#F0F0F0",
            "header_background": "#333333",
            "header_foreground": "#FFFFFF",
            "text_foreground": "#000000",
            "button_background": "#4ECDC4",
            "button_foreground": "#FFFFFF",
            "row_even": "#FFFFFF",
            "row_odd": "#E8F4F8",
            "border_color": "#DDDDDD",
            "element_border": "#333333"
        },
        "templates": copy.deepcopy(TEMPLATES),
        "current_template": "standard"
    }

def load_settings():
    """Загружает настройки из файла."""
    default = get_default_settings()
    
    if not os.path.exists(SETTINGS_FILE):
        save_settings(default)
        return default
    
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            settings = json.load(f)
        
        # Merge с дефолтными настройками
        for key in default:
            if key not in settings:
                settings[key] = default[key]
            elif isinstance(default[key], dict):
                for subkey in default[key]:
                    if subkey not in settings[key]:
                        settings[key][subkey] = default[key][subkey]
        
        # Добавляем системные шаблоны если отсутствуют
        if 'templates' not in settings:
            settings['templates'] = copy.deepcopy(TEMPLATES)
        else:
            for tpl_key, tpl_data in TEMPLATES.items():
                if tpl_key not in settings['templates']:
                    settings['templates'][tpl_key] = copy.deepcopy(tpl_data)
        
        return settings
    except Exception as e:
        print(f"Ошибка загрузки настроек: {e}")
        return default

def save_settings(settings):
    """Сохраняет настройки в файл."""
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Ошибка сохранения настроек: {e}")
        return False

def apply_template(settings, template_key):
    """Применяет шаблон к настройкам."""
    templates = settings.get('templates', {})
    if template_key not in templates:
        return False
    
    template = templates[template_key]
    
    # Применяем шрифты
    if 'fonts' in template and 'fonts' in settings:
        for font_name, font_data in template['fonts'].items():
            if font_name in settings['fonts']:
                settings['fonts'][font_name] = copy.deepcopy(font_data)
    
    # Применяем цвета
    if 'colors' in template and 'colors' in settings:
        for color_name, color_value in template['colors'].items():
            if color_name in settings['colors']:
                settings['colors'][color_name] = color_value
    
    # Применяем цвета категорий
    if 'category_colors' in template and 'category_colors' in settings:
        for cat_name, color_value in template['category_colors'].items():
            if cat_name in settings['category_colors']:
                settings['category_colors'][cat_name] = color_value
    
    # Применяем размеры
    if 'cell_width' in template:
        settings['cell_width'] = template['cell_width']
    if 'cell_height' in template:
        settings['cell_height'] = template['cell_height']
    
    settings['current_template'] = template_key
    return True

def is_system_template(template_key):
    """Проверяет является ли шаблон системным."""
    return template_key in SYSTEM_TEMPLATES

def delete_template(settings, template_key):
    """Удаляет пользовательский шаблон."""
    if is_system_template(template_key):
        return False
    
    if template_key in settings.get('templates', {}):
        del settings['templates'][template_key]
        return True
    return False

def save_custom_template(settings, key, name, description):
    """Сохраняет текущие настройки как новый шаблон."""
    if 'templates' not in settings:
        settings['templates'] = {}
    
    settings['templates'][key] = {
        "name": name,
        "description": description,
        "fonts": copy.deepcopy(settings.get('fonts', {})),
        "colors": copy.deepcopy(settings.get('colors', {})),
        "category_colors": copy.deepcopy(settings.get('category_colors', {})),
        "cell_width": settings.get('cell_width', 65),
        "cell_height": settings.get('cell_height', 75)
    }
    return True