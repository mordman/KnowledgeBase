# ui.py

import tkinter as tk
from tkinter import messagebox
from settings import (
    WINDOW_TITLE, EMPTY, WHITE_PIECE, BLACK_PIECE, WHITE_KING, BLACK_KING,
    MSG_MOVE, MSG_NAME, MSG_CHAT, MSG_GAME_OVER
)
from config import config
from board import Board
from network import NetworkManager
from dialogs import SettingsDialog, NetworkSettingsDialog

class CheckersUI:
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        
        self._apply_window_settings()
        
        self.board = Board()
        self.network = NetworkManager(self._network_callback)

        self.selected_piece = None
        self.valid_moves = []
        self.multi_jump_mode = False
        self.multi_jump_piece = None
        self.is_network_game = False
        self.is_my_turn = True

        self._create_menu()
        self._create_main_frame()
        self._create_chat()

        self._draw_board()
        self._enable_game(False)

    def _apply_window_settings(self):
        """Применение настроек окна"""
        self.root.geometry(f"{config.window_width}x{config.window_height}")
        self.root.minsize(700, 600)

    def _create_main_frame(self):
        """Создание основного фрейма с прокруткой"""
        # Главный контейнер
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas для прокрутки
        self.canvas = tk.Canvas(main_frame, bg='#f0f0f0')
        
        # Скроллбары
        h_scroll = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        v_scroll = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        
        # Настройка скроллинга
        self.canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
        
        # Размещение скроллбаров
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Фрейм внутри canvas для доски
        self.board_frame = tk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.board_frame, anchor='nw')
        
        # Доска внутри board_frame
        self.board_canvas = tk.Canvas(self.board_frame, 
                                      width=config.get_board_pixels(),
                                      height=config.get_board_pixels())
        self.board_canvas.pack(padx=10, pady=10)
        self.board_canvas.bind("<Button-1>", self._on_click)
        
        # Привязка изменения размера
        self.board_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Поддержка прокрутки колёсиком мыши
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _on_frame_configure(self, event):
        """Обновление области прокрутки при изменении размера фрейма"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        """Адаптация размера окна canvas при изменении размера окна"""
        # Можно добавить логику для центрирования доски
        pass

    def _on_mousewheel(self, event):
        """Прокрутка колёсиком мыши"""
        if event.num == 5 or event.delta == -120:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta == 120:
            self.canvas.yview_scroll(-1, "units")

    def _create_menu(self):
        menubar = tk.Menu(self.root)
        gamemenu = tk.Menu(menubar, tearoff=0)
        gamemenu.add_command(label="Сетевая игра", command=self._open_network_settings)
        gamemenu.add_command(label="Локальная игра", command=self._start_local_game)
        gamemenu.add_separator()
        gamemenu.add_command(label="Настройки", command=self._open_settings)
        gamemenu.add_command(label="Выход", command=self.root.quit)
        menubar.add_cascade(label="Игра", menu=gamemenu)
        
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="О игре", command=self._show_about)
        menubar.add_cascade(label="Помощь", menu=helpmenu)
        
        self.root.config(menu=menubar)

    def _open_settings(self):
        """Открытие диалога настроек"""
        def on_settings_saved(need_restart):
            if need_restart:
                if messagebox.askyesno("Перезапуск", "Для применения настроек нужно перезапустить игру. Перезапустить сейчас?"):
                    self.root.destroy()
                    import main
                    main.main()
        
        SettingsDialog(self.root, on_settings_saved)

    def _show_about(self):
        messagebox.showinfo("О игре", 
            "Сетевые Шашки на Python\n\n"
            "Версия: 2.0\n"
            "Поддержка:\n"
            "- Русские правила шашек\n"
            "- Сетевая игра по TCP/IP\n"
            "- Настройка цветов и размеров\n"
            "- Сохранение настроек\n"
            "- Прокрутка поля")

    def _create_chat(self):
        chat_frame = tk.Frame(self.root, height=100)
        chat_frame.pack(fill=tk.X, padx=10, pady=5)

        self.chat_log = tk.Text(chat_frame, height=4, state='disabled')
        self.chat_log.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.chat_entry = tk.Entry(chat_frame)
        self.chat_entry.pack(side=tk.LEFT, padx=5)
        self.chat_entry.bind("<Return>", self._send_chat)

        tk.Button(chat_frame, text="Send", command=self._send_chat).pack(side=tk.LEFT)
        
        # Индикатор количества шашек
        self.piece_count_label = tk.Label(chat_frame, text="")
        self.piece_count_label.pack(side=tk.RIGHT, padx=10)
        self._update_piece_count()

    def _update_piece_count(self):
        """Обновление индикатора количества шашек"""
        counts = self.board.get_piece_count_by_color()
        self.piece_count_label.config(
            text=f"⚪ {counts['white']} | ⚫ {counts['black']}",
            font=("Arial", 10, "bold")
        )

    def _open_network_settings(self):
        NetworkSettingsDialog(self.root, self._apply_network_settings)

    def _apply_network_settings(self, settings):
        name = settings["name"]
        mode = settings["mode"]
        port = settings["port"]

        if mode == "server":
            if self.network.start_server(port, name):
                self.is_network_game = True
                self.is_my_turn = True
        else:
            host = settings["host"]
            if self.network.connect_client(host, port, name):
                self.is_network_game = True
                self.is_my_turn = False

    def _start_local_game(self):
        self.is_network_game = False
        self.network.disconnect()
        self.board.reset()
        self._enable_game(True)
        self._draw_board()
        self._log_message("Локальная игра запущена")

    def _enable_game(self, enabled):
        state = tk.NORMAL if enabled else tk.DISABLED
        self.board_canvas.config(state=state)

    def _log_message(self, text):
        self.chat_log.config(state='normal')
        self.chat_log.insert(tk.END, f"[Система] {text}\n")
        self.chat_log.see(tk.END)
        self.chat_log.config(state='disabled')

    def _add_chat_message(self, name, text):
        self.chat_log.config(state='normal')
        self.chat_log.insert(tk.END, f"{name}: {text}\n")
        self.chat_log.see(tk.END)
        self.chat_log.config(state='disabled')

    def _send_chat(self, event=None):
        text = self.chat_entry.get()
        if text and self.network.connected:
            self.network.send_chat(text)
            self._add_chat_message(self.network.player_name, text)
            self.chat_entry.delete(0, tk.END)

    def _network_callback(self, event_type, data=None):
        if event_type == "log":
            self._log_message(data)
        elif event_type == "game_started":
            self._enable_game(True)
            self.is_my_turn = data.get("is_my_turn", True)
            self._log_message("Игра началась!")
        elif event_type == "game_ended":
            self._enable_game(False)
        elif event_type == "process_message":
            self._process_network_message(data)

    def _process_network_message(self, msg):
        msg_type = msg.get("type")
        if msg_type == "name":
            self.network.opponent_name = msg.get("name")
            self._log_message(f"Соперник: {self.network.opponent_name}")
            if not self.network.is_server:
                self._enable_game(True)
                self.is_my_turn = False
                self._log_message("Игра началась! Ваш ход (Черные).")
        elif msg_type == "move":
            start = tuple(msg["start"])
            end_data = msg["end"]
            if len(end_data) == 4:
                end = (end_data[0], end_data[1], end_data[2], end_data[3])
            else:
                end = tuple(end_data)
            self.board.make_move(start, end)
            self._draw_board()
            self.is_my_turn = True
        elif msg_type == "chat":
            self._add_chat_message(msg["name"], msg["text"])
        elif msg_type == "game_over":
            messagebox.showinfo("Игра окончена", msg["winner"])
            self._enable_game(False)

    def _draw_board(self):
        self.board_canvas.delete("all")
        board_pixels = config.get_board_pixels()
        
        # Обновление размера canvas доски
        self.board_canvas.config(width=board_pixels, height=board_pixels)
        
        # Рамка доски
        self.board_canvas.create_rectangle(0, 0, board_pixels, board_pixels, 
                                     outline=config.color_board_border, width=3)
        
        # Клетки
        for row in range(self.board.board_size):
            for col in range(self.board.board_size):
                x1 = col * config.cell_size
                y1 = row * config.cell_size
                x2 = x1 + config.cell_size
                y2 = y1 + config.cell_size
                color = config.color_light if (row + col) % 2 == 0 else config.color_dark
                self.board_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        # Подсветка ходов
        for move in self.valid_moves:
            if len(move) == 4:  # Ход дамки со взятием
                r, c = move[0], move[1]
            else:
                r, c = move[0], move[1]
            
            x1 = c * config.cell_size + 10
            y1 = r * config.cell_size + 10
            x2 = x1 + config.cell_size - 20
            y2 = y1 + config.cell_size - 20
            self.board_canvas.create_oval(x1, y1, x2, y2, fill=config.color_highlight, outline="", stipple="gray50")

        # Выделение шашки
        if self.selected_piece:
            r, c = self.selected_piece
            x1 = c * config.cell_size
            y1 = r * config.cell_size
            x2 = x1 + config.cell_size
            y2 = y1 + config.cell_size
            color = config.color_multi_jump if self.multi_jump_mode else config.color_selection
            width = 5 if self.multi_jump_mode else 3
            self.board_canvas.create_rectangle(x1, y1, x2, y2, outline=color, width=width)

        # Шашки
        for row in range(self.board.board_size):
            for col in range(self.board.board_size):
                piece = self.board.get_piece(row, col)
                if piece != EMPTY:
                    self._draw_piece(row, col, piece)
        
        # Обновление области прокрутки
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self._update_piece_count()

    def _draw_piece(self, row, col, piece):
        x_center = col * config.cell_size + config.cell_size // 2
        y_center = row * config.cell_size + config.cell_size // 2
        radius = config.get_piece_radius()
        color = config.color_piece_1 if piece in [WHITE_PIECE, WHITE_KING] else config.color_piece_2
        self.board_canvas.create_oval(x_center - radius, y_center - radius,
                                x_center + radius, y_center + radius,
                                fill=color, outline="black", width=2)
        if piece in [WHITE_KING, BLACK_KING]:
            self.board_canvas.create_oval(x_center - radius//2, y_center - radius//2,
                                    x_center + radius//2, y_center + radius//2,
                                    outline="gold", width=3)

    def _on_click(self, event):
        if self.is_network_game and not self.is_my_turn:
            return

        col = event.x // config.cell_size
        row = event.y // config.cell_size
        if not (0 <= row < self.board.board_size and 0 <= col < self.board.board_size):
            return

        clicked_piece = self.board.get_piece(row, col)
        is_my_piece = self.board.get_piece_color(clicked_piece) == self.board.turn

        if self.multi_jump_mode:
            if (row, col) == self.multi_jump_piece:
                self.selected_piece = (row, col)
                self.valid_moves = self.board.get_capture_moves(row, col)
                self._draw_board()
            elif (row, col) in self.valid_moves:
                self._execute_move(self.selected_piece, (row, col))
            return

        if is_my_piece:
            if self.board.has_forced_capture():
                if self.board.can_piece_capture(row, col):
                    self.selected_piece = (row, col)
                    self.valid_moves = self.board.get_valid_moves(row, col, must_capture=True)
                    self._draw_board()
                else:
                    messagebox.showwarning("Внимание", "Есть обязательная рубка другой шашкой!")
            else:
                self.selected_piece = (row, col)
                self.valid_moves = self.board.get_valid_moves(row, col)
                self._draw_board()
            return

        if clicked_piece == EMPTY and self.selected_piece:
            if (row, col) in self.valid_moves:
                # Проверяем, есть ли в valid_moves ходы дамки со взятием
                move_data = None
                for move in self.valid_moves:
                    if len(move) == 4 and move[0] == row and move[1] == col:
                        move_data = move
                        break
                
                if move_data:
                    self._execute_move(self.selected_piece, move_data)
                else:
                    self._execute_move(self.selected_piece, (row, col))

    def _execute_move(self, start, end):
        piece = self.board.get_piece(start[0], start[1])
        is_king = self.board.is_king(piece)
        
        if is_king and len(end) == 4:
            continue_series = self.board.make_move(start, end)
        else:
            continue_series = self.board.make_move(start, end)

        if self.is_network_game:
            self.network.send_move(start, end)

        if continue_series:
            self.multi_jump_mode = True
            self.multi_jump_piece = (end[0], end[1]) if len(end) >= 2 else end
            self.selected_piece = self.multi_jump_piece
            self.valid_moves = self.board.get_capture_moves(self.multi_jump_piece[0], self.multi_jump_piece[1])
            self._draw_board()
            return

        self._end_turn()

    def _end_turn(self):
        self.multi_jump_mode = False
        self.multi_jump_piece = None
        self.selected_piece = None
        self.valid_moves = []
        self.is_my_turn = not self.is_my_turn
        self._draw_board()
        self._check_win()

    def _check_win(self):
        winner = self.board.check_winner()
        if winner:
            msg = "Белые победили!" if winner == WHITE_PIECE else "Черные победили!"
            if self.is_network_game:
                self.network.send_game_over(msg)
            messagebox.showinfo("Игра окончена", msg)
            self._enable_game(False)