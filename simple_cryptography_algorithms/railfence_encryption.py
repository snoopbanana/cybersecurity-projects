"""
Author: snoopbanana (Ngô Quang Vinh)
Date: July 2026
License: MIT License (Copyright (c) 2026 snoopbanana)

Write my simple Rail Fence encryption algorithm.
"""

"""The algorithm arranges the characters in a zigzag pattern on the `key` rails,
 then reads each rail sequentially from top to bottom to form the encoded string.

 key: The number of rails used to create the zigzag path
 """
def encrypt(message: str, key: int) -> str:
    result = []

    # The distance between zigzag vertices in the same row
    step = 2 * (key - 1)

    for row in range(key):
        index = row
        while index < len(message):
            result.append(message[index])

            # Handling middle rows
            if row != 0 and row != key - 1:
                diag_step = step - 2 * row
                if index + diag_step < len(message):
                    result.append(message[index + diag_step])

            index += step

    return "".join(result)

def decrypt(message: str, key: int) -> str:
    result = []
    pattern = []

    # Create pattern
    for row in range(key):
        index = row
        # Flag for the alternating jump steps.
        use_step1 = True

        while index < len(message):
            pattern.append(index)

            if row == 0 or row == key - 1:
                step = 2 * (key - 1)

            # Handling middle rows
            else:
                step1 = 2 * (key - 1 - row) # Down
                step2 = 2 * row # Up

                if use_step1:
                    step = step1
                else:
                    step = step2
                # Reset for next jump
                use_step1 = not use_step1
            
            index += step

    # Append characters base on index from pattern
    for i in range(len(message)):
        index = pattern.index(i)
        result.append(message[index])

    return "".join(result)