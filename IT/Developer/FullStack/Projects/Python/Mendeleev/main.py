#!/usr/bin/env python3
"""Точка входа приложения."""

import tkinter as tk
from config.settings_manager import load_settings
from ui.main_window import MainWindow

def main():
    """Запускает приложение."""
    root = tk.Tk()
    settings = load_settings()
    app = MainWindow(root, settings)
    root.mainloop()

if __name__ == "__main__":
    main()