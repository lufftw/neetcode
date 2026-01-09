"""
LeetCode 746: Min Cost Climbing Stairs
https://leetcode.com/problems/min-cost-climbing-stairs/

Pattern: DP 1D Linear - Min Cost Path
API Kernel: DP1DLinear

You are given an integer array cost where cost[i] is the cost of ith step on a staircase.
Once you pay the cost, you can either climb one or two steps.
You can either start from the step with index 0, or the step with index 1.
Return the minimum cost to reach the top of the floor.
"""

import json
import sys
from typing import List

from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionDP",
        "method": "minCostClimbingStairs",
        "complexity": "O(n) time, O(1) space",
        "description": "Space-optimized DP tracking min cost to each step",
    },
    "dp_space_optimized": {
        "class": "SolutionDP",
        "method": "minCostClimbingStairs",
        "complexity": "O(n) time, O(1) space",
        "description": "Space-optimized using only two variables",
    },
    "dp_array": {
        "class": "SolutionDPArray",
        "method": "minCostClimbingStairs",
        "complexity": "O(n) time, O(n) space",
        "description": "Full DP array, easier to understand",
    },
    "memoization": {
        "class": "SolutionMemoization",
        "method": "minCostClimbingStairs",
        "complexity": "O(n) time, O(n) space",
        "description": "Top-down recursive DP with memoization",
    },
}


def _reference_min_cost(cost: List[int]) -> int:
    """Reference implementation for validation."""
    n = len(cost)
    if n <= 1:
        return 0

    prev2, prev1 = 0, 0
    for i in range(2, n + 1):
        current = min(prev1 + cost[i - 1], prev2 + cost[i - 2])
        prev2, prev1 = prev1, current

    return prev1


def judge(actual, expected, input_data: str) -> bool:
    """Custom judge using reference implementation."""
    cost = json.loads(input_data.strip())
    correct = _reference_min_cost(cost)
    try:
        actual_val = int(actual) if isinstance(actual, str) else actual
        return actual_val == correct
    except (ValueError, TypeError):
        return False


JUDGE_FUNC = judge


class SolutionDP:
    """
    Space-optimized DP solution.

    dp[i] = minimum cost to reach step i
    dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2])

    Base cases: dp[0] = 0, dp[1] = 0 (can start at index 0 or 1 for free)
    Goal: dp[n] (reach beyond the last step)
    """

    def minCostClimbingStairs(self, cost: List[int]) -> int:
        """
        Find minimum cost to reach the top of the staircase.

        Core insight: To reach step i, we must come from i-1 or i-2, paying that
        step's cost. dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2]).
        Can start at index 0 or 1 for free, so dp[0] = dp[1] = 0.

        Invariant: prev1 = min cost to reach step i-1, prev2 = min cost to reach i-2.

        Args:
            cost: Cost of each step

        Returns:
            Minimum cost to reach the top (beyond last step)
        """
        n = len(cost)
        if n <= 1:
            return 0

        prev2, prev1 = 0, 0
        for i in range(2, n + 1):
            current = min(prev1 + cost[i - 1], prev2 + cost[i - 2])
            prev2, prev1 = prev1, current

        return prev1


class SolutionDPArray:
    """
    Full DP array solution.

    dp[i] = minimum cost to reach step i
    Easier to understand and debug than space-optimized version.
    """

    def minCostClimbingStairs(self, cost: List[int]) -> int:
        """
        Find minimum cost using full DP array.

        Core insight: Same recurrence as space-optimized, but keep full array
        for easier understanding. dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2]).

        Invariant: dp[i] = minimum cost to reach step i.

        Args:
            cost: Cost of each step

        Returns:
            Minimum cost to reach the top
        """
        n = len(cost)
        if n <= 1:
            return 0

        dp = [0] * (n + 1)
        # dp[0] = dp[1] = 0: can start at index 0 or 1 for free

        for i in range(2, n + 1):
            dp[i] = min(dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2])

        return dp[n]


class SolutionMemoization:
    """
    Top-down recursive DP with memoization.

    More intuitive: directly models the decision at each step.
    """

    def minCostClimbingStairs(self, cost: List[int]) -> int:
        """
        Find minimum cost using top-down memoization.

        Core insight: min_cost(i) = cost to reach step i, recursively defined
        as min(min_cost(i-1) + cost[i-1], min_cost(i-2) + cost[i-2]).
        Memoize to avoid recomputation.

        Args:
            cost: Cost of each step

        Returns:
            Minimum cost to reach the top
        """
        n = len(cost)
        if n <= 1:
            return 0

        memo = {}

        def min_cost(i: int) -> int:
            """Minimum cost to reach step i."""
            if i <= 1:
                return 0  # Can start at 0 or 1 for free

            if i in memo:
                return memo[i]

            result = min(
                min_cost(i - 1) + cost[i - 1],
                min_cost(i - 2) + cost[i - 2]
            )
            memo[i] = result
            return result

        return min_cost(n)


def solve():
    lines = sys.stdin.read().strip().split("\n")

    cost = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.minCostClimbingStairs(cost)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
