# solutions/0001_two_sum.py
"""
Problem: Two Sum
Link: https://leetcode.com/problems/two-sum/

Given an array of integers nums and an integer target, 
return indices of the two numbers such that they add up to target.

Time Complexity: O(n) - single pass with hash map
Space Complexity: O(n) - hash map storage
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
    Input format:
    Line 1: nums (comma-separated)
    Line 2: target
    
    Example:
    2,7,11,15
    9
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')
    
    # Parse nums array
    nums = list(map(int, lines[0].split(',')))
    # Parse target
    target = int(lines[1])
    
    sol = Solution()
    result = sol.twoSum(nums, target)
    
    # Output format: [0, 1]
    print(result)


if __name__ == "__main__":
    solve()
