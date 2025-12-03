# solutions/0001_two_sum.py
"""
題目: Two Sum
連結: https://leetcode.com/problems/two-sum/

Given an array of integers nums and an integer target, 
return indices of the two numbers such that they add up to target.
"""
from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}

        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return []


def solve():
    """
    輸入格式:
    第一行: nums (用逗號分隔)
    第二行: target
    
    Example:
    2,7,11,15
    9
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')
    
    # 解析 nums
    nums = list(map(int, lines[0].split(',')))
    # 解析 target
    target = int(lines[1])
    
    sol = Solution()
    result = sol.twoSum(nums, target)
    
    # 輸出格式: [0, 1]
    print(result)


if __name__ == "__main__":
    solve()

