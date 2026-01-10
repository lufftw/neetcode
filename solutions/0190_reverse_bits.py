# solutions/0190_reverse_bits.py
"""
Problem 0190 - Reverse Bits

Reverse bits of a given 32 bits unsigned integer.

Note that in some languages (like Java), there is no unsigned integer type.
The integer's internal binary representation is the same, whether signed or unsigned.

LeetCode Constraints:
- The input must be a binary string of length 32

Key Insight:
We need to reverse the bit positions, not the bit values.
Bit at position i should move to position (31 - i).

The simplest approach: iterate through each bit, extract it,
and place it in the reversed position of the result.

Solution Approaches:
1. Bit-by-bit iteration: O(32) = O(1) time, O(1) space
2. Divide and conquer (byte swap): O(1) time, O(1) space
3. Lookup table: O(1) time, O(256) space - good for repeated calls
"""
from typing import List
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionBitByBit",
        "method": "reverseBits",
        "complexity": "O(1) time, O(1) space",
        "description": "Iterate through 32 bits, build reversed result",
    },
    "divide_conquer": {
        "class": "SolutionDivideConquer",
        "method": "reverseBits",
        "complexity": "O(1) time, O(1) space",
        "description": "Swap halves recursively using bit masks",
    },
}


class SolutionBitByBit:
    """
    Bit-by-bit reversal approach.

    Process each of the 32 bits:
    1. Extract the rightmost bit of n using (n & 1)
    2. Add it to result (shifted to correct position)
    3. Shift n right to process next bit

    The result is built from MSB to LSB as we process n from LSB to MSB.

    Example: n = 0b1010
    - Iteration 0: extract 0, result = 0
    - Iteration 1: extract 1, result = 0b1 << 30 = 0b01...
    - etc.
    """

    def reverseBits(self, n: int) -> int:
        result = 0

        for i in range(32):
            # Extract rightmost bit of n
            bit = n & 1
            # Place it at position (31 - i) in result
            result |= bit << (31 - i)
            # Shift n right for next bit
            n >>= 1

        return result


class SolutionDivideConquer:
    """
    Divide and conquer using bit manipulation.

    Reverse by swapping progressively smaller groups:
    1. Swap adjacent 16-bit halves
    2. Swap adjacent 8-bit quarters within each half
    3. Swap adjacent 4-bit nibbles within each quarter
    4. Swap adjacent 2-bit pairs within each nibble
    5. Swap adjacent single bits within each pair

    Uses masks to isolate groups and shift to swap positions.

    This is analogous to how we might reverse a string by
    swapping first/last halves, then quarters, etc.
    """

    def reverseBits(self, n: int) -> int:
        # Swap adjacent 16-bit halves
        n = ((n & 0xFFFF0000) >> 16) | ((n & 0x0000FFFF) << 16)
        # Swap adjacent 8-bit bytes within each 16-bit half
        n = ((n & 0xFF00FF00) >> 8) | ((n & 0x00FF00FF) << 8)
        # Swap adjacent 4-bit nibbles within each byte
        n = ((n & 0xF0F0F0F0) >> 4) | ((n & 0x0F0F0F0F) << 4)
        # Swap adjacent 2-bit pairs within each nibble
        n = ((n & 0xCCCCCCCC) >> 2) | ((n & 0x33333333) << 2)
        # Swap adjacent single bits
        n = ((n & 0xAAAAAAAA) >> 1) | ((n & 0x55555555) << 1)

        return n


def solve():
    import sys
    import json

    data = sys.stdin.read().strip()

    # Input can be binary string (32 chars of 0/1) or integer
    if data.startswith('"'):
        # JSON-quoted binary string
        binary_str = json.loads(data)
        n = int(binary_str, 2)
    elif len(data) == 32 and all(c in "01" for c in data):
        # Raw binary string like "00000010100101000001111010011100"
        n = int(data, 2)
    else:
        # Decimal integer
        n = int(data)

    solver = get_solver(SOLUTIONS)
    result = solver.reverseBits(n)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
