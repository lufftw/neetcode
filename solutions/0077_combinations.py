# solutions/0077_combinations.py
"""
Problem: Combinations
Link: https://leetcode.com/problems/combinations/

Given two integers n and k, return all possible combinations of k numbers chosen from the range [1, n].
You may return the answer in any order.

Example 1:
    Input: n = 4, k = 2
    Output: [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
    Explanation: There are 4 choose 2 = 6 total combinations.
                 Note that combinations are unordered, i.e., [1,2] and [2,1] are considered to be the same combination.

Example 2:
    Input: n = 1, k = 1
    Output: [[1]]
    Explanation: There is 1 choose 1 = 1 total combination.

Constraints:
- 1 <= n <= 20
- 1 <= k <= n

Topics: Backtracking
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


# ============================================================================
# JUDGE_FUNC - Validate combinations
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Combinations results."""
    import math
    lines = input_data.strip().split('\n')
    n = int(lines[0])
    k = int(lines[1])
    
    # Check each combination has k elements from [1, n]
    for combo in actual:
        if len(combo) != k:
            return False
        if len(set(combo)) != k:  # no duplicates
            return False
        for num in combo:
            if num < 1 or num > n:
                return False
    
    # Check no duplicate combinations
    sorted_combos = [tuple(sorted(c)) for c in actual]
    if len(set(sorted_combos)) != len(actual):
        return False
    
    # Check correct count: C(n,k)
    expected_count = math.comb(n, k)
    if len(actual) != expected_count:
        return False
    
    return True


JUDGE_FUNC = judge


# ============================================================================
# Solution 1: Backtracking with Count Pruning
# Time: O(k × C(n,k)), Space: O(k)
#   - Use start_index for canonical ordering
#   - Only collect when path has exactly k elements
#   - Prune when remaining elements < elements needed
# ============================================================================
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
    Line 1: n (integer)
    Line 2: k (integer)
    
    Output format:
    JSON 2D array of combinations
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')
    
    n = int(lines[0])
    k = int(lines[1])
    
    solver = get_solver(SOLUTIONS)
    result = solver.combine(n, k)
    
    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()

