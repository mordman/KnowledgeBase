"""Точка входа в приложение."""

import tkinter as tk
from viewer import JSONXMLViewer


def main():
    root = tk.Tk()
    app = JSONXMLViewer(root)
    root.mainloop()


if __name__ == "__main__":
    main()