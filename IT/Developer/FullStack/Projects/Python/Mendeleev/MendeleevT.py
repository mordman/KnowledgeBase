import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import re
import html

# ==============================================================================
# КОНСТАНТЫ
# ==============================================================================

ELEMENTS_FILE = "elements.json"
MOLECULES_FILE = "molecules.json"
SETTINGS_FILE = "settings.json"

# ==============================================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ==============================================================================

def load_json_file(filename, default_data=None):
    """Загружает данные из JSON файла или создаёт файл с данными по умолчанию."""
    if not os.path.exists(filename):
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(default_data, f, ensure_ascii=False, indent=4)
            print(f"Файл {filename} создан с данными по умолчанию.")
        except Exception as e:
            print(f"Ошибка создания файла {filename}: {e}")
            return default_data if default_data else {}
    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except Exception as e:
        print(f"Ошибка чтения {filename}: {e}. Используются данные по умолчанию.")
        return default_data if default_data else {}

def save_json_file(filename, data):
    """Сохраняет данные в JSON файл."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Ошибка сохранения {filename}: {e}")
        return False

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius, **kwargs):
    """Рисует прямоугольник со скругленными углами на Canvas."""
    points = [
        x1 + radius, y1, x2 - radius, y1, x2, y1, x2, y1 + radius,
        x2, y2 - radius, x2, y2, x2 - radius, y2, x1 + radius, y2,
        x1, y2, x1, y2 - radius, x1, y1 + radius, x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

def wrap_text(text, max_width, font):
    """Переносит текст по строкам в зависимости от ширины."""
    import tkinter.font as tkfont
    f = tkfont.Font(font=font)
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + " " + word if current_line else word
        if f.measure(test_line) < max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    return "\n".join(lines)

# ==============================================================================
# HTML РЕНДЕРЕР
# ==============================================================================

class HTMLTextRenderer:
    """
    Простой рендерер базовых HTML-тегов для Tkinter Text виджета.
    Поддерживает: <b>, <strong>, <i>, <em>, <u>, <br>, <p>, списки (-, 1.)
    """
    def __init__(self, text_widget):
        self.text = text_widget
        self._setup_tags()

    def _setup_tags(self):
        """Настраивает теги форматирования."""
        self.text.tag_configure("bold", font=("Arial", 11, "bold"))
        self.text.tag_configure("italic", font=("Arial", 11, "italic"))
        self.text.tag_configure("underline", font=("Arial", 11, "underline"))
        self.text.tag_configure("bold_italic", font=("Arial", 11, "bold", "italic"))
        self.text.tag_configure("heading", font=("Arial", 13, "bold"), spacing1=10, spacing3=5)
        self.text.tag_configure("list_item", lmargin1=20, lmargin2=20)
        self.text.tag_configure("normal", font=("Arial", 11))

    def render(self, html_content):
        """Парсит HTML и вставляет форматированный текст."""
        self.text.delete("1.0", tk.END)
        
        # Разбиваем на строки для обработки
        lines = html_content.split('\n')
        
        current_tags = ["normal"]
        
        for line in lines:
            line = line.strip()
            if not line:
                self.text.insert(tk.END, "\n")
                continue
            
            # Обработка заголовков (простая эвристика: жирный текст в начале)
            if line.startswith('<b>') and line.endswith('</b>'):
                content = line[3:-4]
                self.text.insert(tk.END, content + "\n", "heading")
                continue

            # Обработка списков
            if line.startswith('- ') or line.startswith('• '):
                content = line[2:]
                self.text.insert(tk.END, "• " + self._parse_inline_tags(content) + "\n", "list_item")
                continue
            
            if re.match(r'^\d+\.\s', line):
                self.text.insert(tk.END, self._parse_inline_tags(line) + "\n", "list_item")
                continue

            # Обычная строка с тегами
            self.text.insert(tk.END, self._parse_inline_tags(line) + "\n", "normal")

    def _parse_inline_tags(self, text):
        """
        Обрабатывает встроенные теги <b>, <i>, <u> внутри строки.
        Возвращает очищенный текст (для упрощения вставки в одну строку).
        Для полноценного смешанного форматирования в Tkinter требуется сложная логика,
        поэтому здесь мы применяем приоритетное форматирование или очищаем теги.
        """
        # Заменяем <br> на перенос
        text = text.replace('<br>', '\n')
        
        # Удаляем теги для отображения, оставляя текст
        # (В Tkinter Text сложно делать частичное форматирование одной вставкой без сложного парсинга)
        # Для простоты и надежности удаляем теги, применяя стиль к всей строке выше
        clean = re.sub(r'<[^>]+>', '', text)
        return html.unescape(clean)

# ==============================================================================
# КЛАССЫ ПРИЛОЖЕНИЯ
# ==============================================================================

class ElementDetailWindow(tk.Toplevel):
    """Окно с подробной информацией об элементе."""
    def __init__(self, parent, element_data, settings):
        super().__init__(parent)
        self.title(f"{element_data['symbol']} - {element_data['name']}")
        self.geometry("550x450")
        self.resizable(True, True)
        
        color = settings.get('category_colors', {}).get(
            element_data.get('category', ''), 
            "#FFFFFF"
        )
        self.configure(bg=color)

        # Заголовок (всегда показываем)
        lbl_title = tk.Label(
            self, 
            text=f"{element_data['name']} ({element_data['symbol']})", 
            font=("Arial", 20, "bold"), 
            bg=color,
            wraplength=500
        )
        lbl_title.pack(pady=15, padx=10)

        # === ПРОВЕРКА: Есть ли HTML? ===
        has_html = 'html' in element_data and element_data['html']
        
        if has_html:
            # === ТОЛЬКО HTML ===
            desc_frame = tk.Frame(self, bg=color)
            desc_frame.pack(fill="both", expand=True, padx=20, pady=10)
            
            text_desc = tk.Text(
                desc_frame,
                font=("Arial", 11),
                bg="#FFFFFF",
                wrap="word",
                padx=10,
                pady=10,
                height=15,
                relief="flat",
                borderwidth=0
            )
            text_desc.pack(fill="both", expand=True)
            
            renderer = HTMLTextRenderer(text_desc)
            renderer.render(element_data['html'])
            text_desc.config(state="disabled")
        else:
            # === ПОЛНАЯ ИНФОРМАЦИЯ + ОПИСАНИЕ ===
            # Основная информация
            info_frame = tk.Frame(self, bg=color)
            info_frame.pack(fill="x", padx=20, pady=5)
            
            info_text = (
                f"Атомный номер: {element_data.get('number', 'N/A')}\n"
                f"Атомная масса: {element_data.get('mass', 'N/A')}\n"
                f"Категория: {element_data.get('category', 'N/A')}\n"
                f"Период: {element_data.get('row', 'N/A')}\n"
                f"Группа: {element_data.get('col', 'N/A')}"
            )
            
            lbl_info = tk.Label(
                info_frame, 
                text=info_text, 
                font=("Arial", 11), 
                bg=color, 
                justify="left",
                anchor="w"
            )
            lbl_info.pack(fill="x")

            # Описание
            desc_frame = tk.Frame(self, bg=color)
            desc_frame.pack(fill="both", expand=True, padx=20, pady=10)
            
            lbl_desc_title = tk.Label(
                desc_frame,
                text="Описание:",
                font=("Arial", 12, "bold"),
                bg=color
            )
            lbl_desc_title.pack(anchor="w")
            
            text_desc = tk.Text(
                desc_frame,
                font=("Arial", 11),
                bg="#FFFFFF",
                wrap="word",
                padx=10,
                pady=10,
                height=10,
                relief="flat",
                borderwidth=0
            )
            text_desc.pack(fill="both", expand=True)
            
            renderer = HTMLTextRenderer(text_desc)
            
            if 'description' in element_data and element_data['description']:
                renderer.render(element_data['description'])
            else:
                renderer.render("Нет описания")
            
            text_desc.config(state="disabled")

        # Кнопки
        btn_frame = tk.Frame(self, bg=color)
        btn_frame.pack(pady=15)
        
        btn_close = tk.Button(
            btn_frame, 
            text="Закрыть", 
            command=self.destroy, 
            font=("Arial", 10),
            bg="#333333",
            fg="white",
            padx=20,
            pady=5
        )
        btn_close.pack(side="left", padx=5)

class MoleculeWindow(tk.Toplevel):
    """Окно со списком молекул."""
    def __init__(self, parent, molecules):
        super().__init__(parent)
        self.title("Примеры молекул")
        self.geometry("700x500")
        self.resizable(True, True)
        
        columns = ("name", "formula", "description")
        tree = ttk.Treeview(self, columns=columns, show="headings")
        
        tree.heading("name", text="Название")
        tree.heading("formula", text="Формула")
        tree.heading("description", text="Описание")
        
        tree.column("name", width=200, minwidth=100)
        tree.column("formula", width=150, minwidth=100)
        tree.column("description", width=350, minwidth=200)
        
        scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=tree.yview)
        scrollbar_x = ttk.Scrollbar(self, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        scrollbar_y.grid(row=0, column=1, sticky="ns", pady=10)
        scrollbar_x.grid(row=1, column=0, sticky="ew", padx=10)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        for mol in molecules:
            tree.insert("", "end", values=(
                mol.get("name", ""), 
                mol.get("formula", ""), 
                mol.get("description", "")
            ))
            
        btn_close = tk.Button(self, text="Закрыть", command=self.destroy)
        btn_close.grid(row=2, column=0, pady=10)

class LegendWindow(tk.Toplevel):
    """Окно с легендой цветов категорий."""
    def __init__(self, parent, category_colors):
        super().__init__(parent)
        self.title("Легенда категорий")
        self.geometry("400x530")
        self.resizable(True, True)
        
        lbl_title = tk.Label(self, text="Категории элементов", font=("Arial", 16, "bold"))
        lbl_title.pack(pady=10)
        
        canvas = tk.Canvas(self, bg="#F0F0F0")
        canvas.pack(fill="both", expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        legend_frame = tk.Frame(canvas, bg="#F0F0F0")
        canvas_window = canvas.create_window((0, 0), window=legend_frame, anchor="nw")
        
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        legend_frame.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", on_canvas_configure)
        
        y_offset = 10
        box_width = 200
        box_height = 30
        
        for category, color in category_colors.items():
            canvas.create_rectangle(
                10, y_offset, 10 + box_height, y_offset + box_height,
                fill=color, outline="#333333", width=2
            )
            canvas.create_text(
                10 + box_height + 10, y_offset + box_height // 2,
                text=category, font=("Arial", 10), anchor="w"
            )
            y_offset += box_height + 5
        
        canvas.configure(scrollregion=(0, 0, 250, y_offset + 10))

class SettingsWindow(tk.Toplevel):
    """Окно настроек приложения."""
    def __init__(self, parent, settings, save_callback):
        super().__init__(parent)
        self.title("Настройки приложения")
        self.geometry("500x400")
        self.resizable(True, True)
        
        self.settings = settings
        self.save_callback = save_callback
        self.color_editors = {}
        
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Вкладка "Размеры"
        size_frame = tk.Frame(notebook)
        notebook.add(size_frame, text="Размеры")
        
        tk.Label(size_frame, text="Размер ячейки (ширина):", font=("Arial", 11)).pack(pady=5)
        self.cell_width_var = tk.IntVar(value=settings.get('cell_width', 65))
        tk.Spinbox(size_frame, from_=40, to=150, textvariable=self.cell_width_var, width=10).pack(pady=5)
        
        tk.Label(size_frame, text="Размер ячейки (высота):", font=("Arial", 11)).pack(pady=5)
        self.cell_height_var = tk.IntVar(value=settings.get('cell_height', 75))
        tk.Spinbox(size_frame, from_=40, to=150, textvariable=self.cell_height_var, width=10).pack(pady=5)
        
        tk.Label(size_frame, text="Ширина окна:", font=("Arial", 11)).pack(pady=5)
        self.window_width_var = tk.IntVar(value=settings.get('window_width', 1200))
        tk.Spinbox(size_frame, from_=800, to=2000, textvariable=self.window_width_var, width=10).pack(pady=5)
        
        tk.Label(size_frame, text="Высота окна:", font=("Arial", 11)).pack(pady=5)
        self.window_height_var = tk.IntVar(value=settings.get('window_height', 850))
        tk.Spinbox(size_frame, from_=600, to=1500, textvariable=self.window_height_var, width=10).pack(pady=5)
        
        # Вкладка "Цвета категорий"
        colors_frame = tk.Frame(notebook)
        notebook.add(colors_frame, text="Цвета категорий")
        
        colors_canvas = tk.Canvas(colors_frame, bg="#F0F0F0")
        colors_canvas.pack(side="left", fill="both", expand=True)
        
        colors_scrollbar = ttk.Scrollbar(colors_frame, orient="vertical", command=colors_canvas.yview)
        colors_scrollbar.pack(side="right", fill="y")
        colors_canvas.configure(yscrollcommand=colors_scrollbar.set)
        
        self.colors_inner_frame = tk.Frame(colors_canvas, bg="#F0F0F0")
        colors_window = colors_canvas.create_window((0, 0), window=self.colors_inner_frame, anchor="nw")
        
        def on_colors_frame_configure(event):
            colors_canvas.configure(scrollregion=colors_canvas.bbox("all"))
        def on_colors_canvas_configure(event):
            colors_canvas.itemconfig(colors_window, width=event.width)
        
        self.colors_inner_frame.bind("<Configure>", on_colors_frame_configure)
        colors_canvas.bind("<Configure>", on_colors_canvas_configure)
        
        category_colors = settings.get('category_colors', {})
        for i, (category, color) in enumerate(category_colors.items()):
            frame = tk.Frame(self.colors_inner_frame, bg="#F0F0F0")
            frame.pack(fill="x", padx=10, pady=5)
            
            tk.Label(frame, text=f"{category}:", font=("Arial", 10), bg="#F0F0F0").pack(side="left", padx=5)
            
            color_var = tk.StringVar(value=color)
            self.color_editors[category] = color_var
            
            entry = tk.Entry(frame, textvariable=color_var, width=15)
            entry.pack(side="left", padx=5)
            
            color_preview = tk.Canvas(frame, width=30, height=20, bg=color, highlightthickness=1, highlightbackground="#333")
            color_preview.pack(side="left", padx=5)
            
            def update_preview(cv=color_preview, var=color_var):
                try:
                    cv.configure(bg=var.get())
                except:
                    pass
            
            color_var.trace_add("write", lambda *args, cv=color_preview, var=color_var: update_preview(cv, var))
        
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        
        btn_save = tk.Button(btn_frame, text="Сохранить", command=self.on_save, font=("Arial", 10), bg="#4ECDC4", fg="white", padx=20, pady=5)
        btn_save.pack(side="left", padx=5)
        
        btn_cancel = tk.Button(btn_frame, text="Отмена", command=self.destroy, font=("Arial", 10), padx=20, pady=5)
        btn_cancel.pack(side="left", padx=5)
    
    def on_save(self):
        self.settings['cell_width'] = self.cell_width_var.get()
        self.settings['cell_height'] = self.cell_height_var.get()
        self.settings['window_width'] = self.window_width_var.get()
        self.settings['window_height'] = self.window_height_var.get()
        
        for category, var in self.color_editors.items():
            self.settings['category_colors'][category] = var.get()
        
        if save_json_file(SETTINGS_FILE, self.settings):
            messagebox.showinfo("Настройки", "Настройки сохранены!\nПерезапустите приложение для применения.")
            self.save_callback()
            self.destroy()
        else:
            messagebox.showerror("Ошибка", "Не удалось сохранить настройки!")

class ElementCard:
    """Класс, управляющий отрисовкой и поведением одного элемента."""
    def __init__(self, canvas, element_data, x, y, width, height, settings):
        self.canvas = canvas
        self.data = element_data
        self.base_x = x
        self.base_y = y
        self.width = width
        self.height = height
        self.settings = settings
        self.color = settings.get('category_colors', {}).get(element_data.get('category', ''), "#FFFFFF")
        self.is_hovered = False
        self.original_ids = []
        
        self.draw()
        self.bind_events()

    def draw(self):
        radius = 10
        self.rect_id = create_rounded_rectangle(
            self.canvas, self.base_x, self.base_y, 
            self.base_x + self.width, self.base_y + self.height, 
            radius, fill=self.color, outline="#333333", width=3
        )
        self.original_ids.append(self.rect_id)
        
        center_x = self.base_x + self.width / 2
        center_y = self.base_y + self.height / 2
        
        self.text_symbol = self.canvas.create_text(center_x, center_y, text=self.data.get('symbol', '?'), font=("Arial", 16, "bold"), fill="#000000")
        self.original_ids.append(self.text_symbol)
        
        self.text_number = self.canvas.create_text(self.base_x + 5, self.base_y + 5, text=str(self.data.get('number', '')), font=("Arial", 9), anchor="nw", fill="#000000")
        self.original_ids.append(self.text_number)
        
        self.text_mass = self.canvas.create_text(self.base_x + 5, self.base_y + self.height - 5, text=str(self.data.get('mass', '')), font=("Arial", 8), anchor="sw", fill="#000000")
        self.original_ids.append(self.text_mass)

    def bind_events(self):
        for item_id in self.original_ids:
            self.canvas.tag_bind(item_id, "<Enter>", self.on_enter)
            self.canvas.tag_bind(item_id, "<Leave>", self.on_leave)
            self.canvas.tag_bind(item_id, "<Button-1>", self.on_click)

    def on_enter(self, event):
        if self.is_hovered: return
        self.is_hovered = True
        scale_factor = 1.15
        center_x = self.base_x + self.width / 2
        center_y = self.base_y + self.height / 2
        for item_id in self.original_ids:
            self.canvas.scale(item_id, center_x, center_y, scale_factor, scale_factor)
            self.canvas.tag_raise(item_id)

    def on_leave(self, event):
        if not self.is_hovered: return
        self.is_hovered = False
        scale_factor = 1 / 1.15
        center_x = self.base_x + self.width / 2
        center_y = self.base_y + self.height / 2
        for item_id in self.original_ids:
            self.canvas.scale(item_id, center_x, center_y, scale_factor, scale_factor)

    def on_click(self, event):
        ElementDetailWindow(self.canvas.master, self.data, self.settings)

class PeriodicTableApp:
    """Главный класс приложения."""
    def __init__(self, root):
        self.root = root
        self.settings = self.load_settings()
        
        window_width = self.settings.get('window_width', 1200)
        window_height = self.settings.get('window_height', 850)
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.title("Интерактивная Таблица Менделеева")
        self.root.configure(bg="#F0F0F0")
        
        self.cell_width = self.settings.get('cell_width', 65)
        self.cell_height = self.settings.get('cell_height', 75)
        self.padding = 4
        
        top_frame = tk.Frame(root, bg="#333333", height=60)
        top_frame.pack(fill="x", side="top")
        
        btn_frame = tk.Frame(top_frame, bg="#333333")
        btn_frame.pack(pady=10, padx=10)
        
        self.btn_molecules = tk.Button(btn_frame, text="🧪 Молекулы", command=self.open_molecules, font=("Arial", 11, "bold"), bg="#4ECDC4", fg="white", relief="flat", padx=15, pady=5)
        self.btn_molecules.pack(side="left", padx=5)
        
        self.btn_legend = tk.Button(btn_frame, text="📋 Легенда", command=self.open_legend, font=("Arial", 11, "bold"), bg="#FF9F1C", fg="white", relief="flat", padx=15, pady=5)
        self.btn_legend.pack(side="left", padx=5)
        
        self.btn_settings = tk.Button(btn_frame, text="⚙️ Настройки", command=self.open_settings, font=("Arial", 11, "bold"), bg="#9D8DF1", fg="white", relief="flat", padx=15, pady=5)
        self.btn_settings.pack(side="left", padx=5)
        
        self.canvas = tk.Canvas(root, bg="#F0F0F0", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        scrollbar_y = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        scrollbar_x = tk.Scrollbar(root, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        
        self.elements = self.load_elements()
        self.draw_table()
        self.canvas.bind("<Configure>", self.on_canvas_configure)

    def load_settings(self):
        default_settings = {
            "cell_width": 65, "cell_height": 75, "window_width": 1200, "window_height": 850,
            "category_colors": {
                "Щелочные металлы": "#FF6B6B", "Щелочноземельные металлы": "#FFE66D",
                "Переходные металлы": "#4ECDC4", "Постпереходные металлы": "#C7F464",
                "Полуметаллы": "#A8D8EA", "Неметаллы": "#F7FFF7", "Галогены": "#FF9F1C",
                "Благородные газы": "#D4A5A5", "Лантаноиды": "#9D8DF1",
                "Актиноиды": "#C77DFF", "Неизвестные свойства": "#808080"
            }
        }
        settings = load_json_file(SETTINGS_FILE, default_settings)
        for key in default_settings:
            if key not in settings:
                settings[key] = default_settings[key]
        return settings

    def load_elements(self):
        return load_json_file(ELEMENTS_FILE, [])

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def draw_table(self):
        max_row = 0
        max_col = 0
        for el in self.elements:
            row = el.get('row', 1)
            col = el.get('col', 1)
            x = (col - 1) * (self.cell_width + self.padding) + self.padding + 20
            y = (row - 1) * (self.cell_height + self.padding) + self.padding + 20
            ElementCard(self.canvas, el, x, y, self.cell_width, self.cell_height, self.settings)
            if row > max_row: max_row = row
            if col > max_col: max_col = col
        
        total_width = max_col * (self.cell_width + self.padding) + 40
        total_height = max_row * (self.cell_height + self.padding) + 40
        self.canvas.configure(scrollregion=(0, 0, total_width, total_height))

    def open_molecules(self):
        molecules = load_json_file(MOLECULES_FILE, [{"name": "Вода", "formula": "H2O", "description": "Оксид водорода"}])
        MoleculeWindow(self.root, molecules)

    def open_legend(self):
        LegendWindow(self.root, self.settings.get('category_colors', {}))

    def open_settings(self):
        SettingsWindow(self.root, self.settings, self.on_settings_saved)

    def on_settings_saved(self):
        self.settings = self.load_settings()
        self.cell_width = self.settings.get('cell_width', 65)
        self.cell_height = self.settings.get('cell_height', 75)
        self.canvas.delete("all")
        self.draw_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = PeriodicTableApp(root)
    root.mainloop()