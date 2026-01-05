"""
Problem: Continuous Subarray Sum
Link: https://leetcode.com/problems/continuous-subarray-sum/

Given an integer array nums and an integer k, return true if nums has a good
subarray or false otherwise.

A good subarray is a subarray where:
- its length is at least two, and
- the sum of the elements of the subarray is a multiple of k.

Note: A subarray is a contiguous part of the array.

Example 1:
    Input: nums = [23,2,4,6,7], k = 6
    Output: true
    Explanation: [2, 4] is a continuous subarray of size 2 whose elements
                 sum up to 6.

Example 2:
    Input: nums = [23,2,6,4,7], k = 6
    Output: true
    Explanation: [23, 2, 6, 4, 7] is a continuous subarray of size 5 whose
                 elements sum up to 42, which is a multiple of 6.

Example 3:
    Input: nums = [23,2,6,4,7], k = 13
    Output: false

Constraints:
- 1 <= nums.length <= 10^5
- 0 <= nums[i] <= 10^9
- 0 <= sum(nums[i]) <= 2^31 - 1
- 1 <= k <= 2^31 - 1

Topics: Array, Hash Table, Math, Prefix Sum
"""

import json
from typing import List

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionPrefixMod",
        "method": "checkSubarraySum",
        "complexity": "O(n) time, O(min(n,k)) space",
        "description": "Prefix sum modulo k with hash map tracking remainders",
    },
    "prefix_mod": {
        "class": "SolutionPrefixMod",
        "method": "checkSubarraySum",
        "complexity": "O(n) time, O(min(n,k)) space",
        "description": "Prefix sum modulo k with hash map tracking remainders",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate result: check if good subarray exists."""
    lines = input_data.strip().split("\n")
    nums = json.loads(lines[0])
    k = int(lines[1])

    correct = _reference_check_subarray_sum(nums, k)

    if isinstance(actual, bool):
        return actual == correct

    if isinstance(actual, str):
        actual_lower = actual.strip().lower()
        if actual_lower == "true":
            return correct is True
        elif actual_lower == "false":
            return correct is False

    return False


def _reference_check_subarray_sum(nums: List[int], k: int) -> bool:
    """O(n) reference using prefix sum modulo."""
    prefix_mod = 0
    first_occurrence: dict[int, int] = {0: -1}

    for i, num in enumerate(nums):
        prefix_mod = (prefix_mod + num) % k

        if prefix_mod in first_occurrence:
            if i - first_occurrence[prefix_mod] >= 2:
                return True
        else:
            first_occurrence[prefix_mod] = i

    return False


JUDGE_FUNC = judge


# ============================================================================
# Solution: Prefix Sum Modulo K
# Time: O(n), Space: O(min(n, k))
#
# Mathematical Foundation:
#   For sum(nums[i+1..j]) to be a multiple of k:
#       (prefix[j] - prefix[i]) % k == 0
#   This is equivalent to:
#       prefix[j] % k == prefix[i] % k
#
#   So if two prefix sums have the same remainder when divided by k,
#   the subarray between them has a sum that's a multiple of k.
#
# Why Track Remainders (Not Full Sums):
#   - Full prefix sums can grow to 2^31, requiring O(n) space for unique values
#   - Remainders are in range [0, k-1], so at most k unique values
#   - Space complexity: O(min(n, k))
#
# Length Constraint (>= 2):
#   We need j - i >= 2, so we track FIRST occurrence of each remainder.
#   Only count as valid if current_index - first_occurrence >= 2.
#   This is why we DON'T update first_occurrence when remainder already exists.
#
# Initialization {0: -1}:
#   If prefix_mod == 0 at index j >= 1, subarray nums[0..j] has sum divisible by k.
#   Length = j - (-1) = j + 1 >= 2 when j >= 1.
#
# Pattern: prefix_sum_modular_arithmetic
# See: docs/patterns/prefix_sum/templates.md Section 4 (Continuous Subarray Sum)
# ============================================================================
class SolutionPrefixMod:
    def checkSubarraySum(self, nums: List[int], k: int) -> bool:
        """
        Check if array contains a subarray of length >= 2 with sum divisible by k.

        Key insight: If prefix[j] % k == prefix[i] % k with j - i >= 2,
        then subarray (i, j] has sum divisible by k.
        """
        prefix_mod = 0

        # Map: remainder -> first index where this remainder occurred
        # {0: -1} handles subarray starting from index 0
        first_occurrence: dict[int, int] = {0: -1}

        for current_index, num in enumerate(nums):
            # Update prefix sum modulo k
            # Using modulo keeps values bounded and captures divisibility
            prefix_mod = (prefix_mod + num) % k

            if prefix_mod in first_occurrence:
                # Same remainder found at earlier position
                # Check if subarray length >= 2
                subarray_length = current_index - first_occurrence[prefix_mod]
                if subarray_length >= 2:
                    return True
                # Note: Do NOT update first_occurrence here!
                # We keep the earliest index to maximize potential subarray length
            else:
                # Record first occurrence of this remainder
                first_occurrence[prefix_mod] = current_index

        return False


def solve():
    """
    Input format (JSON per line):
        Line 1: nums as JSON array
        Line 2: k as integer

    Output format:
        true or false
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    nums = json.loads(lines[0])
    k = int(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.checkSubarraySum(nums, k)

    print("true" if result else "false")


if __name__ == "__main__":
    solve()
