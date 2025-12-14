# solutions/0078_subsets.py
"""
Problem: Subsets
Link: https://leetcode.com/problems/subsets/

Given an integer array nums of unique elements, return all possible subsets.

Sub-Pattern: Subset enumeration with start-index canonicalization
Key Insight: Use start_index to only consider elements at or after the current
position. This inherently prevents duplicates like {1,2} and {2,1} and ensures
we generate each subset exactly once in a canonical order.

Every node in the decision tree (including empty) is a valid subset.
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

