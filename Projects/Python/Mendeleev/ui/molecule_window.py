"""Окно списка молекул."""

import tkinter as tk
from tkinter import ttk
from utils.helpers import get_font_tuple
from utils.formula_renderer import FormulaRenderer

class MoleculeWindow(tk.Toplevel):
    """Окно со списком молекул."""
    
    def __init__(self, parent, molecules, settings):
        super().__init__(parent)
        self.title("Примеры молекул")
        self.geometry("700x500")
        self.resizable(True, True)
        
        self.settings = settings
        self.colors = settings.get('colors', {})
        self.fonts = settings.get('fonts', {})
        
        self.configure(bg=self.colors.get("window_background", "#F0F0F0"))
        self._create_widgets(molecules)
    
    def _create_widgets(self, molecules):
        """Создаёт виджеты окна."""
        # Заголовок
        title_font = get_font_tuple(self.fonts.get('molecule_title'))
        tk.Label(
            self,
            text="Химические формулы",
            font=title_font,
            bg=self.colors.get("window_background", "#F0F0F0"),
            fg=self.colors.get("text_foreground", "#000000")
        ).pack(pady=10)
        
        # Canvas с прокруткой
        canvas = tk.Canvas(self, bg=self.colors.get("canvas_background", "#F0F0F0"))
        canvas.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        molecules_frame = tk.Frame(canvas, bg=self.colors.get("canvas_background", "#F0F0F0"))
        canvas_window = canvas.create_window((0, 0), window=molecules_frame, anchor="nw")
        
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        molecules_frame.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", on_canvas_configure)
        
        # Заголовки
        self._create_header(molecules_frame)
        
        # Список молекул
        self._create_molecule_list(molecules_frame, molecules)
        
        # Кнопка закрытия
        btn_font = get_font_tuple(self.fonts.get('button_text'))
        tk.Button(
            self,
            text="Закрыть",
            command=self.destroy,
            font=btn_font,
            bg=self.colors.get("button_background", "#4ECDC4"),
            fg=self.colors.get("button_foreground", "#FFFFFF")
        ).pack(pady=10)
    
    def _create_header(self, parent):
        """Создаёт заголовки таблицы."""
        header_frame = tk.Frame(parent, bg=self.colors.get("header_background", "#333333"))
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        header_font = get_font_tuple(self.fonts.get('button_text'))
        headers = ["Название", "Формула", "Описание"]
        widths = [20, 20, 30]
        
        for text, width in zip(headers, widths):
            tk.Label(
                header_frame,
                text=text,
                font=header_font,
                fg=self.colors.get("header_foreground", "#FFFFFF"),
                bg=self.colors.get("header_background", "#333333"),
                width=width,
                anchor="w"
            ).pack(side="left", padx=5, pady=5)
    
    def _create_molecule_list(self, parent, molecules):
        """Создаёт список молекул."""
        color_even = self.colors.get("row_even", "#FFFFFF")
        color_odd = self.colors.get("row_odd", "#E8F4F8")
        
        name_font = get_font_tuple(self.fonts.get('molecule_name'))
        formula_font = get_font_tuple(self.fonts.get('molecule_formula'))
        desc_font = get_font_tuple(self.fonts.get('molecule_description'))
        
        for i, mol in enumerate(molecules):
            bg_color = color_even if i % 2 == 0 else color_odd
            
            row_frame = tk.Frame(
                parent,
                bg=bg_color,
                highlightthickness=1,
                highlightbackground=self.colors.get("border_color", "#DDDDDD")
            )
            row_frame.pack(fill="x", padx=10, pady=1)
            
            # Название
            tk.Label(
                row_frame,
                text=mol.get("name", ""),
                font=name_font,
                bg=bg_color,
                fg=self.colors.get("text_foreground", "#000000"),
                width=20,
                anchor="w",
                padx=5
            ).pack(side="left", padx=5, pady=5)
            
            # Формула
            formula_frame = tk.Frame(row_frame, bg=bg_color, width=200, height=30)
            formula_frame.pack(side="left", padx=5, pady=5)
            formula_frame.pack_propagate(False)
            
            formula_text = tk.Text(
                formula_frame,
                font=formula_font,
                bg=bg_color,
                fg=self.colors.get("text_foreground", "#000000"),
                wrap="word",
                padx=5,
                pady=5,
                height=1,
                relief="flat",
                borderwidth=0,
                highlightthickness=0
            )
            formula_text.pack(fill="both", expand=True)
            
            renderer = FormulaRenderer(formula_text, self.settings)
            renderer.render(mol.get("formula", ""), format_type="markdown")
            formula_text.config(state="disabled")
            
            # Описание
            tk.Label(
                row_frame,
                text=mol.get("description", ""),
                font=desc_font,
                bg=bg_color,
                fg=self.colors.get("text_foreground", "#000000"),
                width=30,
                anchor="w",
                padx=5,
                wraplength=250
            ).pack(side="left", padx=5, pady=5)