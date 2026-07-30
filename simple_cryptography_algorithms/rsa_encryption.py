"""
Author: snoopbanana (Ngô Quang Vinh)
Date: July 2026
License: MIT License (Copyright (c) 2026 snoopbanana)

Write my simple RSA algorithm.
"""

"""
Phase 1: Key Generation
- Choose two extremely large prime numbers p and q.
- Calculate n = p × q (n is modulus and public).
- Calculate the Euler function ϕ(n)=(p−1)×(q−1).
- Choose the number e such that 1<e<ϕ(n) and gcd(e,ϕ(n))=1 (usually e=65537 is chosen).
- The value of d is the modulo inverse of e with respect to ϕ(n), which is: d×e≡1(modϕ(n))

You get: 
- Public key: Pair (e, n)
- Private key: Pair (d, n)

Phase 2: Encryption
- c = (m ^ e) mod n 
where c is ciphertext and m is message

Phase 3: Decryption
- m = (c ^ d) mod n
"""

# To generate 2 random prime numbers p and q
from cryptography.hazmat.primitives.asymmetric import rsa

e = 65537

def generate_key() -> tuple[int, int]:
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    p, q = key.private_numbers().p, key.private_numbers().q
    n = p * q

    phi = (p - 1) * (q - 1)
    # Calculate modulo inverse
    d = pow(e, -1, phi)

    return d, n

def encrypt(message: bytes, e: int, n: int) -> int:
    m = int.from_bytes(message, byteorder='big')

    c = pow(m, e, n)

    return c

def decrypt(c: int, d: int, n: int) -> bytes:
    m = pow(c, d, n)

    byte_length = (m.bit_length() + 7) // 8
    message = m.to_bytes(byte_length, byteorder='big')

    return message


