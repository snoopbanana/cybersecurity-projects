"""
Script testing if every algorithms run correctly.
"""

import pytest
import pytest_asyncio

import xor_encryption
import caesar_encryption
import railfence_encryption
import vigenere_encryption
import rc4_encryption
import adler_checksum
import base64_algorithm
import sha256_hash
import diffie_hellman
import rsa_encryption

def test_xor_encryption():
    assert xor_encryption.encrypt("hello", "123") == "YW_]]"
    assert xor_encryption.decrypt("YW_]]", "123") == "hello"

def test_caesar_encryption():
    assert caesar_encryption.encrypt("hello", 3) == "khoor"
    assert caesar_encryption.decrypt("khoor", 3) == "hello"

def test_railfence_encryption():
    assert railfence_encryption.encrypt("hello", 3) == "hoell"
    assert railfence_encryption.decrypt("hoell", 3) == "hello"

def test_vigenere_encryption():
    assert vigenere_encryption.encrypt("hello", "hey") == "oijss"
    assert vigenere_encryption.decrypt("oijss", "hey") == "hello"

def test_rc4_encryption():
    assert rc4_encryption.encrypt("hey", "hey") == "u+#"
    assert rc4_encryption.decrypt("u+#", "hey") == "hey"

def test_adler_checksum():
    text = "hello"
    byte_data = text.encode('utf-8')
    assert adler_checksum.checksum(byte_data) == "062c0215"

def test_base64_algoirthm():
    text = "hello"
    byte_data = text.encode('utf-8')
    assert base64_algorithm.encode(byte_data) == "aGVsbG8="

    text = "aGVsbG8="
    assert base64_algorithm.decode(text) == b"hello"

def test_sha256_hash():
    text = "hello"
    byte_data = text.encode('utf-8')
    assert sha256_hash.hash(byte_data) == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"

@pytest.mark.asyncio
async def test_diffie_hellman():
    assert await diffie_hellman.diffie_hellman(a=123, b=456) is True

def test_rsa_encryption():
    text = "hello"
    byte_data = text.encode('utf-8')

    d, n = rsa_encryption.generate_key()
    c = rsa_encryption.encrypt(byte_data, rsa_encryption.e, n)
    assert rsa_encryption.decrypt(c, d, n) == byte_data
    