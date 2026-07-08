# Substitution Cipher Project

This project explores classical substitution ciphers and basic cryptanalysis. It includes Caesar encryption/decryption, monoalphabetic substitution, frequency analysis, and affine ciphers.

## Files

| File | Purpose |
|---|---|
| `substitution_ciphers.ipynb` | Notebook walkthrough with explanations and experiments |
| `substitution_ciphers.py` | Reusable Python implementations |
| `ciphertext_caesar.txt` | Caesar-cipher challenge text |
| `ciphertext_simple.txt` | Monoalphabetic substitution challenge text |
| `ciphertext_affine.txt` | Affine-cipher challenge text |
| `wikipedia_cybersecurity.txt` | Reference text used for language-frequency analysis |
| `distribution_pickle.pkl` | Saved distribution data used by the notebook |

## Main Ideas

- Caesar shifts are easy to break by brute force.
- Simple substitution ciphers preserve letter-frequency patterns.
- Affine ciphers can be attacked by trying the valid key space.

