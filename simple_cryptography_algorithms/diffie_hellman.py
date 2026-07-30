"""
Author: snoopbanana (Ngô Quang Vinh)
Date: July 2026
License: MIT License (Copyright (c) 2026 snoopbanana)

Write my simple Diffie - Hellman algorithm.
"""

"""
Public (p,g): p is an extremely large prime number, g is an integer (called a generator).
Private: Alice chooses number a, Bob chooses number b.

Diffie-Hellman Key Exchange Protocol:

ALICE                                     BOB
 ---------------------                    ---------------------
  Choose secret: a                         Choose secret: b
         │                                        │
         ▼                                        ▼
  Compute: A = (g^a) mod p                 Compute: B = (g^b) mod p
         │                                        │
         ├─── Send Public Key A (Over Network) ──►│
         │                                        │
         │◄── Send Public Key B (Over Network) ───┤
         │                                        │
         ▼                                        ▼
  Receive B, compute:                      Receive A, compute:
  Key = (B^a) mod p                        Key = (A^b) mod p
      = (g^b)^a mod p                          = (g^a)^b mod p
      = (g^(a*b)) mod p                        = (g^(a*b)) mod p
"""

from cryptography.hazmat.primitives.asymmetric import dh
import asyncio

def generate_parameters() -> int:
    # Automatically generate public parameters p (2048-bit) and g
    parameters = dh.generate_parameters(generator=2, key_size=2048)

    # Extract p and g as integers.
    numbers = parameters.parameter_numbers()
    p = numbers.p
    g = numbers.g

    return p, g

async def alice(p, g, a, a_to_b, b_to_a) -> int:
    A = pow(g, a, p)

    # Send the Public Key to B
    await a_to_b.put(A)
    # Waiting to receive the Public Key from B
    B = await b_to_a.get()

    return pow(B, a, p)

async def bob(p, g, b, a_to_b, b_to_a) -> int:
    B = pow(g, b, p)

    # Send the Public Key to A
    await b_to_a.put(B)
    # Waiting to receive the Public Key from B
    A = await a_to_b.get()

    return pow(A, b, p)



async def diffie_hellman(a, b) -> bool:
    p, g = generate_parameters()

    # Initialize two asynchronous queues
    a_to_b = asyncio.Queue()
    b_to_a = asyncio.Queue()

    secret_a, secret_b = await asyncio.gather(
        alice(p, g, a, a_to_b, b_to_a),
        bob (p, g, b, a_to_b, b_to_a)
    )

    return secret_a == secret_b
