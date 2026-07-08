class Bits:
    """
    A class to represent a mutable sequence of bits.
    """

    def __init__(self, value, length=None):
        self.bits = []
        if isinstance(value, list) or isinstance(value, tuple):
            self.bits = [bool(bit) for bit in value]
        elif isinstance(value, int):
            bin_value = bin(value)[2:]
            self.bits = [bool(int(bit)) for bit in bin_value.zfill(length or len(bin_value))]
        elif isinstance(value, bytes):
            self.bits = [bool((value[i // 8] >> (7 - (i % 8))) & 1) for i in range(len(value) * 8)]
        else:
            raise ValueError("Unsupported value type")

    def __getitem__(self, index):
        if isinstance(index, slice):
            return Bits(self.bits[index])
        return self.bits[index]

    def __setitem__(self, index, value):
        self.bits[index] = bool(value)

    def parity_bit(self):
        return sum(self.bits) % 2

    def __len__(self):
        return len(self.bits)

    def __str__(self):
        return ''.join('1' if bit else '0' for bit in self.bits)

    def __repr__(self):
        return f"Bits({str(self)})"

    def append(self, bit):
        self.bits.append(bool(bit))

    def pop(self, index=-1):
        return self.bits.pop(index)

    def __xor__(self, other):
        """Compute the bitwise XOR between two Bits objects."""
        max_len = max(len(self), len(other))
        
        # Pad the shorter sequence with False (representing 0) to match lengths
        self_bits_padded = self.bits + [False] * (max_len - len(self))
        other_bits_padded = other.bits + [False] * (max_len - len(other))

        return Bits([b1 ^ b2 for b1, b2 in zip(self_bits_padded, other_bits_padded)])

    def __and__(self, other):
        if len(self) != len(other):
            raise ValueError("Bits sequences must be of the same length for AND operation.")
        return Bits([b1 & b2 for b1, b2 in zip(self.bits, other.bits)])

    def __add__(self, other):
        return Bits(self.bits + other.bits)

    def __mul__(self, scalar):
        return Bits(self.bits * scalar)

    def copy(self):
        return Bits(self.bits.copy())

    def to_bytes(self):
        byte_array = []
        for i in range(0, len(self.bits), 8):
            byte_value = 0
            chunk = self.bits[i:i + 8]
            for j, bit in enumerate(chunk):
                byte_value |= (int(bit) << (7 - j))
            byte_array.append(byte_value)
        return bytes(byte_array)
