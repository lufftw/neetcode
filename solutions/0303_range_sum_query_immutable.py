"""
Problem: Range Sum Query - Immutable
Link: https://leetcode.com/problems/range-sum-query-immutable/

Given an integer array nums, handle multiple queries of the following type:
Calculate the sum of the elements of nums between indices left and right
inclusive where left <= right.

Implement the NumArray class:
- NumArray(int[] nums) Initializes the object with the integer array nums.
- int sumRange(int left, int right) Returns the sum of the elements of nums
  between indices left and right inclusive.

Example 1:
    Input: ["NumArray", "sumRange", "sumRange", "sumRange"]
           [[[-2, 0, 3, -5, 2, -1]], [0, 2], [2, 5], [0, 5]]
    Output: [null, 1, -1, -3]
    Explanation:
        NumArray numArray = new NumArray([-2, 0, 3, -5, 2, -1]);
        numArray.sumRange(0, 2); // return (-2) + 0 + 3 = 1
        numArray.sumRange(2, 5); // return 3 + (-5) + 2 + (-1) = -1
        numArray.sumRange(0, 5); // return (-2) + 0 + 3 + (-5) + 2 + (-1) = -3

Constraints:
- 1 <= nums.length <= 10^4
- -10^5 <= nums[i] <= 10^5
- 0 <= left <= right < nums.length
- At most 10^4 calls will be made to sumRange.

Topics: Array, Design, Prefix Sum
"""

import json
from typing import List


SOLUTIONS = {
    "default": {
        "class": "NumArray",
        "method": "sumRange",
        "complexity": "O(n) init, O(1) query, O(n) space",
        "description": "Prefix sum array for O(1) range sum queries",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result for design class problems.

    Args:
        actual: Program output (list of results)
        expected: Expected output (None if from generator)
        input_data: Raw input string

    Returns:
        bool: True if correct results
    """
    lines = input_data.strip().split("\n")
    commands = json.loads(lines[0])
    args_list = json.loads(lines[1])

    correct = _reference_solution(commands, args_list)

    if isinstance(actual, list):
        actual_list = actual
    else:
        actual_str = actual.strip()
        try:
            actual_list = json.loads(actual_str) if actual_str else []
        except (ValueError, json.JSONDecodeError):
            return False

    return actual_list == correct


def _reference_solution(commands: List[str], args_list: List[List]) -> List:
    """Reference implementation using prefix sum."""
    results = []
    obj = None

    for cmd, args in zip(commands, args_list):
        if cmd == "NumArray":
            obj = _RefNumArray(args[0])
            results.append(None)
        elif cmd == "sumRange":
            results.append(obj.sumRange(args[0], args[1]))

    return results


class _RefNumArray:
    """Reference implementation for validation."""

    def __init__(self, nums: List[int]):
        self.prefix = [0]
        for num in nums:
            self.prefix.append(self.prefix[-1] + num)

    def sumRange(self, left: int, right: int) -> int:
        return self.prefix[right + 1] - self.prefix[left]


JUDGE_FUNC = judge


# ============================================================================
# Solution: Prefix Sum Array (BASE TEMPLATE for PrefixSumRangeQuery)
# Time: O(n) initialization, O(1) per query
# Space: O(n) for prefix sum array
#
# Core Insight:
#   Any range sum [left, right] can be computed as the difference of two
#   prefix sums: prefix[right+1] - prefix[left].
#
# Why O(1) Query:
#   Without preprocessing, each sumRange requires O(right - left + 1) time.
#   With 10^4 queries on array of 10^4 elements, brute force is O(10^8).
#   Prefix sum reduces this to O(n + q) where q = number of queries.
#
# Prefix Array Convention:
#   prefix[i] = sum of elements nums[0..i-1] (elements BEFORE index i)
#   prefix[0] = 0 (empty prefix, crucial for handling left=0 case)
#   prefix[n] = sum of entire array
#
# Mathematical Derivation:
#   sum(nums[left..right]) = sum(nums[0..right]) - sum(nums[0..left-1])
#                          = prefix[right+1] - prefix[left]
#
# Pattern: prefix_sum_range_query
# See: docs/patterns/prefix_sum/templates.md Section 1 (Base Template)
# ============================================================================
class NumArray:
    """
    Range sum query data structure with O(n) preprocessing and O(1) queries.

    The prefix sum technique transforms repeated range sum queries from
    O(n) per query to O(1) per query at the cost of O(n) preprocessing.
    """

    def __init__(self, nums: List[int]):
        """
        Build prefix sum array in O(n) time.

        prefix[i] represents the sum of all elements before index i.
        This convention makes the range sum formula elegant:
        sum[left, right] = prefix[right+1] - prefix[left]
        """
        # Initialize with 0 for empty prefix (handles left=0 edge case)
        self.prefix_sum: List[int] = [0]

        # Build prefix sum: each element = previous sum + current number
        for num in nums:
            self.prefix_sum.append(self.prefix_sum[-1] + num)

    def sumRange(self, left: int, right: int) -> int:
        """
        Return sum of nums[left..right] in O(1) time.

        Uses the fundamental prefix sum identity:
        sum(nums[left..right]) = prefix[right+1] - prefix[left]

        Visual proof:
        prefix[right+1] = nums[0] + nums[1] + ... + nums[right]
        prefix[left]    = nums[0] + nums[1] + ... + nums[left-1]
        Difference      = nums[left] + ... + nums[right] ✓
        """
        return self.prefix_sum[right + 1] - self.prefix_sum[left]


def solve():
    """
    Input format (JSON per line):
        Line 1: List of commands ["NumArray", "sumRange", ...]
        Line 2: List of arguments [[[nums]], [left, right], ...]

    Output format:
        JSON array of results [null, result1, result2, ...]
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    commands = json.loads(lines[0])
    args_list = json.loads(lines[1])

    results = []
    obj = None

    for cmd, args in zip(commands, args_list):
        if cmd == "NumArray":
            obj = NumArray(args[0])
            results.append(None)
        elif cmd == "sumRange":
            results.append(obj.sumRange(args[0], args[1]))

    print(json.dumps(results))


if __name__ == "__main__":
    solve()
