"""
Author: snoopbanana
Date: July 2026
License: MIT License (Copyright (c) 2026 snoopbanana)

Write my simple program to recreate client from your own real-time chat between client and server.
"""

import socket
import threading
import time
import sys

# To ensure smooth UI Terminal experiences 
# and prevents messages from other threads from interrupting
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

class Client:

    def __init__(self) -> None:
        #AF_INET = IPv4, SOCK_STREAM = TCP
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def connect(self) -> None:
        self.client.connect(("127.0.0.1", 12345))

    def send_message(self) -> None:
        session = PromptSession()
        
        while True:
            if self.client is None:
                time.sleep(0.1)
                continue

            try:
                with patch_stdout():
                    message = session.prompt("Client: ")
                if self.client and message.strip():
                    self.client.send(message.encode())
            
            except (KeyboardInterrupt, EOFError):
                with patch_stdout():
                    print("\nTyping cancelled.")
                continue
            
            except Exception as e:
                self.client = None
                with patch_stdout():
                    print(f"\nDisconnected due to {e}")

    def receive_message(self) -> None:
        while True:
            try:
                if self.client is None:
                    time.sleep(0.1)
                    continue

                data = self.client.recv(1024).decode()

                if not data:
                    self.client = None
                    with patch_stdout():
                        print("\nServer disconnected.")
                    break

                with patch_stdout():
                    print(f"Server: {data}")

            except Exception as e:
                self.client = None
                with patch_stdout():
                    print(f"\nDisconnected due to {e}")
                break


    def initiate_threads(self) -> None:
        send_thread = threading.Thread(target=self.send_message, daemon=True)
        receive_thread = threading.Thread(target=self.receive_message, daemon=True)

        send_thread.start()
        receive_thread.start()


def main() -> None:
    try:
        client = Client()
        client.connect()
        client.initiate_threads()

        while True:
            time.sleep(1)
    
    # Press Ctrl + C to exit
    except KeyboardInterrupt:
        client.client.close()
        print("Disconnected.")

if __name__ == "__main__":
    main()