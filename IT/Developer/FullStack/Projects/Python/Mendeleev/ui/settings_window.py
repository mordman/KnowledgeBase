"""Окно настроек приложения."""

import tkinter as tk
from tkinter import ttk, messagebox
from utils.helpers import get_font_tuple, save_json_file
from config.settings_manager import apply_template, is_system_template, delete_template, save_custom_template, SETTINGS_FILE

class SettingsWindow(tk.Toplevel):
    """Окно настроек с поддержкой шаблонов."""
    
    def __init__(self, parent, settings, save_callback):
        super().__init__(parent)
        self.title("Настройки приложения")
        self.geometry("650x550")
        self.resizable(True, True)
        
        self.settings = settings
        self.save_callback = save_callback
        self.color_editors = {}
        self.font_editors = {}
        
        self.colors = settings.get('colors', {})
        self.fonts = settings.get('fonts', {})
        self.templates = settings.get('templates', {})
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Создаёт виджеты окна."""
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        self._create_templates_tab(notebook)
        self._create_size_tab(notebook)
        self._create_fonts_tab(notebook)
        self._create_colors_tab(notebook)
        self._create_categories_tab(notebook)
        
        # Кнопки
        btn_frame = tk.Frame(self, bg=self.colors.get("window_background", "#F0F0F0"))
        btn_frame.pack(pady=10)
        
        btn_font = get_font_tuple(self.fonts.get('button_text'))
        
        tk.Button(
            btn_frame,
            text="💾 Сохранить",
            command=self._on_save,
            font=btn_font,
            bg=self.colors.get("button_background", "#4ECDC4"),
            fg=self.colors.get("button_foreground", "#FFFFFF"),
            padx=20,
            pady=5
        ).pack(side="left", padx=5)
        
        tk.Button(
            btn_frame,
            text="❌ Отмена",
            command=self.destroy,
            font=btn_font,
            padx=20,
            pady=5
        ).pack(side="left", padx=5)
    
    def _create_templates_tab(self, notebook):
        """Вкладка шаблонов."""
        frame = tk.Frame(notebook, bg=self.colors.get("window_background", "#F0F0F0"))
        notebook.add(frame, text="📋 Шаблоны")
        
        tk.Label(
            frame,
            text="Выберите готовый шаблон настроек",
            font=("Arial", 12, "bold"),
            bg=self.colors.get("window_background", "#F0F0F0"),
            fg=self.colors.get("text_foreground", "#000000")
        ).pack(pady=10)
        
        # Список шаблонов
        list_frame = tk.Frame(frame, bg=self.colors.get("window_background", "#F0F0F0"))
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        canvas = tk.Canvas(list_frame, bg=self.colors.get("window_background", "#F0F0F0"))
        canvas.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        inner_frame = tk.Frame(canvas, bg=self.colors.get("window_background", "#F0F0F0"))
        canvas_window = canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        inner_frame.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", on_canvas_configure)
        
        current = self.settings.get('current_template', 'standard')
        
        for key, data in self.templates.items():
            bg = self.colors.get("row_even", "#FFFFFF") if key == current else self.colors.get("row_odd", "#E8F4F8")
            border = "#4ECDC4" if key == current else self.colors.get("border_color", "#DDDDDD")
            
            tpl_frame = tk.Frame(inner_frame, bg=bg, highlightthickness=2, highlightbackground=border)
            tpl_frame.pack(fill="x", padx=10, pady=5)
            
            tk.Label(
                tpl_frame,
                text=f"📌 {data.get('name', key)}",
                font=("Arial", 12, "bold"),
                bg=bg,
                fg=self.colors.get("text_foreground", "#000000"),
                anchor="w"
            ).pack(fill="x", padx=10, pady=(10, 5))
            
            tk.Label(
                tpl_frame,
                text=data.get('description', ''),
                font=("Arial", 10),
                bg=bg,
                fg=self.colors.get("text_foreground", "#000000"),
                anchor="w",
                wraplength=500
            ).pack(fill="x", padx=10, pady=(0, 10))
            
            btn_frame = tk.Frame(tpl_frame, bg=bg)
            btn_frame.pack(fill="x", padx=10, pady=10)
            
            tk.Button(
                btn_frame,
                text="✅ Применить",
                command=lambda k=key: self._apply_template(k),
                font=("Arial", 10),
                bg="#4ECDC4",
                fg="#FFFFFF",
                padx=15,
                pady=3
            ).pack(side="left", padx=5)
            
            tk.Button(
                btn_frame,
                text="👁️ Предпросмотр",
                command=lambda k=key: self._preview_template(k),
                font=("Arial", 10),
                bg="#9D8DF1",
                fg="#FFFFFF",
                padx=15,
                pady=3
            ).pack(side="left", padx=5)
            
            if not is_system_template(key):
                tk.Button(
                    btn_frame,
                    text="🗑️ Удалить",
                    command=lambda k=key: self._delete_template(k),
                    font=("Arial", 10),
                    bg="#FF6B6B",
                    fg="#FFFFFF",
                    padx=15,
                    pady=3
                ).pack(side="left", padx=5)
        
        # Управление
        ctrl_frame = tk.Frame(frame, bg=self.colors.get("window_background", "#F0F0F0"))
        ctrl_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Button(
            ctrl_frame,
            text="💾 Сохранить текущие как шаблон",
            command=self._save_current_as_template,
            font=("Arial", 10),
            bg="#4ECDC4",
            fg="#FFFFFF",
            padx=15,
            pady=5
        ).pack(side="left", padx=5)
        
        tk.Button(
            ctrl_frame,
            text="🔄 Сбросить к стандарту",
            command=lambda: self._apply_template('standard'),
            font=("Arial", 10),
            bg="#FF9F1C",
            fg="#FFFFFF",
            padx=15,
            pady=5
        ).pack(side="left", padx=5)
    
    def _create_size_tab(self, notebook):
        """Вкладка размеров."""
        frame = tk.Frame(notebook, bg=self.colors.get("window_background", "#F0F0F0"))
        notebook.add(frame, text="📏 Размеры")
        
        label_font = get_font_tuple(self.fonts.get('settings_label'))
        
        params = [
            ("Размер ячейки (ширина):", "cell_width", 40, 150, self.settings.get('cell_width', 65)),
            ("Размер ячейки (высота):", "cell_height", 40, 150, self.settings.get('cell_height', 75)),
            ("Ширина окна:", "window_width", 800, 2000, self.settings.get('window_width', 1200)),
            ("Высота окна:", "window_height", 600, 1500, self.settings.get('window_height', 850))
        ]
        
        self.size_vars = {}
        for text, key, from_, to, value in params:
            tk.Label(frame, text=text, font=label_font, bg=frame.cget("bg")).pack(pady=5)
            var = tk.IntVar(value=value)
            self.size_vars[key] = var
            tk.Spinbox(frame, from_=from_, to=to, textvariable=var, width=10).pack(pady=5)
    
    def _create_fonts_tab(self, notebook):
        """Вкладка шрифтов."""
        frame = tk.Frame(notebook, bg=self.colors.get("window_background", "#F0F0F0"))
        notebook.add(frame, text="🔤 Шрифты")
        
        canvas = tk.Canvas(frame, bg=frame.cget("bg"))
        canvas.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        inner = tk.Frame(canvas, bg=frame.cget("bg"))
        canvas_window = canvas.create_window((0, 0), window=inner, anchor="nw")
        
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        inner.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", on_canvas_configure)
        
        label_font = get_font_tuple(self.fonts.get('settings_label'))
        font_families = ["Arial", "Times New Roman", "Courier New", "Verdana", "Tahoma", "Georgia"]
        
        for font_name, font_data in self.fonts.items():
            row = tk.Frame(inner, bg=frame.cget("bg"))
            row.pack(fill="x", padx=10, pady=5)
            
            tk.Label(row, text=f"{font_name}:", font=label_font, bg=row.cget("bg"), width=25, anchor="w").pack(side="left", padx=5)
            
            family_var = tk.StringVar(value=font_data.get("family", "Arial"))
            ttk.Combobox(row, textvariable=family_var, width=12, values=font_families).pack(side="left", padx=5)
            
            size_var = tk.IntVar(value=font_data.get("size", 11))
            tk.Spinbox(row, from_=6, to=72, textvariable=size_var, width=5).pack(side="left", padx=5)
            
            weight_var = tk.StringVar(value=font_data.get("weight", "normal"))
            ttk.Combobox(row, textvariable=weight_var, width=8, values=["normal", "bold"]).pack(side="left", padx=5)
            
            self.font_editors[font_name] = {"family": family_var, "size": size_var, "weight": weight_var}
    
    def _create_colors_tab(self, notebook):
        """Вкладка цветов интерфейса."""
        frame = tk.Frame(notebook, bg=self.colors.get("window_background", "#F0F0F0"))
        notebook.add(frame, text="🎨 Цвета интерфейса")
        
        self._create_color_editor(frame, self.colors, "interface_")
    
    def _create_categories_tab(self, notebook):
        """Вкладка цветов категорий."""
        frame = tk.Frame(notebook, bg=self.colors.get("window_background", "#F0F0F0"))
        notebook.add(frame, text="🏷️ Цвета категорий")
        
        self._create_color_editor(frame, self.settings.get('category_colors', {}), "")
    
    def _create_color_editor(self, parent, colors_dict, prefix):
        """Создаёт редактор цветов."""
        canvas = tk.Canvas(parent, bg=parent.cget("bg"))
        canvas.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        inner = tk.Frame(canvas, bg=parent.cget("bg"))
        canvas_window = canvas.create_window((0, 0), window=inner, anchor="nw")
        
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        inner.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", on_canvas_configure)
        
        label_font = get_font_tuple(self.fonts.get('settings_label'))
        
        for name, value in colors_dict.items():
            row = tk.Frame(inner, bg=parent.cget("bg"))
            row.pack(fill="x", padx=10, pady=5)
            
            tk.Label(row, text=f"{name}:", font=label_font, bg=row.cget("bg"), width=25, anchor="w").pack(side="left", padx=5)
            
            var = tk.StringVar(value=value)
            key = f"{prefix}{name}"
            self.color_editors[key] = var
            
            tk.Entry(row, textvariable=var, width=15).pack(side="left", padx=5)
            
            preview = tk.Canvas(row, width=30, height=20, bg=value, highlightthickness=1, highlightbackground="#333")
            preview.pack(side="left", padx=5)
            
            var.trace_add("write", lambda *args, cv=preview, v=var: self._update_preview(cv, v))
    
    def _update_preview(self, canvas, var):
        """Обновляет предпросмотр цвета."""
        try:
            canvas.configure(bg=var.get())
        except:
            pass
    
    def _apply_template(self, key):
        """Применяет шаблон."""
        if apply_template(self.settings, key):
            save_json_file(SETTINGS_FILE, self.settings)
            messagebox.showinfo("Шаблон применён", f"Шаблон '{self.templates[key].get('name', key)}' применён!")
            self.destroy()
            self.save_callback()
        else:
            messagebox.showerror("Ошибка", f"Шаблон '{key}' не найден!")
    
    def _preview_template(self, key):
        """Предпросмотр шаблона."""
        tpl = self.templates.get(key, {})
        info = f"Шаблон: {tpl.get('name', key)}\n\n{tpl.get('description', '')}\n\n"
        
        if 'fonts' in tpl:
            info += "📝 Шрифты:\n"
            for name, data in list(tpl['fonts'].items())[:3]:
                info += f"  • {name}: {data.get('family')} {data.get('size')}pt\n"
        
        messagebox.showinfo(f"Предпросмотр: {tpl.get('name', key)}", info)
    
    def _delete_template(self, key):
        """Удаляет шаблон."""
        if is_system_template(key):
            messagebox.showwarning("Нельзя удалить", "Системные шаблоны нельзя удалить!")
            return
        
        if messagebox.askyesno("Удаление", f"Удалить шаблон '{key}'?"):
            if delete_template(self.settings, key):
                save_json_file(SETTINGS_FILE, self.settings)
                messagebox.showinfo("Удалено", "Шаблон удалён!")
                self.destroy()
                self.save_callback()
    
    def _save_current_as_template(self):
        """Сохраняет текущие настройки как шаблон."""
        dialog = tk.Toplevel(self)
        dialog.title("Сохранить как шаблон")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        
        tk.Label(dialog, text="Название:").pack(pady=10)
        name_var = tk.StringVar()
        tk.Entry(dialog, textvariable=name_var, width=40).pack(pady=5)
        
        tk.Label(dialog, text="Описание:").pack(pady=10)
        desc_var = tk.StringVar()
        tk.Entry(dialog, textvariable=desc_var, width=40).pack(pady=5)
        
        def on_save():
            name = name_var.get().strip()
            if not name:
                messagebox.showerror("Ошибка", "Введите название!")
                return
            
            key = name.lower().replace(' ', '_')
            if save_custom_template(self.settings, key, name, desc_var.get().strip()):
                save_json_file(SETTINGS_FILE, self.settings)
                messagebox.showinfo("Сохранено", f"Шаблон '{name}' сохранён!")
                dialog.destroy()
                self.destroy()
                self.save_callback()
        
        tk.Button(dialog, text="Сохранить", command=on_save, bg="#4ECDC4", fg="white").pack(pady=10)
        tk.Button(dialog, text="Отмена", command=dialog.destroy).pack()
    
    def _on_save(self):
        """Сохраняет настройки."""
        for key, var in self.size_vars.items():
            self.settings[key] = var.get()
        
        for font_name, editors in self.font_editors.items():
            self.settings['fonts'][font_name] = {
                "family": editors["family"].get(),
                "size": editors["size"].get(),
                "weight": editors["weight"].get()
            }
        
        for key, var in self.color_editors.items():
            if key.startswith("interface_"):
                self.settings['colors'][key.replace("interface_", "")] = var.get()
            else:
                self.settings['category_colors'][key] = var.get()
        
        if save_json_file(SETTINGS_FILE, self.settings):
            messagebox.showinfo("Настройки", "Настройки сохранены!")
            self.save_callback()
            self.destroy()
        else:
            messagebox.showerror("Ошибка", "Не удалось сохранить!")