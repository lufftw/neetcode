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
    "dp_space_optimized": {
        "class": "SolutionDP",
        "method": "climbStairs",
        "complexity": "O(n) time, O(1) space",
        "description": "Canonical bottom-up DP with O(1) space",
    },
    "dp_array": {
        "class": "SolutionDPArray",
        "method": "climbStairs",
        "complexity": "O(n) time, O(n) space",
        "description": "Bottom-up DP with full array, easier to understand",
    },
    "memoization": {
        "class": "SolutionMemoization",
        "method": "climbStairs",
        "complexity": "O(n) time, O(n) space",
        "description": "Top-down recursive DP with memoization",
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
        """
        Count distinct ways to climb n stairs taking 1 or 2 steps at a time.

        Core insight: Ways to reach step n = ways to reach (n-1) + ways to reach (n-2),
        since we can arrive from either. This is exactly the Fibonacci sequence.
        Space-optimize by keeping only the last two values.

        Invariant: prev1 = ways to reach step i-1, prev2 = ways to reach step i-2.

        Args:
            n: Number of stairs to climb

        Returns:
            Number of distinct ways to reach the top
        """
        if n <= 2:
            return n

        prev2, prev1 = 1, 2
        for _ in range(3, n + 1):
            prev2, prev1 = prev1, prev2 + prev1

        return prev1


class SolutionDPArray:
    """
    Bottom-up DP with full array.

    Easier to understand than space-optimized version.
    dp[i] represents the number of ways to reach step i.
    """

    def climbStairs(self, n: int) -> int:
        """
        Count ways using full DP array.

        Core insight: Same recurrence dp[i] = dp[i-1] + dp[i-2],
        but store all values in an array for clarity.

        Args:
            n: Number of stairs to climb

        Returns:
            Number of distinct ways to reach the top
        """
        if n <= 2:
            return n

        dp = [0] * (n + 1)
        dp[1] = 1
        dp[2] = 2

        for i in range(3, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]

        return dp[n]


class SolutionMemoization:
    """
    Top-down recursive DP with memoization.

    Natural recursive thinking: to reach step n, we can come from
    step n-1 or step n-2. Memoization avoids recomputation.
    """

    def climbStairs(self, n: int) -> int:
        """
        Count ways using top-down memoization.

        Core insight: Recursive definition matches problem structure.
        climbStairs(n) = climbStairs(n-1) + climbStairs(n-2).
        Memoize to avoid exponential recomputation.

        Args:
            n: Number of stairs to climb

        Returns:
            Number of distinct ways to reach the top
        """
        memo = {}

        def dp(step: int) -> int:
            if step <= 2:
                return step
            if step in memo:
                return memo[step]

            memo[step] = dp(step - 1) + dp(step - 2)
            return memo[step]

        return dp(n)


def solve():
    lines = sys.stdin.read().strip().split("\n")

    n = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.climbStairs(n)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
