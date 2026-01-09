# solutions/0001_two_sum.py
"""
Problem: Two Sum
Link: https://leetcode.com/problems/two-sum/

Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
You may assume that each input would have exactly one solution, and you may not use the same element twice.
You can return the answer in any order.

Example 1:
    Input: nums = [2,7,11,15], target = 9
    Output: [0,1]
    Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:
    Input: nums = [3,2,4], target = 6
    Output: [1,2]

Example 3:
    Input: nums = [3,3], target = 6
    Output: [0,1]

Constraints:
- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9
- -10^9 <= target <= 10^9
- Only one valid answer exists.

Topics: Array, Hash Table

Hint 1: A really brute force way would be to search for all possible pairs of numbers but that would be too slow. Again, it's best to try out brute force solutions for just for completeness. It is from these brute force solutions that you can come up with optimizations.

Hint 2: So, if we fix one of the numbers, say <code>x</code>, we have to scan the entire array to find the next number <code>y</code> which is <code>value - x</code> where value is the input parameter. Can we change our array somehow so that this search becomes faster?

Hint 3: The second train of thought is, without changing the array, can we use additional space somehow? Like maybe a hash map to speed up the search?

Follow-up: Can you come up with an algorithm that is less than O(n^2) time complexity?
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
    "hash_map": {
        "class": "Solution",
        "method": "twoSum",
        "complexity": "O(n) time, O(n) space",
        "description": "Optimal: single pass with hash map",
    },
    "bruteforce": {
        "class": "SolutionBruteforce",
        "method": "twoSum",
        "complexity": "O(n²) time, O(1) space",
        "description": "Baseline: check all pairs",
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


# ============================================================================
# Solution 2: Brute Force
# Time: O(n²), Space: O(1)
#   - Check all pairs - baseline to show optimization
# ============================================================================
class SolutionBruteforce:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        """
        Find two indices whose values sum to target using brute force.

        Core insight: Check every pair (i, j) where i < j. This is the naive
        approach that helps understand why hash map optimization matters.

        Time: O(n²) - nested loops
        Space: O(1) - no extra data structures

        Args:
            nums: Array of integers
            target: Target sum

        Returns:
            Indices of two numbers that sum to target
        """
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []


def solve():
    """
    Input format (canonical JSON):
    Line 1: nums as JSON array
    Line 2: target as integer
    
    Example:
    [2,7,11,15]
    9
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')
    
    # Parse nums array (JSON format)
    nums = json.loads(lines[0])
    # Parse target
    target = int(lines[1])
    
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.twoSum(nums, target)
    
    # Output format: canonical JSON
    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
