"""
Problem: Ugly Number III
Link: https://leetcode.com/problems/ugly-number-iii/

An ugly number is a positive integer that is divisible by a, b, or c.

Given four integers n, a, b, and c, return the n-th ugly number.

Example 1:
    Input: n = 3, a = 2, b = 3, c = 5
    Output: 4
    Explanation: The ugly numbers are 2, 3, 4, 5, 6, 8, 9, 10... The 3rd is 4.

Example 2:
    Input: n = 4, a = 2, b = 3, c = 4
    Output: 6
    Explanation: The ugly numbers are 2, 3, 4, 6, 8, 9, 10, 12... The 4th is 6.

Example 3:
    Input: n = 5, a = 2, b = 11, c = 13
    Output: 10
    Explanation: The ugly numbers are 2, 4, 6, 8, 10, 11, 12, 13... The 5th is 10.

Constraints:
- 1 <= n, a, b, c <= 10^9
- 1 <= a * b * c <= 10^18
- It is guaranteed that the result will be in range [1, 2 * 10^9].

Topics: Math, Binary Search, Number Theory
"""
from math import gcd
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "nthUglyNumber",
        "complexity": "O(log(max_val)) time, O(1) space",
        "description": "Binary search with inclusion-exclusion principle",
    },
}


# ============================================================================
# Solution: Binary Search with Inclusion-Exclusion Principle
# Time: O(log(max_val)), Space: O(1) where max_val = 2 * 10^9
#
# Key insight: We can binary search for the answer. For any number x, we can
# count how many ugly numbers are <= x using the inclusion-exclusion principle.
#
# Count of numbers divisible by a OR b OR c:
# = |A| + |B| + |C| - |A∩B| - |A∩C| - |B∩C| + |A∩B∩C|
# = x/a + x/b + x/c - x/lcm(a,b) - x/lcm(a,c) - x/lcm(b,c) + x/lcm(a,b,c)
#
# Binary search: find smallest x such that count(x) >= n
# ============================================================================
class Solution:
    def nthUglyNumber(self, n: int, a: int, b: int, c: int) -> int:
        """
        Find the n-th ugly number divisible by a, b, or c.

        Uses binary search on the answer space [1, 2*10^9].
        For each candidate x, count ugly numbers <= x using inclusion-exclusion.
        Find the smallest x where count >= n.

        Args:
            n: Which ugly number to find
            a, b, c: Divisors that define ugly numbers

        Returns:
            The n-th ugly number
        """
        def lcm(x: int, y: int) -> int:
            """Compute least common multiple of x and y."""
            return x * y // gcd(x, y)

        # Precompute LCMs for efficiency
        ab = lcm(a, b)
        ac = lcm(a, c)
        bc = lcm(b, c)
        abc = lcm(ab, c)

        def count_ugly(x: int) -> int:
            """
            Count ugly numbers <= x using inclusion-exclusion.

            |A ∪ B ∪ C| = |A| + |B| + |C| - |A∩B| - |A∩C| - |B∩C| + |A∩B∩C|
            """
            return (x // a + x // b + x // c
                    - x // ab - x // ac - x // bc
                    + x // abc)

        # Binary search for smallest x where count_ugly(x) >= n
        lo, hi = 1, 2 * 10**9

        while lo < hi:
            mid = (lo + hi) // 2
            if count_ugly(mid) >= n:
                hi = mid
            else:
                lo = mid + 1

        return lo


def solve():
    """
    Input format:
    Line 1: n (integer)
    Line 2: a (integer)
    Line 3: b (integer)
    Line 4: c (integer)
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')

    n = json.loads(lines[0])
    a = json.loads(lines[1])
    b = json.loads(lines[2])
    c = json.loads(lines[3])

    solver = get_solver(SOLUTIONS)
    result = solver.nthUglyNumber(n, a, b, c)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
