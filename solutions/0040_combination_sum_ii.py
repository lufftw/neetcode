# solutions/0040_combination_sum_ii.py
"""
Problem: Combination Sum II
Link: https://leetcode.com/problems/combination-sum-ii/

Given a collection of candidate numbers (candidates) and a target number (target), find all unique combinations in candidates where the candidate numbers sum to target.
Each number in candidates may only be used once in the combination.

Example 1:
    Input: candidates = [10,1,2,7,6,1,5], target = 8
    Output: [
[1,1,6],
[1,2,5],
[1,7],
[2,6]
]

Example 2:
    Input: candidates = [2,5,2,1,2], target = 5
    Output: [
[1,2,2],
[5]
]

Constraints:
- 1 <= candidates.length <= 100
- 1 <= candidates[i] <= 50
- 1 <= target <= 30

Topics: Array, Backtracking

Note: The solution set must not contain duplicate combinations.
"""
from typing import List
from _runner import get_solver


# ============================================================================
# JUDGE_FUNC - Custom validation for combination problems
# ============================================================================
def judge(actual: List[List[int]], expected, input_data: str) -> bool:
    """
    Validate Combination Sum II results.
    
    Checks:
    1. Each combination sums to target
    2. Each element used at most as many times as it appears in candidates
    3. No duplicate combinations
    """
    import json
    lines = input_data.strip().split('\n')
    candidates = json.loads(lines[0])
    target = int(lines[1])
    
    from collections import Counter
    candidates_count = Counter(candidates)
    
    for combo in actual:
        # Check sum equals target
        if sum(combo) != target:
            return False
        # Check element usage doesn't exceed availability
        combo_count = Counter(combo)
        for num, cnt in combo_count.items():
            if cnt > candidates_count.get(num, 0):
                return False
    
    # Check no duplicate combinations
    sorted_combos = [tuple(sorted(c)) for c in actual]
    if len(set(sorted_combos)) != len(actual):
        return False
    
    if expected is not None:
        return len(actual) == len(expected)
    
    return True


JUDGE_FUNC = judge


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "combinationSum2",
        "complexity": "O(2^n) time, O(n) space",
        "description": "Backtracking with no-reuse and deduplication",
    },
}


# ============================================================================
# Solution 1: Backtracking with No-Reuse and Deduplication
# Time: O(2^n), Space: O(n)
#   - Sort to bring duplicates together for deduplication
#   - No reuse: recurse with i+1 (each element used at most once)
#   - Same-level dedup: skip if i > start and candidates[i] == candidates[i-1]
# ============================================================================
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
    import json
    """
    Input format:
    Line 1: candidates (comma-separated)
    Line 2: target
    
    Example:
    10,1,2,7,6,1,5
    8
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')
    
    candidates = json.loads(lines[0])
    target = int(lines[1])
    
    solver = get_solver(SOLUTIONS)
    result = solver.combinationSum2(candidates, target)
    
    print(result)


if __name__ == "__main__":
    solve()

