# 💬 Real-Time Multi-Threaded CLI Chat Application

A lightweight, bidirectional real-time chat application (Server - Client) running entirely inside the Command Line Interface (CLI). The system leverages the **TCP Socket** protocol combined with a **Multi-threaded architecture** to achieve seamless asynchronous data transmission.

---

## 🛠️ Threading Architecture

To completely eliminate the blocking issues inherent in synchronous I/O operations, the application isolates core tasks into independent background threads (`daemon=True`) that execute concurrently:

### 1. Server Side (`server.py`)
Spawns 3 separate background daemon threads:
*   **Accept Thread (`accept_client`)**: Continuously listens for incoming connections from new clients (`.accept()`). If a client is already connected, it goes into a temporary sleep cycle to optimize system resources.
*   **Send Thread (`send_message`)**: Responsible for rendering the prompt interface and actively pushing data packets over the network as soon as the server administrator types a message.
*   **Receive Thread (`receive_message`)**: Stays active, waiting for incoming stream data from the network (`.recv(1024)`). It automatically releases the connection state (`self.client_socket = None`) if it detects a clean disconnect (0-byte payload) or an abrupt connection failure.

### 2. Client Side (`client.py`)
Spawns 2 separate background daemon threads:
*   **Send Thread (`send_message`)** and **Receive Thread (`receive_message`)** execute concurrently in an identical fashion to the server side, ensuring instant, real-time message exchange.

---

## 🛡️ Resolving the UI Race Condition

A fundamental challenge when building real-time full-duplex chat applications inside a Terminal is that the **Receive Thread** can trigger an output (`print`) at any given moment—even while the user is actively typing a message in the **Send Thread**. Without proper handling, this results in overlapping text, broken lines, and a corrupted terminal UI.

This project resolves this race condition elegantly by integrating the `prompt_toolkit` library:
*   **`PromptSession`**: Manages the local input buffer state independently, isolating physical keyboard interrupt events (`KeyboardInterrupt`, `EOFError`) locally to the typing thread without impacting data reception.
*   **`patch_stdout`**: Functions as an asynchronous standard output (`stdout`) coordinator. When a new message arrives from the network, `patch_stdout` instantly hides the user's active input prompt (`Server: ` or `Client: `), flushes the incoming message onto a clean line, and seamlessly restores the user's uncommitted text right below it.

---

## 🚀 Installation & Usage

### 1. Install Dependencies
The application utilizes Python's core native network libraries, requiring only the terminal UI enhancement package:
```bash
pip install prompt_toolkit
