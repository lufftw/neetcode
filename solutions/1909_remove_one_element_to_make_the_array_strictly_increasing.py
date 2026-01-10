"""
Problem: Remove One Element to Make the Array Strictly Increasing
Link: https://leetcode.com/problems/remove-one-element-to-make-the-array-strictly-increasing/

Check if removing exactly one element makes array strictly increasing.

Constraints:
- 2 <= nums.length <= 1000
- 1 <= nums[i] <= 10^9

Topics: Array
"""
from typing import List
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "canBeIncreasing",
        "complexity": "O(n) time, O(1) space",
        "description": "Find first violation, try removing either element",
    },
}


# JUDGE_FUNC for generated tests
def _reference(nums: List[int]) -> bool:
    """Reference implementation using brute force."""
    n = len(nums)
    for skip in range(n):
        valid = True
        prev = -1
        for i in range(n):
            if i == skip:
                continue
            if nums[i] <= prev:
                valid = False
                break
            prev = nums[i]
        if valid:
            return True
    return False


def judge(actual, expected, input_data: str) -> bool:
    nums = json.loads(input_data.strip())
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(nums)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Find Violation and Try Removals
# Time: O(n), Space: O(1)
# ============================================================================
class Solution:
    # Key insight: Find the first index i where nums[i] >= nums[i+1].
    # At this "violation point", we must remove either nums[i] or nums[i+1].
    #
    # After removing, check if remaining array is strictly increasing.
    # If either removal works, return True.
    #
    # Edge case: Already strictly increasing (no violation) -> True.

    def canBeIncreasing(self, nums: List[int]) -> bool:
        n = len(nums)

        def is_strictly_increasing_after_skip(skip_idx: int) -> bool:
            """Check if array is strictly increasing after skipping one index."""
            prev = -1  # Sentinel since nums[i] >= 1
            for i in range(n):
                if i == skip_idx:
                    continue
                if nums[i] <= prev:
                    return False
                prev = nums[i]
            return True

        # Find first violation: nums[i] >= nums[i+1]
        for i in range(n - 1):
            if nums[i] >= nums[i + 1]:
                # Try removing nums[i] or nums[i+1]
                return (is_strictly_increasing_after_skip(i) or
                        is_strictly_increasing_after_skip(i + 1))

        # No violation found - already strictly increasing
        return True


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: nums (JSON array)

    Example:
        [1,2,10,5,7]
        -> true
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.canBeIncreasing(nums)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
