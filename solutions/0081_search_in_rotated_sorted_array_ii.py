# solutions/0081_search_in_rotated_sorted_array_ii.py
"""
Problem: Search in Rotated Sorted Array II
Link: https://leetcode.com/problems/search-in-rotated-sorted-array-ii/

There is an integer array nums sorted in non-decreasing order (not necessarily
with distinct values).

Before being passed to your function, nums is rotated at an unknown pivot index k
(0 <= k < nums.length) such that the resulting array is
[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]].

For example, [0,1,2,4,4,4,5,6,6,7] might be rotated at pivot index 5 and become
[4,5,6,6,7,0,1,2,4,4].

Given the array nums after the rotation and an integer target, return true if
target is in nums, or false if it is not in nums.

You must decrease the overall operation steps as much as possible.

Example 1:
    Input: nums = [2,5,6,0,0,1,2], target = 0
    Output: true

Example 2:
    Input: nums = [2,5,6,0,0,1,2], target = 3
    Output: false

Constraints:
- 1 <= nums.length <= 5000
- -10^4 <= nums[i] <= 10^4
- nums is guaranteed to be rotated at some pivot.
- -10^4 <= target <= 10^4

Topics: Array, Binary Search

Follow up: This problem is similar to Search in Rotated Sorted Array, but nums
may contain duplicates. Would this affect the runtime complexity? How and why?
"""
from typing import List
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate search result in rotated sorted array with duplicates.

    Returns True/False indicating if target exists.
    """
    import json
    lines = input_data.strip().split('\n')
    nums = json.loads(lines[0])
    target = int(lines[1])

    # actual should be boolean
    expected_result = target in nums
    return actual == expected_result


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "search",
        "complexity": "O(n) worst, O(log n) average time, O(1) space",
        "description": "Binary search with ambiguity handling for duplicates",
    },
}


# ============================================
# Solution 1: Sorted-Half Detection with Duplicate Handling
# Time: O(n) worst case, O(log n) average, Space: O(1)
#   - When nums[left] == nums[mid] == nums[right], cannot determine sorted half
#   - In ambiguous case, shrink search space linearly by incrementing left/right
#   - Worst case: all elements equal except one, e.g., [1,1,1,0,1,1,1]
#   - Average case: O(log n) when duplicates are sparse
# ============================================
class Solution:
    def search(self, nums: List[int], target: int) -> bool:
        """
        Search for target in rotated sorted array with possible duplicates.

        Key Challenge:
        When nums[left] == nums[mid] == nums[right], we cannot determine
        which half is sorted. In this case, we must shrink linearly.

        Example: [1, 0, 1, 1, 1] with target = 0
        - left=0, right=4, mid=2
        - nums[0]=1, nums[2]=1, nums[4]=1
        - Cannot tell if [1,0,1] or [1,1,1] is sorted

        Solution: When this ambiguity occurs, shrink search space by 1.

        Algorithm:
        1. Standard binary search with left <= right loop
        2. Handle ambiguous case: nums[left] == nums[mid] == nums[right]
           by shrinking linearly
        3. Otherwise, same as distinct element version

        Complexity Impact:
        - Worst case: O(n) when all elements are equal except one
        - Average case: O(log n) when duplicates are sparse

        Time Complexity: O(n) worst case, O(log n) average
        Space Complexity: O(1) - only pointers

        Args:
            nums: Rotated sorted array (may have duplicates)
            target: Value to find

        Returns:
            True if target exists, False otherwise
        """
        if not nums:
            return False

        left, right = 0, len(nums) - 1

        while left <= right:
            mid = left + (right - left) // 2

            if nums[mid] == target:
                return True

            # Ambiguous case: can't determine which half is sorted
            if nums[left] == nums[mid] == nums[right]:
                left += 1
                right -= 1
            elif nums[left] <= nums[mid]:
                # Left half [left, mid] is sorted
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                # Right half [mid, right] is sorted
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1

        return False


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
