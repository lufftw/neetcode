# solutions/0035_search_insert_position.py
"""
Problem: Search Insert Position
Link: https://leetcode.com/problems/search-insert-position/

Given a sorted array of distinct integers and a target value, return the index
if the target is found. If not, return the index where it would be if it were
inserted in order.

You must write an algorithm with O(log n) runtime complexity.

Example 1:
    Input: nums = [1,3,5,6], target = 5
    Output: 2

Example 2:
    Input: nums = [1,3,5,6], target = 2
    Output: 1

Example 3:
    Input: nums = [1,3,5,6], target = 7
    Output: 4

Constraints:
- 1 <= nums.length <= 10^4
- -10^4 <= nums[i] <= 10^4
- nums contains distinct values sorted in ascending order.
- -10^4 <= target <= 10^4

Topics: Array, Binary Search
"""
from typing import List
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate search insert position result.

    For this problem, there's only one correct answer.
    """
    import json
    lines = input_data.strip().split('\n')
    nums = json.loads(lines[0])
    target = int(lines[1])

    # actual should be valid insert position
    if not isinstance(actual, int):
        return False

    if not (0 <= actual <= len(nums)):
        return False

    # If target exists, actual should point to it
    if actual < len(nums) and nums[actual] == target:
        return True

    # Otherwise, it should be the correct insert position
    # All elements before actual should be < target
    # All elements from actual onwards should be >= target
    for i in range(actual):
        if nums[i] >= target:
            return False
    for i in range(actual, len(nums)):
        if nums[i] < target:
            return False

    return True


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "searchInsert",
        "complexity": "O(log n) time, O(1) space",
        "description": "Lower bound binary search",
    },
}


# ============================================
# Solution 1: Lower Bound
# Time: O(log n), Space: O(1)
#   - Purest form of lower_bound: first index where nums[i] >= target
#   - If target exists, returns its index
#   - If target doesn't exist, returns insertion position
#   - Invariant: all elements at indices < left are < target
# ============================================
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        """
        Find index of target or its insertion position.

        This is exactly lower_bound: first position where nums[i] >= target.

        Algorithm:
        1. Initialize search space [0, len(nums)]
        2. Binary search for first index where nums[mid] >= target
        3. Return the converged position

        Edge Cases:
        - Target smaller than all elements: returns 0
        - Target larger than all elements: returns len(nums)
        - Target equals some element: returns that index

        Time Complexity: O(log n) - standard binary search
        Space Complexity: O(1) - only pointers

        Args:
            nums: Sorted array of distinct integers
            target: Value to find or insert

        Returns:
            Index of target or insertion position
        """
        left, right = 0, len(nums)

        while left < right:
            # Overflow-safe midpoint calculation
            mid = left + (right - left) // 2

            if nums[mid] >= target:
                # nums[mid] is a candidate for the answer
                # But there might be an earlier position
                right = mid
            else:
                # nums[mid] < target, so target must go after mid
                left = mid + 1

        # left == right: converged to the insertion point
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
    result = solver.searchInsert(nums, target)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
