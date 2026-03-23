# dialogs.py

import tkinter as tk
from tkinter import colorchooser, messagebox
from config import config

class ColorPickerDialog(tk.Toplevel):
    """Диалог выбора цвета"""
    
    def __init__(self, parent, title, initial_color, callback):
        super().__init__(parent)
        self.title(title)
        self.geometry("300x150")
        self.resizable(False, False)
        self.callback = callback
        self.initial_color = initial_color
        
        self.preview = tk.Label(self, bg=initial_color, width=20, height=5)
        self.preview.pack(pady=10)
        
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Выбрать цвет", command=self._choose_color).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="OK", command=self._ok).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Отмена", command=self.destroy).pack(side=tk.LEFT, padx=5)
        
        self.selected_color = initial_color
        self.transient(parent)
        self.grab_set()
    
    def _choose_color(self):
        color = colorchooser.askcolor(color=self.initial_color, title="Выберите цвет")[1]
        if color:
            self.selected_color = color
            self.preview.config(bg=color)
    
    def _ok(self):
        self.callback(self.selected_color)
        self.destroy()


class SettingsDialog(tk.Toplevel):
    """Диалог настроек игры"""
    
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.title("Настройки игры")
        self.geometry("480x600")
        self.resizable(False, False)
        self.callback = callback
        
        self._create_widgets()
        self.transient(parent)
        self.grab_set()
    
    def _create_widgets(self):
        # Размер поля
        frame = tk.LabelFrame(self, text="Размер поля")
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(frame, text="Размер доски (клеток):").grid(row=0, column=0, padx=5, pady=5)
        self.board_size_var = tk.IntVar(value=config.board_size)
        self.board_size_spin = tk.Spinbox(frame, from_=6, to=10, width=5, 
                                          textvariable=self.board_size_var, 
                                          command=self._on_board_size_change)
        self.board_size_spin.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Размер клетки (px):").grid(row=1, column=0, padx=5, pady=5)
        self.cell_size_var = tk.IntVar(value=config.cell_size)
        tk.Spinbox(frame, from_=40, to=120, width=5, textvariable=self.cell_size_var).grid(row=1, column=1, padx=5, pady=5)
        
        # Количество шашек
        frame = tk.LabelFrame(self, text="Количество шашек")
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(frame, text="Рядов шашек (с каждой стороны):").grid(row=0, column=0, padx=5, pady=5)
        max_rows = config.get_max_piece_rows()
        self.piece_rows_var = tk.IntVar(value=config.piece_rows)
        self.piece_rows_spin = tk.Spinbox(frame, from_=1, to=max_rows, width=5, 
                                          textvariable=self.piece_rows_var)
        self.piece_rows_spin.grid(row=0, column=1, padx=5, pady=5)
        
        self.piece_count_label = tk.Label(frame, text=f"Всего шашек: {self._calculate_piece_count()}")
        self.piece_count_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        # Размер окна
        frame = tk.LabelFrame(self, text="Размер окна")
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(frame, text="Ширина:").grid(row=0, column=0, padx=5, pady=5)
        self.window_width_var = tk.IntVar(value=config.window_width)
        tk.Spinbox(frame, from_=600, to=1200, width=8, textvariable=self.window_width_var).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Высота:").grid(row=1, column=0, padx=5, pady=5)
        self.window_height_var = tk.IntVar(value=config.window_height)
        tk.Spinbox(frame, from_=500, to=1000, width=8, textvariable=self.window_height_var).grid(row=1, column=1, padx=5, pady=5)
        
        # Размер шашек
        frame = tk.LabelFrame(self, text="Размер шашек")
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(frame, text="Масштаб (0.5-0.9):").grid(row=0, column=0, padx=5, pady=5)
        self.piece_scale_var = tk.DoubleVar(value=config.piece_scale)
        tk.Scale(frame, from_=0.5, to=0.9, resolution=0.05, orient=tk.HORIZONTAL,
                 variable=self.piece_scale_var, length=200).grid(row=0, column=1, padx=5, pady=5)
        
        # Цвета
        frame = tk.LabelFrame(self, text="Цвета")
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        colors = [
            ("Светлые клетки", "color_light", config.color_light),
            ("Тёмные клетки", "color_dark", config.color_dark),
            ("Белые шашки", "color_piece_1", config.color_piece_1),
            ("Чёрные шашки", "color_piece_2", config.color_piece_2),
            ("Подсветка хода", "color_highlight", config.color_highlight),
            ("Серия ударов", "color_multi_jump", config.color_multi_jump),
            ("Выделение", "color_selection", config.color_selection),
            ("Рамка доски", "color_board_border", config.color_board_border),
        ]
        
        self.color_vars = {}
        self.color_buttons = {}
        
        for i, (label, key, default) in enumerate(colors):
            row = i // 2
            col = (i % 2) * 2
            
            tk.Label(frame, text=label + ":").grid(row=row, column=col, padx=5, pady=3, sticky=tk.W)
            
            btn = tk.Button(frame, bg=default, width=10, 
                           command=lambda k=key, d=default: self._pick_color(k, d))
            btn.grid(row=row, column=col+1, padx=5, pady=3)
            self.color_buttons[key] = btn
            self.color_vars[key] = default
        
        # Кнопки
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="Сохранить", command=self._save).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="По умолчанию", command=self._reset).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Отмена", command=self.destroy).pack(side=tk.LEFT, padx=10)
    
    def _on_board_size_change(self):
        """Обновление максимального количества рядов при изменении размера доски"""
        board_size = self.board_size_var.get()
        max_rows = board_size // 2 - 1
        current_rows = self.piece_rows_var.get()
        
        # Обновляем Spinbox для рядов шашек
        self.piece_rows_spin.config(to=max_rows)
        
        # Если текущее значение больше нового максимума, уменьшаем
        if current_rows > max_rows:
            self.piece_rows_var.set(max_rows)
        
        # Обновляем метку количества шашек
        self.piece_count_label.config(text=f"Всего шашек: {self._calculate_piece_count()}")
    
    def _calculate_piece_count(self):
        """Расчёт общего количества шашек"""
        board_size = self.board_size_var.get()
        piece_rows = self.piece_rows_var.get()
        
        # Количество тёмных клеток в ряду
        cells_per_row = board_size // 2
        
        # Общее количество шашек
        total = piece_rows * cells_per_row * 2  # *2 для обеих сторон
        
        return total
    
    def _pick_color(self, key, initial):
        def callback(color):
            self.color_vars[key] = color
            self.color_buttons[key].config(bg=color)
        ColorPickerDialog(self, f"Выберите цвет: {key}", initial, callback)
    
    def _save(self):
        config.board_size = self.board_size_var.get()
        config.cell_size = self.cell_size_var.get()
        config.window_width = self.window_width_var.get()
        config.window_height = self.window_height_var.get()
        config.piece_scale = self.piece_scale_var.get()
        config.piece_rows = self.piece_rows_var.get()
        
        for key, value in self.color_vars.items():
            setattr(config, key, value)
        
        if config.save():
            messagebox.showinfo("Настройки", "Настройки сохранены!\nПерезапустите игру для применения.")
            self.callback(True)
        else:
            messagebox.showerror("Ошибка", "Не удалось сохранить настройки")
        
        self.destroy()
    
    def _reset(self):
        if messagebox.askyesno("Сброс", "Сбросить все настройки к значениям по умолчанию?"):
            config.reset_to_defaults()
            self.destroy()
            SettingsDialog(self.master, self.callback)


