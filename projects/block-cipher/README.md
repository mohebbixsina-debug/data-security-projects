# Block Cipher Project

This project implements and analyzes AES-128 as an educational block cipher. It includes AES core transformations, confusion/diffusion experiments, and common block modes of operation.

## Files

| File | Purpose |
|---|---|
| `block_ciphers.ipynb` | Notebook walkthrough with explanations and experiments |
| `aes.py` | AES-128 single-block encryption/decryption implementation |
| `blockcipher.py` | ECB, CBC, CFB, and OFB mode wrapper |
| `diffusion_confusion.py` | Monte Carlo helpers for avalanche-style experiments |

## Main Ideas

- AES combines substitution, row shifting, column mixing, and round-key addition.
- Small changes in plaintext or key should spread across the ciphertext.
- Modes of operation define how a block cipher processes messages longer than one block.

