# solutions/0040_combination_sum_ii.py
"""
Problem: Combination Sum II
Link: https://leetcode.com/problems/combination-sum-ii/

Given an array of candidates (may contain duplicates) and a target,
return all unique combinations where candidates sum to target.
Each candidate may only be used once.

Sub-Pattern: Target search without reuse, with duplicate handling
Key Insight: Combine no-reuse (recurse with i+1) with same-level 
deduplication (skip if i > start and candidates[i] == candidates[i-1]).

Delta from Combination Sum (LeetCode 39):
- No reuse: recurse with i+1 instead of i
- Handle duplicates: sort + same-level skip
"""
from typing import List
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "combinationSum2",
        "complexity": "O(2^n) time, O(n) space",
        "description": "Backtracking with no-reuse and deduplication",
    },
}


class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        Find all unique combinations that sum to target, each element used at most once.
        
        Algorithm:
        - Sort to bring duplicates together
        - No reuse: recurse with i+1 (not i)
        - Same-level deduplication: skip if i > start_index and current == previous
        
        Deduplication Rule:
        - Skip candidates[i] if i > start_index AND candidates[i] == candidates[i-1]
        - This prevents choosing the same value twice at the same tree level
        
        Example with [1, 1, 2, 5], target=3:
        - Path [] at level 0: can choose first 1 (i=0)
        - Path [] at level 0: skip second 1 (i=1 > start=0, 1==1)
        - Path [1] at level 1: can choose second 1 (i=1 == start=1)
        - Result includes [1,1,2] but not duplicate paths
        
        Time Complexity: O(2^n) worst case
        Space Complexity: O(n) for recursion
        """
        results: List[List[int]] = []
        path: List[int] = []
        
        # CRITICAL: Sort for deduplication and pruning
        candidates.sort()
        
        def backtrack(start_index: int, remaining: int) -> None:
            # BASE CASE: Found valid combination
            if remaining == 0:
                results.append(path[:])
                return
            
            # PRUNING: Overshot target
            if remaining < 0:
                return
            
            for i in range(start_index, len(candidates)):
                # === DEDUPLICATION ===
                # Skip this candidate if:
                # 1. It's not the first candidate at this level (i > start_index)
                # 2. It equals the previous candidate (duplicate)
                if i > start_index and candidates[i] == candidates[i - 1]:
                    continue
                
                candidate = candidates[i]
                
                # === PRUNING ===
                # If current exceeds remaining (sorted), break
                if candidate > remaining:
                    break
                
                # === CHOOSE ===
                path.append(candidate)
                
                # === EXPLORE ===
                # NO REUSE: Recurse with i+1 (each element used at most once)
                backtrack(i + 1, remaining - candidate)
                
                # === UNCHOOSE ===
                path.pop()
        
        backtrack(0, target)
        return results


def solve():
    """
    Input format:
    Line 1: candidates (comma-separated)
    Line 2: target
    
    Example:
    10,1,2,7,6,1,5
    8
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')
    
    candidates = list(map(int, lines[0].split(',')))
    target = int(lines[1])
    
    solver = get_solver(SOLUTIONS)
    result = solver.combinationSum2(candidates, target)
    
    print(result)


if __name__ == "__main__":
    solve()

