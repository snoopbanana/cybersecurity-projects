"""
Author: snoopbanana (Ngô Quang Vinh)
Date: July 2026
License: MIT License (Copyright (c) 2026 snoopbanana)

Write my simple Vigenere encryption algorithm.
"""

import string

def adjust_key(message: str, key: str) -> str:
    repeated_key = (key * (len(message) // len (key) + 1))[:len(message)]
    return repeated_key

def encrypt(message: str, key: str) -> str:
    result = []
    # Adjust the key so they share the same length
    key = adjust_key(message, key)
    # Convert key to all uppercase to easily synchronization
    key = key.upper()

    for index, character in enumerate(message):
        if character.isupper():
            msg_char_index = string.ascii_uppercase.index(character)

            key_char_index = string.ascii_uppercase.index(key[index])
            # Just shifting, like Caesar cyphertext
            new_character = string.ascii_uppercase[(msg_char_index + key_char_index) % 26]
            result.append(new_character)


        if character.islower():
            msg_char_index = string.ascii_lowercase.index(character)
            key_char_index = string.ascii_uppercase.index(key[index])
            new_character = string.ascii_lowercase[(msg_char_index + key_char_index) % 26]
            result.append(new_character)

    return "".join(result)


"""Literally the same as encryption part except you use minus instead of plus to reverse the shifting"""
def decrypt(message: str, key: str) -> str:
    result = []
        # Adjust the key so they share the same length
    key = adjust_key(message, key)
    key = key.upper()

    for index, character in enumerate(message):
        if character.isupper():
            msg_char_index = string.ascii_uppercase.index(character)

            key_char_index = string.ascii_uppercase.index(key[index])
            new_character = string.ascii_uppercase[(msg_char_index - key_char_index) % 26]
            result.append(new_character)


        if character.islower():
            msg_char_index = string.ascii_lowercase.index(character)
            key_char_index = string.ascii_uppercase.index(key[index])
            new_character = string.ascii_lowercase[(msg_char_index - key_char_index) % 26]
            result.append(new_character)

    return "".join(result)