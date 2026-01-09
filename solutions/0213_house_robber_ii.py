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
    "dp_decomposition": {
        "class": "SolutionDP",
        "method": "rob",
        "complexity": "O(n) time, O(1) space",
        "description": "Space-optimized DP with circular decomposition",
    },
    "memoization": {
        "class": "SolutionMemoization",
        "method": "rob",
        "complexity": "O(n) time, O(n) space",
        "description": "Top-down recursive DP with memoization",
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
        """
        Find maximum money robbing non-adjacent houses arranged in a circle.

        Core insight: Since first and last houses are adjacent in circle, we can't
        rob both. Decompose into two linear problems: (1) houses 0 to n-2 (exclude last),
        (2) houses 1 to n-1 (exclude first). Answer is max of both cases.

        Invariant: Each linear subproblem maintains the House Robber I invariant;
        the circular constraint is handled by case decomposition.

        Args:
            nums: Money in each house (circular arrangement)

        Returns:
            Maximum money that can be robbed
        """
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


class SolutionMemoization:
    """
    Top-down recursive DP with memoization.

    Same circular decomposition, but using memoization for linear subproblems.
    """

    def rob(self, nums: List[int]) -> int:
        """
        Find maximum robbery using top-down memoization.

        Core insight: Same decomposition as iterative DP - handle circular
        constraint by solving two linear problems. Each linear problem uses
        memoization: rob(i) = max(rob(i+1), nums[i] + rob(i+2)).

        Args:
            nums: Money in each house (circular arrangement)

        Returns:
            Maximum money that can be robbed
        """
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]
        if len(nums) == 2:
            return max(nums)

        def rob_linear_memo(arr: List[int]) -> int:
            memo = {}

            def dp(i: int) -> int:
                """Max robbery from houses i to end."""
                if i >= len(arr):
                    return 0

                if i in memo:
                    return memo[i]

                # Either skip this house or rob it
                result = max(dp(i + 1), arr[i] + dp(i + 2))
                memo[i] = result
                return result

            return dp(0)

        return max(rob_linear_memo(nums[:-1]), rob_linear_memo(nums[1:]))


def solve():
    lines = sys.stdin.read().strip().split("\n")

    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.rob(nums)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
