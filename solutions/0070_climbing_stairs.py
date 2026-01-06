"""
LeetCode 70: Climbing Stairs
https://leetcode.com/problems/climbing-stairs/

Pattern: DP 1D Linear - Fibonacci-Style (Count Ways)
API Kernel: DP1DLinear

You are climbing a staircase. It takes n steps to reach the top.
Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?
"""

import json
import sys
from typing import List

from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionDP",
        "method": "climbStairs",
        "complexity": "O(n) time, O(1) space",
        "description": "Space-optimized DP using two variables",
    },
}


def _reference_climb_stairs(n: int) -> int:
    """Reference implementation for validation."""
    if n <= 2:
        return n
    prev2, prev1 = 1, 2
    for _ in range(3, n + 1):
        prev2, prev1 = prev1, prev2 + prev1
    return prev1


def judge(actual, expected, input_data: str) -> bool:
    """Custom judge using reference implementation."""
    n = json.loads(input_data.strip())
    correct = _reference_climb_stairs(n)
    try:
        actual_val = int(actual) if isinstance(actual, str) else actual
        return actual_val == correct
    except (ValueError, TypeError):
        return False


JUDGE_FUNC = judge


class SolutionDP:
    """
    Space-optimized DP solution.

    The number of ways to reach step n equals the sum of ways to reach
    step n-1 (then take 1 step) and step n-2 (then take 2 steps).

    dp[n] = dp[n-1] + dp[n-2]

    This is the Fibonacci sequence: 1, 2, 3, 5, 8, 13, ...
    """

    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n

        prev2, prev1 = 1, 2
        for _ in range(3, n + 1):
            prev2, prev1 = prev1, prev2 + prev1

        return prev1


def solve():
    lines = sys.stdin.read().strip().split("\n")

    n = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.climbStairs(n)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
