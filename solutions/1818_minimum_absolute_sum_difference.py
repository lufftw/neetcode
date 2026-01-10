"""
Problem: Minimum Absolute Sum Difference
Link: https://leetcode.com/problems/minimum-absolute-sum-difference/

You are given two positive integer arrays nums1 and nums2, both of length n.

The absolute sum difference is sum of |nums1[i] - nums2[i]| for all i.

You can replace at most one element of nums1 with any other element in nums1
to minimize the absolute sum difference.

Return the minimum absolute sum difference after replacing at most one element.
Since the answer may be large, return it modulo 10^9 + 7.

Example 1:
    Input: nums1 = [1,7,5], nums2 = [2,3,5]
    Output: 3
    Explanation: Replace 7 with 1 or 5 -> |1-2| + |1-3| + |5-5| = 3

Example 2:
    Input: nums1 = [2,4,6,8,10], nums2 = [2,4,6,8,10]
    Output: 0

Example 3:
    Input: nums1 = [1,10,4,4,2,7], nums2 = [9,3,5,1,7,4]
    Output: 20

Constraints:
- n == nums1.length
- n == nums2.length
- 1 <= n <= 10^5
- 1 <= nums1[i], nums2[i] <= 10^5

Topics: Array, Binary Search, Greedy, Sorting
"""
from typing import List
from bisect import bisect_left
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "minAbsoluteSumDiff",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Binary search for best replacement at each position",
    },
}


# ============================================================================
# Solution: Binary Search for Best Replacement
# Time: O(n log n), Space: O(n)
#
# Key insight: We can only replace ONE element. For each position i, find
# the element in nums1 that is closest to nums2[i]. This minimizes the
# contribution at position i.
#
# Strategy:
# 1. Calculate total absolute sum without any replacement
# 2. Sort a copy of nums1 for efficient binary search
# 3. For each position i, find max possible reduction by replacing nums1[i]
#    with the closest value to nums2[i] in sorted nums1
# 4. Return (total - max_reduction) % MOD
# ============================================================================
class Solution:
    def minAbsoluteSumDiff(self, nums1: List[int], nums2: List[int]) -> int:
        """
        Minimize absolute sum difference by replacing at most one element.

        For each position, calculate how much we can reduce the absolute
        difference by replacing with the optimal element from nums1.
        Use binary search on sorted nums1 to find closest values.

        Args:
            nums1: First array (can replace one element)
            nums2: Second array (fixed)

        Returns:
            Minimum absolute sum difference modulo 10^9 + 7
        """
        MOD = 10**9 + 7
        n = len(nums1)

        # Calculate original total absolute sum
        total = sum(abs(a - b) for a, b in zip(nums1, nums2))

        # Sort nums1 for binary search
        sorted_nums1 = sorted(nums1)

        # Find maximum reduction achievable by replacing one element
        max_reduction = 0

        for i in range(n):
            original_diff = abs(nums1[i] - nums2[i])
            target = nums2[i]

            # Binary search for closest value to target in sorted_nums1
            pos = bisect_left(sorted_nums1, target)

            # Check value at pos (>= target) if exists
            if pos < n:
                new_diff = abs(sorted_nums1[pos] - target)
                reduction = original_diff - new_diff
                max_reduction = max(max_reduction, reduction)

            # Check value at pos-1 (< target) if exists
            if pos > 0:
                new_diff = abs(sorted_nums1[pos - 1] - target)
                reduction = original_diff - new_diff
                max_reduction = max(max_reduction, reduction)

        return (total - max_reduction) % MOD


def solve():
    """
    Input format:
    Line 1: nums1 (JSON array)
    Line 2: nums2 (JSON array)
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')

    nums1 = json.loads(lines[0])
    nums2 = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.minAbsoluteSumDiff(nums1, nums2)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
