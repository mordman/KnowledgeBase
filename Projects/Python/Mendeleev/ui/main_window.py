"""Главное окно приложения."""

import tkinter as tk
from tkinter import ttk
from utils.helpers import load_json_file, get_font_tuple
from ui.element_card import ElementCard

ELEMENTS_FILE = "data/elements.json"
MOLECULES_FILE = "data/molecules.json"

class MainWindow:
    """Главное окно таблицы Менделеева."""
    
    def __init__(self, root, settings):
        self.root = root
        self.settings = settings
        self.colors = settings.get('colors', {})
        self.fonts = settings.get('fonts', {})
        
        self.cell_width = settings.get('cell_width', 65)
        self.cell_height = settings.get('cell_height', 75)
        self.padding = 4
        
        self._setup_window()
        self._create_widgets()
        self._load_elements()
        self._draw_table()
    
    def _setup_window(self):
        """Настраивает окно."""
        w = self.settings.get('window_width', 1200)
        h = self.settings.get('window_height', 850)
        self.root.geometry(f"{w}x{h}")
        self.root.title("Интерактивная Таблица Менделеева")
        self.root.configure(bg=self.colors.get("window_background", "#F0F0F0"))
    
    def _create_widgets(self):
        """Создаёт виджеты."""
        # Верхняя панель
        top = tk.Frame(self.root, bg=self.colors.get("header_background", "#333333"), height=60)
        top.pack(fill="x", side="top")
        
        btn_frame = tk.Frame(top, bg=top.cget("bg"))
        btn_frame.pack(pady=10, padx=10)
        
        btn_font = get_font_tuple(self.fonts.get('button_text'))
        buttons = [
            ("🧪 Молекулы", self._open_molecules, "#4ECDC4"),
            ("📋 Легенда", self._open_legend, "#FF9F1C"),
            ("⚙️ Настройки", self._open_settings, "#9D8DF1")
        ]
        
        for text, cmd, bg in buttons:
            tk.Button(
                btn_frame,
                text=text,
                command=cmd,
                font=btn_font,
                bg=bg,
                fg=self.colors.get("button_foreground", "#FFFFFF"),
                relief="flat",
                padx=15,
                pady=5
            ).pack(side="left", padx=5)
        
        # Canvas
        self.canvas = tk.Canvas(
            self.root,
            bg=self.colors.get("canvas_background", "#F0F0F0"),
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        
        # === ИСПРАВЛЕНИЕ: Прокрутка ===
        # Вертикальная прокрутка
        self.scrollbar_y = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollbar_y.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)
        
        # Горизонтальная прокрутка
        self.scrollbar_x = tk.Scrollbar(self.root, orient="horizontal", command=self.canvas.xview)
        self.scrollbar_x.pack(side="bottom", fill="x")
        self.canvas.configure(xscrollcommand=self.scrollbar_x.set)
        
        # Привязка изменения размера
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
    
    def _load_elements(self):
        """Загружает элементы."""
        self.elements = load_json_file(ELEMENTS_FILE, [])
    
    def _draw_table(self):
        """Отрисовывает таблицу."""
        max_row = max_col = 0
        
        for el in self.elements:
            row = el.get('row', 1)
            col = el.get('col', 1)
            
            x = (col - 1) * (self.cell_width + self.padding) + self.padding + 20
            y = (row - 1) * (self.cell_height + self.padding) + self.padding + 20
            
            ElementCard(self.canvas, el, x, y, self.cell_width, self.cell_height, self.settings)
            
            max_row = max(max_row, row)
            max_col = max(max_col, col)
        
        self.canvas.configure(
            scrollregion=(
                0, 0,
                max_col * (self.cell_width + self.padding) + 40,
                max_row * (self.cell_height + self.padding) + 40
            )
        )
    
    def _open_molecules(self):
        """Открывает окно молекул."""
        from ui.molecule_window import MoleculeWindow
        molecules = load_json_file(MOLECULES_FILE, [])
        MoleculeWindow(self.root, molecules, self.settings)
    
    def _open_legend(self):
        """Открывает легенду."""
        from ui.legend_window import LegendWindow
        LegendWindow(self.root, self.settings.get('category_colors', {}), self.settings)
    
    def _open_settings(self):
        """Открывает настройки."""
        from ui.settings_window import SettingsWindow
        SettingsWindow(self.root, self.settings, self._on_settings_saved)
    
    def _on_settings_saved(self):
        """Обработчик сохранения настроек."""
        from config.settings_manager import load_settings
        self.settings = load_settings()
        self.colors = self.settings.get('colors', {})
        self.fonts = self.settings.get('fonts', {})
        self.cell_width = self.settings.get('cell_width', 65)
        self.cell_height = self.settings.get('cell_height', 75)
        
        self.canvas.delete("all")
        self._draw_table()