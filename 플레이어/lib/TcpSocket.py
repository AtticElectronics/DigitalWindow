import socket
import threading

class TCPServer:
    def __init__(self, host, port, max_clients, callback):
        self.host = host
        self.port = port
        self.max_clients = max_clients
        self.callback = callback
        self.clients = []
        self.running = True  # 서버 실행 상태
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.max_clients)
        self.accept_thread = threading.Thread(target=self.accept_clients)
        self.accept_thread.start()

    def accept_clients(self):
        while self.running:
            try:
                client, address = self.server_socket.accept()
                print(f"Connected with {address}")
                client_thread = threading.Thread(target=self.handle_client, args=(client,))
                client_thread.start()
            except Exception as e:
                print(f"Accepting clients error: {e}")

    def handle_client(self, client):
        while self.running:
            try:
                data = client.recv(1024)
                if data:
                    print(data)
                    self.callback(data.decode('utf-8'))
                else:
                    break
            except Exception as e:
                print(f"Error handling client data: {e}")
                break
        client.close()

    def stop(self):
        self.running = False
        self.server_socket.close()


import socket
import threading
import time

class TCPClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None
        self.connecting = False
        self.send_lock = threading.Lock()
        self.reconnect_thread = None

    def ensure_connection(self):
        while not self.connecting:
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((self.host, self.port))
                print("Connected to the server.")
                self.connecting = True
            except socket.error:
                print("Connection failed, retrying...")
                time.sleep(5)  # 재시도 간격

    def connect(self):
        if not self.reconnect_thread or not self.reconnect_thread.is_alive():
            self.reconnect_thread = threading.Thread(target=self.ensure_connection)
            self.reconnect_thread.start()

    def send_message(self, message):
        if self.send_lock.locked():
            print("Previous send operation still in progress, message skipped.")
            return

        with self.send_lock:
            if self.client_socket:
                try:
                    self.client_socket.sendall(message.encode('utf-8'))
                except socket.error:
                    print("Failed to send message, attempting to reconnect...")
                    self.client_socket = None
                    self.connecting = False
                    self.connect()

    def close(self):
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None
            self.connecting = False
