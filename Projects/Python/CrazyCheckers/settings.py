# settings.py

# Сетевые настройки
DEFAULT_PORT = 5555
BUFFER_SIZE = 1024
HOST_DEFAULT = "127.0.0.1"

# Графические настройки по умолчанию
DEFAULT_BOARD_SIZE = 8
DEFAULT_CELL_SIZE = 80
DEFAULT_WINDOW_WIDTH = 800
DEFAULT_WINDOW_HEIGHT = 700
DEFAULT_PIECE_SCALE = 0.75
DEFAULT_PIECE_ROWS = 3  # Количество рядов шашек с каждой стороны

# Цвета по умолчанию
DEFAULT_COLOR_LIGHT = "#F0D9B5"
DEFAULT_COLOR_DARK = "#B58863"
DEFAULT_COLOR_PIECE_1 = "#FFFFFF"
DEFAULT_COLOR_PIECE_2 = "#333333"
DEFAULT_COLOR_HIGHLIGHT = "#7FFF00"
DEFAULT_COLOR_MULTI_JUMP = "#FFFF00"
DEFAULT_COLOR_SELECTION = "#FF0000"
DEFAULT_BOARD_BORDER = "#5C4033"

# Типы фигур (константы для импорта)
EMPTY = 0
WHITE_PIECE = 1
BLACK_PIECE = 2
WHITE_KING = 3
BLACK_KING = 4

# Типы сообщений сети
MSG_MOVE = "move"
MSG_NAME = "name"
MSG_CHAT = "chat"
MSG_GAME_OVER = "game_over"

# Путь к файлу конфигурации
CONFIG_FILE = "config.json"

# Заголовок окна
WINDOW_TITLE = "Сетевые Шашки"