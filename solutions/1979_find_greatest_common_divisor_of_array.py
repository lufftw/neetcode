"""
LeetCode 1979: Find Greatest Common Divisor of Array
https://leetcode.com/problems/find-greatest-common-divisor-of-array/

Pattern: Math / Number Theory - GCD
API Kernel: MathNumberTheory

Given an integer array nums, return the greatest common divisor of the
smallest number and largest number in nums.
"""

import json
import math
import sys
from typing import List

from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionMath",
        "method": "findGCD",
        "complexity": "O(n + log(min(a,b))) time, O(1) space",
        "description": "Find min/max then compute GCD using Euclidean algorithm",
    },
}


def _reference_gcd(nums: List[int]) -> int:
    """Reference implementation for validation."""
    return math.gcd(min(nums), max(nums))


def judge(actual, expected, input_data: str) -> bool:
    """Custom judge using reference implementation."""
    nums = json.loads(input_data.strip())
    correct = _reference_gcd(nums)
    try:
        actual_val = int(actual) if isinstance(actual, str) else actual
        return actual_val == correct
    except (ValueError, TypeError):
        return False


JUDGE_FUNC = judge


class SolutionMath:
    """
    Find GCD of min and max elements.

    GCD computed using Euclidean algorithm: gcd(a, b) = gcd(b, a % b)
    Python's math.gcd handles this efficiently.
    """

    def findGCD(self, nums: List[int]) -> int:
        return math.gcd(min(nums), max(nums))


def solve():
    lines = sys.stdin.read().strip().split("\n")

    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.findGCD(nums)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
