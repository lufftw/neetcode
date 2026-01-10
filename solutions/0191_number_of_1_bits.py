# solutions/0191_number_of_1_bits.py
"""
Problem 0191 - Number of 1 Bits (Hamming Weight)

Write a function that takes the binary representation of an unsigned integer
and returns the number of '1' bits it has (also known as the Hamming weight).

LeetCode Constraints:
- The input must be a binary string of length 32

Key Insight:
The Hamming weight counts set bits. Several approaches exist:

1. Iterate through 32 bits: check each bit with (n >> i) & 1
2. Brian Kernighan: n & (n-1) clears lowest set bit, count iterations
3. Built-in: bin(n).count('1') - leverages optimized library code

Brian Kernighan is optimal when few bits are set, as it only iterates
k times where k = number of 1 bits.

Solution Approaches:
1. Brian Kernighan's algorithm: O(k) time where k = popcount
2. Iterate through 32 bits: O(32) = O(1) time
"""
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionKernighan",
        "method": "hammingWeight",
        "complexity": "O(k) time, O(1) space",
        "description": "Brian Kernighan: n & (n-1) clears lowest set bit",
    },
    "iterate": {
        "class": "SolutionIterate",
        "method": "hammingWeight",
        "complexity": "O(32) time, O(1) space",
        "description": "Check each of 32 bits individually",
    },
}


class SolutionKernighan:
    """
    Brian Kernighan's algorithm.

    Key insight: n & (n - 1) clears the lowest set bit of n.

    Example:
    - n = 12 = 1100
    - n - 1 = 11 = 1011
    - n & (n-1) = 1000 = 8 (lowest set bit cleared)

    Count how many times we can apply this until n becomes 0.
    Each application removes exactly one 1-bit.

    Time: O(k) where k is the number of 1 bits
    Best case: O(1) when n = 0
    Worst case: O(32) when all bits are set
    """

    def hammingWeight(self, n: int) -> int:
        count = 0
        while n:
            n &= (n - 1)  # Clear lowest set bit
            count += 1
        return count


class SolutionIterate:
    """
    Iterate through all 32 bits.

    Check each bit position by ANDing with 1 after right-shifting.
    This is a straightforward approach that always takes 32 iterations.

    Alternative: AND with powers of 2 (1, 2, 4, ...) to check each bit.

    Time: O(32) = O(1) - fixed number of iterations
    """

    def hammingWeight(self, n: int) -> int:
        count = 0
        for _ in range(32):
            count += n & 1
            n >>= 1
        return count


def solve():
    import sys

    data = sys.stdin.read().strip()

    # Input can be binary string or integer
    if len(data) == 32 and all(c in "01" for c in data):
        # Raw binary string
        n = int(data, 2)
    else:
        n = int(data)

    solver = get_solver(SOLUTIONS)
    result = solver.hammingWeight(n)

    print(result)


if __name__ == "__main__":
    solve()
