# solutions/0004_median_of_two_sorted_arrays.py
"""
題目: Median of Two Sorted Arrays
連結: https://leetcode.com/problems/median-of-two-sorted-arrays/

Given two sorted arrays nums1 and nums2 of size m and n respectively,
return the median of the two sorted arrays.
"""
from typing import List


class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        i = 0
        j = 0
        m, n = len(nums1), len(nums2)
        l = m + n

        is_odd = True if l % 2 == 1 else False
        mid = l // 2

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
            else:  # nums1[i] > nums2[j]
                cur = nums2[j]
                j += 1
            idx += 1

        if is_odd:
            return cur
        else:
            return (prev + cur) / 2


def solve():
    """
    輸入格式:
    第一行: nums1 (用逗號分隔，空陣列用空行)
    第二行: nums2 (用逗號分隔，空陣列用空行)
    
    Example:
    1,3
    2
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')
    
    # 解析 nums1
    nums1 = list(map(int, lines[0].split(','))) if lines[0] else []
    # 解析 nums2
    nums2 = list(map(int, lines[1].split(','))) if lines[1] else []
    
    sol = Solution()
    result = sol.findMedianSortedArrays(nums1, nums2)
    
    # 輸出格式: 浮點數
    print(result)


if __name__ == "__main__":
    solve()

