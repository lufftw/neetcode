# solutions/0001_two_sum.py
"""
Problem: Two Sum
Link: https://leetcode.com/problems/two-sum/

Given an array of integers nums and an integer target, 
return indices of the two numbers such that they add up to target.

Constraints:
- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9
- -10^9 <= target <= 10^9
- Only one valid answer exists.
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
        "method": "twoSum",
        "complexity": "O(n) time, O(n) space",
        "description": "Single pass with hash map",
    },
}


# ============================================
# Solution 1: Hash Map
# Time: O(n), Space: O(n)
#   - Single pass through array
#   - Hash map stores seen numbers and their indices
# ============================================
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
    
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.twoSum(nums, target)
    
    # Output format: [0, 1]
    print(result)


if __name__ == "__main__":
    solve()
