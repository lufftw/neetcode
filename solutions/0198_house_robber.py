"""
LeetCode 198: House Robber
https://leetcode.com/problems/house-robber/

Pattern: DP 1D Linear - Include/Exclude
API Kernel: DP1DLinear

You are a professional robber planning to rob houses along a street.
Each house has a certain amount of money stashed. Adjacent houses have
security systems connected - if two adjacent houses are broken into on
the same night, it will alert the police.

Given an integer array nums representing the amount of money of each house,
return the maximum amount of money you can rob tonight without alerting the police.
"""

import json
import sys
from typing import List

from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionDP",
        "method": "rob",
        "complexity": "O(n) time, O(1) space",
        "description": "Space-optimized DP with include/exclude decision",
    },
    "dp_space_optimized": {
        "class": "SolutionDP",
        "method": "rob",
        "complexity": "O(n) time, O(1) space",
        "description": "Canonical bottom-up DP with O(1) space",
    },
    "dp_array": {
        "class": "SolutionDPArray",
        "method": "rob",
        "complexity": "O(n) time, O(n) space",
        "description": "Bottom-up DP with full array, easier to understand",
    },
    "memoization": {
        "class": "SolutionMemoization",
        "method": "rob",
        "complexity": "O(n) time, O(n) space",
        "description": "Top-down recursive DP with memoization",
    },
}


def _reference_rob(nums: List[int]) -> int:
    """Reference implementation for validation."""
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]

    prev2 = nums[0]
    prev1 = max(nums[0], nums[1])

    for i in range(2, len(nums)):
        current = max(prev1, prev2 + nums[i])
        prev2, prev1 = prev1, current

    return prev1


def judge(actual, expected, input_data: str) -> bool:
    """Custom judge using reference implementation."""
    nums = json.loads(input_data.strip())
    correct = _reference_rob(nums)
    try:
        actual_val = int(actual) if isinstance(actual, str) else actual
        return actual_val == correct
    except (ValueError, TypeError):
        return False


JUDGE_FUNC = judge


class SolutionDP:
    """
    Space-optimized DP solution using include/exclude pattern.

    dp[i] = maximum money robbed from houses 0 to i
    dp[i] = max(dp[i-1], dp[i-2] + nums[i])
        - dp[i-1]: skip house i
        - dp[i-2] + nums[i]: rob house i (can't rob i-1)

    Base cases:
        dp[0] = nums[0]
        dp[1] = max(nums[0], nums[1])
    """

    def rob(self, nums: List[int]) -> int:
        """
        Find maximum money robbing non-adjacent houses.

        Core insight: At each house, choose max of (skip it, rob it). If we rob house i,
        we add nums[i] to best result excluding house i-1. The recurrence is:
        dp[i] = max(dp[i-1], dp[i-2] + nums[i]).

        Invariant: prev1 = max profit from houses 0..i-1, prev2 = max profit from 0..i-2.

        Args:
            nums: Money in each house

        Returns:
            Maximum money that can be robbed
        """
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]

        prev2 = nums[0]
        prev1 = max(nums[0], nums[1])

        for i in range(2, len(nums)):
            current = max(prev1, prev2 + nums[i])
            prev2, prev1 = prev1, current

        return prev1


class SolutionDPArray:
    """
    Bottom-up DP with full array.

    Easier to understand than space-optimized version.
    dp[i] represents the maximum money robbed from houses 0 to i.
    """

    def rob(self, nums: List[int]) -> int:
        """
        Find maximum money using full DP array.

        Core insight: Same recurrence dp[i] = max(dp[i-1], dp[i-2] + nums[i]),
        but store all values in an array for clarity.

        Args:
            nums: Money in each house

        Returns:
            Maximum money that can be robbed
        """
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]

        n = len(nums)
        dp = [0] * n
        dp[0] = nums[0]
        dp[1] = max(nums[0], nums[1])

        for i in range(2, n):
            dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])

        return dp[n - 1]


class SolutionMemoization:
    """
    Top-down recursive DP with memoization.

    Natural recursive thinking: for each house, decide to rob it or skip it.
    If we rob house i, we can't rob house i-1.
    """

    def rob(self, nums: List[int]) -> int:
        """
        Find maximum money using top-down memoization.

        Core insight: Define subproblem as "max money from houses i to n-1".
        At each house: max(skip it, rob it + solve remaining).
        Memoize to avoid exponential recomputation.

        Args:
            nums: Money in each house

        Returns:
            Maximum money that can be robbed
        """
        if not nums:
            return 0

        memo = {}

        def dp(i: int) -> int:
            if i >= len(nums):
                return 0
            if i in memo:
                return memo[i]

            # Choice: skip house i, or rob house i (then skip i+1)
            memo[i] = max(dp(i + 1), nums[i] + dp(i + 2))
            return memo[i]

        return dp(0)


def solve():
    lines = sys.stdin.read().strip().split("\n")

    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.rob(nums)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
