"""
LeetCode 213: House Robber II
https://leetcode.com/problems/house-robber-ii/

Pattern: DP 1D Linear - Circular Array Decomposition
API Kernel: DP1DLinear

You are a professional robber planning to rob houses along a street.
Each house has a certain amount of money stashed. All houses at this place are arranged in a circle.
That means the first house is the neighbor of the last one. Meanwhile, adjacent houses have a
security system connected, and it will automatically contact the police if two adjacent houses
were broken into on the same night.

Return the maximum amount of money you can rob tonight without alerting the police.
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
        "description": "Decompose circular into two linear problems: exclude first or exclude last",
    },
}


def _rob_linear(nums: List[int]) -> int:
    """Helper: max non-adjacent sum for linear array."""
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


def _reference_rob_circular(nums: List[int]) -> int:
    """Reference implementation for validation."""
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    if len(nums) == 2:
        return max(nums)

    # Can't rob both first and last
    return max(_rob_linear(nums[:-1]), _rob_linear(nums[1:]))


def judge(actual, expected, input_data: str) -> bool:
    """Custom judge using reference implementation."""
    nums = json.loads(input_data.strip())
    correct = _reference_rob_circular(nums)
    try:
        actual_val = int(actual) if isinstance(actual, str) else actual
        return actual_val == correct
    except (ValueError, TypeError):
        return False


JUDGE_FUNC = judge


class SolutionDP:
    """
    Decompose circular array into two linear problems.

    Since houses form a circle, we can't rob both the first and last house.
    Two cases:
    1. Rob houses 0 to n-2 (exclude last)
    2. Rob houses 1 to n-1 (exclude first)

    Answer = max(case1, case2)
    """

    def rob(self, nums: List[int]) -> int:
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]
        if len(nums) == 2:
            return max(nums)

        def rob_linear(arr: List[int]) -> int:
            if len(arr) == 1:
                return arr[0]
            prev2 = arr[0]
            prev1 = max(arr[0], arr[1])
            for i in range(2, len(arr)):
                prev2, prev1 = prev1, max(prev1, prev2 + arr[i])
            return prev1

        return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))


def solve():
    lines = sys.stdin.read().strip().split("\n")

    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.rob(nums)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
