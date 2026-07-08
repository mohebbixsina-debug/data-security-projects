# Stream Cipher Project

This project studies stream ciphers built from linear feedback shift registers. It includes bit manipulation utilities, LFSR generation, Berlekamp-Massey recovery, an alternating-step generator, and a known-plaintext attack demo.

## Files

| File | Purpose |
|---|---|
| `stream_ciphers.ipynb` | Notebook walkthrough with explanations and experiments |
| `bits.py` | Mutable bit-sequence helper |
| `lfsr.py` | LFSR implementation and Berlekamp-Massey algorithm |
| `bitgenerator.py` | Alternating-step generator |
| `kpa_attack.py` | Known-plaintext attack helper |
| `binary_sequence.bin` | Sample binary sequence |
| `ciphertext.bin` | Ciphertext used in the attack demo |
| `known-plaintext.txt` | Known plaintext fragment |

## Main Ideas

- LFSRs generate deterministic binary streams from a compact state.
- Berlekamp-Massey can recover the shortest LFSR for a binary sequence.
- If part of the plaintext is known, a stream cipher can leak enough keystream to support recovery attacks.

