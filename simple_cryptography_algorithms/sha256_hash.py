"""
Author: snoopbanana (Ngô Quang Vinh)
Date: July 2026
License: MIT License (Copyright (c) 2026 snoopbanana)

Write my simple SHA-256 algorithm.
"""

import math
from K_constants import K

def hash(data: bytes) -> str:
    # Store the original length
    bits_length = len(data) * 8
    # Add the first bit 1 (byte 0x80)
    data += b"\x80"

    # Add 0x00 bytes until 
    # the length (bytes) leaves a remainder of 56 when divided by 64.
    while len(data) % 64 != 56:
        data += b"\x00"

    # Concatenate 8 bytes representing the original length.
    data += bits_length.to_bytes(8, 'big')

    # SHA-256 uses 8 fixed numbers (called H0 to H7).
    H = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ]

    # For a 512-bit (64-byte) block, split it into first 16 words of 32 bits from the data above.
    W = [0] * 64
    for i in range(16):
        W[i] = int.from_bytes(data[i * 4 : (i + 1) * 4], 'big')

    # Define the Rotate Right and Shift Right functions
    # x >> n: Shift all bits of x to the right by n steps.
    # x << (32 - n): Take the n bits that were dropped in the previous step and move them to the left end.
    # |: OR operation to combine two parts above
    # & 0xFFFFFFFF: To force the result to always fit within the 32-bit range.
    def rotr(x, n): return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF
    def shr(x, n): return x >> n

    # Define the functions sigma0 and sigma1
    def sig0(x): return rotr(x, 7) ^ rotr(x, 18) ^ shr(x, 3)
    def sig1(x): return rotr(x, 17) ^ rotr(x, 19) ^ shr(x, 10)

    # Generate the next 48 words (W[16] to W[63])
    for i in range(16, 64):
        W[i] = (W[i - 16] + sig0(W[i - 15]) + W[i - 7] + sig1(W[i - 2])) & 0xFFFFFFFF

    # Copy 8 values H0 -> H7  into 8 working variables a, b, c, d, e, f, g, h:
    a, b, c, d, e, f, g, h = H[0], H[1], H[2], H[3], H[4], H[5], H[6], H[7]

    # ~ is bit inversion
    def Ch(x, y, z): return (x & y) ^ (~x & z)
    def Maj(x, y, z): return (x & y) ^ (x & z) ^ (y & z)
    def SIG0(x): return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)
    def SIG1(x): return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)

    # Run 64 loops
    for i in range(64):
        # Calculate the two intermediate variables T1 and T2.
        T1 = (h + SIG1(e) + Ch(e, f, g) + K[i] + W[i]) & 0xFFFFFFFF
        T2 = (SIG0(a) + Maj(a, b, c)) & 0xFFFFFFFF

        h = g
        g = f
        f = e
        e = (d + T1) & 0xFFFFFFFF
        d = c
        c = b
        b = a
        a = (T1 + T2) & 0xFFFFFFFF

    H[0] = (H[0] + a) & 0xFFFFFFFF
    H[1] = (H[1] + b) & 0xFFFFFFFF
    H[2] = (H[2] + c) & 0xFFFFFFFF
    H[3] = (H[3] + d) & 0xFFFFFFFF
    H[4] = (H[4] + e) & 0xFFFFFFFF
    H[5] = (H[5] + f) & 0xFFFFFFFF
    H[6] = (H[6] + g) & 0xFFFFFFFF
    H[7] = (H[7] + h) & 0xFFFFFFFF

    # Standardize 8 Hex characters (08x) for each H
    return "".join(f"{h:08x}" for h in H)