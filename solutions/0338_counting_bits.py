# solutions/0338_counting_bits.py
"""
Problem 0338 - Counting Bits

Given an integer n, return an array ans of length n + 1 such that
for each i (0 <= i <= n), ans[i] is the number of 1's in the binary
representation of i.

LeetCode Constraints:
- 0 <= n <= 10^5

Key Insight:
We can use previously computed results to avoid redundant work.
The number of 1's in i relates to smaller numbers by two key observations:

1. i >> 1 (right shift): i and i>>1 have same bits except possibly LSB
   So: countBits(i) = countBits(i >> 1) + (i & 1)

2. i & (i-1) (clear lowest set bit): removes exactly one 1-bit
   So: countBits(i) = countBits(i & (i-1)) + 1

Both give O(n) DP solutions with different intuitions.

Solution Approaches:
1. DP with right shift: ans[i] = ans[i >> 1] + (i & 1)
2. DP with lowest bit removal: ans[i] = ans[i & (i-1)] + 1
3. Brian Kernighan for each number: O(n * popcount) naively
"""
from typing import List
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionDPShift",
        "method": "countBits",
        "complexity": "O(n) time, O(n) space",
        "description": "DP using right shift: ans[i] = ans[i>>1] + (i&1)",
    },
    "dp_lowest": {
        "class": "SolutionDPLowestBit",
        "method": "countBits",
        "complexity": "O(n) time, O(n) space",
        "description": "DP using lowest bit removal: ans[i] = ans[i&(i-1)] + 1",
    },
}


class SolutionDPShift:
    """
    DP using right shift relation.

    Observation: i and i >> 1 (integer division by 2) have the same
    binary representation except for the least significant bit.

    Examples:
    - 6 = 110, 6 >> 1 = 3 = 011 (same except LSB)
    - 7 = 111, 7 >> 1 = 3 = 011 (same except LSB)

    So popcount(i) = popcount(i >> 1) + (i & 1)
    where (i & 1) checks if LSB is 1.

    We can fill the array in order since i >> 1 < i for all i > 0.
    """

    def countBits(self, n: int) -> List[int]:
        ans = [0] * (n + 1)

        for i in range(1, n + 1):
            # Count for i/2 (already computed) + LSB of i
            ans[i] = ans[i >> 1] + (i & 1)

        return ans


class SolutionDPLowestBit:
    """
    DP using lowest set bit removal.

    Key insight: i & (i - 1) clears the lowest set bit of i.

    Example:
    - 12 = 1100, 11 = 1011, 12 & 11 = 1000 = 8
    - The operation turned off the rightmost 1

    So popcount(i) = popcount(i & (i-1)) + 1

    This is valid because i & (i-1) < i, so we've already computed
    that value when processing in order.

    Alternative perspective: we're counting how many times we can
    apply the "remove lowest bit" operation until we reach 0.
    """

    def countBits(self, n: int) -> List[int]:
        ans = [0] * (n + 1)

        for i in range(1, n + 1):
            # Count for (i with lowest bit removed) + 1
            ans[i] = ans[i & (i - 1)] + 1

        return ans


def solve():
    import sys
    import json

    data = sys.stdin.read().strip()
    n = int(data)

    solver = get_solver(SOLUTIONS)
    result = solver.countBits(n)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
