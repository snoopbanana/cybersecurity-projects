"""
Author: snoopbanana
Date: July 2026
License: MIT License (Copyright (c) 2026 snoopbanana)

Write my simple program to recreate server from your own real-time chat between client and server.
"""


import socket
import threading
import time
import sys

# To ensure smooth UI Terminal experiences 
# and prevents messages from other threads from interrupting
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

class Server:

    def __init__(self) -> None:
        # AF_INET = IPv4, SOCK_STREAM = TCP
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = None
    
    def bind(self) -> None:
        self.server.bind(("127.0.0.1", 12345))

    def listen(self) -> None:
        self.server.listen()

    def accept_client(self) -> None:
        while True:
            if self.client_socket is not None:
                time.sleep(0.5)
                continue

            connection, _ = self.server.accept()
            self.client_socket = connection


    def receive_message(self) -> None:
        while True:
            try:
                if self.client_socket is None:
                    time.sleep(0.1)
                    continue
                
                data = self.client_socket.recv(1024).decode()
                
                if not data:
                    self.client_socket = None
                    with patch_stdout():
                        print("\nClient disconnected.")
                    continue
                
                with patch_stdout():
                    print(f"Client: {data}")
            
            except Exception as e:
                self.client_socket = None
                with patch_stdout():
                    print(f"Disconnected due to {e}.")


    def send_message(self) -> None:
        session = PromptSession()

        while True:
            if self.client_socket is None:
                time.sleep(0.1)
                continue

            try:
                with patch_stdout():
                    message = session.prompt("Server: ")
                
                if self.client_socket and message.strip():
                    self.client_socket.send(message.encode())
            
            except (KeyboardInterrupt, EOFError):
                with patch_stdout():
                    print("\nTyping cancelled.")
                continue
            
            except Exception as e:
                self.client_socket = None
                with patch_stdout():
                    print(f"\nDisconnected due to {e}")


    def initiate_threads(self) -> None:
        accept_thread = threading.Thread(target=self.accept_client, daemon=True)
        send_thread = threading.Thread(target=self.send_message, daemon=True)
        receive_thread = threading.Thread(target=self.receive_message, daemon=True)

        accept_thread.start()
        send_thread.start()
        receive_thread.start()

def main() -> None:
    try:
        server = Server()
        server.bind()
        server.listen()
        server.initiate_threads()

        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        server.server.close()
        print("Disconnected.")

if __name__ == "__main__":
    main()