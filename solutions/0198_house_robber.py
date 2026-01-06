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


def solve():
    lines = sys.stdin.read().strip().split("\n")

    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.rob(nums)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
