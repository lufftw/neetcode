"""
Problem: Shortest Subarray with Sum at Least K
Link: https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/

Given an integer array nums and an integer k, return the length of the
shortest non-empty subarray of nums with a sum of at least k. If there is
no such subarray, return -1.

A subarray is a contiguous part of an array.

Example 1:
    Input: nums = [1], k = 1
    Output: 1

Example 2:
    Input: nums = [1,2], k = 4
    Output: -1

Example 3:
    Input: nums = [2,-1,2], k = 3
    Output: 3

Constraints:
- 1 <= nums.length <= 10^5
- -10^5 <= nums[i] <= 10^5
- 1 <= k <= 10^9

Topics: Array, Binary Search, Queue, Sliding Window, Heap, Prefix Sum, Monotonic Queue
"""

import json
from collections import deque
from typing import List

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionMonotonicDeque",
        "method": "shortestSubarray",
        "complexity": "O(n) time, O(n) space",
        "description": "Prefix sum with monotonic increasing deque",
    },
    "deque": {
        "class": "SolutionMonotonicDeque",
        "method": "shortestSubarray",
        "complexity": "O(n) time, O(n) space",
        "description": "Prefix sum with monotonic increasing deque",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual is the correct shortest subarray length.

    Args:
        actual: Program output (int as string or int)
        expected: Expected output (None if from generator)
        input_data: Raw input string (JSON array and k)

    Returns:
        bool: True if correct length
    """
    lines = input_data.strip().split("\n")
    nums = json.loads(lines[0]) if lines[0] else []
    k = int(lines[1])

    # Compute correct answer using reference solution
    correct = _reference_shortest_subarray(nums, k)

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


def _reference_shortest_subarray(nums: List[int], k: int) -> int:
    """O(n) reference using prefix sum and monotonic deque."""
    n = len(nums)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]

    dq: deque[int] = deque()  # Indices with increasing prefix values
    result = float("inf")

    for j in range(n + 1):
        # Try to find valid subarray ending at j
        while dq and prefix[j] - prefix[dq[0]] >= k:
            result = min(result, j - dq.popleft())

        # Maintain increasing order of prefix sums
        while dq and prefix[dq[-1]] >= prefix[j]:
            dq.pop()

        dq.append(j)

    return result if result != float("inf") else -1


JUDGE_FUNC = judge


# ============================================================================
# Solution 1: Prefix Sum with Monotonic Increasing Deque
# Time: O(n), Space: O(n)
#   - Prefix sum converts to: sum(nums[i:j]) = prefix[j] - prefix[i]
#   - For each j, find smallest i where prefix[j] - prefix[i] >= k
#   - Maintain increasing deque of prefix sums
#
# Key Insight: With negative numbers, simple sliding window doesn't work.
# If prefix[i1] >= prefix[i2] where i1 < i2, then i1 is dominated because
# using i2 gives both a larger sum difference AND a shorter subarray.
# ============================================================================
class SolutionMonotonicDeque:
    def shortestSubarray(self, nums: List[int], k: int) -> int:
        n = len(nums)

        # Build prefix sum array: prefix[i] = sum(nums[0:i])
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + nums[i]

        # Deque stores indices with increasing prefix values
        candidates: deque[int] = deque()
        min_length = float("inf")

        for j in range(n + 1):
            # 1. Find valid subarrays: prefix[j] - prefix[i] >= k
            #    Once found, pop the starting index (won't give shorter answer later)
            while candidates and prefix[j] - prefix[candidates[0]] >= k:
                min_length = min(min_length, j - candidates.popleft())

            # 2. Maintain increasing order of prefix sums
            #    Remove larger prefix values (dominated by current)
            while candidates and prefix[candidates[-1]] >= prefix[j]:
                candidates.pop()

            candidates.append(j)

        return min_length if min_length != float("inf") else -1


def solve():
    """
    Input format (JSON):
        Line 1: nums as JSON array
        Line 2: k as integer

    Output format:
        Integer representing shortest subarray length, or -1 if not found
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    nums = json.loads(lines[0])
    k = int(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.shortestSubarray(nums, k)

    print(result)


if __name__ == "__main__":
    solve()
