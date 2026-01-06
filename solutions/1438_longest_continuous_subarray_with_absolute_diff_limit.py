"""
Problem: Longest Continuous Subarray With Absolute Diff Limit
Link: https://leetcode.com/problems/longest-continuous-subarray-with-absolute-diff-limit/

Given an array of integers nums and an integer limit, return the size of the
longest non-empty subarray such that the absolute difference between any two
elements of this subarray is less than or equal to limit.

Example 1:
    Input: nums = [8,2,4,7], limit = 4
    Output: 2
    Explanation: All subarrays are:
    [8] max - min = 0
    [8,2] max - min = 6 > 4
    [8,2,4] max - min = 6 > 4
    ...
    [2,4] max - min = 2 <= 4 (longest valid subarray)

Example 2:
    Input: nums = [10,1,2,4,7,2], limit = 5
    Output: 4
    Explanation: [2,4,7,2] is longest, max - min = 5 <= 5

Example 3:
    Input: nums = [4,2,2,2,4,4,2,2], limit = 0
    Output: 3

Constraints:
- 1 <= nums.length <= 10^5
- 1 <= nums[i] <= 10^9
- 0 <= limit <= 10^9

Topics: Array, Queue, Sliding Window, Heap (Priority Queue), Monotonic Queue
"""

import json
from collections import deque
from typing import List

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionTwoDeques",
        "method": "longestSubarray",
        "complexity": "O(n) time, O(n) space",
        "description": "Two monotonic deques for max and min tracking",
    },
    "two_deques": {
        "class": "SolutionTwoDeques",
        "method": "longestSubarray",
        "complexity": "O(n) time, O(n) space",
        "description": "Two monotonic deques for max and min tracking",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual is the correct longest subarray length.

    Args:
        actual: Program output (int as string or int)
        expected: Expected output (None if from generator)
        input_data: Raw input string (JSON array and limit)

    Returns:
        bool: True if correct length
    """
    lines = input_data.strip().split("\n")
    nums = json.loads(lines[0]) if lines[0] else []
    limit = int(lines[1])

    # Compute correct answer using reference solution
    correct = _reference_longest_subarray(nums, limit)

    # Parse actual output
    if isinstance(actual, int):
        actual_val = actual
    else:
        actual_str = str(actual).strip()
        try:
            actual_val = int(actual_str)
        except ValueError:
            return False

    return actual_val == correct


def _reference_longest_subarray(nums: List[int], limit: int) -> int:
    """O(n) reference using two monotonic deques."""
    if not nums:
        return 0

    max_dq: deque[int] = deque()  # Decreasing: front is max
    min_dq: deque[int] = deque()  # Increasing: front is min
    left = 0
    result = 0

    for right, num in enumerate(nums):
        # Maintain max deque (decreasing)
        while max_dq and nums[max_dq[-1]] < num:
            max_dq.pop()
        max_dq.append(right)

        # Maintain min deque (increasing)
        while min_dq and nums[min_dq[-1]] > num:
            min_dq.pop()
        min_dq.append(right)

        # Shrink window if constraint violated
        while nums[max_dq[0]] - nums[min_dq[0]] > limit:
            left += 1
            if max_dq[0] < left:
                max_dq.popleft()
            if min_dq[0] < left:
                min_dq.popleft()

        result = max(result, right - left + 1)

    return result


JUDGE_FUNC = judge


# ============================================================================
# Solution 1: Two Monotonic Deques (Max + Min)
# Time: O(n), Space: O(n)
#   - One deque maintains decreasing order (front is max)
#   - One deque maintains increasing order (front is min)
#   - Shrink window from left when max - min > limit
#
# Key Insight: The absolute difference between ANY two elements in a subarray
# equals max - min of that subarray. So we need to track both simultaneously.
# ============================================================================
class SolutionTwoDeques:
    def longestSubarray(self, nums: List[int], limit: int) -> int:
        if not nums:
            return 0

        # Deques store indices; front is max/min for current window
        max_deque: deque[int] = deque()  # Decreasing values
        min_deque: deque[int] = deque()  # Increasing values
        left = 0
        max_length = 0

        for right, num in enumerate(nums):
            # Maintain max deque: remove smaller elements from back
            while max_deque and nums[max_deque[-1]] < num:
                max_deque.pop()
            max_deque.append(right)

            # Maintain min deque: remove larger elements from back
            while min_deque and nums[min_deque[-1]] > num:
                min_deque.pop()
            min_deque.append(right)

            # Shrink window while constraint is violated
            while nums[max_deque[0]] - nums[min_deque[0]] > limit:
                left += 1
                # Remove stale indices from front
                if max_deque[0] < left:
                    max_deque.popleft()
                if min_deque[0] < left:
                    min_deque.popleft()

            # Update maximum length
            max_length = max(max_length, right - left + 1)

        return max_length


def solve():
    """
    Input format (JSON):
        Line 1: nums as JSON array
        Line 2: limit as integer

    Output format:
        Integer representing longest subarray length
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    nums = json.loads(lines[0])
    limit = int(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.longestSubarray(nums, limit)

    print(result)


if __name__ == "__main__":
    solve()
