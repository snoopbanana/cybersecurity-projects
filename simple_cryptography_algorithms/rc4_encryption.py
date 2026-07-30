"""
Author: snoopbanana (Ngô Quang Vinh)
Date: July 2026
License: MIT License (Copyright (c) 2026 snoopbanana)

Write my simple RC4 encryption algorithm.
"""

def encrypt(message: str, key: str) -> str:
    j = 0
    # Create an array S containing 256 numbers from 0 to 255.
    S = list(range(256))
    # Convert key to bytes
    key = bytes(key, 'utf-8')

    # KSA - Array Mixing S
    for index in range(256):
        j = (j + S[index] + key[index % len(key)]) % 256
        S[index], S[j] = S[j], S[index]

    # PRGA - Key Generation & XOR
    # Create two pointer
    i = 0
    j = 0
    result = bytearray()

    for byte in message.encode('utf-8'):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]

        result.append(byte ^ K)

    return result.decode('latin-1')

def decrypt(message: str, key: str) -> str:
    return encrypt(message, key)

