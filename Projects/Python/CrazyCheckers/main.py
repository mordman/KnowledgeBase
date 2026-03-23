# main.py

import tkinter as tk
from ui import CheckersUI

def main():
    root = tk.Tk()
    app = CheckersUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()