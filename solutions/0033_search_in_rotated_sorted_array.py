# solutions/0033_search_in_rotated_sorted_array.py
"""
Problem: Search in Rotated Sorted Array
Link: https://leetcode.com/problems/search-in-rotated-sorted-array/

There is an integer array nums sorted in ascending order (with distinct values).

Prior to being passed to your function, nums is possibly rotated at an unknown
pivot index k (1 <= k < nums.length) such that the resulting array is
[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]].

For example, [0,1,2,4,5,6,7] might be rotated at pivot index 3 and become
[4,5,6,7,0,1,2].

Given the array nums after the possible rotation and an integer target, return
the index of target if it is in nums, or -1 if it is not in nums.

You must write an algorithm with O(log n) runtime complexity.

Example 1:
    Input: nums = [4,5,6,7,0,1,2], target = 0
    Output: 4

Example 2:
    Input: nums = [4,5,6,7,0,1,2], target = 3
    Output: -1

Example 3:
    Input: nums = [1], target = 0
    Output: -1

Constraints:
- 1 <= nums.length <= 5000
- -10^4 <= nums[i] <= 10^4
- All values of nums are unique.
- nums is an ascending array that is possibly rotated.
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
    Validate search result in rotated sorted array.

    For this problem, there's only one correct answer (or -1 if not found).
    """
    import json
    lines = input_data.strip().split('\n')
    nums = json.loads(lines[0])
    target = int(lines[1])

    # Validate actual result
    if actual == -1:
        # Target should not exist in array
        return target not in nums
    else:
        # actual should be valid index and nums[actual] == target
        if not (0 <= actual < len(nums)):
            return False
        return nums[actual] == target


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "search",
        "complexity": "O(log n) time, O(1) space",
        "description": "Single-pass binary search with sorted-half detection",
    },
}


# ============================================
# Solution 1: Sorted-Half Detection
# Time: O(log n), Space: O(1)
#   - For any mid, at least one of [left, mid] or [mid, right] is sorted
#   - If nums[left] <= nums[mid]: left half is sorted
#   - Check if target is in sorted half using exact bounds
#   - Invariant: if target exists, it remains in [left, right]
# ============================================
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        """
        Search for target in rotated sorted array.

        Key Insight:
        In a rotated sorted array, for any mid point, at least one half
        [left, mid] or [mid, right] is guaranteed to be sorted.

        Algorithm:
        1. Standard binary search with left <= right loop
        2. For each mid, determine which half is sorted
        3. Check if target is in the sorted half (using exact bounds)
        4. Narrow search to the appropriate half

        Determining sorted half:
        - If nums[left] <= nums[mid]: left half is sorted
        - Otherwise: right half is sorted

        Why this doesn't skip the answer:
        - When left half is sorted: if target is in [nums[left], nums[mid]),
          we search left; otherwise we search right
        - When right half is sorted: if target is in (nums[mid], nums[right]],
          we search right; otherwise we search left
        - Each decision is based on exact sorted bounds, never guessing

        Time Complexity: O(log n) - standard binary search
        Space Complexity: O(1) - only pointers

        Args:
            nums: Rotated sorted array with distinct elements
            target: Value to find

        Returns:
            Index of target, or -1 if not found
        """
        if not nums:
            return -1

        left, right = 0, len(nums) - 1

        while left <= right:
            mid = left + (right - left) // 2

            if nums[mid] == target:
                return mid

            # Determine which half is sorted
            if nums[left] <= nums[mid]:
                # Left half [left, mid] is sorted
                if nums[left] <= target < nums[mid]:
                    # Target is in the sorted left half
                    right = mid - 1
                else:
                    # Target must be in the right half
                    left = mid + 1
            else:
                # Right half [mid, right] is sorted
                if nums[mid] < target <= nums[right]:
                    # Target is in the sorted right half
                    left = mid + 1
                else:
                    # Target must be in the left half
                    right = mid - 1

        return -1


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
    result = solver.search(nums, target)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
