# solutions/0090_subsets_ii.py
"""
Problem: Subsets II
Link: https://leetcode.com/problems/subsets-ii/

Given an integer array nums that may contain duplicates, return all unique subsets.

Sub-Pattern: Subset enumeration with duplicates (sort + same-level skip)
Key Insight: Sort the array, then skip duplicate values at the same tree level.
The condition "i > start_index" ensures we only skip duplicates, not the first
occurrence at each level.

Delta from Base (LeetCode 78):
- Sort the input array to bring duplicates together
- Add same-level deduplication: skip nums[i] if i > start_index and nums[i] == nums[i-1]
"""
from typing import List
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "subsetsWithDup",
        "complexity": "O(n × 2^n) time, O(n) space",
        "description": "Backtracking with sorting and same-level deduplication",
    },
}


class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        """
        Generate all unique subsets when input may have duplicates.
        
        Algorithm:
        - Sort to bring duplicates together
        - Use same-level deduplication: at each tree level, skip duplicate
          values that we've already processed
        
        Deduplication Logic:
        - Skip nums[i] if i > start_index AND nums[i] == nums[i-1]
        - The condition i > start_index ensures we don't skip the first
          occurrence at each level (which is valid to include)
        
        Example with [1, 2, 2]:
        - At start_index=1, we can include first 2 (i=1)
        - At start_index=1, we skip second 2 (i=2 > start=1, 2==2)
        - But at start_index=2, we can include second 2 (i=2 == start=2)
        
        Invariants:
        1. After sorting, duplicates are adjacent
        2. At each tree level, each unique value is tried exactly once
        3. This ensures each unique subset is generated exactly once
        
        Time Complexity: O(n × 2^n) worst case
        Space Complexity: O(n)
        """
        results: List[List[int]] = []
        n = len(nums)
        
        # CRITICAL: Sort to bring duplicates together
        nums.sort()
        
        path: List[int] = []
        
        def backtrack(start_index: int) -> None:
            # Collect every subset
            results.append(path[:])
            
            for i in range(start_index, n):
                # === DEDUPLICATION ===
                # Skip this element if:
                # 1. It's not the first element at this level (i > start_index)
                # 2. It equals the previous element (nums[i] == nums[i-1])
                #
                # This ensures we only process each unique value once per level
                if i > start_index and nums[i] == nums[i - 1]:
                    continue
                
                path.append(nums[i])
                backtrack(i + 1)
                path.pop()
        
        backtrack(0)
        return results


def solve():
    """
    Input format:
    Line 1: nums (comma-separated)
    
    Example:
    1,2,2
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')
    
    nums = list(map(int, lines[0].split(',')))
    
    solver = get_solver(SOLUTIONS)
    result = solver.subsetsWithDup(nums)
    
    print(result)


if __name__ == "__main__":
    solve()

