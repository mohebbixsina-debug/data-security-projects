"""Educational implementations of classical substitution ciphers.

The functions in this module mirror the notebook experiments, but keep the
core cipher logic reusable from the command line, tests, or another notebook.
They are intentionally simple and readable because the goal is to study the
cryptanalytic ideas, not to provide production cryptography.
"""

from collections import Counter
import math
import string


ALPHABET = string.ascii_lowercase


def caesar_encrypt(plaintext, shift=0):
    """Encrypt text with a Caesar shift while preserving non-letters."""
    shift %= 26
    result = []

    for char in plaintext:
        lower = char.lower()
        if lower in ALPHABET:
            enc = ALPHABET[(ALPHABET.index(lower) + shift) % 26]
            result.append(enc.upper() if char.isupper() else enc)
        else:
            result.append(char)

    return "".join(result)


def caesar_decrypt(ciphertext, shift=0):
    """Decrypt a Caesar-shifted message."""
    return caesar_encrypt(ciphertext, -shift)


def substitution_encrypt(plaintext, mapping):
    """Encrypt text with a monoalphabetic substitution mapping."""
    _validate_mapping(mapping)
    return _translate_with_mapping(plaintext, mapping)


def substitution_decrypt(ciphertext, mapping):
    """Decrypt text encrypted with a monoalphabetic substitution mapping."""
    _validate_mapping(mapping)
    inverse = {cipher: plain for plain, cipher in mapping.items()}
    return _translate_with_mapping(ciphertext, inverse)


def affine_encrypt(plaintext, a, b):
    """Encrypt with the affine cipher: E(x) = (a*x + b) mod 26."""
    if math.gcd(a, 26) != 1:
        raise ValueError("Parameter 'a' must be coprime with 26.")

    result = []
    for char in plaintext:
        lower = char.lower()
        if lower in ALPHABET:
            x = ALPHABET.index(lower)
            enc = ALPHABET[(a * x + b) % 26]
            result.append(enc.upper() if char.isupper() else enc)
        else:
            result.append(char)
    return "".join(result)


def affine_decrypt(ciphertext, a, b):
    """Decrypt an affine cipher message."""
    if math.gcd(a, 26) != 1:
        raise ValueError("Parameter 'a' must be coprime with 26.")

    inverse_a = pow(a, -1, 26)
    result = []
    for char in ciphertext:
        lower = char.lower()
        if lower in ALPHABET:
            y = ALPHABET.index(lower)
            dec = ALPHABET[(inverse_a * (y - b)) % 26]
            result.append(dec.upper() if char.isupper() else dec)
        else:
            result.append(char)
    return "".join(result)


def letter_distribution(text):
    """Return normalized letter frequencies for a text."""
    letters = [char for char in text.lower() if char in ALPHABET]
    total = len(letters)
    counts = Counter(letters)

    if total == 0:
        return {letter: 0.0 for letter in ALPHABET}

    return {letter: counts[letter] / total for letter in ALPHABET}


def brute_force_caesar(ciphertext):
    """Return all 26 Caesar decryptions for quick manual inspection."""
    return {shift: caesar_decrypt(ciphertext, shift) for shift in range(26)}


def brute_force_affine(ciphertext):
    """Try every valid affine key and return candidate plaintexts."""
    candidates = {}
    valid_a_values = [a for a in range(26) if math.gcd(a, 26) == 1]

    for a in valid_a_values:
        for b in range(26):
            candidates[(a, b)] = affine_decrypt(ciphertext, a, b)

    return candidates


def _translate_with_mapping(text, mapping):
    result = []
    for char in text:
        lower = char.lower()
        if lower in mapping:
            translated = mapping[lower]
            result.append(translated.upper() if char.isupper() else translated)
        else:
            result.append(char)
    return "".join(result)


def _validate_mapping(mapping):
    keys = set(mapping.keys())
    values = set(mapping.values())
    expected = set(ALPHABET)

    if keys != expected or values != expected:
        raise ValueError("Mapping must be a one-to-one mapping of the lowercase alphabet.")


if __name__ == "__main__":
    message = "Data Security!"
    caesar = caesar_encrypt(message, shift=4)
    print("Caesar:", caesar, "->", caesar_decrypt(caesar, shift=4))

    affine = affine_encrypt(message, a=5, b=8)
    print("Affine:", affine, "->", affine_decrypt(affine, a=5, b=8))
