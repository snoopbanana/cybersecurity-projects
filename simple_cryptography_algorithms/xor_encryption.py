"""
Author: snoopbanana (Ngô Quang Vinh)
Date: July 2026
License: MIT License (Copyright (c) 2026 snoopbanana)

Write my simple XOR encryption algorithm.
"""

"""Handling cases where the key is longer than the message or vice versa."""

def adjust_key(message, key) -> str:
    repeated_key = (key * (len(message) // len(key) + 1))[:len(message)]
    return repeated_key

def encrypt(message, key) -> str:
    # Convert messsage to bytes
    message_bytes = message.encode('utf-8', errors="surrogateescape")
    adjusted_key = adjust_key(message, key)
    # Convert key to bytes
    key_bytes = adjusted_key.encode('utf-8', errors="surrogateescape")

    
    # Take each byte of the message and XOR it with each byte of the key.
    result_bytes = bytes(x ^ y for x, y in zip(message_bytes, key_bytes))
    # Revert it into human readable string
    result = result_bytes.decode('utf-8', errors="surrogateescape")

    return result

"""Decryption use the same logic as encryption"""
def decrypt(message, key) -> str:
    return encrypt(message, key)
