import tkinter as tk
from tkinter import messagebox, Toplevel, filedialog, ttk
import json
import os
from datetime import datetime

class PomodoroWidget:
    def __init__(self):
        self.root = tk.Tk()
        
        # --- Пути к файлам ---
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_file = os.path.join(self.base_dir, "config.json")
        self.history_file = os.path.join(self.base_dir, "pomodoro_history.json")
        self.themes_dir = os.path.join(self.base_dir, "themes")
        
        # --- Загрузка настроек ---
        self.config = self.load_config()
        
        # --- Загрузка тем ---
        self.themes = self.load_themes()
        
        # --- Применяем тему ---
        self.theme_key = self.config.get('theme', 'dark')
        self.theme = self.themes.get(self.theme_key, self.themes.get('dark'))
        
        # --- Настройки окна ---
        self.root.title("Pomodoro")
        self.root.geometry(f"{self.config['window_width']}x{self.config['window_height']}+{self.config['window_position_x']}+{self.config['window_position_y']}")
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', self.config['window_opacity'])
        self.root.configure(bg=self.theme['bg_primary'])
        
        # Переменные таймера
        self.work_time = self.config['work_time_minutes'] * 60
        self.break_time = self.config['break_time_minutes'] * 60
        self.current_time = self.work_time
        self.is_running = False
        self.is_work_mode = True
        self.job_id = None
        self.session_start = None
        
        # Тексты режимов
        self.work_text = self.config.get('work_text', 'WORK')
        self.break_text = self.config.get('break_text', 'BREAK')
        
        # Для перетаскивания
        self.start_x = 0
        self.start_y = 0
        
        # История сессий
        self.history = self.load_history()
        
        # --- Интерфейс ---
        self.top_frame = tk.Frame(self.root, bg=self.theme['bg_primary'])
        self.top_frame.pack(fill=tk.X, padx=5, pady=3)
        
        # Кнопка настроек
        self.btn_settings = tk.Button(
            self.top_frame, text="⚙️", font=self.theme['font_button'],
            bg=self.theme['bg_button'], fg=self.theme['fg_primary'], bd=0,
            command=self.open_settings,
            activebackground=self.theme['bg_button_active'], activeforeground=self.theme['fg_primary'],
            cursor="hand2", width=2
        )
        self.btn_settings.pack(side=tk.LEFT)
        self.create_tooltip(self.btn_settings, "Настройки")
        
        # Кнопка статистики
        self.btn_stats = tk.Button(
            self.top_frame, text="📊", font=self.theme['font_button'],
            bg=self.theme['bg_button'], fg=self.theme['fg_primary'], bd=0,
            command=self.open_stats,
            activebackground=self.theme['bg_button_active'], activeforeground=self.theme['fg_primary'],
            cursor="hand2", width=2
        )
        self.btn_stats.pack(side=tk.LEFT, padx=3)
        self.create_tooltip(self.btn_stats, "Статистика")
        
        # Пустое пространство для перетаскивания
        self.drag_area = tk.Frame(self.top_frame, bg=self.theme['bg_primary'])
        self.drag_area.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Кнопка закрытия
        self.btn_close = tk.Button(
            self.top_frame, text="✕", font=("Arial", 12, "bold"),
            bg=self.theme['btn_close_bg'], fg=self.theme['btn_close_fg'], bd=0,
            command=self.close_app,
            activebackground='#ff6666', activeforeground='#ffffff',
            cursor="hand2", width=3
        )
        self.btn_close.pack(side=tk.RIGHT)
        self.create_tooltip(self.btn_close, "Закрыть")
        
        # Таймер
        self.label_time = tk.Label(
            self.root, 
            text="25:00", 
            font=self.theme['font_time'], 
            bg=self.theme['bg_primary'], 
            fg=self.theme['fg_accent']
        )
        self.label_time.pack(expand=True)
        
        # Режим
        self.label_mode = tk.Label(
            self.root,
            text=self.work_text,
            font=self.theme['font_text'],
            bg=self.theme['bg_primary'],
            fg=self.theme['fg_secondary']
        )
        self.label_mode.pack(pady=(0, 5))

        # --- Привязка событий ---
        self.drag_area.bind("<ButtonPress-1>", self.on_press)
        self.drag_area.bind("<B1-Motion>", self.move_window)
        self.drag_area.bind("<ButtonRelease-1>", self.save_position)
        self.label_time.bind("<ButtonPress-1>", self.on_press)
        self.label_time.bind("<B1-Motion>", self.move_window)
        self.label_time.bind("<ButtonRelease-1>", lambda e: (self.start_pause(e), self.save_position(e)))
        
        self.root.bind("<Button-3>", self.reset_timer)
        self.root.bind("<Double-Button-1>", self.close_app)
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    def load_config(self):
        """Загружает настройки из config.json"""
        default_config = {
            "work_time_minutes": 25,
            "break_time_minutes": 5,
            "window_opacity": 0.95,
            "window_position_x": 100,
            "window_position_y": 100,
            "window_width": 240,
            "window_height": 100,
            "theme": "dark",
            "show_notifications": True,
            "auto_start_break": True,
            "work_text": "WORK",
            "break_text": "BREAK"
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            except Exception as e:
                print(f"Ошибка загрузки конфига: {e}")
        
        self.save_config(default_config)
        return default_config

    def save_config(self, config=None):
        """Сохраняет настройки в config.json"""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Ошибка сохранения конфига: {e}")
            return False

    def load_themes(self):
        """Загружает все темы из папки themes/"""
        themes = {}
        
        if not os.path.exists(self.themes_dir):
            os.makedirs(self.themes_dir)
            self.create_default_themes()
        
        for filename in os.listdir(self.themes_dir):
            if filename.endswith('.json'):
                theme_key = filename[:-5]
                theme_path = os.path.join(self.themes_dir, filename)
                try:
                    with open(theme_path, 'r', encoding='utf-8') as f:
                        theme_data = json.load(f)
                        for font_key in ['font_time', 'font_text', 'font_button']:
                            if font_key in theme_data and isinstance(theme_data[font_key], list):
                                theme_data[font_key] = tuple(theme_data[font_key])
                        themes[theme_key] = theme_data
                except Exception as e:
                    print(f"Ошибка загрузки темы {filename}: {e}")
        
        if not themes:
            self.create_default_themes()
            return self.load_themes()
        
        return themes

    def create_default_themes(self):
        """Создаёт дефолтные темы в папке themes/"""
        default_themes = {
            "dark": {
                "name": "Тёмная",
                "bg_primary": "#1a1a1a",
                "bg_secondary": "#2a2a2a",
                "bg_button": "#333333",
                "bg_button_active": "#555555",
                "fg_primary": "#ffffff",
                "fg_secondary": "#888888",
                "fg_accent": "#4CAF50",
                "fg_break": "#2196F3",
                "fg_pause": "#FF9800",
                "btn_close_bg": "#ff4444",
                "btn_close_fg": "#ffffff",
                "font_time": ["Helvetica", 32, "bold"],
                "font_text": ["Arial", 10, "bold"],
                "font_button": ["Arial", 11]
            },
            "light": {
                "name": "Светлая",
                "bg_primary": "#f5f5f5",
                "bg_secondary": "#ffffff",
                "bg_button": "#e0e0e0",
                "bg_button_active": "#c0c0c0",
                "fg_primary": "#333333",
                "fg_secondary": "#666666",
                "fg_accent": "#2E7D32",
                "fg_break": "#1565C0",
                "fg_pause": "#EF6C00",
                "btn_close_bg": "#d32f2f",
                "btn_close_fg": "#ffffff",
                "font_time": ["Helvetica", 32, "bold"],
                "font_text": ["Arial", 10, "bold"],
                "font_button": ["Arial", 11]
            },
            "blue": {
                "name": "Синяя",
                "bg_primary": "#0d1b2a",
                "bg_secondary": "#1b263b",
                "bg_button": "#415a77",
                "bg_button_active": "#778da9",
                "fg_primary": "#e0e1dd",
                "fg_secondary": "#a0a0a0",
                "fg_accent": "#00b4d8",
                "fg_break": "#90e0ef",
                "fg_pause": "#ffb703",
                "btn_close_bg": "#e63946",
                "btn_close_fg": "#ffffff",
                "font_time": ["Segoe UI", 32, "bold"],
                "font_text": ["Segoe UI", 10, "bold"],
                "font_button": ["Segoe UI", 11]
            }
        }
        
        for theme_key, theme_data in default_themes.items():
            theme_path = os.path.join(self.themes_dir, f"{theme_key}.json")
            with open(theme_path, 'w', encoding='utf-8') as f:
                json.dump(theme_data, f, ensure_ascii=False, indent=4)

    def save_theme(self, theme_key, theme_data):
        """Сохраняет тему в файл"""
        theme_copy = theme_data.copy()
        for font_key in ['font_time', 'font_text', 'font_button']:
            if font_key in theme_copy and isinstance(theme_copy[font_key], tuple):
                theme_copy[font_key] = list(theme_copy[font_key])
        
        theme_path = os.path.join(self.themes_dir, f"{theme_key}.json")
        with open(theme_path, 'w', encoding='utf-8') as f:
            json.dump(theme_copy, f, ensure_ascii=False, indent=4)
        
        self.themes[theme_key] = theme_data
        return True

    def delete_theme(self, theme_key):
        """Удаляет тему (нельзя удалять dark)"""
        if theme_key == 'dark':
            return False
        
        theme_path = os.path.join(self.themes_dir, f"{theme_key}.json")
        if os.path.exists(theme_path):
            os.remove(theme_path)
            if theme_key in self.themes:
                del self.themes[theme_key]
            return True
        return False

    def import_theme(self, file_path):
        """Импортирует тему из файла"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                theme_data = json.load(f)
            
            required_fields = ['name', 'bg_primary', 'fg_primary', 'font_time']
            for field in required_fields:
                if field not in theme_data:
                    return False, f"Отсутствует поле: {field}"
            
            filename = os.path.basename(file_path)
            theme_key = filename[:-5] if filename.endswith('.json') else filename
            
            for font_key in ['font_time', 'font_text', 'font_button']:
                if font_key in theme_data and isinstance(theme_data[font_key], list):
                    theme_data[font_key] = tuple(theme_data[font_key])
            
            self.save_theme(theme_key, theme_data)
            return True, f"Тема '{theme_data.get('name', theme_key)}' импортирована!"
        except Exception as e:
            return False, f"Ошибка импорта: {str(e)}"

    def export_theme(self, theme_key):
        """Экспортирует тему в файл"""
        if theme_key not in self.themes:
            return False, "Тема не найдена"
        
        theme_data = self.themes[theme_key]
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile=f"{theme_key}.json",
            title="Экспорт темы"
        )
        
        if file_path:
            try:
                self.save_theme(theme_key, theme_data)
                import shutil
                source = os.path.join(self.themes_dir, f"{theme_key}.json")
                shutil.copy2(source, file_path)
                return True, f"Тема экспортирована в {file_path}"
            except Exception as e:
                return False, f"Ошибка экспорта: {str(e)}"
        
        return False, "Отменено"

    def save_position(self, event=None):
        """Сохраняет позицию и размер окна"""
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        
        if self.config['window_position_x'] != x or self.config['window_position_y'] != y:
            self.config['window_position_x'] = x
            self.config['window_position_y'] = y
        if self.config['window_width'] != w or self.config['window_height'] != h:
            self.config['window_width'] = w
            self.config['window_height'] = h
        self.save_config()

    def apply_theme(self, theme_key):
        """Применяет тему ко всем элементам"""
        if theme_key not in self.themes:
            return
        
        self.theme_key = theme_key
        self.theme = self.themes[theme_key]
        self.config['theme'] = theme_key
        
        self.root.configure(bg=self.theme['bg_primary'])
        self.top_frame.configure(bg=self.theme['bg_primary'])
        self.drag_area.configure(bg=self.theme['bg_primary'])
        
        for btn in [self.btn_settings, self.btn_stats]:
            btn.configure(
                font=self.theme['font_button'],
                bg=self.theme['bg_button'],
                fg=self.theme['fg_primary'],
                activebackground=self.theme['bg_button_active']
            )
        
        color = self.theme['fg_accent'] if self.is_work_mode else self.theme['fg_break']
        self.label_time.configure(
            font=self.theme['font_time'],
            bg=self.theme['bg_primary'],
            fg=color
        )
        self.label_mode.configure(
            font=self.theme['font_text'],
            bg=self.theme['bg_primary'],
            fg=self.theme['fg_secondary']
        )

    def create_tooltip(self, widget, text):
        """Создает всплывающую подсказку"""
        def on_enter(event):
            self.tooltip = Toplevel(self.root)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_attributes('-topmost', True)
            label = tk.Label(
                self.tooltip, text=text,
                bg='#ffffcc', fg='#000000',
                font=("Arial", 9),
                padx=5, pady=2,
                relief=tk.SOLID, borderwidth=1
            )
            label.pack()
            
            x = widget.winfo_rootx() + widget.winfo_width() // 2 - label.winfo_reqwidth() // 2
            y = widget.winfo_rooty() - label.winfo_reqheight() - 5
            self.tooltip.wm_geometry(f"+{x}+{y}")
        
        def on_leave(event):
            if hasattr(self, 'tooltip'):
                self.tooltip.destroy()
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def on_press(self, event):
        self.start_x = event.x_root - self.root.winfo_x()
        self.start_y = event.y_root - self.root.winfo_y()

    def move_window(self, event):
        x = event.x_root - self.start_x
        y = event.y_root - self.start_y
        self.root.geometry(f'+{x}+{y}')

    def start_pause(self, event=None):
        if self.is_running:
            self.is_running = False
            if self.job_id:
                self.root.after_cancel(self.job_id)
            self.label_time.config(fg=self.theme['fg_pause'])
        else:
            self.is_running = True
            if self.session_start is None:
                self.session_start = datetime.now()
            self.countdown()
            color = self.theme['fg_accent'] if self.is_work_mode else self.theme['fg_break']
            self.label_time.config(fg=color)

    def reset_timer(self, event=None):
        if self.session_start and self.is_work_mode:
            self.save_session()
        
        self.is_running = False
        if self.job_id:
            self.root.after_cancel(self.job_id)
        
        self.is_work_mode = True
        self.current_time = self.work_time
        self.session_start = None
        self.update_display()
        self.label_time.config(fg=self.theme['fg_accent'])
        self.label_mode.config(text=self.work_text)

    def countdown(self):
        if self.is_running:
            if self.current_time > 0:
                self.current_time -= 1
                self.update_display()
                self.job_id = self.root.after(1000, self.countdown)
            else:
                self.switch_mode()

    def switch_mode(self):
        self.save_session()
        
        if self.config['show_notifications']:
            self.root.bell()
        
        if self.is_work_mode:
            self.is_work_mode = False
            self.current_time = self.break_time
            self.label_mode.config(text=self.break_text)
            color = self.theme['fg_break']
        else:
            self.is_work_mode = True
            self.current_time = self.work_time
            self.label_mode.config(text=self.work_text)
            color = self.theme['fg_accent']
            
        self.session_start = datetime.now()
        self.label_time.config(fg=color)
        self.update_display()
        
        if self.config['auto_start_break']:
            self.countdown()

    def save_session(self):
        if self.session_start:
            duration = (datetime.now() - self.session_start).total_seconds()
            if duration > 0:
                session = {
                    "date": self.session_start.strftime("%Y-%m-%d %H:%M:%S"),
                    "type": "Work" if self.is_work_mode else "Break",
                    "duration_seconds": int(duration)
                }
                self.history.append(session)
                self.save_history()
            self.session_start = None

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_history(self):
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def update_display(self):
        minutes = self.current_time // 60
        seconds = self.current_time % 60
        time_string = f"{minutes:02d}:{seconds:02d}"
        self.label_time.config(text=time_string)

    def open_settings(self):
        # Создаём окно настроек (БЕЗ ПРОКРУТКИ)
        settings_win = Toplevel(self.root)
        settings_win.title("Настройки")
        settings_win.overrideredirect(True)
        settings_win.attributes('-topmost', True)
        settings_win.configure(bg=self.theme['bg_secondary'])
        
        x = self.root.winfo_x() + 50
        y = self.root.winfo_y() + 50
        
        # --- Основной контейнер (просто Frame, без Canvas) ---
        content_frame = tk.Frame(settings_win, bg=self.theme['bg_secondary'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # --- Время работы ---
        tk.Label(content_frame, text="Время работы (мин):", 
                bg=self.theme['bg_secondary'], fg=self.theme['fg_primary'], 
                font=("Arial", 10)).pack(pady=3)
        work_entry = tk.Entry(content_frame, font=("Arial", 12), width=10)
        work_entry.insert(0, str(self.config['work_time_minutes']))
        work_entry.pack()
        
        # --- Время отдыха ---
        tk.Label(content_frame, text="Время отдыха (мин):", 
                bg=self.theme['bg_secondary'], fg=self.theme['fg_primary'], 
                font=("Arial", 10)).pack(pady=3)
        break_entry = tk.Entry(content_frame, font=("Arial", 12), width=10)
        break_entry.insert(0, str(self.config['break_time_minutes']))
        break_entry.pack()
        
        # --- Размер окна ---
        size_frame = tk.Frame(content_frame, bg=self.theme['bg_secondary'])
        size_frame.pack(pady=5)
        
        tk.Label(size_frame, text="Ширина:", 
                bg=self.theme['bg_secondary'], fg=self.theme['fg_primary'], 
                font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        width_entry = tk.Entry(size_frame, font=("Arial", 12), width=6)
        width_entry.insert(0, str(self.config['window_width']))
        width_entry.pack(side=tk.LEFT)
        
        tk.Label(size_frame, text="Высота:", 
                bg=self.theme['bg_secondary'], fg=self.theme['fg_primary'], 
                font=("Arial", 10)).pack(side=tk.LEFT, padx=15)
        height_entry = tk.Entry(size_frame, font=("Arial", 12), width=6)
        height_entry.insert(0, str(self.config['window_height']))
        height_entry.pack(side=tk.LEFT)
        
        # --- Текст режимов ---
        tk.Label(content_frame, text="Текст режима работы:", 
                bg=self.theme['bg_secondary'], fg=self.theme['fg_primary'], 
                font=("Arial", 10)).pack(pady=3)
        work_text_entry = tk.Entry(content_frame, font=("Arial", 12), width=15)
        work_text_entry.insert(0, self.work_text)
        work_text_entry.pack()
        
        tk.Label(content_frame, text="Текст режима отдыха:", 
                bg=self.theme['bg_secondary'], fg=self.theme['fg_primary'], 
                font=("Arial", 10)).pack(pady=3)
        break_text_entry = tk.Entry(content_frame, font=("Arial", 12), width=15)
        break_text_entry.insert(0, self.break_text)
        break_text_entry.pack()
        
        # --- Выбор темы (Combobox) ---
        tk.Label(content_frame, text="Тема оформления:", 
                bg=self.theme['bg_secondary'], fg=self.theme['fg_primary'], 
                font=("Arial", 10)).pack(pady=5)
        
        theme_names = [(key, self.themes[key]['name']) for key in self.themes.keys()]
        theme_values = [f"{name} ({key})" for key, name in theme_names]
        
        self.theme_var = tk.StringVar(value=f"{self.themes[self.config['theme']]['name']} ({self.config['theme']})")
        theme_combo = ttk.Combobox(
            content_frame,
            textvariable=self.theme_var,
            values=theme_values,
            state="readonly",
            font=("Arial", 11),
            width=25
        )
        theme_combo.pack(pady=5)
        
        # --- Управление темами ---
        theme_btn_frame = tk.Frame(content_frame, bg=self.theme['bg_secondary'])
        theme_btn_frame.pack(pady=10)
        
        def get_selected_theme_key():
            selected = self.theme_var.get()
            for key, name in theme_names:
                if f"{name} ({key})" == selected:
                    return key
            return self.config['theme']
        
        def import_theme():
            file_path = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json")],
                title="Импорт темы"
            )
            if file_path:
                success, message = self.import_theme(file_path)
                if success:
                    self.themes = self.load_themes()
                    self.status_label.config(text=f"✓ {message}", fg=self.theme['fg_accent'])
                    settings_win.destroy()
                    self.open_settings()
                else:
                    self.status_label.config(text=f"✕ {message}", fg='#ff4444')
        
        def export_theme():
            theme_key = get_selected_theme_key()
            success, message = self.export_theme(theme_key)
            self.status_label.config(text=f"{'✓' if success else '✕'} {message}", 
                                    fg=self.theme['fg_accent'] if success else '#ff4444')
        
        def delete_theme():
            theme_key = get_selected_theme_key()
            if theme_key == 'dark':
                messagebox.showwarning("Предупреждение", "Нельзя удалить тему 'dark'")
                return
            
            theme_name = self.themes[theme_key]['name']
            if messagebox.askyesno("Удаление", f"Удалить тему '{theme_name}'?"):
                if self.delete_theme(theme_key):
                    self.config['theme'] = 'dark'
                    self.apply_theme('dark')
                    self.status_label.config(text="✓ Тема удалена", fg=self.theme['fg_accent'])
                    settings_win.destroy()
                    self.open_settings()
                else:
                    self.status_label.config(text="✕ Ошибка удаления", fg='#ff4444')
        
        tk.Button(theme_btn_frame, text="📥 Импорт", command=import_theme,
                 bg=self.theme['bg_button'], fg=self.theme['fg_primary'], bd=0, 
                 font=("Arial", 9), cursor="hand2").pack(side=tk.LEFT, padx=3)
        
        tk.Button(theme_btn_frame, text="📤 Экспорт", command=export_theme,
                 bg=self.theme['bg_button'], fg=self.theme['fg_primary'], bd=0, 
                 font=("Arial", 9), cursor="hand2").pack(side=tk.LEFT, padx=3)
        
        tk.Button(theme_btn_frame, text="🗑️ Удалить", command=delete_theme,
                 bg=self.theme['btn_close_bg'], fg='#ffffff', bd=0, 
                 font=("Arial", 9), cursor="hand2").pack(side=tk.LEFT, padx=3)
        
        # --- Уведомления ---
        self.notify_var = tk.BooleanVar(value=self.config['show_notifications'])
        notify_check = tk.Checkbutton(
            content_frame, text="Звуковые уведомления",
            variable=self.notify_var,
            bg=self.theme['bg_secondary'], fg=self.theme['fg_primary'],
            selectcolor=self.theme['bg_button'], activebackground=self.theme['bg_secondary'],
            activeforeground=self.theme['fg_primary'],
            font=("Arial", 9)
        )
        notify_check.pack(pady=3)
        
        # --- Автозапуск перерыва ---
        self.auto_start_var = tk.BooleanVar(value=self.config['auto_start_break'])
        auto_check = tk.Checkbutton(
            content_frame, text="Автозапуск перерыва",
            variable=self.auto_start_var,
            bg=self.theme['bg_secondary'], fg=self.theme['fg_primary'],
            selectcolor=self.theme['bg_button'], activebackground=self.theme['bg_secondary'],
            activeforeground=self.theme['fg_primary'],
            font=("Arial", 9)
        )
        auto_check.pack(pady=3)
        
        # --- Статус сохранения ---
        self.status_label = tk.Label(
            content_frame, text="",
            bg=self.theme['bg_secondary'], fg=self.theme['fg_accent'],
            font=("Arial", 9)
        )
        self.status_label.pack(pady=2)
        
        # --- Кнопки управления ---
        btn_frame = tk.Frame(content_frame, bg=self.theme['bg_secondary'])
        btn_frame.pack(pady=10)
        
        def save_settings():
            try:
                work_min = int(work_entry.get())
                break_min = int(break_entry.get())
                width = int(width_entry.get())
                height = int(height_entry.get())
                work_txt = work_text_entry.get().strip()
                break_txt = break_text_entry.get().strip()
                selected_theme = get_selected_theme_key()
                
                if work_min > 0 and break_min > 0 and width > 150 and height > 80:
                    if work_txt and break_txt:
                        self.config['work_time_minutes'] = work_min
                        self.config['break_time_minutes'] = break_min
                        self.config['window_width'] = width
                        self.config['window_height'] = height
                        self.config['work_text'] = work_txt
                        self.config['break_text'] = break_txt
                        self.config['theme'] = selected_theme
                        self.config['show_notifications'] = self.notify_var.get()
                        self.config['auto_start_break'] = self.auto_start_var.get()
                        
                        if self.save_config():
                            self.work_time = work_min * 60
                            self.break_time = break_min * 60
                            self.work_text = work_txt
                            self.break_text = break_txt
                            self.root.geometry(f"{width}x{height}+{self.root.winfo_x()}+{self.root.winfo_y()}")
                            self.apply_theme(selected_theme)
                            
                            if not self.is_running:
                                self.current_time = self.work_time
                                self.update_display()
                                self.label_mode.config(text=self.work_text)
                            
                            self.status_label.config(text="✓ Настройки сохранены!")
                            settings_win.after(2000, lambda: self.status_label.config(text=""))
                        else:
                            self.status_label.config(text="✕ Ошибка сохранения!", fg='#ff4444')
                    else:
                        self.status_label.config(text="✕ Текст не может быть пустым!", fg='#ff4444')
                else:
                    self.status_label.config(text="✕ Некорректные значения!", fg='#ff4444')
            except ValueError:
                self.status_label.config(text="✕ Введите числа!", fg='#ff4444')
        
        def reset_defaults():
            if messagebox.askyesno("Сброс", "Вернуть настройки по умолчанию?"):
                work_entry.delete(0, tk.END)
                work_entry.insert(0, "25")
                break_entry.delete(0, tk.END)
                break_entry.insert(0, "5")
                width_entry.delete(0, tk.END)
                width_entry.insert(0, "240")
                height_entry.delete(0, tk.END)
                height_entry.insert(0, "100")
                work_text_entry.delete(0, tk.END)
                work_text_entry.insert(0, "WORK")
                break_text_entry.delete(0, tk.END)
                break_text_entry.insert(0, "BREAK")
                self.theme_var.set(f"{self.themes['dark']['name']} (dark)")
                self.notify_var.set(True)
                self.auto_start_var.set(True)
                self.status_label.config(text="Настройки сброшены", fg=self.theme['fg_pause'])
        
        tk.Button(btn_frame, text="Сохранить", command=save_settings,
                 bg=self.theme['fg_accent'], fg='#ffffff', bd=0, font=("Arial", 10),
                 cursor="hand2", width=12).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Сброс", command=reset_defaults,
                 bg=self.theme['fg_pause'], fg='#ffffff', bd=0, font=("Arial", 10),
                 cursor="hand2", width=12).pack(side=tk.LEFT, padx=5)
        
        tk.Button(settings_win, text="✕", command=settings_win.destroy,
                 bg=self.theme['btn_close_bg'], fg='#ffffff', bd=0, font=("Arial", 8),
                 cursor="hand2").place(x=375, y=2)
        
        # --- Авто-размер окна ---
        settings_win.update_idletasks()
        content_width = 400
        content_height = content_frame.winfo_reqheight() + 80
        settings_win.geometry(f"{content_width}x{content_height}+{x}+{y}")

    def open_stats(self):
        stats_win = Toplevel(self.root)
        stats_win.title("Статистика")
        stats_win.overrideredirect(True)
        stats_win.attributes('-topmost', True)
        stats_win.configure(bg=self.theme['bg_secondary'])
        
        x = self.root.winfo_x() + 50
        y = self.root.winfo_y() + 50
        stats_win.geometry(f"+{x}+{y}")
        
        # Заголовок
        tk.Label(stats_win, text="📊 История сессий", 
                bg=self.theme['bg_secondary'], fg=self.theme['fg_primary'], 
                font=("Arial", 14, "bold")).pack(pady=10)
        
        # --- Текстовое поле с прокруткой ---
        text_frame = tk.Frame(stats_win, bg=self.theme['bg_secondary'])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        stats_text = tk.Text(
            text_frame,
            bg=self.theme['bg_primary'],
            fg=self.theme['fg_primary'],
            font=("Consolas", 10),
            wrap=tk.WORD,
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        
        # Скроллбар для текста
        text_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=stats_text.yview)
        stats_text.configure(yscrollcommand=text_scrollbar.set)
        
        stats_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Формируем текст статистики
        total_work = sum(s["duration_seconds"] for s in self.history if s["type"] == "Work")
        total_break = sum(s["duration_seconds"] for s in self.history if s["type"] == "Break")
        total_sessions = len(self.history)
        
        output = f"{'='*40}\n"
        output += f" ОБЩАЯ СТАТИСТИКА\n"
        output += f"{'='*40}\n"
        output += f"Всего сессий: {total_sessions}\n"
        output += f"Всего работы: {total_work // 60} мин ({total_work // 3600} ч {total_work % 3600 // 60} мин)\n"
        output += f"Всего отдыха: {total_break // 60} мин\n\n"
        output += f"{'='*40}\n"
        output += f" ПОСЛЕДНИЕ 10 СЕССИЙ\n"
        output += f"{'='*40}\n"
        
        recent_history = self.history[-10:][::-1]
        for i, session in enumerate(recent_history, 1):
            date_str = session["date"].split(" ")[0]
            time_str = session["date"].split(" ")[1][:5]
            duration_min = session["duration_seconds"] // 60
            type_name = session["type"]
            output += f"{i}. {date_str} {time_str} | {type_name:5} | {duration_min} мин\n"
        
        if not recent_history:
            output += "\nИстория пуста\n"
        
        output += f"\n{'='*40}\n"
        
        # Вставляем текст
        stats_text.insert("1.0", output)
        stats_text.config(state=tk.DISABLED)  # Только для чтения
        
        # --- Кнопки (всегда видны внизу) ---
        btn_frame = tk.Frame(stats_win, bg=self.theme['bg_secondary'])
        btn_frame.pack(pady=10, side=tk.BOTTOM, fill=tk.X)
        
        def clear_history():
            if messagebox.askyesno("Подтверждение", "Очистить всю историю?"):
                self.history = []
                self.save_history()
                stats_win.destroy()
                self.open_stats()
        
        tk.Button(btn_frame, text="Очистить историю", command=clear_history,
                 bg=self.theme['btn_close_bg'], fg='#ffffff', bd=0, font=("Arial", 9),
                 cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Закрыть", command=stats_win.destroy,
                 bg=self.theme['bg_button'], fg=self.theme['fg_primary'], bd=0, 
                 font=("Arial", 9),
                 cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        tk.Button(stats_win, text="✕", command=stats_win.destroy,
                 bg=self.theme['btn_close_bg'], fg='#ffffff', bd=0, font=("Arial", 8),
                 cursor="hand2").place(x=375, y=2)
        
        # Авто-размер
        stats_win.update_idletasks()
        stats_win.geometry(f"400x400+{x}+{y}")
        
        # --- Прокрутка колёсиком для статистики ---
        def on_stats_mousewheel(event):
            try:
                stats_text.yview_scroll(int(-1*(event.delta/120)), "units")
            except:
                pass
        
        stats_text.bind_all("<MouseWheel>", on_stats_mousewheel)
        
        # --- Очистка при закрытии ---
        def on_stats_close():
            try:
                stats_text.unbind_all("<MouseWheel>")
            except:
                pass
            stats_win.destroy()
        
        stats_win.protocol("WM_DELETE_WINDOW", on_stats_close)

    def close_app(self, event=None):
        self.save_position()
        self.save_config()
        
        if self.session_start and self.is_work_mode:
            self.save_session()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PomodoroWidget()
    app.run()