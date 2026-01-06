"""
LeetCode 494: Target Sum
https://leetcode.com/problems/target-sum/

Pattern: DP Knapsack/Subset - 0/1 Knapsack Count with Transformation
API Kernel: DPKnapsackSubset

You are given an integer array nums and an integer target.
You want to build an expression out of nums by adding one of the symbols '+' and '-'
before each integer in nums and then concatenate all the integers.

Return the number of different expressions that you can build, which evaluates to target.
"""

import json
import sys
from typing import List

from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionDP",
        "method": "findTargetSumWays",
        "complexity": "O(n * target) time, O(target) space",
        "description": "Transform to subset sum count problem",
    },
}


def _reference_target_sum(nums: List[int], target: int) -> int:
    """Reference implementation for validation."""
    total = sum(nums)

    # P - N = target, P + N = total -> P = (target + total) / 2
    if (total + target) % 2 != 0 or total + target < 0:
        return 0

    subset_target = (total + target) // 2

    dp = [0] * (subset_target + 1)
    dp[0] = 1

    for num in nums:
        for s in range(subset_target, num - 1, -1):
            dp[s] += dp[s - num]

    return dp[subset_target]


def judge(actual, expected, input_data: str) -> bool:
    """Custom judge using reference implementation."""
    lines = input_data.strip().split("\n")
    nums = json.loads(lines[0])
    target = json.loads(lines[1])
    correct = _reference_target_sum(nums, target)
    try:
        actual_val = int(actual) if isinstance(actual, str) else actual
        return actual_val == correct
    except (ValueError, TypeError):
        return False


JUDGE_FUNC = judge


class SolutionDP:
    """
    Transform target sum to subset count.

    Let P = sum of nums with '+', N = sum of nums with '-'
    P - N = target
    P + N = total
    Adding: 2P = target + total -> P = (target + total) / 2

    So we need to count subsets that sum to (target + total) / 2.
    """

    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        total = sum(nums)

        # Check if solution exists
        if (total + target) % 2 != 0 or total + target < 0:
            return 0

        subset_target = (total + target) // 2

        dp = [0] * (subset_target + 1)
        dp[0] = 1

        for num in nums:
            # Backwards for 0/1 property
            for s in range(subset_target, num - 1, -1):
                dp[s] += dp[s - num]

        return dp[subset_target]


def solve():
    lines = sys.stdin.read().strip().split("\n")

    nums = json.loads(lines[0])
    target = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.findTargetSumWays(nums, target)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