class NetworkSettingsDialog(tk.Toplevel):
    """Диалог сетевых настроек"""
    
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.title("Настройки сети")
        self.geometry("480x650")
        self.resizable(False, False)
        self.callback = callback

        tk.Label(self, text="Имя игрока:").pack(pady=5)
        self.name_entry = tk.Entry(self, width=30)
        self.name_entry.insert(0, "Игрок")
        self.name_entry.pack()

        tk.Label(self, text="Режим:").pack(pady=5)
        self.mode = tk.StringVar(value="server")
        tk.Radiobutton(self, text="Создать игру (Сервер)", variable=self.mode, value="server").pack()
        tk.Radiobutton(self, text="Присоединиться (Клиент)", variable=self.mode, value="client").pack()

        tk.Label(self, text="IP адрес:").pack(pady=5)
        self.host_entry = tk.Entry(self, width=30)
        self.host_entry.insert(0, "127.0.0.1")
        self.host_entry.pack()

        tk.Label(self, text="Порт:").pack(pady=5)
        self.port_entry = tk.Entry(self, width=30)
        self.port_entry.insert(0, "5555")
        self.port_entry.pack()

        tk.Button(self, text="Подключиться", command=self._submit).pack(pady=20)
        self.transient(parent)
        self.grab_set()

    def _submit(self):
        result = {
            "name": self.name_entry.get(),
            "mode": self.mode.get(),
            "host": self.host_entry.get(),
            "port": int(self.port_entry.get())
        }
        self.callback(result)
        self.destroy()