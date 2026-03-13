"""Окно легенды категорий."""

import tkinter as tk
from tkinter import ttk
from utils.helpers import get_font_tuple

class LegendWindow(tk.Toplevel):
    """Окно с легендой цветов категорий."""
    
    def __init__(self, parent, category_colors, settings):
        super().__init__(parent)
        self.title("Легенда категорий")
        self.geometry("400x500")
        self.resizable(True, True)
        
        self.settings = settings
        self.colors = settings.get('colors', {})
        self.fonts = settings.get('fonts', {})
        
        self.configure(bg=self.colors.get("window_background", "#F0F0F0"))
        self._create_widgets(category_colors)
    
    def _create_widgets(self, category_colors):
        """Создаёт виджеты окна."""
        title_font = get_font_tuple(self.fonts.get('legend_title'))
        tk.Label(
            self,
            text="Категории элементов",
            font=title_font,
            bg=self.colors.get("window_background", "#F0F0F0"),
            fg=self.colors.get("text_foreground", "#000000")
        ).pack(pady=10)
        
        # Canvas с прокруткой
        canvas = tk.Canvas(self, bg=self.colors.get("canvas_background", "#F0F0F0"))
        canvas.pack(fill="both", expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        legend_frame = tk.Frame(canvas, bg=self.colors.get("canvas_background", "#F0F0F0"))
        canvas_window = canvas.create_window((0, 0), window=legend_frame, anchor="nw")
        
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        legend_frame.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", on_canvas_configure)
        
        # Отрисовка легенды
        category_font = get_font_tuple(self.fonts.get('legend_category'))
        y_offset = 10
        box_height = 30
        
        for category, color in category_colors.items():
            canvas.create_rectangle(
                10, y_offset, 10 + box_height, y_offset + box_height,
                fill=color,
                outline=self.colors.get("element_border", "#333333"),
                width=2
            )
            canvas.create_text(
                10 + box_height + 10, y_offset + box_height // 2,
                text=category,
                font=category_font,
                anchor="w",
                fill=self.colors.get("text_foreground", "#000000")
            )
            y_offset += box_height + 5
        
        canvas.configure(scrollregion=(0, 0, 250, y_offset + 10))