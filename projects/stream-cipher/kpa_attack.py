from bits import Bits
from lfsr import LFSR, berlekamp_massey

def kpa_attack(ciphertext_bits, known_plaintext_bits):
    """
    Perform a Known Plaintext Attack to decrypt the full ciphertext.
    
    Args:
        ciphertext_bits (Bits): The full ciphertext bits from ciphertext.bin
        known_plaintext_bits (Bits): The known initial plaintext bits from known-plaintext.txt

    Returns:
        tuple(str, list): (Recovered plaintext as UTF-8 string, Recovered feedback polynomial taps)
    """
    # Step 1: Recover part of the keystream
    known_ciphertext_part = ciphertext_bits[:len(known_plaintext_bits)]
    recovered_keystream = known_ciphertext_part ^ known_plaintext_bits

    # Step 2: Run Berlekamp-Massey on the recovered keystream
    feedback_poly, lfsr_length = berlekamp_massey(recovered_keystream.bits)

    if lfsr_length == 0:
        raise ValueError("Failed to recover LFSR structure. Not enough known plaintext.")

    # Step 3: Recover initial state (first lfsr_length bits of recovered keystream)
    initial_state = recovered_keystream.bits[:lfsr_length]

    # Step 4: Build the recovered LFSR
    lfsr = LFSR(feedback_poly, state=initial_state)

    # Step 5: Generate full keystream
    full_keystream = lfsr.run_steps(len(ciphertext_bits))

    # Step 6: Decrypt the full ciphertext
    recovered_plaintext_bits = ciphertext_bits ^ full_keystream

    # Step 7: Convert recovered plaintext bits into bytes and decode as UTF-8
    recovered_plaintext_bytes = recovered_plaintext_bits.to_bytes()
    recovered_plaintext = recovered_plaintext_bytes.decode('utf-8', errors='replace')

    return recovered_plaintext, feedback_poly
