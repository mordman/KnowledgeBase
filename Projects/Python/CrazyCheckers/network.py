# network.py

import socket
import threading
import json
import queue
from settings import DEFAULT_PORT, BUFFER_SIZE, MSG_MOVE, MSG_NAME, MSG_CHAT, MSG_GAME_OVER

class NetworkManager:
    def __init__(self, ui_callback):
        self.ui_callback = ui_callback
        self.socket = None
        self.is_server = False
        self.connected = False
        self.player_name = "Игрок"
        self.opponent_name = "Соперник"
        self.message_queue = queue.Queue()
        self.running = False
        self.thread = None

    def start_server(self, port, name):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(('0.0.0.0', port))
            self.socket.listen(1)
            self.player_name = name
            self.is_server = True
            self.running = True

            self.ui_callback("log", f"Сервер запущен на порту {port}. Ожидание игрока...")

            self.thread = threading.Thread(target=self._accept_connection)
            self.thread.daemon = True
            self.thread.start()
            return True
        except Exception as e:
            self.ui_callback("log", f"Ошибка запуска сервера: {e}")
            return False

    def _accept_connection(self):
        try:
            conn, addr = self.socket.accept()
            self.socket = conn
            self.connected = True
            self.ui_callback("log", f"Игрок подключился: {addr}")
            self._send({"type": MSG_NAME, "name": self.player_name})

            self.thread = threading.Thread(target=self._receive_loop)
            self.thread.daemon = True
            self.thread.start()

            self.ui_callback("game_started", {"is_my_turn": True})
        except Exception as e:
            self.ui_callback("log", f"Ошибка подключения: {e}")

    def connect_client(self, host, port, name):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            self.player_name = name
            self.is_server = False
            self.connected = True
            self.running = True

            self.ui_callback("log", f"Подключено к {host}:{port}")

            self.thread = threading.Thread(target=self._receive_loop)
            self.thread.daemon = True
            self.thread.start()
            return True
        except Exception as e:
            self.ui_callback("log", f"Ошибка подключения: {e}")
            return False

    def _receive_loop(self):
        while self.running and self.connected:
            try:
                data = self.socket.recv(BUFFER_SIZE).decode('utf-8')
                if not data:
                    break
                message = json.loads(data)
                self.message_queue.put(message)
                self.ui_callback("process_message", message)
            except Exception as e:
                self.ui_callback("log", f"Ошибка связи: {e}")
                break
        self.disconnect()

    def _send(self, data):
        if self.socket and self.connected:
            try:
                self.socket.send(json.dumps(data).encode('utf-8'))
            except Exception as e:
                self.ui_callback("log", f"Ошибка отправки: {e}")
                self.disconnect()

    def send_move(self, start, end):
        self._send({"type": MSG_MOVE, "start": start, "end": end})

    def send_chat(self, text):
        self._send({"type": MSG_CHAT, "name": self.player_name, "text": text})

    def send_game_over(self, winner):
        self._send({"type": MSG_GAME_OVER, "winner": winner})

    def disconnect(self):
        self.running = False
        self.connected = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        self.socket = None
        self.ui_callback("log", "Соединение разорвано")
        self.ui_callback("game_ended", {})