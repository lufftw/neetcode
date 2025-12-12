# solutions/0004_median_of_two_sorted_arrays.py
"""
Problem: Median of Two Sorted Arrays
Link: https://leetcode.com/problems/median-of-two-sorted-arrays/

Given two sorted arrays nums1 and nums2 of size m and n respectively,
return the median of the two sorted arrays.

Constraints:
- nums1.length == m
- nums2.length == n
- 0 <= m <= 1000
- 0 <= n <= 1000
- 1 <= m + n <= 2000
- -10^6 <= nums1[i], nums2[i] <= 10^6
"""
from typing import List
from _runner import get_solver


# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# Polymorphic pattern: each entry specifies class + method
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "findMedianSortedArrays",
        "complexity": "O(m+n) time, O(1) space",
        "description": "Two pointer merge approach",
    },
}


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
# Uses brute force O(m+n) merge to compute the correct answer,
# then compares with the solution output.
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate median calculation using brute force verification.
    
    Args:
        actual: Program output
        expected: Expected output (None if from generator)
        input_data: Raw input string
    
    Returns:
        bool: True if correct
    """
    # Parse input
    lines = input_data.strip().split('\n')
    nums1 = _parse_array(lines[0])
    nums2 = _parse_array(lines[1]) if len(lines) > 1 else []
    
    # Compute correct answer using brute force
    correct = _brute_force_median(nums1, nums2)
    
    # Compare with tolerance for floating point
    try:
        return abs(float(actual) - correct) < 1e-5
    except (ValueError, TypeError):
        return False


def _parse_array(line: str) -> List[int]:
    """Parse array from various formats."""
    line = line.strip()
    if not line or line == '[]':
        return []
    
    # Handle Python list format: [1,2,3]
    if line.startswith('[') and line.endswith(']'):
        import ast
        return ast.literal_eval(line)
    
    # Handle comma-separated format: 1,2,3
    return list(map(int, line.split(',')))


def _brute_force_median(nums1: List[int], nums2: List[int]) -> float:
    """O(m+n) brute force solution for verification."""
    merged = sorted(nums1 + nums2)
    n = len(merged)
    if n == 0:
        return 0.0
    if n % 2 == 1:
        return float(merged[n // 2])
    else:
        return (merged[n // 2 - 1] + merged[n // 2]) / 2.0


JUDGE_FUNC = judge


# ============================================
# Solution 1: Two Pointer Merge
# Time: O(m+n), Space: O(1)
#   - Merge two sorted arrays using two pointers
#   - Track median position during merge
# ============================================
class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        i = 0
        j = 0
        m, n = len(nums1), len(nums2)
        total = m + n

        is_odd = total % 2 == 1
        mid = total // 2

        prev, cur = None, None
        idx = 0

        while (i < m or j < n) and idx <= mid:
            prev = cur
            if i == m:
                cur = nums2[j]
                j += 1
            elif j == n:
                cur = nums1[i]
                i += 1
            elif nums1[i] <= nums2[j]:
                cur = nums1[i]
                i += 1
            else:
                cur = nums2[j]
                j += 1
            idx += 1

        if is_odd:
            return cur
        else:
            return (prev + cur) / 2


# ============================================
# I/O Handler
# ============================================
def solve():
    """
    Input format:
    Line 1: nums1 (comma-separated or Python list format)
    Line 2: nums2 (comma-separated or Python list format)
    
    Examples:
    1,3
    2
    
    Or:
    [1,3]
    [2]
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')
    
    nums1 = _parse_array(lines[0])
    nums2 = _parse_array(lines[1]) if len(lines) > 1 else []
    
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.findMedianSortedArrays(nums1, nums2)
    
    print(result)


if __name__ == "__main__":
    solve()

