# solutions/0078_subsets.py
"""
Problem: Subsets
Link: https://leetcode.com/problems/subsets/

Given an integer array nums of unique elements, return all possible subsets
(the power set). The solution set must not contain duplicate subsets.
Every node in the decision tree (including empty) is a valid subset.

Constraints:
- 1 <= nums.length <= 10
- -10 <= nums[i] <= 10
- All the numbers of nums are unique
"""
from typing import List
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "subsets",
        "complexity": "O(n × 2^n) time, O(n) space",
        "description": "Backtracking with start-index canonicalization",
    },
}


# ============================================================================
# JUDGE_FUNC - Validate subsets
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Subsets results."""
    nums = list(map(int, input_data.strip().split(',')))
    n = len(nums)
    nums_set = set(nums)
    
    # Each subset should only contain elements from nums
    for subset in actual:
        for num in subset:
            if num not in nums_set:
                return False
    
    # Check no duplicate subsets
    sorted_subsets = [tuple(sorted(s)) for s in actual]
    if len(set(sorted_subsets)) != len(actual):
        return False
    
    # Check correct count: 2^n subsets
    if len(actual) != (1 << n):
        return False
    
    return True


JUDGE_FUNC = judge


# ============================================================================
# Solution 1: Backtracking with Start-Index Canonicalization
# Time: O(n × 2^n), Space: O(n)
#   - Use start_index to enforce canonical ordering
#   - Collect at every node (not just leaves)
#   - 2^n subsets, O(n) to copy each
# ============================================================================
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        """
        Generate all subsets (power set) of distinct integers.
        
        Algorithm:
        - Each subset is a collection of elements with no ordering
        - To avoid generating {1,2} and {2,1} as separate subsets,
          we enforce a canonical ordering using start_index
        - Only elements from start_index onwards can be added
        - Every intermediate path is a valid subset (collect at every node)
        
        Key Difference from Permutations:
        - No "used" array needed — start_index handles it
        - Collect at EVERY node, not just leaves
        - Result size is 2^n, not n!
        
        Invariants:
        1. path contains elements in ascending index order
        2. Elements in path are from nums[0:start_index]
        3. Each subset appears exactly once
        
        Time Complexity: O(n × 2^n)
            - 2^n subsets to generate
            - O(n) to copy each subset
        
        Space Complexity: O(n) for recursion depth
        """
        results: List[List[int]] = []
        n = len(nums)
        path: List[int] = []
        
        def backtrack(start_index: int) -> None:
            # COLLECT: Every path (including empty) is a valid subset
            # Unlike permutations, we collect at every node, not just leaves
            results.append(path[:])
            
            # EXPLORE: Only consider elements from start_index onwards
            # This ensures canonical ordering and prevents duplicates
            for i in range(start_index, n):
                # === CHOOSE ===
                path.append(nums[i])
                
                # === EXPLORE ===
                # Move start_index forward to i+1
                # This ensures elements are always in ascending index order
                backtrack(i + 1)
                
                # === UNCHOOSE ===
                path.pop()
        
        backtrack(0)
        return results


def solve():
    """
    Input format:
    Line 1: nums (comma-separated)
    
    Example:
    1,2,3
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')
    
    nums = list(map(int, lines[0].split(',')))
    
    solver = get_solver(SOLUTIONS)
    result = solver.subsets(nums)
    
    print(result)


if __name__ == "__main__":
    solve()

