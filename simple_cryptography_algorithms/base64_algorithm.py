"""
Author: snoopbanana (Ngô Quang Vinh)
Date: July 2026
License: MIT License (Copyright (c) 2026 snoopbanana)

Write my simple base64 algorithm.
"""

"""
Computers store data as bytes, each byte containing 8 bits. 
However, Base64 only reads in groups of 6 bits at a time. 
Since 6 bits make up 2⁶ = 64 possibilities, it fits perfectly to
64 secure characters on the keyboard: 
A to Z (26 characters), a to z (26 characters), 0 to 9 (10 characters), and + and /

Base64 takes 3 bytes of original data (3 × 8 = 24 bits).
 Then it divides these 24 bits into 4 chunks, each 6 bits. 
 Each 6-bit chunk is converted into one character in the Base64 table.
   → Result: Every 3 bytes of input will expand into 4 Base64 characters.
"""


# Standard 64-character character set
BASE64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def encode(data: bytes) -> str:
    bits_list = ""
    
    for byte in data:
        bits_list += format(byte, "08b")

    while len(bits_list) % 6 != 0:
        bits_list += '0'

    result = ""
    for index in range(0, len(bits_list), 6):
        six_bits = bits_list[index : index + 6]
        decimal_value = int(six_bits, 2)

        result += BASE64[decimal_value]

    # Replace the last character of the result with ... equals sign (=):
    # 1 when length of data leaves a remainder of 2 when divided by 3
    # and 2 when leaves a remainder of 1 when divided by 3 
    if len(data) % 3 == 2:
        result += "="
    if len(data) % 3 == 1:
        result += "=="

    return result

# Decrypt is encrypt but on reversed.
def decode(data: str) -> bytes:
    missing_bytes = 0

    # Number of '=' at the end of ciphertext is
    # equal to the number of missing bytes and remove '='
    for character in reversed(data):
        if character != '=':
            break
        missing_bytes += 1
        data = data[:-1]

    bits_sequence = ""
    # Reverse lookup the index of character in data in BASE64 character set
    for character in data:
        index = BASE64.index(character)

        # Convert the index into 6-bit binary string
        six_bits = f"{index:06b}"

        # Combine 6-bit clusters into a single long bit sequence.
        bits_sequence += six_bits

    # Remove the extra zero bits at the end of the bit sequence.
    # They are equal to the number of '=' padding.
    if missing_bytes > 0:
        bits_sequence = bits_sequence[:-missing_bytes * 2]


    original_data = b""
    # Cut the bit sequence into small groups, each group containing exactly 8 bits.
    for i in range(0, len(bits_sequence), 8):
        eight_bits = bits_sequence[i: i + 8]

        # Convert 8-bits groups to an integer value,
        # which representing each byte of raw data
        number = int(eight_bits, 2)
        byte_data = number.to_bytes(1, byteorder='big')

        original_data += byte_data

    return original_data
