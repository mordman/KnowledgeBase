# config.py

import json
import os
from settings import (
    CONFIG_FILE,
    DEFAULT_BOARD_SIZE, DEFAULT_CELL_SIZE,
    DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT, DEFAULT_PIECE_SCALE,
    DEFAULT_PIECE_ROWS,
    DEFAULT_COLOR_LIGHT, DEFAULT_COLOR_DARK,
    DEFAULT_COLOR_PIECE_1, DEFAULT_COLOR_PIECE_2,
    DEFAULT_COLOR_HIGHLIGHT, DEFAULT_COLOR_MULTI_JUMP,
    DEFAULT_COLOR_SELECTION, DEFAULT_BOARD_BORDER
)

class Config:
    """Управление конфигурацией игры"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.load()
    
    def load(self):
        """Загрузка настроек из файла"""
        self.board_size = DEFAULT_BOARD_SIZE
        self.cell_size = DEFAULT_CELL_SIZE
        self.window_width = DEFAULT_WINDOW_WIDTH
        self.window_height = DEFAULT_WINDOW_HEIGHT
        self.piece_scale = DEFAULT_PIECE_SCALE
        self.piece_rows = DEFAULT_PIECE_ROWS
        
        self.color_light = DEFAULT_COLOR_LIGHT
        self.color_dark = DEFAULT_COLOR_DARK
        self.color_piece_1 = DEFAULT_COLOR_PIECE_1
        self.color_piece_2 = DEFAULT_COLOR_PIECE_2
        self.color_highlight = DEFAULT_COLOR_HIGHLIGHT
        self.color_multi_jump = DEFAULT_COLOR_MULTI_JUMP
        self.color_selection = DEFAULT_COLOR_SELECTION
        self.color_board_border = DEFAULT_BOARD_BORDER
        
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._apply_dict(data)
            except Exception as e:
                print(f"Ошибка загрузки конфигурации: {e}")
    
    def _apply_dict(self, data):
        """Применение настроек из словаря"""
        if 'board_size' in data:
            self.board_size = int(data['board_size'])
        if 'cell_size' in data:
            self.cell_size = int(data['cell_size'])
        if 'window_width' in data:
            self.window_width = int(data['window_width'])
        if 'window_height' in data:
            self.window_height = int(data['window_height'])
        if 'piece_scale' in data:
            self.piece_scale = float(data['piece_scale'])
        if 'piece_rows' in data:
            self.piece_rows = int(data['piece_rows'])
        if 'color_light' in data:
            self.color_light = data['color_light']
        if 'color_dark' in data:
            self.color_dark = data['color_dark']
        if 'color_piece_1' in data:
            self.color_piece_1 = data['color_piece_1']
        if 'color_piece_2' in data:
            self.color_piece_2 = data['color_piece_2']
        if 'color_highlight' in data:
            self.color_highlight = data['color_highlight']
        if 'color_multi_jump' in data:
            self.color_multi_jump = data['color_multi_jump']
        if 'color_selection' in data:
            self.color_selection = data['color_selection']
        if 'color_board_border' in data:
            self.color_board_border = data['color_board_border']
    
    def save(self):
        """Сохранение настроек в файл"""
        data = {
            'board_size': self.board_size,
            'cell_size': self.cell_size,
            'window_width': self.window_width,
            'window_height': self.window_height,
            'piece_scale': self.piece_scale,
            'piece_rows': self.piece_rows,
            'color_light': self.color_light,
            'color_dark': self.color_dark,
            'color_piece_1': self.color_piece_1,
            'color_piece_2': self.color_piece_2,
            'color_highlight': self.color_highlight,
            'color_multi_jump': self.color_multi_jump,
            'color_selection': self.color_selection,
            'color_board_border': self.color_board_border
        }
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Ошибка сохранения конфигурации: {e}")
            return False
    
    def reset_to_defaults(self):
        """Сброс к настройкам по умолчанию"""
        self._initialized = False
        self.__init__()
        self.save()
    
    def get_board_pixels(self):
        """Размер доски в пикселях"""
        return self.board_size * self.cell_size
    
    def get_piece_radius(self):
        """Радиус шашки"""
        return int(self.cell_size * self.piece_scale / 2)
    
    def get_max_piece_rows(self):
        """Максимально возможное количество рядов для текущего размера доски"""
        return self.board_size // 2 - 1
    
    def get_min_window_size(self):
        """Минимальный размер окна с учётом скроллбаров и интерфейса"""
        return {
            'width': 700,
            'height': 600
        }
    
    def to_dict(self):
        """Возвращает настройки как словарь"""
        return {
            'board_size': self.board_size,
            'cell_size': self.cell_size,
            'window_width': self.window_width,
            'window_height': self.window_height,
            'piece_scale': self.piece_scale,
            'piece_rows': self.piece_rows,
            'color_light': self.color_light,
            'color_dark': self.color_dark,
            'color_piece_1': self.color_piece_1,
            'color_piece_2': self.color_piece_2,
            'color_highlight': self.color_highlight,
            'color_multi_jump': self.color_multi_jump,
            'color_selection': self.color_selection,
            'color_board_border': self.color_board_border
        }

# Глобальный экземпляр конфигурации
config = Config()