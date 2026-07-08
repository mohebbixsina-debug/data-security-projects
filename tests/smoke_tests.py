"""Small runnable checks for the Data Security portfolio projects.

These tests are intentionally lightweight: they verify that the educational
implementations run and that the main cryptographic demonstrations are wired
correctly. They are not meant to replace a production cryptography test suite.
"""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
BLOCK_DIR = ROOT / "projects" / "block-cipher"
STREAM_DIR = ROOT / "projects" / "stream-cipher"
SUBSTITUTION_DIR = ROOT / "projects" / "substitution-cipher"


def add_import_path(path):
    path = str(path)
    if path not in sys.path:
        sys.path.insert(0, path)


def test_aes_known_vector():
    add_import_path(BLOCK_DIR)
    from aes import AES

    key = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
    plaintext = bytes.fromhex("00112233445566778899aabbccddeeff")
    expected = bytes.fromhex("69c4e0d86a7b0430d8cdb78070b4c55a")

    aes = AES(key)
    ciphertext = aes.encrypt(plaintext)

    assert ciphertext == expected
    assert aes.decrypt(ciphertext) == plaintext


def test_block_modes_round_trip():
    add_import_path(BLOCK_DIR)
    from blockcipher import BlockCipher

    key = b"ThisIsA16ByteKey"
    iv = bytes(range(16))
    plaintext = b"Data security mode demo with more than one block."

    for mode in ["ECB", "CBC", "CFB", "OFB"]:
        cipher = BlockCipher(key=key, iv=iv, mode=mode)
        ciphertext = cipher.encrypt(plaintext)
        recovered = cipher.decrypt(ciphertext)
        assert recovered == plaintext, mode


def test_stream_cipher_utilities():
    add_import_path(STREAM_DIR)
    from bits import Bits
    from bitgenerator import AlternatingStep
    from lfsr import LFSR, berlekamp_massey

    bits = Bits(b"A")
    assert bits[:4] ^ Bits([1, 0, 1, 0])
    assert Bits([0, 1, 0, 0, 0, 0, 0, 1]).to_bytes() == b"A"

    lfsr = LFSR({4, 1, 0}, state=Bits([1, 0, 0, 1]))
    assert len(lfsr.run_steps(16)) == 16

    generator = AlternatingStep(seed=Bits([1] * 12))
    assert len([next(generator) for _ in range(32)]) == 32

    poly, length = berlekamp_massey([1, 0, 0, 1, 1, 1, 0, 1])
    assert isinstance(poly, list)
    assert length >= 0


def test_substitution_cipher_round_trips():
    add_import_path(SUBSTITUTION_DIR)
    from substitution_ciphers import (
        affine_decrypt,
        affine_encrypt,
        caesar_decrypt,
        caesar_encrypt,
        letter_distribution,
        substitution_decrypt,
        substitution_encrypt,
    )

    message = "Data Security!"
    assert caesar_decrypt(caesar_encrypt(message, 7), 7) == message
    assert affine_decrypt(affine_encrypt(message, 5, 8), 5, 8) == message

    alphabet = "abcdefghijklmnopqrstuvwxyz"
    shifted = "defghijklmnopqrstuvwxyzabc"
    mapping = dict(zip(alphabet, shifted))
    encrypted = substitution_encrypt(message, mapping)
    assert substitution_decrypt(encrypted, mapping) == message

    distribution = letter_distribution("aab!")
    assert distribution["a"] == 2 / 3
    assert distribution["b"] == 1 / 3


def test_known_plaintext_attack_demo_files():
    add_import_path(STREAM_DIR)
    from bits import Bits
    from kpa_attack import kpa_attack

    ciphertext = Bits((STREAM_DIR / "ciphertext.bin").read_bytes())
    known_plaintext = Bits((STREAM_DIR / "known-plaintext.txt").read_bytes())

    recovered, feedback_poly = kpa_attack(ciphertext, known_plaintext)

    assert isinstance(recovered, str)
    assert len(recovered) > 0
    assert isinstance(feedback_poly, list)


if __name__ == "__main__":
    tests = [
        test_substitution_cipher_round_trips,
        test_aes_known_vector,
        test_block_modes_round_trip,
        test_stream_cipher_utilities,
        test_known_plaintext_attack_demo_files,
    ]

    for test in tests:
        test()
        print(f"PASS {test.__name__}")
