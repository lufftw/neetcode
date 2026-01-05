# solutions/0034_find_first_and_last_position_of_element_in_sorted_array.py
"""
Problem: Find First and Last Position of Element in Sorted Array
Link: https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/

Given an array of integers nums sorted in non-decreasing order, find the starting
and ending position of a given target value.

If target is not found in the array, return [-1, -1].

You must write an algorithm with O(log n) runtime complexity.

Example 1:
    Input: nums = [5,7,7,8,8,10], target = 8
    Output: [3,4]

Example 2:
    Input: nums = [5,7,7,8,8,10], target = 6
    Output: [-1,-1]

Example 3:
    Input: nums = [], target = 0
    Output: [-1,-1]

Constraints:
- 0 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9
- nums is a non-decreasing array.
- -10^9 <= target <= 10^9

Topics: Array, Binary Search
"""
from typing import List
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate first and last position result.

    For this problem, there's only one correct answer.
    """
    import json
    lines = input_data.strip().split('\n')
    nums = json.loads(lines[0])
    target = int(lines[1])

    # actual should be [first, last] or [-1, -1]
    if not isinstance(actual, list) or len(actual) != 2:
        return False

    first, last = actual

    if first == -1 and last == -1:
        # Target should not exist
        return target not in nums

    # Validate range
    if not (0 <= first <= last < len(nums)):
        return False

    # All elements in range should equal target
    for i in range(first, last + 1):
        if nums[i] != target:
            return False

    # Elements before first and after last should not equal target
    if first > 0 and nums[first - 1] == target:
        return False
    if last < len(nums) - 1 and nums[last + 1] == target:
        return False

    return True


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "searchRange",
        "complexity": "O(log n) time, O(1) space",
        "description": "Lower bound + upper bound binary search",
    },
}


# ============================================
# Solution 1: Lower Bound + Upper Bound
# Time: O(log n), Space: O(1)
#   - Uses predicate boundary search pattern from BinarySearchBoundary kernel
#   - lower_bound finds first index where nums[i] >= target
#   - upper_bound finds first index where nums[i] > target
#   - Last occurrence = upper_bound - 1
#   - Handles duplicates correctly by design
# ============================================
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        """
        Find the starting and ending position of target in sorted array.

        Algorithm:
        1. Use lower_bound to find first occurrence (first index >= target)
        2. Verify target actually exists at that position
        3. Use upper_bound to find position after last occurrence (first index > target)
        4. Last occurrence = upper_bound - 1

        Time Complexity: O(log n) - two binary searches
        Space Complexity: O(1) - only pointers

        Args:
            nums: Sorted array in non-decreasing order
            target: Value to find range for

        Returns:
            [first, last] indices, or [-1, -1] if not found
        """
        if not nums:
            return [-1, -1]

        # Find first position where nums[i] >= target
        first = self._lower_bound(nums, target)

        # Check if target exists at this position
        if first == len(nums) or nums[first] != target:
            return [-1, -1]

        # Find first position where nums[i] > target
        # Last occurrence is one position before this
        last = self._upper_bound(nums, target) - 1

        return [first, last]

    def _lower_bound(self, nums: List[int], target: int) -> int:
        """
        Find first index where nums[i] >= target.

        Predicate: nums[mid] >= target

        Invariant:
        - All elements before 'left' are < target
        - All elements from 'right' onwards are >= target

        Returns len(nums) if all elements < target.
        """
        left, right = 0, len(nums)

        while left < right:
            mid = left + (right - left) // 2

            if nums[mid] >= target:
                # nums[mid] is a candidate, but there might be earlier ones
                right = mid
            else:
                # nums[mid] < target, answer must be after mid
                left = mid + 1

        return left

    def _upper_bound(self, nums: List[int], target: int) -> int:
        """
        Find first index where nums[i] > target.

        Predicate: nums[mid] > target

        Invariant:
        - All elements before 'left' are <= target
        - All elements from 'right' onwards are > target

        Returns len(nums) if all elements <= target.
        """
        left, right = 0, len(nums)

        while left < right:
            mid = left + (right - left) // 2

            if nums[mid] > target:
                # nums[mid] is a candidate (first > target)
                right = mid
            else:
                # nums[mid] <= target, answer must be after mid
                left = mid + 1

        return left


# ============================================
# Entry point
# ============================================
def solve():
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    nums = json.loads(lines[0])
    target = int(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.searchRange(nums, target)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
