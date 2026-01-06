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
        n = len(cost)
        if n <= 1:
            return 0

        prev2, prev1 = 0, 0
        for i in range(2, n + 1):
            current = min(prev1 + cost[i - 1], prev2 + cost[i - 2])
            prev2, prev1 = prev1, current

        return prev1


def solve():
    lines = sys.stdin.read().strip().split("\n")

    cost = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.minCostClimbingStairs(cost)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
