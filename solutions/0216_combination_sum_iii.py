# solutions/0216_combination_sum_iii.py
"""
Problem: Combination Sum III
Link: https://leetcode.com/problems/combination-sum-iii/

Find all valid combinations of k numbers that sum up to n, where:
- Only numbers 1 through 9 are used
- Each number is used at most once

Sub-Pattern: Fixed-count target search with bounded range
Key Insight: Dual constraint — both count (exactly k) and sum (exactly n)
must be satisfied. Prune on both dimensions.

Delta from Combination Sum II (LeetCode 40):
- Fixed count k (not just sum target)
- Fixed range [1-9] (no duplicates, all distinct)
- Simpler deduplication (no duplicates in input)
"""
from typing import List
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "combinationSum3",
        "complexity": "O(C(9,k) × k) time, O(k) space",
        "description": "Backtracking with dual constraint pruning",
    },
}


class Solution:
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        """
        Find all combinations of k numbers from [1-9] that sum to n.
        
        Algorithm:
        - Fixed size k: must have exactly k numbers in combination
        - Fixed sum n: numbers must sum to exactly n
        - Range [1-9]: all distinct, no duplicates to handle
        
        Dual Constraint:
        - Count constraint: len(path) must equal k
        - Sum constraint: sum(path) must equal n
        
        Pruning Strategies:
        1. If current number > remaining sum, break (numbers are increasing)
        2. If path already has k numbers, stop adding
        3. If not enough numbers remaining to fill path to k, stop
        
        Time Complexity: O(C(9,k) × k)
            - At most C(9,k) combinations
            - O(k) to copy each
        
        Space Complexity: O(k) for recursion depth
        """
        results: List[List[int]] = []
        path: List[int] = []
        
        def backtrack(start: int, remaining: int) -> None:
            # BASE CASE: Have exactly k numbers
            if len(path) == k:
                # Check if sum is exactly n (remaining = 0)
                if remaining == 0:
                    results.append(path[:])
                # Either way, don't add more numbers
                return
            
            # === PRUNING: Not enough numbers left to fill path ===
            # We need (k - len(path)) more numbers
            # Available numbers from start to 9 is (9 - start + 1)
            need = k - len(path)
            available = 9 - start + 1
            if available < need:
                return
            
            for i in range(start, 10):
                # === PRUNING: Current number too large ===
                # If i > remaining, this and all larger numbers exceed target
                if i > remaining:
                    break
                
                # === CHOOSE ===
                path.append(i)
                
                # === EXPLORE ===
                backtrack(i + 1, remaining - i)
                
                # === UNCHOOSE ===
                path.pop()
        
        backtrack(1, n)
        return results


def solve():
    """
    Input format:
    Line 1: k
    Line 2: n
    
    Example:
    3
    7
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')
    
    k = int(lines[0])
    n = int(lines[1])
    
    solver = get_solver(SOLUTIONS)
    result = solver.combinationSum3(k, n)
    
    print(result)


if __name__ == "__main__":
    solve()

