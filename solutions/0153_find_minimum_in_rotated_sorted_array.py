"""
Problem: Find Minimum in Rotated Sorted Array
Link: https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/

Suppose an array of length n sorted in ascending order is rotated between 1 and n times.
For example, [0,1,2,4,5,6,7] might become [4,5,6,7,0,1,2] if rotated 4 times.

Given the sorted rotated array nums of unique elements, return the minimum element.

You must write an algorithm that runs in O(log n) time.

Example 1:
    Input: nums = [3,4,5,1,2]
    Output: 1

Example 2:
    Input: nums = [4,5,6,7,0,1,2]
    Output: 0

Example 3:
    Input: nums = [11,13,15,17]
    Output: 11

Constraints:
- n == nums.length
- 1 <= n <= 5000
- -5000 <= nums[i] <= 5000
- All integers of nums are unique.
- nums is sorted and rotated between 1 and n times.

Topics: Array, Binary Search
"""
import json
from typing import List
from _runner import get_solver


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionBinarySearch",
        "method": "findMin",
        "complexity": "O(log n) time, O(1) space",
        "description": "Binary search comparing mid with right boundary",
    },
    "binary_search": {
        "class": "SolutionBinarySearch",
        "method": "findMin",
        "complexity": "O(log n) time, O(1) space",
        "description": "Binary search comparing mid with right",
    },
    "find_pivot": {
        "class": "SolutionFindPivot",
        "method": "findMin",
        "complexity": "O(log n) time, O(1) space",
        "description": "Find rotation pivot point",
    },
}


# ============================================================================
# Solution 1: Binary Search - Compare with Right
# Time: O(log n), Space: O(1)
#   - If nums[mid] > nums[right]: minimum is in right half
#   - Else: minimum is in left half (including mid)
#   - Converges to the minimum
# ============================================================================
class SolutionBinarySearch:
    """
    Binary search by comparing mid with right boundary.

    Key insight: In a rotated sorted array, exactly one half is properly sorted.
    The minimum is at the rotation point (inflection point).

    If nums[mid] > nums[right]:
        - Mid is in the "larger" portion (left of pivot)
        - Minimum must be in right half (not including mid)
    Else:
        - Mid is in the "smaller" portion (right of pivot) OR array not rotated
        - Minimum could be at mid or left of mid

    We narrow down until left == right, which is the minimum.
    """

    def findMin(self, nums: List[int]) -> int:
        left, right = 0, len(nums) - 1

        while left < right:
            mid = (left + right) // 2

            if nums[mid] > nums[right]:
                # Mid is in larger portion, min is to the right
                left = mid + 1
            else:
                # Mid could be the min or min is to the left
                right = mid

        return nums[left]


# ============================================================================
# Solution 2: Find Pivot Point
# Time: O(log n), Space: O(1)
#   - Find the index where the rotation happens
#   - The pivot is where nums[i] > nums[i+1]
#   - Minimum is at pivot+1
# ============================================================================
class SolutionFindPivot:
    """
    Find the pivot point where rotation occurred.

    The pivot is the point where nums[pivot] > nums[pivot + 1].
    The minimum element is at pivot + 1.

    We binary search for this pivot point:
    - If nums[mid] > nums[mid + 1]: mid is the pivot
    - If nums[mid] < nums[mid - 1]: mid is the minimum (mid-1 is pivot)
    - If nums[mid] > nums[0]: pivot is in right half
    - Else: pivot is in left half
    """

    def findMin(self, nums: List[int]) -> int:
        n = len(nums)

        # Check if array is not rotated (or rotated n times)
        if n == 1 or nums[0] < nums[n - 1]:
            return nums[0]

        left, right = 0, n - 1

        while left <= right:
            mid = (left + right) // 2

            # Check if mid is the pivot point
            if mid < n - 1 and nums[mid] > nums[mid + 1]:
                return nums[mid + 1]

            # Check if mid is the minimum (left of mid is pivot)
            if mid > 0 and nums[mid - 1] > nums[mid]:
                return nums[mid]

            # Decide which half to search
            if nums[mid] >= nums[0]:
                # Mid is in left sorted portion, search right
                left = mid + 1
            else:
                # Mid is in right sorted portion, search left
                right = mid - 1

        return nums[0]


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: nums as JSON array

    Example:
        [3,4,5,1,2]
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')

    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.findMin(nums)

    print(result)


if __name__ == "__main__":
    solve()
