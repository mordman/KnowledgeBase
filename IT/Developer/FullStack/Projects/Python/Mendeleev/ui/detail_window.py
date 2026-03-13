"""Окно деталей элемента."""

import tkinter as tk
from utils.helpers import get_font_tuple
from utils.formula_renderer import FormulaRenderer

class ElementDetailWindow(tk.Toplevel):
    """Окно с подробной информацией об элементе."""
    
    def __init__(self, parent, element_data, settings):
        super().__init__(parent)
        self.title(f"{element_data['symbol']} - {element_data['name']}")
        self.geometry("550x450")
        self.resizable(True, True)
        
        self.settings = settings
        self.colors = settings.get('colors', {})
        self.fonts = settings.get('fonts', {})
        
        color = settings.get('category_colors', {}).get(
            element_data.get('category', ''),
            self.colors.get("window_background", "#FFFFFF")
        )
        self.configure(bg=color)
        
        self._create_widgets(element_data, color)
    
    def _create_widgets(self, element_data, color):
        """Создаёт виджеты окна."""
        # Заголовок
        title_font = get_font_tuple(self.fonts.get('detail_title'))
        tk.Label(
            self,
            text=f"{element_data['name']} ({element_data['symbol']})",
            font=title_font,
            bg=color,
            fg=self.colors.get("text_foreground", "#000000"),
            wraplength=500
        ).pack(pady=15, padx=10)
        
        has_html = 'html' in element_data and element_data['html']
        has_md = 'markdown' in element_data and element_data['markdown']
        
        if has_html or has_md:
            self._render_content(element_data, color, has_md)
        else:
            self._render_full_info(element_data, color)
        
        # Кнопка закрытия
        btn_font = get_font_tuple(self.fonts.get('button_text'))
        tk.Button(
            self,
            text="Закрыть",
            command=self.destroy,
            font=btn_font,
            bg=self.colors.get("button_background", "#333333"),
            fg=self.colors.get("button_foreground", "#FFFFFF"),
            padx=20,
            pady=5
        ).pack(pady=15)
    
    def _render_content(self, element_data, color, use_md):
        """Рендерит HTML/Markdown контент."""
        desc_font = self.fonts.get('detail_description', {"family": "Arial", "size": 11})
        text_desc = tk.Text(
            self,
            font=(desc_font["family"], desc_font["size"]),
            bg=self.colors.get("row_even", "#FFFFFF"),
            fg=self.colors.get("text_foreground", "#000000"),
            wrap="word",
            padx=10,
            pady=10,
            height=15,
            relief="flat",
            borderwidth=0
        )
        text_desc.pack(fill="both", expand=True, padx=20, pady=10)
        
        renderer = FormulaRenderer(text_desc, self.settings)
        content = element_data['markdown'] if use_md else element_data['html']
        renderer.render(content, format_type="markdown" if use_md else "html")
        text_desc.config(state="disabled")
    
    def _render_full_info(self, element_data, color):
        """Рендерит полную информацию."""
        info_font = get_font_tuple(self.fonts.get('detail_info'))
        
        # Основная информация
        info_text = (
            f"Атомный номер: {element_data.get('number', 'N/A')}\n"
            f"Атомная масса: {element_data.get('mass', 'N/A')}\n"
            f"Категория: {element_data.get('category', 'N/A')}\n"
            f"Период: {element_data.get('period', 'N/A')}\n"
            f"Группа: {element_data.get('group', 'N/A')}"
        )
        
        tk.Label(
            self,
            text=info_text,
            font=info_font,
            bg=color,
            fg=self.colors.get("text_foreground", "#000000"),
            justify="left",
            anchor="w"
        ).pack(fill="x", padx=20, pady=5)
        
        # Описание
        desc_font = self.fonts.get('detail_description', {"family": "Arial", "size": 11})
        text_desc = tk.Text(
            self,
            font=(desc_font["family"], desc_font["size"]),
            bg=self.colors.get("row_even", "#FFFFFF"),
            fg=self.colors.get("text_foreground", "#000000"),
            wrap="word",
            padx=10,
            pady=10,
            height=10,
            relief="flat",
            borderwidth=0
        )
        text_desc.pack(fill="both", expand=True, padx=20, pady=10)
        
        renderer = FormulaRenderer(text_desc, self.settings)
        description = element_data.get('description', 'Нет описания')
        renderer.render(description, format_type="markdown")
        text_desc.config(state="disabled")