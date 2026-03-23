# board.py

from settings import EMPTY, WHITE_PIECE, BLACK_PIECE, WHITE_KING, BLACK_KING
from config import config

class Board:
    def __init__(self):
        self.reset()

    def reset(self):
        """Сброс доски к начальному состоянию"""
        self.board_size = config.board_size
        self.piece_rows = config.piece_rows
        self.board = [[EMPTY] * self.board_size for _ in range(self.board_size)]
        self.turn = WHITE_PIECE
        self.setup_pieces()

    def setup_pieces(self):
        """Расстановка шашек с учётом количества рядов"""
        for row in range(self.board_size):
            for col in range(self.board_size):
                if (row + col) % 2 == 1:
                    # Чёрные шашки (сверху)
                    if row < self.piece_rows:
                        self.board[row][col] = BLACK_PIECE
                    # Белые шашки (снизу)
                    elif row >= self.board_size - self.piece_rows:
                        self.board[row][col] = WHITE_PIECE

    def get_piece(self, row, col):
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            return self.board[row][col]
        return EMPTY

    def set_piece(self, row, col, piece):
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            self.board[row][col] = piece

    def get_piece_color(self, piece):
        if piece in [WHITE_PIECE, WHITE_KING]:
            return WHITE_PIECE
        if piece in [BLACK_PIECE, BLACK_KING]:
            return BLACK_PIECE
        return EMPTY

    def is_king(self, piece):
        return piece in [WHITE_KING, BLACK_KING]

    def get_valid_moves(self, row, col, must_capture=False):
        piece = self.get_piece(row, col)
        if piece == EMPTY:
            return []

        captures = self.get_capture_moves(row, col)
        if must_capture or self.has_forced_capture():
            return captures if captures else []

        if captures:
            return captures

        return self.get_normal_moves(row, col)

    def get_normal_moves(self, row, col):
        """Обычные ходы без взятия"""
        piece = self.get_piece(row, col)
        is_king = self.is_king(piece)
        moves = []

        directions = []
        if piece in [WHITE_PIECE, WHITE_KING]:
            directions.append(-1)
        if piece in [BLACK_PIECE, BLACK_KING] or is_king:
            directions.append(1)

        for d_row in directions:
            for d_col in [-1, 1]:
                if is_king:
                    # Дамка ходит на любое расстояние по диагонали
                    for step in range(1, self.board_size):
                        new_r = row + d_row * step
                        new_c = col + d_col * step
                        if not self._is_on_board(new_r, new_c):
                            break
                        if self.get_piece(new_r, new_c) != EMPTY:
                            break
                        moves.append((new_r, new_c))
                else:
                    # Обычная шашка ходит на 1 клетку
                    new_r, new_c = row + d_row, col + d_col
                    if self._is_on_board(new_r, new_c) and self.get_piece(new_r, new_c) == EMPTY:
                        if piece == WHITE_PIECE and d_row == 1:
                            continue
                        if piece == BLACK_PIECE and d_row == -1:
                            continue
                        moves.append((new_r, new_c))
        return moves

    def get_capture_moves(self, row, col):
        """Возвращает все возможные взятия (для шашек и дамок)"""
        piece = self.get_piece(row, col)
        is_king = self.is_king(piece)
        captures = []

        if is_king:
            # Дамка может рубить на любом расстоянии
            captures.extend(self._get_king_captures(row, col))
        else:
            # Обычная шашка рубит только на 1 клетку (но может назад)
            captures.extend(self._get_piece_captures(row, col))

        return captures

    def _get_piece_captures(self, row, col):
        """Взятие обычной шашкой (на 1 клетку в любую сторону)"""
        piece = self.get_piece(row, col)
        captures = []

        for d_row in [-1, 1]:
            for d_col in [-1, 1]:
                mid_r, mid_c = row + d_row, col + d_col
                jump_r, jump_c = row + d_row * 2, col + d_col * 2

                if self._is_on_board(jump_r, jump_c) and self.get_piece(jump_r, jump_c) == EMPTY:
                    mid_piece = self.get_piece(mid_r, mid_c)
                    if mid_piece != EMPTY and self.get_piece_color(mid_piece) != self.get_piece_color(piece):
                        captures.append((jump_r, jump_c))
        return captures

    def _get_king_captures(self, row, col):
        """Взятие дамкой (на любом расстоянии по диагонали)"""
        piece = self.get_piece(row, col)
        captures = []

        for d_row in [-1, 1]:
            for d_col in [-1, 1]:
                # Ищем шашку противника в этом направлении
                enemy_pos = None
                for step in range(1, self.board_size):
                    check_r = row + d_row * step
                    check_c = col + d_col * step
                    
                    if not self._is_on_board(check_r, check_c):
                        break
                    
                    check_piece = self.get_piece(check_r, check_c)
                    
                    if check_piece != EMPTY:
                        # Нашли шашку
                        if self.get_piece_color(check_piece) != self.get_piece_color(piece):
                            enemy_pos = (check_r, check_c, step)
                        break  # Любая шашка блокирует дальнейший поиск
                
                if enemy_pos:
                    enemy_r, enemy_c, enemy_step = enemy_pos
                    # Проверяем клетки за шашкой противника
                    for land_step in range(enemy_step + 1, self.board_size):
                        land_r = row + d_row * land_step
                        land_c = col + d_col * land_step
                        
                        if not self._is_on_board(land_r, land_c):
                            break
                        
                        if self.get_piece(land_r, land_c) != EMPTY:
                            break  # Дальше нельзя
                        
                        # Можно приземлиться на эту клетку
                        captures.append((land_r, land_c, enemy_r, enemy_c))

        return captures

    def has_forced_capture(self):
        """Проверка наличия обязательной рубки"""
        for row in range(self.board_size):
            for col in range(self.board_size):
                piece = self.get_piece(row, col)
                if self.get_piece_color(piece) == self.turn:
                    if self.get_capture_moves(row, col):
                        return True
        return False

    def can_piece_capture(self, row, col):
        return len(self.get_capture_moves(row, col)) > 0

    def make_move(self, start, end, captured_piece=None):
        """
        Выполнение хода
        captured_piece: (row, col) для дамок - координаты взятой шашки
        """
        r1, c1 = start
        r2, c2 = end
        piece = self.get_piece(r1, c1)
        is_capture = False
        captured_pos = None

        # Проверяем тип хода
        if len(end) == 4:  # Ход дамки со взятием (r2, c2, captured_r, captured_c)
            is_capture = True
            r2, c2, cap_r, cap_c = end
            captured_pos = (cap_r, cap_c)
        elif abs(r2 - r1) == 2:  # Ход шашки со взятием
            is_capture = True
            captured_pos = ((r1 + r2) // 2, (c1 + c2) // 2)

        self.set_piece(r2, c2, piece)
        self.set_piece(r1, c1, EMPTY)

        if is_capture and captured_pos:
            self.set_piece(captured_pos[0], captured_pos[1], EMPTY)

        # Превращение в дамку
        if piece == WHITE_PIECE and r2 == 0:
            self.set_piece(r2, c2, WHITE_KING)
        elif piece == BLACK_PIECE and r2 == self.board_size - 1:
            self.set_piece(r2, c2, BLACK_KING)

        # Проверка на продолжение серии взятий
        if is_capture:
            if self.is_king(piece) or (r2 == 0 and piece == WHITE_PIECE) or (r2 == self.board_size - 1 and piece == BLACK_PIECE):
                # Дамка или только что стала дамкой
                if self.get_capture_moves(r2, c2):
                    return True  # Продолжение серии
            elif self.get_capture_moves(r2, c2):
                return True  # Продолжение серии

        self.turn = BLACK_PIECE if self.turn == WHITE_PIECE else WHITE_PIECE
        return False

    def _is_on_board(self, row, col):
        return 0 <= row < self.board_size and 0 <= col < self.board_size

    def count_pieces(self, color):
        count = 0
        for row in range(self.board_size):
            for col in range(self.board_size):
                piece = self.get_piece(row, col)
                if self.get_piece_color(piece) == color:
                    count += 1
        return count

    def check_winner(self):
        white = self.count_pieces(WHITE_PIECE)
        black = self.count_pieces(BLACK_PIECE)
        if white == 0:
            return BLACK_PIECE
        if black == 0:
            return WHITE_PIECE
        return None

    def get_board_state(self):
        return [row[:] for row in self.board]

    def load_board_state(self, state):
        self.board = [row[:] for row in state]
        self.board_size = len(state)

    def get_piece_count(self):
        """Возвращает общее количество шашек на поле"""
        white = self.count_pieces(WHITE_PIECE)
        black = self.count_pieces(BLACK_PIECE)
        return white + black

    def get_piece_count_by_color(self):
        """Возвращает количество шашек по цветам"""
        return {
            'white': self.count_pieces(WHITE_PIECE),
            'black': self.count_pieces(BLACK_PIECE)
        }