"""
Author: snoopbanana (Ngô Quang Vinh)
Date: July 2026
License: MIT License (Copyright (c) 2026 snoopbanana)

Write my simple Caesar encryption algorithm.
"""

import string


def encrypt(message: str, key: int) -> str:
    result = []
    # The shift key should be in range of 0-25.
    key = key % 26

    for character in message:
        if character.isupper():
            index = string.ascii_uppercase.index(character)
            new_character = string.ascii_uppercase[(index + key) % 26]
            result.append(new_character)
        
        elif character.islower():
            index = string.ascii_lowercase.index(character)
            new_character = string.ascii_lowercase[(index + key) % 26]
            result.append(new_character)
        
        else:
            # No changes to special characters, spaces, punctuations and numbers.
            result.append(character)
        
    return "".join(result)

def decrypt(message: str, key: int) -> str:
    return encrypt(message, -key)