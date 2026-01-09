# solutions/0162_find_peak_element.py
"""
Problem: Find Peak Element
Link: https://leetcode.com/problems/find-peak-element/

A peak element is an element that is strictly greater than its neighbors.

Given a 0-indexed integer array nums, find a peak element, and return its index.
If the array contains multiple peaks, return the index to any of the peaks.

You may imagine that nums[-1] = nums[n] = -infinity. In other words, an element
is always considered to be strictly greater than a neighbor that is outside the
array.

You must write an algorithm that runs in O(log n) time.

Example 1:
    Input: nums = [1,2,3,1]
    Output: 2
    Explanation: 3 is a peak element and your function should return the index
    number 2.

Example 2:
    Input: nums = [1,2,1,3,5,6,4]
    Output: 5
    Explanation: Your function can return either index number 1 where the peak
    element is 2, or index number 5 where the peak element is 6.

Constraints:
- 1 <= nums.length <= 1000
- -2^31 <= nums[i] <= 2^31 - 1
- nums[i] != nums[i + 1] for all valid i.

Topics: Array, Binary Search
"""
from typing import List
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate peak element result.

    A valid peak is any index where the element is greater than its neighbors.
    Multiple valid answers may exist.
    """
    import json
    nums = json.loads(input_data.strip())

    # actual should be valid index
    if not isinstance(actual, int):
        return False

    if not (0 <= actual < len(nums)):
        return False

    # Check if actual is a valid peak
    # nums[-1] and nums[n] are considered -infinity
    left_ok = (actual == 0) or (nums[actual] > nums[actual - 1])
    right_ok = (actual == len(nums) - 1) or (nums[actual] > nums[actual + 1])

    return left_ok and right_ok


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "findPeakElement",
        "complexity": "O(log n) time, O(1) space",
        "description": "Binary search with slope direction invariant",
    },
    "binary_search": {
        "class": "Solution",
        "method": "findPeakElement",
        "complexity": "O(log n) time, O(1) space",
        "description": "Optimal: slope-based binary search",
    },
    "linear_scan": {
        "class": "SolutionLinear",
        "method": "findPeakElement",
        "complexity": "O(n) time, O(1) space",
        "description": "Baseline: find first descent",
    },
}


# ============================================
# Solution 1: Slope Direction Binary Search
# Time: O(log n), Space: O(1)
#   - Boundary condition: nums[-1] = nums[n] = -infinity guarantees peak exists
#   - If nums[mid] < nums[mid + 1]: ascending slope, peak is on the right
#   - If nums[mid] > nums[mid + 1]: descending slope, mid could be peak
#   - Invariant: there's always a peak in [left, right]
# ============================================
class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        """
        Find a peak element and return its index.

        Key Insight:
        - nums[-1] = nums[n] = -infinity (boundary condition)
        - This guarantees at least one peak exists
        - If nums[mid] < nums[mid + 1], we're on ascending slope
        - Following the ascending direction must lead to a peak

        Algorithm:
        1. Compare nums[mid] with nums[mid + 1]
        2. If ascending (mid < mid+1): search right half
        3. If descending (mid > mid+1): search left half (keep mid)
        4. Converge to single element - must be a peak

        Why we never skip a peak:
        - Ascending at mid: peak must be in [mid+1, right]
          (mid cannot be peak because neighbor is larger)
        - Descending at mid: peak is in [left, mid]
          (mid might be the peak, so we keep it)
        - We converge to a peak, not skip over it

        Invariant:
        - At all times, there exists a peak in [left, right]
        - When we go right (ascending), we follow towards a peak
        - When we go left (descending), mid could be the peak

        Time Complexity: O(log n) - halve search space each iteration
        Space Complexity: O(1) - only pointers

        Args:
            nums: Array where adjacent elements are never equal

        Returns:
            Index of any peak element
        """
        left, right = 0, len(nums) - 1

        while left < right:
            mid = left + (right - left) // 2

            if nums[mid] < nums[mid + 1]:
                # Ascending slope: peak must be on the right
                # mid cannot be the peak (neighbor is larger)
                # Safe to exclude mid
                left = mid + 1
            else:
                # Descending slope: peak is on the left or at mid
                # mid could be the peak, so keep it in range
                right = mid

        # left == right: only one candidate remains
        # This element must be a peak due to our invariant
        return left


# ============================================
# Solution 2: Linear Scan
# Time: O(n), Space: O(1)
# ============================================
class SolutionLinear:
    def findPeakElement(self, nums: List[int]) -> int:
        """
        Find a peak element using linear scan.

        Core insight: Walk from left. Since nums[-1] = -infinity, we start
        ascending. The first index where nums[i] > nums[i+1] is a peak.
        If we reach the end, the last element is a peak (since nums[n] = -infinity).

        This is O(n) baseline showing why binary search is better.

        Args:
            nums: Array where adjacent elements differ

        Returns:
            Index of any peak element
        """
        n = len(nums)

        for i in range(n - 1):
            if nums[i] > nums[i + 1]:
                return i

        # If we never found a descent, last element is the peak
        return n - 1


# ============================================
# Entry point
# ============================================
def solve():
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.findPeakElement(nums)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
