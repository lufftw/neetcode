# solutions/0039_combination_sum.py
"""
Problem: Combination Sum
Link: https://leetcode.com/problems/combination-sum/

Given an array of distinct integers and a target, return all unique
combinations where the chosen numbers sum to target. Each number may
be used unlimited times.

Sub-Pattern: Target search with element reuse
Key Insight: Allow reuse by NOT incrementing start_index when recursing.
Prune branches where remaining target < 0 or current element > remaining.

Constraints:
- 1 <= candidates.length <= 30
- 2 <= candidates[i] <= 40
- All elements of candidates are distinct
- 1 <= target <= 40
"""
from typing import List
from _runner import get_solver


# ============================================================================
# JUDGE_FUNC - Custom validation for combination problems
# ============================================================================
def judge(actual: List[List[int]], expected, input_data: str) -> bool:
    """
    Validate Combination Sum results.
    
    Checks:
    1. Each combination sums to target
    2. Each combination uses only candidates (with reuse allowed)
    3. No duplicate combinations
    4. Correct number of combinations
    """
    lines = input_data.strip().split('\n')
    candidates = list(map(int, lines[0].split(',')))
    target = int(lines[1])
    candidates_set = set(candidates)
    
    # Validate each combination
    for combo in actual:
        # Check sum equals target
        if sum(combo) != target:
            return False
        # Check all elements are from candidates
        for num in combo:
            if num not in candidates_set:
                return False
    
    # Check no duplicates (sort each combo for comparison)
    sorted_combos = [tuple(sorted(c)) for c in actual]
    if len(set(sorted_combos)) != len(actual):
        return False
    
    # Compare count with expected if available
    if expected is not None:
        return len(actual) == len(expected)
    
    return True


JUDGE_FUNC = judge


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "combinationSum",
        "complexity": "O(n^(t/m)) time, O(t/m) space",
        "description": "Backtracking with reuse and target pruning",
    },
}


# ============================================================================
# Solution 1: Backtracking with Element Reuse
# Time: O(n^(t/m)), Space: O(t/m)
#   - Track remaining target; allow reuse by recursing with same index
#   - Prune when candidate > remaining (sorted array optimization)
#   - t = target, m = min(candidates), n = len(candidates)
# ============================================================================
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        Find all combinations that sum to target with unlimited reuse.
        
        Algorithm:
        - Track remaining target (target minus current sum)
        - When remaining = 0, found a valid combination
        - Allow reuse by recursing with same index i (not i+1)
        - Prune when remaining < 0 (overshot) or candidate > remaining
        
        Key Difference from Combinations:
        - Elements can be reused: recurse with i, not i+1
        - This allows picking the same element multiple times
        
        Pruning (with sorted candidates):
        - If candidates[i] > remaining, break (all subsequent are larger)
        
        Time Complexity: O(n^(t/m))
            - Branching factor up to n at each level
            - Depth up to t/m (using smallest element repeatedly)
            - t = target, m = min(candidates)
        
        Space Complexity: O(t/m) for recursion depth
        """
        results: List[List[int]] = []
        path: List[int] = []
        
        # Optional: Sort for consistent output and better pruning
        candidates.sort()
        
        def backtrack(start_index: int, remaining: int) -> None:
            # BASE CASE: Found valid combination
            if remaining == 0:
                results.append(path[:])
                return
            
            # PRUNING: Overshot target (shouldn't happen with other pruning)
            if remaining < 0:
                return
            
            for i in range(start_index, len(candidates)):
                candidate = candidates[i]
                
                # === PRUNING ===
                # If current candidate exceeds remaining, all subsequent
                # candidates (which are >= current due to sorting) will too
                if candidate > remaining:
                    break
                
                # === CHOOSE ===
                path.append(candidate)
                
                # === EXPLORE ===
                # REUSE ALLOWED: Recurse with same index i
                # This means we can pick candidate again
                backtrack(i, remaining - candidate)
                
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
    2,3,6,7
    7
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')
    
    candidates = list(map(int, lines[0].split(',')))
    target = int(lines[1])
    
    solver = get_solver(SOLUTIONS)
    result = solver.combinationSum(candidates, target)
    
    print(result)


if __name__ == "__main__":
    solve()

