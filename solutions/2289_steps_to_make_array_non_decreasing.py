"""
Problem: Steps to Make Array Non-decreasing
Link: https://leetcode.com/problems/steps-to-make-array-non-decreasing/

In one step, remove all elements nums[i] where nums[i-1] > nums[i].
Find total steps until array is non-decreasing.

Constraints:
- 1 <= nums.length <= 10^5
- 1 <= nums[i] <= 10^9

Topics: Array, Stack, Monotonic Stack
"""
from typing import List
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "totalSteps",
        "complexity": "O(n) time, O(n) space",
        "description": "Monotonic stack tracking removal steps",
    },
}


# JUDGE_FUNC for generated tests
def _reference(nums: List[int]) -> int:
    """Reference implementation using monotonic stack."""
    n = len(nums)
    # dp[i] = step at which nums[i] is removed (0 if not removed)
    dp = [0] * n
    stack = []  # stack of indices

    result = 0

    for i in range(n):
        step = 0
        # Pop all elements smaller than nums[i]
        while stack and nums[stack[-1]] <= nums[i]:
            # The popped element would be removed before or same time as current
            step = max(step, dp[stack.pop()])

        if stack:
            # nums[i] will be removed by nums[stack[-1]] at step+1
            dp[i] = step + 1
            result = max(result, dp[i])

        stack.append(i)

    return result


def judge(actual, expected, input_data: str) -> bool:
    import json
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
# Solution: Monotonic Stack with Step Tracking
# Time: O(n), Space: O(n)
#   - Each element pushed/popped once
#   - Track when each element gets removed
# ============================================================================
class Solution:
    # Key insight: Element i is removed when a greater element to its left
    # "reaches" it through removals
    #
    # For each element:
    #   - Pop all smaller/equal elements from stack (they're removed first)
    #   - The max removal step among popped elements determines when
    #     the current element can be removed (one step after)
    #   - If stack is not empty, current element will be removed
    #
    # Stack maintains decreasing sequence of surviving elements

    def totalSteps(self, nums: List[int]) -> int:
        n = len(nums)
        dp = [0] * n  # dp[i] = step when nums[i] is removed
        stack = []     # stack of indices (decreasing values)

        result = 0

        for i in range(n):
            step = 0
            # Pop elements that will be removed before current
            while stack and nums[stack[-1]] <= nums[i]:
                step = max(step, dp[stack.pop()])

            if stack:
                # Current element will be removed by stack[-1]
                # It happens one step after all between them are removed
                dp[i] = step + 1
                result = max(result, dp[i])

            stack.append(i)

        return result


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: nums (JSON array)

    Example:
        [5,3,4,4,7,3,6,11,8,5,11]
        -> 3
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')
    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.totalSteps(nums)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
