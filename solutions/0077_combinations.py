# solutions/0077_combinations.py
"""
Problem: Combinations
Link: https://leetcode.com/problems/combinations/

Given two integers n and k, return all possible combinations of k numbers
chosen from the range [1, n].

Sub-Pattern: Fixed-size subset enumeration
Key Insight: Same as subsets, but only collect when path length equals k.
Add pruning to skip branches that can't possibly reach size k.

Delta from Subsets (LeetCode 78):
- Only collect when len(path) == k (not at every node)
- Add count-based pruning: stop early if not enough elements remain
"""
from typing import List
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "combine",
        "complexity": "O(k × C(n,k)) time, O(k) space",
        "description": "Backtracking with count pruning",
    },
}


class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        """
        Generate all combinations of k numbers from range [1, n].
        
        Algorithm:
        - Similar to subsets, use start_index for canonical ordering
        - Only collect when path has exactly k elements
        - Prune branches where remaining elements < elements needed
        
        Pruning Optimization:
        - We need (k - len(path)) more elements
        - Available elements from i to n is (n - i + 1)
        - Prune when available < needed
        - Upper bound for loop: n - (k - len(path)) + 1
        
        Example: n=4, k=3, path=[1]
        - Need 2 more elements
        - From i=2, available = 4-2+1 = 3 → OK
        - From i=3, available = 4-3+1 = 2 → OK
        - From i=4, available = 4-4+1 = 1 → too few, prune
        
        Time Complexity: O(k × C(n,k))
            - C(n,k) combinations
            - O(k) to copy each
        
        Space Complexity: O(k) for recursion depth
        """
        results: List[List[int]] = []
        path: List[int] = []
        
        def backtrack(start: int) -> None:
            # BASE CASE: Combination is complete
            if len(path) == k:
                results.append(path[:])
                return
            
            # === PRUNING ===
            # Calculate how many more elements we need
            need = k - len(path)
            
            # Upper bound: we need at least 'need' elements from [start, n]
            # Available from start to n is (n - start + 1)
            # Loop should stop when (n - i + 1) < need
            # i.e., stop when i > n - need + 1
            # So upper bound for i is n - need + 1 (inclusive)
            upper_bound = n - need + 1
            
            for i in range(start, upper_bound + 1):
                path.append(i)
                backtrack(i + 1)
                path.pop()
        
        backtrack(1)
        return results


def solve():
    """
    Input format:
    Line 1: n
    Line 2: k
    
    Example:
    4
    2
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')
    
    n = int(lines[0])
    k = int(lines[1])
    
    solver = get_solver(SOLUTIONS)
    result = solver.combine(n, k)
    
    print(result)


if __name__ == "__main__":
    solve()

