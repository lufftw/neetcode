# solutions/0090_subsets_ii.py
"""
Problem: Subsets II
Link: https://leetcode.com/problems/subsets-ii/

Given an integer array nums that may contain duplicates, return all possible
subsets (the power set). The solution set must not contain duplicate subsets.
Delta from Base (LeetCode 78):
- Sort the input array to bring duplicates together
- Add same-level deduplication: skip nums[i] if i > start_index and nums[i] == nums[i-1]

Constraints:
- 1 <= nums.length <= 10
- -10 <= nums[i] <= 10
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


# ============================================================================
# JUDGE_FUNC - Validate subsets with duplicates
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Subsets II results."""
    from collections import Counter
    nums = list(map(int, input_data.strip().split(',')))
    nums_count = Counter(nums)
    
    # Each subset should only contain elements from nums (respecting counts)
    for subset in actual:
        subset_count = Counter(subset)
        for num, cnt in subset_count.items():
            if cnt > nums_count.get(num, 0):
                return False
    
    # Check no duplicate subsets
    sorted_subsets = [tuple(sorted(s)) for s in actual]
    if len(set(sorted_subsets)) != len(actual):
        return False
    
    if expected is not None:
        return len(actual) == len(expected)
    
    return True


JUDGE_FUNC = judge


# ============================================================================
# Solution 1: Backtracking with Sorting and Same-Level Deduplication
# Time: O(n × 2^n), Space: O(n)
#   - Sort to bring duplicates together
#   - Skip if i > start_index and nums[i] == nums[i-1]
#   - Ensures each unique subset is generated exactly once
# ============================================================================
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

