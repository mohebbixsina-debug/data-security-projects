from bits import Bits

class LFSR:
    def __init__(self, poly, state=None):
        # poly: set of degrees where the feedback taps are
        self.poly = set(poly)
        self.length = max(self.poly)  # polynomial degree
        if self.length <= 0:
            raise ValueError("LFSR polynomial must have positive degree.")

        if state is None:
            self.state = Bits([1] * self.length)  # default: all ones
        elif isinstance(state, Bits):
            if len(state) < self.length:
                raise ValueError("Initial state is shorter than the LFSR degree.")
            self.state = Bits(state.bits[:self.length])
        else:
            self.state = Bits(state, length=self.length)
            if len(self.state) < self.length:
                raise ValueError("Initial state is shorter than the LFSR degree.")
            if len(self.state) > self.length:
                self.state = Bits(self.state.bits[:self.length])
        
        self.output = self.state[0]  # output: first bit
        self.feedback = None  # last feedback bit

    def __iter__(self):
        return self

    def __str__(self):
        return (f"LFSR(poly={sorted(self.poly, reverse=True)}, "
                f"state={self.state}, output={int(self.output)})")

    def __next__(self):
        # Calculate feedback bit
        self.feedback = False
        for deg in self.poly:
            if deg == 0:
                self.feedback ^= True  # constant term (1)
            else:
                self.feedback ^= self.state[self.length - deg]

        self.output = self.state[0]  # Output before shift

        # Shift left and insert feedback at the end
        for i in range(self.length - 1):
            self.state[i] = self.state[i + 1]
        self.state[-1] = self.feedback

        return self.output

    def run_steps(self, N=1, state=None):
        """Run N steps and return output bits."""
        if state is not None:
            saved_state = self.state
            self.state = Bits(state, length=self.length)

        outputs = []
        for _ in range(N):
            outputs.append(int(next(self)))
        
        if state is not None:
            self.state = saved_state  # restore previous state

        return Bits(outputs)

    def cycle(self, state=None):
        """Run until the initial state is reached again and return the cycle."""
        if state is not None:
            saved_state = self.state
            self.state = Bits(state, length=self.length)
        else:
            saved_state = self.state.copy()

        initial = str(self.state)
        cycle_bits = []

        while True:
            bit = next(self)
            cycle_bits.append(int(bit))
            if str(self.state) == initial:
                break

        if state is not None:
            self.state = saved_state  # restore previous state

        return Bits(cycle_bits)

#berlekamp_massey:

def berlekamp_massey(bits):
    '''Finds the shortest LFSR (feedback polynomial) for the given bit sequence.'''
    n = len(bits)
    P = [0]  # P(x) = 1
    Q = [0]  # Q(x) = 1
    m = 0
    r = 1

    def get_bit(seq, idx):
        return seq[idx] if idx >= 0 else 0

    for t in range(n):
        # Calculate discrepancy d
        d = 0 
        for j in P:
            d ^= get_bit(bits, t - j)
        #case A:
        if d == 1: 
            if 2 * m <= t:
                R = P.copy()
                # P(x) = P(x) + Q(x) * x^r
                P = list(set(P) ^ set([q + r for q in Q]))
                Q = R
                m = t + 1 - m
                r = 0
        #case B:
            else: #case A
                # P(x) = P(x) + Q(x) * x^r
                P = list(set(P) ^ set([q + r for q in Q]))
        r += 1

    P.sort()
    return P, m

