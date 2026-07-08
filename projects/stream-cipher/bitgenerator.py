from lfsr import LFSR
from bits import Bits


class AlternatingStep:
    """
    Alternating-Step Generator using three LFSRs:
    - lfsrC (control): decides which of lfsr0 or lfsr1 is clocked
    - lfsr0, lfsr1: data registers
    Output bit is XOR of lfsr0 and lfsr1 outputs with irregular clocking.
    """
    def __init__(self, seed=None, polyC=None, poly0=None, poly1=None):
        # Set default polynomials
        polyC = polyC if polyC is not None else [0, 2, 5]  # x^5 + x^2 + 1
        poly0 = poly0 if poly0 is not None else [0, 1, 3]  # x^3 + x + 1
        poly1 = poly1 if poly1 is not None else [0, 1, 4]  # x^4 + x + 1

        # Determine register lengths
        lenC = max(polyC)
        len0 = max(poly0)
        len1 = max(poly1)

        # Prepare seed bits
        if seed is None:
            seed_bits = [True] * (lenC + len0 + len1)
        else:
            bits_obj = Bits(seed) if not isinstance(seed, Bits) else seed
            seed_bits = bits_obj.bits
            if len(seed_bits) < lenC + len0 + len1:
                raise ValueError("Seed too short for the required LFSR lengths")

        # Partition seed for each LFSR
        stateC = seed_bits[:lenC]
        state0 = seed_bits[lenC:lenC + len0]
        state1 = seed_bits[lenC + len0:lenC + len0 + len1]

        # Initialize LFSRs
        self.lfsrC = LFSR(polyC, stateC)
        self.lfsr0 = LFSR(poly0, state0)
        self.lfsr1 = LFSR(poly1, state1)

        # Prime the outputs of data registers
        self.lfsr0_output = next(self.lfsr0)
        self.lfsr1_output = next(self.lfsr1)
        self.output = None

    def __iter__(self):
        return self

    def __next__(self):
        # Clock control LFSR
        control = next(self.lfsrC)

        # Clock one data LFSR based on control bit
        if control:
            # Clock lfsr0; lfsr1 holds
            self.lfsr0_output = next(self.lfsr0)
        else:
            # Clock lfsr1; lfsr0 holds
            self.lfsr1_output = next(self.lfsr1)

        # XOR the outputs of both data LFSRs
        self.output = self.lfsr0_output ^ self.lfsr1_output
        return self.output
