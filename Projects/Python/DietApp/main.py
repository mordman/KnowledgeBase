#!/usr/bin/env python3
"""
Точка входа приложения "Оптимальная Диета"
Версия: 1.1
"""

import tkinter as tk
from tkinter import ttk
from gui.app import DietApp


def main():
    """Запуск приложения"""
    root = tk.Tk()
    
    # Настройки окна
    root.minsize(1000, 700)
    root.title("Оптимальная Диета v1.1")
    
    # Стилизация
    style = ttk.Style()
    style.theme_use('clam')  # или 'default', 'alt', 'vista', 'winnative'
    
    # Создание и запуск приложения
    app = DietApp(root)
    
    # Запуск главного цикла
    root.mainloop()


if __name__ == "__main__":
    main()