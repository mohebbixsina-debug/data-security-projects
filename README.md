# Data Security Projects

This repository brings together three hands-on data security projects built around core cryptography ideas: classical substitution ciphers, LFSR-based stream ciphers, and an educational AES/block-cipher implementation.

Each project includes a readable notebook, reusable Python code, and a small runnable check. The goal is to show both sides of cryptography practice: how the algorithms work internally, and how weak designs can be analyzed or attacked.

## Projects

| Project | What it Covers |
|---|---|
| `projects/substitution-cipher/` | Caesar, monoalphabetic substitution, frequency analysis, and affine ciphers |
| `projects/stream-cipher/` | Bit utilities, LFSRs, Berlekamp-Massey, alternating-step generation, and a known-plaintext attack |
| `projects/block-cipher/` | AES-128 internals, confusion/diffusion experiments, and ECB/CBC/CFB/OFB modes |

## Highlights

- Implemented classical encryption and decryption routines from scratch.
- Used frequency analysis and brute force to attack substitution-style ciphers.
- Built LFSR-based stream-cipher utilities and recovered keystream structure with Berlekamp-Massey.
- Implemented AES-128 core transformations, including encryption and decryption.
- Demonstrated block-cipher modes of operation: ECB, CBC, CFB, and OFB.
- Added smoke tests that verify the main code paths still run correctly.

## Repository Layout

```text
projects/
  substitution-cipher/
  stream-cipher/
  block-cipher/
tests/
  smoke_tests.py
```

Each project folder has its own README with a short explanation of the files and concepts.

## Quick Start

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
```

Run the project checks:

```bash
python tests/smoke_tests.py
```

Expected output:

```text
PASS test_substitution_cipher_round_trips
PASS test_aes_known_vector
PASS test_block_modes_round_trip
PASS test_stream_cipher_utilities
PASS test_known_plaintext_attack_demo_files
```

## Notes

These implementations are written for learning and demonstration. They are useful for understanding how cryptographic systems work internally, but they should not be used as production cryptographic libraries.

## CV Summary

Implemented and analyzed substitution ciphers, LFSR-based stream ciphers, known-plaintext attacks, and an educational AES/block-cipher system with ECB, CBC, CFB, and OFB modes in Python.
