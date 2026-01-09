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
    "dp_1d": {
        "class": "SolutionDP",
        "method": "canPartition",
        "complexity": "O(n * target) time, O(target) space",
        "description": "Space-optimized 1D DP, canonical 0/1 knapsack",
    },
    "dp_2d": {
        "class": "SolutionDP2D",
        "method": "canPartition",
        "complexity": "O(n * target) time, O(n * target) space",
        "description": "Full 2D DP table, easier to understand",
    },
    "memoization": {
        "class": "SolutionMemoization",
        "method": "canPartition",
        "complexity": "O(n * target) time, O(n * target) space",
        "description": "Top-down recursive DP with memoization",
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
        """
        Determine if array can be partitioned into two equal-sum subsets.

        Core insight: Transform to "can we select a subset summing to total/2?"
        This is 0/1 knapsack boolean DP. Backward iteration ensures each number
        is used at most once.

        Invariant: dp[s] = True iff sum s is achievable using a subset of
        numbers processed so far.

        Args:
            nums: Array of positive integers

        Returns:
            True if equal partition exists
        """
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


class SolutionDP2D:
    """
    Full 2D DP table for 0/1 Knapsack.

    dp[i][s] = True if we can achieve sum s using first i numbers.
    More space but easier to understand and debug.
    """

    def canPartition(self, nums: List[int]) -> bool:
        """
        Determine if array can be partitioned using 2D DP table.

        Core insight: Same as 1D but explicitly track which items are considered.
        dp[i][s] = dp[i-1][s] (skip nums[i-1]) OR dp[i-1][s-nums[i-1]] (take it).

        Args:
            nums: Array of positive integers

        Returns:
            True if equal partition exists
        """
        total = sum(nums)
        if total % 2 != 0:
            return False

        target = total // 2
        n = len(nums)

        # dp[i][s] = can we make sum s using first i items?
        dp = [[False] * (target + 1) for _ in range(n + 1)]

        # Base case: sum 0 is always achievable (empty subset)
        for i in range(n + 1):
            dp[i][0] = True

        for i in range(1, n + 1):
            num = nums[i - 1]
            for s in range(target + 1):
                # Option 1: don't take current number
                dp[i][s] = dp[i - 1][s]
                # Option 2: take current number (if possible)
                if s >= num:
                    dp[i][s] = dp[i][s] or dp[i - 1][s - num]

        return dp[n][target]


class SolutionMemoization:
    """
    Top-down recursive DP with memoization.

    More intuitive: directly models the decision at each step.
    """

    def canPartition(self, nums: List[int]) -> bool:
        """
        Determine if array can be partitioned using top-down memoization.

        Core insight: At each index, decide to include or exclude the number.
        Memoize (index, remaining_sum) pairs to avoid recomputation.

        Args:
            nums: Array of positive integers

        Returns:
            True if equal partition exists
        """
        total = sum(nums)
        if total % 2 != 0:
            return False

        target = total // 2
        memo = {}

        def dp(index: int, remaining: int) -> bool:
            """Can we make 'remaining' sum using nums[index:]?"""
            if remaining == 0:
                return True
            if index >= len(nums) or remaining < 0:
                return False

            if (index, remaining) in memo:
                return memo[(index, remaining)]

            # Try including or excluding current number
            result = dp(index + 1, remaining - nums[index]) or dp(index + 1, remaining)

            memo[(index, remaining)] = result
            return result

        return dp(0, target)


def solve():
    lines = sys.stdin.read().strip().split("\n")

    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.canPartition(nums)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
