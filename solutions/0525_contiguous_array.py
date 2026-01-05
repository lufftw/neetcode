"""
Problem: Contiguous Array
Link: https://leetcode.com/problems/contiguous-array/

Given a binary array nums, return the maximum length of a contiguous subarray
with an equal number of 0 and 1.

Example 1:
    Input: nums = [0,1]
    Output: 2
    Explanation: [0, 1] is the longest contiguous subarray with an equal
                 number of 0 and 1.

Example 2:
    Input: nums = [0,1,0]
    Output: 2
    Explanation: [0, 1] (or [1, 0]) is a longest contiguous subarray with
                 equal numbers of 0 and 1.

Constraints:
- 1 <= nums.length <= 10^5
- nums[i] is either 0 or 1.

Topics: Array, Hash Table, Prefix Sum
"""

import json
from typing import List

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionPrefixSum",
        "method": "findMaxLength",
        "complexity": "O(n) time, O(n) space",
        "description": "Transform: 0→-1, find longest subarray with sum 0",
    },
    "prefix": {
        "class": "SolutionPrefixSum",
        "method": "findMaxLength",
        "complexity": "O(n) time, O(n) space",
        "description": "Transform: 0→-1, find longest subarray with sum 0",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate result: maximum length of balanced subarray."""
    lines = input_data.strip().split("\n")
    nums = json.loads(lines[0])

    correct = _reference_find_max_length(nums)

    if isinstance(actual, int):
        return actual == correct

    try:
        actual_val = int(str(actual).strip())
        return actual_val == correct
    except (ValueError, TypeError):
        return False


def _reference_find_max_length(nums: List[int]) -> int:
    """O(n) reference using transformed prefix sum."""
    max_length = 0
    prefix_sum = 0
    first_occurrence: dict[int, int] = {0: -1}

    for i, num in enumerate(nums):
        prefix_sum += 1 if num == 1 else -1

        if prefix_sum in first_occurrence:
            max_length = max(max_length, i - first_occurrence[prefix_sum])
        else:
            first_occurrence[prefix_sum] = i

    return max_length


JUDGE_FUNC = judge


# ============================================================================
# Solution: Prefix Sum with Problem Transformation
# Time: O(n), Space: O(n)
#
# Problem Transformation (Key Insight):
#   Original problem: Find subarray with equal 0s and 1s
#   Transformed problem: Find subarray with sum = 0 (where 0 → -1, 1 → +1)
#
#   Why this works:
#   - If count(0) == count(1) in a subarray
#   - Then count(1) * (+1) + count(0) * (-1) = count(1) - count(0) = 0
#   - So subarray with equal 0s and 1s ↔ subarray with sum 0
#
# Algorithm:
#   Use prefix sum technique to find longest subarray with sum 0.
#   If prefix[j] == prefix[i], then subarray (i, j] has sum 0.
#   Track FIRST occurrence of each prefix sum (for longest subarray).
#
# Why Track First Occurrence (Not Last):
#   We want the LONGEST subarray. If prefix sum P appears at indices i1 < i2,
#   using i1 gives subarray length (j - i1), using i2 gives (j - i2).
#   Since i1 < i2, we get longer subarray by using i1 (first occurrence).
#
# Initialization {0: -1}:
#   If prefix_sum == 0 at index j, the entire subarray nums[0..j] is balanced.
#   Length = j - (-1) = j + 1. Without {0: -1}, we'd miss this case.
#
# Pattern: prefix_sum_transform
# See: docs/patterns/prefix_sum/templates.md Section 3 (Contiguous Array)
# ============================================================================
class SolutionPrefixSum:
    def findMaxLength(self, nums: List[int]) -> int:
        """
        Find longest contiguous subarray with equal 0s and 1s.

        Transform the problem: treat 0 as -1, then find longest subarray
        with sum 0 using prefix sum technique.
        """
        max_length = 0
        prefix_sum = 0

        # Map: prefix_sum value -> first index where this sum occurred
        # Initialize with {0: -1} to handle subarray starting from index 0
        first_occurrence: dict[int, int] = {0: -1}

        for current_index, num in enumerate(nums):
            # Transform: 0 contributes -1, 1 contributes +1
            # Equal 0s and 1s ⟺ transformed sum = 0
            prefix_sum += 1 if num == 1 else -1

            if prefix_sum in first_occurrence:
                # Found same prefix sum at earlier index
                # Subarray between them has sum 0 (equal 0s and 1s)
                subarray_length = current_index - first_occurrence[prefix_sum]
                max_length = max(max_length, subarray_length)
            else:
                # Record first occurrence (keep earliest for longest subarray)
                first_occurrence[prefix_sum] = current_index

        return max_length


def solve():
    """
    Input format (JSON per line):
        Line 1: nums as JSON array of 0s and 1s

    Output format:
        Integer maximum length of balanced subarray
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.findMaxLength(nums)

    print(result)


if __name__ == "__main__":
    solve()
