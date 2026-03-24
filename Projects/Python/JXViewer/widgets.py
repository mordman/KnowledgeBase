"""Кастомные виджеты для приложения."""

import tkinter as tk
from tkinter import ttk
from config import CONFIG


class TaggedTreeview(ttk.Treeview):
    """Treeview с автоматической настройкой цветовых тегов."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setup_tags()

    def _setup_tags(self):
        colors = CONFIG["colors"]
        self.tag_configure("string", foreground=colors["string"])
        self.tag_configure("number", foreground=colors["number"])
        self.tag_configure("boolean", foreground=colors["boolean"])
        self.tag_configure("null", foreground=colors["null"])
        self.tag_configure("key", foreground=colors["key"])
        self.tag_configure("xml_attr", foreground=colors["xml_attr"])
        self.tag_configure("highlight", background=colors["highlight"])


class ClosableNotebook(ttk.Notebook):
    """Notebook с поддержкой контекстного меню для вкладок."""

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Закрыть вкладку")
        self.context_menu.add_command(label="Закрыть все")
        self.bind("<ButtonPress-3>", self._on_right_click)

    def _on_right_click(self, event):
        index = self.index(f"@{event.x},{event.y}")
        if index >= 0:
            self.select(index)
            self.context_menu.post(event.x_root, event.y_root)