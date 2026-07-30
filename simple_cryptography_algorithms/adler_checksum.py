"""
Author: snoopbanana (Ngô Quang Vinh)
Date: July 2026
License: MIT License (Copyright (c) 2026 snoopbanana)

Write my simple Adler-32 algorithm.
"""

"""
Adler-32 uses two cumulative sums (Running Sums).

It calculates two 16-bit values ​​called A and B, then combine them into a 32-bit number: Adler-32=(B×65536)+A.

The standard modulo value used is M=65521 (this is the largest prime number less than 2 16 =65536).
"""
MOD_ADLER = 65521

def checksum(data: bytes) -> str:
    a = 1
    b = 0

    for byte in data:
        a = (a + byte) % MOD_ADLER
        b = (b + a) % MOD_ADLER

    checksum_int = (b << 16) | a
    return f"{checksum_int:08x}"