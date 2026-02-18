import tkinter as tk
from tkinter import messagebox, Toplevel, filedialog, ttk
import json, os
from datetime import datetime

class Pomodoro:
    THEMES_DIR = "themes"
    CONFIG_FILE = "config.json"
    HISTORY_FILE = "pomodoro_history.json"
    
    DEFAULTS = {
        "work_time": 25, "break_time": 5, "opacity": 0.95,
        "pos_x": 100, "pos_y": 100, "width": 240, "height": 100,
        "theme": "dark", "sound": True, "auto_start": True,
        "work_text": "WORK", "break_text": "BREAK"
    }

    def __init__(self):
        self.root = tk.Tk()
        self.config = self.load_config()
        self.themes = self.load_themes()
        self.theme = self.themes.get(self.config['theme'], self.themes['dark'])
        self.history = self.load_json(self.HISTORY_FILE, [])
        
        self.time = self.config['work_time'] * 60
        self.max_time = self.time
        self.running = False
        self.work_mode = True
        self.job = None
        self.start_time = None
        
        self.setup_window()
        self.setup_ui()
        self.setup_bindings()
        self.update_display()

    def load_config(self):
        config = self.DEFAULTS.copy()
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    config.update(loaded)
            except:
                pass
        self.save_json(self.CONFIG_FILE, config)
        return config

    def load_json(self, path, default):
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        self.save_json(path, default)
        return default

    def save_json(self, path, data):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def load_themes(self):
        if not os.path.exists(self.THEMES_DIR):
            os.makedirs(self.THEMES_DIR)
            for k, v in self.get_default_themes().items():
                self.save_json(f"{self.THEMES_DIR}/{k}.json", v)
        
        themes = {}
        for f in os.listdir(self.THEMES_DIR):
            if f.endswith('.json'):
                try:
                    with open(f"{self.THEMES_DIR}/{f}", 'r', encoding='utf-8') as file:
                        t = json.load(file)
                        for k in ['font_time', 'font_text', 'font_button']:
                            if k in t and isinstance(t[k], list):
                                t[k] = tuple(t[k])
                        themes[f[:-5]] = t
                except:
                    pass
        return themes or self.get_default_themes()

    def get_default_themes(self):
        return {
            "dark": {"name": "Тёмная", "bg_primary": "#1a1a1a", "bg_secondary": "#2a2a2a",
                "bg_button": "#333333", "bg_button_active": "#555555", "fg_primary": "#ffffff",
                "fg_secondary": "#888888", "fg_accent": "#4CAF50", "fg_break": "#2196F3",
                "fg_pause": "#FF9800", "btn_close_bg": "#ff4444", "btn_close_fg": "#ffffff",
                "font_time": ("Helvetica", 32, "bold"), "font_text": ("Arial", 10, "bold"),
                "font_button": ("Arial", 11)},
            "light": {"name": "Светлая", "bg_primary": "#f5f5f5", "bg_secondary": "#ffffff",
                "bg_button": "#e0e0e0", "bg_button_active": "#c0c0c0", "fg_primary": "#333333",
                "fg_secondary": "#666666", "fg_accent": "#2E7D32", "fg_break": "#1565C0",
                "fg_pause": "#EF6C00", "btn_close_bg": "#d32f2f", "btn_close_fg": "#ffffff",
                "font_time": ("Helvetica", 32, "bold"), "font_text": ("Arial", 10, "bold"),
                "font_button": ("Arial", 11)},
            "blue": {"name": "Синяя", "bg_primary": "#0d1b2a", "bg_secondary": "#1b263b",
                "bg_button": "#415a77", "bg_button_active": "#778da9", "fg_primary": "#e0e1dd",
                "fg_secondary": "#a0a0a0", "fg_accent": "#00b4d8", "fg_break": "#90e0ef",
                "fg_pause": "#ffb703", "btn_close_bg": "#e63946", "btn_close_fg": "#ffffff",
                "font_time": ("Segoe UI", 32, "bold"), "font_text": ("Segoe UI", 10, "bold"),
                "font_button": ("Segoe UI", 11)}
        }

    def setup_window(self):
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True, '-alpha', self.config['opacity'])
        self.root.geometry(f"{self.config['width']}x{self.config['height']}+{self.config['pos_x']}+{self.config['pos_y']}")
        self.root.configure(bg=self.theme['bg_primary'])
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    def setup_ui(self):
        top = tk.Frame(self.root, bg=self.theme['bg_primary'])
        top.pack(fill=tk.X, padx=5, pady=3)
        
        for txt, cmd, tip in [("⚙️", self.open_settings, "Настройки"), 
                               ("📊", self.open_stats, "Статистика")]:
            btn = tk.Button(top, text=txt, font=self.theme['font_button'],
                bg=self.theme['bg_button'], fg=self.theme['fg_primary'], bd=0,
                activebackground=self.theme['bg_button_active'], command=cmd, cursor="hand2", width=2)
            btn.pack(side=tk.LEFT, padx=2)
            self.tooltip(btn, tip)
        
        tk.Frame(top, bg=self.theme['bg_primary']).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        close = tk.Button(top, text="✕", font=("Arial", 12, "bold"),
            bg=self.theme['btn_close_bg'], fg=self.theme['btn_close_fg'], bd=0,
            activebackground='#ff6666', command=self.close_app, cursor="hand2", width=3)
        close.pack(side=tk.RIGHT)
        self.tooltip(close, "Закрыть")
        
        self.lbl_time = tk.Label(self.root, text="25:00", font=self.theme['font_time'],
            bg=self.theme['bg_primary'], fg=self.theme['fg_accent'])
        self.lbl_time.pack(expand=True)
        
        self.lbl_mode = tk.Label(self.root, text=self.config['work_text'],
            font=self.theme['font_text'], bg=self.theme['bg_primary'], fg=self.theme['fg_secondary'])
        self.lbl_mode.pack(pady=(0, 5))

    def setup_bindings(self):
        for widget in [self.root, self.lbl_time]:
            widget.bind("<ButtonPress-1>", lambda e: setattr(self, '_drag', (e.x_root - self.root.winfo_x(), e.y_root - self.root.winfo_y())))
            widget.bind("<B1-Motion>", lambda e: self.root.geometry(f'+{e.x_root - self._drag[0]}+{e.y_root - self._drag[1]}'))
        self.lbl_time.bind("<ButtonRelease-1>", lambda e: self.toggle())
        self.root.bind("<Button-3>", lambda e: self.reset())
        self.root.bind("<Double-Button-1>", lambda e: self.close_app())

    def tooltip(self, widget, text):
        def show(e):
            self.tip = Toplevel(self.root)
            self.tip.overrideredirect(True)
            self.tip.attributes('-topmost', True)
            tk.Label(self.tip, text=text, bg='#ffffcc', fg='#000000', font=("Arial", 9), padx=5, pady=2, relief=tk.SOLID, borderwidth=1).pack()
            self.tip.geometry(f"+{widget.winfo_rootx() + widget.winfo_width()//2 - 30}+{widget.winfo_rooty() - 25}")
        def hide(e): 
            if hasattr(self, 'tip'): self.tip.destroy()
        widget.bind("<Enter>", show)
        widget.bind("<Leave>", hide)

    def toggle(self):
        if self.running:
            self.running = False
            if self.job: self.root.after_cancel(self.job)
            self.lbl_time.config(fg=self.theme['fg_pause'])
        else:
            self.running = True
            if not self.start_time: self.start_time = datetime.now()
            self.countdown()
            self.lbl_time.config(fg=self.theme['fg_accent'] if self.work_mode else self.theme['fg_break'])

    def countdown(self):
        if self.running and self.time > 0:
            self.time -= 1
            self.update_display()
            self.job = self.root.after(1000, self.countdown)
        elif self.running:
            self.switch_mode()

    def switch_mode(self):
        self.save_session()
        if self.config['sound']: self.root.bell()
        self.work_mode = not self.work_mode
        self.time = (self.config['work_time'] if self.work_mode else self.config['break_time']) * 60
        self.max_time = self.time
        self.start_time = datetime.now()
        self.lbl_mode.config(text=self.config['work_text' if self.work_mode else 'break_text'])
        self.lbl_time.config(fg=self.theme['fg_accent' if self.work_mode else 'fg_break'])
        self.update_display()
        if self.config['auto_start']: self.countdown()

    def reset(self):
        self.save_session()
        self.running = False
        if self.job: self.root.after_cancel(self.job)
        self.work_mode = True
        self.time = self.config['work_time'] * 60
        self.max_time = self.time
        self.start_time = None
        self.lbl_time.config(fg=self.theme['fg_accent'])
        self.lbl_mode.config(text=self.config['work_text'])
        self.update_display()

    def update_display(self):
        self.lbl_time.config(text=f"{self.time//60:02d}:{self.time%60:02d}")

    def save_session(self):
        if self.start_time:
            dur = int((datetime.now() - self.start_time).total_seconds())
            if dur > 0:
                self.history.append({"date": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "type": "Work" if self.work_mode else "Break", "duration": dur})
                self.save_json(self.HISTORY_FILE, self.history)
        self.start_time = None

    def create_btn(self, parent, text, cmd, bg=None, fg=None, width=12):
        return tk.Button(parent, text=text, command=cmd, bg=bg or self.theme['bg_button'],
            fg=fg or self.theme['fg_primary'], bd=0, font=("Arial", 10), cursor="hand2", width=width)

    def open_settings(self):
        win = Toplevel(self.root)
        win.overrideredirect(True)
        win.attributes('-topmost', True)
        win.configure(bg=self.theme['bg_secondary'])
        x, y = self.root.winfo_x() + 50, self.root.winfo_y() + 50
        win.geometry(f"+{x}+{y}")
        
        f = tk.Frame(win, bg=self.theme['bg_secondary'])
        f.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        entries = {}
        for label, key, default in [
            ("Время работы (мин):", "work_time", self.config['work_time']),
            ("Время отдыха (мин):", "break_time", self.config['break_time']),
            ("Ширина:", "width", self.config['width']),
            ("Высота:", "height", self.config['height']),
            ("Текст работы:", "work_text", self.config['work_text']),
            ("Текст отдыха:", "break_text", self.config['break_text'])
        ]:
            tk.Label(f, text=label, bg=self.theme['bg_secondary'], fg=self.theme['fg_primary']).pack(pady=2)
            e = tk.Entry(f, font=("Arial", 12), width=15)
            e.insert(0, str(default))
            e.pack()
            entries[key] = e
        
        tk.Label(f, text="Тема:", bg=self.theme['bg_secondary'], fg=self.theme['fg_primary']).pack(pady=5)
        theme_names = [(k, v['name']) for k, v in self.themes.items()]
        theme_var = tk.StringVar(value=f"{self.themes[self.config['theme']]['name']} ({self.config['theme']})")
        ttk.Combobox(f, textvariable=theme_var, values=[f"{n} ({k})" for k, n in theme_names],
            state="readonly", font=("Arial", 11), width=25).pack(pady=5)
        
        for txt, var, val in [("Звук", tk.BooleanVar(value=self.config['sound']), 'sound'),
                               ("Автозапуск", tk.BooleanVar(value=self.config['auto_start']), 'auto_start')]:
            tk.Checkbutton(f, text=txt, variable=var, bg=self.theme['bg_secondary'],
                fg=self.theme['fg_primary'], selectcolor=self.theme['bg_button']).pack(pady=2)
            entries[val] = var
        
        status = tk.Label(f, text="", bg=self.theme['bg_secondary'], fg=self.theme['fg_accent'])
        status.pack(pady=5)
        
        def save():
            try:
                for k in ['work_time', 'break_time', 'width', 'height']:
                    self.config[k] = int(entries[k].get())
                for k in ['work_text', 'break_text']:
                    self.config[k] = entries[k].get().strip()
                self.config['sound'] = entries['sound'].get()
                self.config['auto_start'] = entries['auto_start'].get()
                
                sel = theme_var.get()
                for k, n in theme_names:
                    if f"{n} ({k})" == sel: self.config['theme'] = k
                
                self.save_json(self.CONFIG_FILE, self.config)
                self.time = self.config['work_time'] * 60
                self.max_time = self.time
                self.root.geometry(f"{self.config['width']}x{self.config['height']}+{self.root.winfo_x()}+{self.root.winfo_y()}")
                self.apply_theme(self.config['theme'])
                if not self.running:
                    self.lbl_mode.config(text=self.config['work_text'])
                    self.update_display()
                status.config(text="✓ Сохранено!")
                win.after(2000, lambda: status.config(text=""))
            except: status.config(text="✕ Ошибка!", fg='#ff4444')
        
        def reset():
            if messagebox.askyesno("Сброс", "Вернуть настройки?"):
                for k, v in self.DEFAULTS.items():
                    if k in entries:
                        if isinstance(v, bool): entries[k].set(v)
                        else: entries[k].delete(0, tk.END); entries[k].insert(0, str(v))
                theme_var.set(f"{self.themes['dark']['name']} (dark)")
                status.config(text="Сброшено", fg=self.theme['fg_pause'])
        
        bf = tk.Frame(f, bg=self.theme['bg_secondary'])
        bf.pack(pady=10)
        self.create_btn(bf, "Сохранить", save, self.theme['fg_accent']).pack(side=tk.LEFT, padx=5)
        self.create_btn(bf, "Сброс", reset, self.theme['fg_pause']).pack(side=tk.LEFT, padx=5)
        
        tk.Button(win, text="✕", command=win.destroy, bg=self.theme['btn_close_bg'],
            fg='#ffffff', bd=0, font=("Arial", 8), cursor="hand2").place(x=375, y=2)
        
        win.update_idletasks()
        win.geometry(f"400x{f.winfo_reqheight() + 80}+{x}+{y}")

    def open_stats(self):
        win = Toplevel(self.root)
        win.overrideredirect(True)
        win.attributes('-topmost', True)
        win.configure(bg=self.theme['bg_secondary'])
        win.geometry(f"+{self.root.winfo_x() + 50}+{self.root.winfo_y() + 50}")
        
        tk.Label(win, text="📊 Статистика", bg=self.theme['bg_secondary'],
            fg=self.theme['fg_primary'], font=("Arial", 14, "bold")).pack(pady=10)
        
        tf = tk.Frame(win, bg=self.theme['bg_secondary'])
        tf.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        txt = tk.Text(tf, bg=self.theme['bg_primary'], fg=self.theme['fg_primary'],
            font=("Consolas", 10), wrap=tk.WORD, relief=tk.FLAT, padx=10, pady=10)
        sb = ttk.Scrollbar(tf, orient="vertical", command=txt.yview)
        txt.configure(yscrollcommand=sb.set)
        txt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        
        work = sum(s['duration'] for s in self.history if s['type'] == 'Work')
        rest = sum(s['duration'] for s in self.history if s['type'] == 'Break')
        
        out = f"{'='*40}\n ВСЕГО: {len(self.history)} сессий\n"
        out += f"Работа: {work//60} мин | Отдых: {rest//60} мин\n{'='*40}\n ПОСЛЕДНИЕ 10:\n{'='*40}\n"
        for i, s in enumerate(self.history[-10:][::-1], 1):
            out += f"{i}. {s['date'][:16]} | {s['type']:5} | {s['duration']//60} мин\n"
        
        txt.insert("1.0", out)
        txt.config(state=tk.DISABLED)
        
        bf = tk.Frame(win, bg=self.theme['bg_secondary'])
        bf.pack(pady=10, side=tk.BOTTOM, fill=tk.X)
        
        def clear():
            if messagebox.askyesno("Очистить", "Удалить историю?"):
                self.history = []
                self.save_json(self.HISTORY_FILE, [])
                win.destroy()
                self.open_stats()
        
        self.create_btn(bf, "Очистить", clear, self.theme['btn_close_bg']).pack(side=tk.LEFT, padx=5)
        self.create_btn(bf, "Закрыть", win.destroy, self.theme['bg_button']).pack(side=tk.LEFT, padx=5)
        tk.Button(win, text="✕", command=win.destroy, bg=self.theme['btn_close_bg'],
            fg='#ffffff', bd=0, font=("Arial", 8), cursor="hand2").place(x=375, y=2)
        win.geometry("400x400")
        
        def wheel(e):
            try: txt.yview_scroll(int(-e.delta/120), "units")
            except: pass
        txt.bind_all("<MouseWheel>", wheel)
        win.protocol("WM_DELETE_WINDOW", lambda: (txt.unbind_all("<MouseWheel>"), win.destroy()))

    def apply_theme(self, key):
        if key not in self.themes: return
        self.theme = self.themes[key]
        self.root.configure(bg=self.theme['bg_primary'])
        self.lbl_time.configure(font=self.theme['font_time'], bg=self.theme['bg_primary'],
            fg=self.theme['fg_accent' if self.work_mode else 'fg_break'])
        self.lbl_mode.configure(font=self.theme['font_text'], bg=self.theme['bg_primary'],
            fg=self.theme['fg_secondary'])

    def close_app(self):
        self.save_session()
        self.config['pos_x'], self.config['pos_y'] = self.root.winfo_x(), self.root.winfo_y()
        self.config['width'], self.config['height'] = self.root.winfo_width(), self.root.winfo_height()
        self.save_json(self.CONFIG_FILE, self.config)
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    Pomodoro().run()