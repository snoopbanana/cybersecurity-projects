"""
Author: snoopbanana
Date: July 2026
License: MIT License (Copyright (c) 2026 snoopbanana)

Write my own simple Telnet Client to go through port 80 of one server. Then automatically send "GET /HTTP/1.1" 
and print out results
"""

import socket
import sys

try:
    domain_name = input("Type your target domain name: ")
    target_port = int(input("Type your target_port: "))
    target_ip = socket.gethostbyname(domain_name)
except socket.gaierror:
    print("Failed: Can't resolve domain name")
    # Exit immediately in order to prevent chain errors
    sys.exit(1)
except ValueError:
    print("Failed: Target port input must be an integer")
    sys.exit(1)

try:
    # Create socket object
    # AF_INET = IPv4, SOCK_STREAM = TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set timeout to 10 seconds 
    client_socket.settimeout(10)

    print(f"Trying to reach {target_ip}:{target_port}...")

    client_socket.connect((target_ip, target_port))
    print("Successfully connected")

    messages_option = input('Do you want to send "GET / HTTP/1.1" or not?(y/n): ').strip().lower()
    if messages_option == "n":
        input_message = input()
        message = f"{input_message}\r\n\r\n"
    
    # Automatically send GET /HTTP/1.1
    else:
        message = (
            "GET / HTTP/1.1\r\n"
            f"Host: {domain_name}\r\n"
            "Connection: close\r\n\r\n"
        )
    client_socket.sendall(message.encode("utf-8"))

    # Maximum hold 4096 bytes each time (4Kb)
    response = client_socket.recv(4096)
    
    # Decode data back to readable human form
    result = response.decode("utf-8", errors="replace")
    print(result)

except socket.timeout:
    print("Failed: Timeout")
except socket.error as e:
    print(f"Network error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    client_socket.close()
    print("Disconnected.")