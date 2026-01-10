"""
Problem: Split the Array to Make Coprime Products
Link: https://leetcode.com/problems/split-the-array-to-make-coprime-products/

Find smallest index i where product(nums[0:i+1]) and product(nums[i+1:]) are coprime.

Constraints:
- 1 <= n <= 10^4
- 1 <= nums[i] <= 10^6

Topics: Array, Hash Table, Math, Number Theory
"""
from typing import List
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "findValidSplit",
        "complexity": "O(n * sqrt(M)) time, O(n + P) space",
        "description": "Track last occurrence of each prime factor",
    },
}


# JUDGE_FUNC for generated tests
def _reference(nums: List[int]) -> int:
    """Reference implementation."""
    n = len(nums)

    def factorize(x):
        factors = set()
        d = 2
        while d * d <= x:
            if x % d == 0:
                factors.add(d)
                while x % d == 0:
                    x //= d
            d += 1
        if x > 1:
            factors.add(x)
        return factors

    all_factors = [factorize(x) for x in nums]
    last_occurrence = {}
    for i in range(n):
        for p in all_factors[i]:
            last_occurrence[p] = i

    right_boundary = 0
    for i in range(n - 1):
        for p in all_factors[i]:
            right_boundary = max(right_boundary, last_occurrence[p])
        if right_boundary <= i:
            return i
    return -1


def judge(actual, expected, input_data: str) -> bool:
    nums = json.loads(input_data.strip())
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(nums)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Prime Factor Last Occurrence
# Time: O(n * sqrt(M)) where M is max value, Space: O(n + P) for factors
# ============================================================================
class Solution:
    # Key insight:
    #   - Two products are coprime iff they share no common prime factor
    #   - For each prime in left part, it must not appear in right part
    #   - Equivalently: all primes in left have last occurrence <= split index
    #
    # Algorithm:
    #   1. Factorize each number
    #   2. Track last occurrence index of each prime
    #   3. Sweep left to right, tracking max last occurrence (right_boundary)
    #   4. When right_boundary <= i, we found a valid split

    def findValidSplit(self, nums: List[int]) -> int:
        n = len(nums)

        def factorize(x: int) -> set:
            """Return set of prime factors."""
            factors = set()
            d = 2
            while d * d <= x:
                if x % d == 0:
                    factors.add(d)
                    while x % d == 0:
                        x //= d
                d += 1
            if x > 1:
                factors.add(x)
            return factors

        # Precompute factors for each number
        all_factors = [factorize(x) for x in nums]

        # For each prime, find its last occurrence
        last_occurrence = {}
        for i in range(n):
            for p in all_factors[i]:
                last_occurrence[p] = i

        # Find first valid split
        right_boundary = 0
        for i in range(n - 1):  # Can't split at last index
            for p in all_factors[i]:
                right_boundary = max(right_boundary, last_occurrence[p])
            if right_boundary <= i:
                return i

        return -1


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: nums (JSON array)

    Example:
        [4,7,8,15,3,5]
        -> 2
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.findValidSplit(nums)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
