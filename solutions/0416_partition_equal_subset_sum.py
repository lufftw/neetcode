"""
LeetCode 416: Partition Equal Subset Sum
https://leetcode.com/problems/partition-equal-subset-sum/

Pattern: DP Knapsack/Subset - 0/1 Knapsack Boolean
API Kernel: DPKnapsackSubset

Given an integer array nums, return true if you can partition the array into two
subsets such that the sum of the elements in both subsets is equal, or false otherwise.
"""

import json
import sys
from typing import List

from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionDP",
        "method": "canPartition",
        "complexity": "O(n * target) time, O(target) space",
        "description": "0/1 Knapsack boolean DP with backward iteration",
    },
}


def _reference_can_partition(nums: List[int]) -> bool:
    """Reference implementation for validation."""
    total = sum(nums)
    if total % 2 != 0:
        return False

    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True

    for num in nums:
        for s in range(target, num - 1, -1):
            dp[s] = dp[s] or dp[s - num]

    return dp[target]


def judge(actual, expected, input_data: str) -> bool:
    """Custom judge using reference implementation."""
    nums = json.loads(input_data.strip())
    correct = _reference_can_partition(nums)
    try:
        if isinstance(actual, str):
            actual_val = actual.lower() == "true"
        else:
            actual_val = bool(actual)
        return actual_val == correct
    except (ValueError, TypeError):
        return False


JUDGE_FUNC = judge


class SolutionDP:
    """
    0/1 Knapsack Boolean DP.

    Problem transforms to: Can we select a subset that sums to total/2?

    dp[s] = True if sum s is achievable using some subset
    dp[s] = dp[s] OR dp[s - num]

    Key insight: Iterate backwards to ensure each num is used at most once.
    """

    def canPartition(self, nums: List[int]) -> bool:
        total = sum(nums)
        if total % 2 != 0:
            return False

        target = total // 2
        dp = [False] * (target + 1)
        dp[0] = True

        for num in nums:
            # Backwards to ensure 0/1 property (each num used at most once)
            for s in range(target, num - 1, -1):
                dp[s] = dp[s] or dp[s - num]

        return dp[target]


def solve():
    lines = sys.stdin.read().strip().split("\n")

    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.canPartition(nums)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
