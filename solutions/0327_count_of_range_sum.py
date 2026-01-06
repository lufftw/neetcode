"""
Problem: Count of Range Sum
Link: https://leetcode.com/problems/count-of-range-sum/

Given an integer array nums and two integers lower and upper, return the number
of range sums that lie in [lower, upper] inclusive.

Range sum S(i, j) is defined as the sum of the elements in nums between indices
i and j inclusive, where i <= j.

Example 1:
    Input: nums = [-2,5,-1], lower = -2, upper = 2
    Output: 3
    Explanation: The three ranges are: [0,0], [2,2], and [0,2]
                 and their respective sums are: -2, -1, 2.

Example 2:
    Input: nums = [0], lower = 0, upper = 0
    Output: 1

Constraints:
- 1 <= nums.length <= 10^5
- -2^31 <= nums[i] <= 2^31 - 1
- -10^5 <= lower <= upper <= 10^5
- The answer is guaranteed to fit in a 32-bit integer.

Topics: Array, Binary Search, Divide and Conquer, Binary Indexed Tree,
        Segment Tree, Merge Sort, Ordered Set
"""

import json
from typing import List

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionMergeSort",
        "method": "countRangeSum",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Merge sort with range counting using prefix sums",
    },
    "merge_sort": {
        "class": "SolutionMergeSort",
        "method": "countRangeSum",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Merge sort with range counting using prefix sums",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result.

    Args:
        actual: Program output (integer)
        expected: Expected output (None if from generator)
        input_data: Raw input string

    Returns:
        bool: True if correct
    """
    lines = input_data.strip().split("\n")
    nums = json.loads(lines[0])
    lower = json.loads(lines[1])
    upper = json.loads(lines[2])

    # Compute correct answer using reference solution
    correct = _reference_count_range_sum(nums, lower, upper)

    # Parse actual output
    if isinstance(actual, int):
        actual_val = actual
    else:
        actual_str = str(actual).strip()
        try:
            actual_val = int(actual_str)
        except (ValueError, TypeError):
            return False

    return actual_val == correct


def _reference_count_range_sum(nums: List[int], lower: int, upper: int) -> int:
    """Reference implementation using merge sort."""
    # Compute prefix sums
    prefix = [0]
    for num in nums:
        prefix.append(prefix[-1] + num)

    count = 0

    def merge_sort(arr: List[int]) -> List[int]:
        nonlocal count
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])
        return merge(left, right)

    def merge(left: List[int], right: List[int]) -> List[int]:
        nonlocal count

        # Count valid pairs
        j_low = j_high = 0
        for prefix_i in left:
            while j_low < len(right) and right[j_low] < prefix_i + lower:
                j_low += 1
            while j_high < len(right) and right[j_high] <= prefix_i + upper:
                j_high += 1
            count += j_high - j_low

        # Standard merge
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    merge_sort(prefix)
    return count


JUDGE_FUNC = judge


# ============================================================================
# Solution 1: Merge Sort with Range Counting
# Time: O(n log n), Space: O(n)
#
# Key Insight: For subarray sum in [lower, upper]:
#   lower <= prefix[j] - prefix[i] <= upper  (where i < j)
#   Rearranging: prefix[j] - upper <= prefix[i] <= prefix[j] - lower
#
# During merge sort, left array has smaller indices, right has larger.
# For each prefix[j] in right, count prefix[i] in left within range.
# ============================================================================
class SolutionMergeSort:
    def countRangeSum(self, nums: List[int], lower: int, upper: int) -> int:
        # Compute prefix sums
        prefix = [0]
        for num in nums:
            prefix.append(prefix[-1] + num)

        self.count = 0
        self.lower = lower
        self.upper = upper

        self._merge_sort(prefix)
        return self.count

    def _merge_sort(self, arr: List[int]) -> List[int]:
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = self._merge_sort(arr[:mid])
        right = self._merge_sort(arr[mid:])
        return self._merge(left, right)

    def _merge(self, left: List[int], right: List[int]) -> List[int]:
        # Count valid pairs: for each prefix_i in left, count prefix_j in right
        # such that prefix_i + lower <= prefix_j <= prefix_i + upper
        # Equivalently: lower <= prefix_j - prefix_i <= upper
        #
        # Since we want i < j (left has smaller indices), we count
        # prefix_j in right that fall in [prefix_i + lower, prefix_i + upper]

        j_low = j_high = 0
        for prefix_i in left:
            # Find range [prefix_i + lower, prefix_i + upper] in sorted right
            while j_low < len(right) and right[j_low] < prefix_i + self.lower:
                j_low += 1
            while j_high < len(right) and right[j_high] <= prefix_i + self.upper:
                j_high += 1
            self.count += j_high - j_low

        # Standard merge
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result


def solve():
    """
    Input format (JSON per line):
        Line 1: nums array
        Line 2: lower bound
        Line 3: upper bound

    Output format:
        Integer count
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    nums = json.loads(lines[0])
    lower = json.loads(lines[1])
    upper = json.loads(lines[2])

    solver = get_solver(SOLUTIONS)
    result = solver.countRangeSum(nums, lower, upper)

    print(result)


if __name__ == "__main__":
    solve()
