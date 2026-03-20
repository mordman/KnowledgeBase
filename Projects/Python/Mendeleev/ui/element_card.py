"""Карточка химического элемента."""

import tkinter as tk
from utils.helpers import create_rounded_rectangle, get_font_tuple

class ElementCard:
    """Интерактивная карточка элемента."""
    
    def __init__(self, canvas, element_data, x, y, width, height, settings):
        self.canvas = canvas
        self.data = element_data
        self.base_x = x
        self.base_y = y
        self.width = width
        self.height = height
        self.settings = settings
        self.colors = settings.get('colors', {})
        self.fonts = settings.get('fonts', {})
        
        self.color = settings.get('category_colors', {}).get(
            element_data.get('category', ''), 
            "#FFFFFF"
        )
        self.is_hovered = False
        self.original_ids = []
        
        self._draw()
        self._bind_events()
    
    def _draw(self):
        """Отрисовка элемента."""
        radius = 10
        
        self.rect_id = create_rounded_rectangle(
            self.canvas, self.base_x, self.base_y,
            self.base_x + self.width, self.base_y + self.height,
            radius,
            fill=self.color,
            outline=self.colors.get("element_border", "#333333"),
            width=3
        )
        self.original_ids.append(self.rect_id)
        
        center_x = self.base_x + self.width / 2
        center_y = self.base_y + self.height / 2
        
        # Символ
        symbol_font = get_font_tuple(self.fonts.get('element_symbol'))
        self.text_symbol = self.canvas.create_text(
            center_x, center_y,
            text=self.data.get('symbol', '?'),
            font=symbol_font,
            fill=self.colors.get("text_foreground", "#000000")
        )
        self.original_ids.append(self.text_symbol)
        
        # Номер
        number_font = get_font_tuple(self.fonts.get('element_number'))
        self.text_number = self.canvas.create_text(
            self.base_x + 5, self.base_y + 5,
            text=str(self.data.get('number', '')),
            font=number_font,
            anchor="nw",
            fill=self.colors.get("text_foreground", "#000000")
        )
        self.original_ids.append(self.text_number)
        
        # Масса
        mass_font = get_font_tuple(self.fonts.get('element_mass'))
        self.text_mass = self.canvas.create_text(
            self.base_x + 5, self.base_y + self.height - 5,
            text=str(self.data.get('mass', '')),
            font=mass_font,
            anchor="sw",
            fill=self.colors.get("text_foreground", "#000000")
        )
        self.original_ids.append(self.text_mass)
    
    def _bind_events(self):
        """Привязка событий."""
        for item_id in self.original_ids:
            self.canvas.tag_bind(item_id, "<Enter>", self._on_enter)
            self.canvas.tag_bind(item_id, "<Leave>", self._on_leave)
            self.canvas.tag_bind(item_id, "<Button-1>", self._on_click)
    
    def _on_enter(self, event):
        """Наведение мыши."""
        if self.is_hovered:
            return
        self.is_hovered = True
        scale_factor = 1.15
        center_x = self.base_x + self.width / 2
        center_y = self.base_y + self.height / 2
        
        for item_id in self.original_ids:
            self.canvas.scale(item_id, center_x, center_y, scale_factor, scale_factor)
            self.canvas.tag_raise(item_id)
    
    def _on_leave(self, event):
        """Уход мыши."""
        if not self.is_hovered:
            return
        self.is_hovered = False
        scale_factor = 1 / 1.15
        center_x = self.base_x + self.width / 2
        center_y = self.base_y + self.height / 2
        
        for item_id in self.original_ids:
            self.canvas.scale(item_id, center_x, center_y, scale_factor, scale_factor)
    
    def _on_click(self, event):
        """Клик по элементу."""
        from ui.detail_window import ElementDetailWindow
        ElementDetailWindow(self.canvas.master, self.data, self.settings)