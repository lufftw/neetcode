# solutions/0216_combination_sum_iii.py
"""
Problem: Combination Sum III
Link: https://leetcode.com/problems/combination-sum-iii/

Find all valid combinations of k numbers that sum up to n such that the following conditions are true:
Only numbers 1 through 9 are used.
Each number is used at most once.
Return a list of all possible valid combinations. The list must not contain the same combination twice, and the combinations may be returned in any order.

Example 1:
    Input: k = 3, n = 7
    Output: [[1,2,4]]
    Explanation: 1 + 2 + 4 = 7
                 There are no other valid combinations.

Example 2:
    Input: k = 3, n = 9
    Output: [[1,2,6],[1,3,5],[2,3,4]]
    Explanation: 1 + 2 + 6 = 9
                 1 + 3 + 5 = 9
                 2 + 3 + 4 = 9
                 There are no other valid combinations.

Example 3:
    Input: k = 4, n = 1
    Output: []
    Explanation: There are no valid combinations.
                 Using 4 different numbers in the range [1,9], the smallest sum we can get is 1+2+3+4 = 10 and since 10 > 1, there are no valid combination.

Constraints:
- 2 <= k <= 9
- 1 <= n <= 60

Topics: Array, Backtracking
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


# ============================================================================
# JUDGE_FUNC - Validate Combination Sum III
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Combination Sum III results."""
    lines = input_data.strip().split('\n')
    k = int(lines[0])
    n = int(lines[1])
    
    for combo in actual:
        # Check exactly k numbers
        if len(combo) != k:
            return False
        # Check sum equals n
        if sum(combo) != n:
            return False
        # Check all numbers in [1,9] and unique
        if len(set(combo)) != k:
            return False
        for num in combo:
            if num < 1 or num > 9:
                return False
    
    # Check no duplicate combinations
    sorted_combos = [tuple(sorted(c)) for c in actual]
    if len(set(sorted_combos)) != len(actual):
        return False
    
    if expected is not None:
        return len(actual) == len(expected)
    
    return True


JUDGE_FUNC = judge


# ============================================================================
# Solution 1: Backtracking with Dual Constraint Pruning
# Time: O(C(9,k) × k), Space: O(k)
#   - Fixed size k and fixed sum n constraints
#   - Range [1-9]: all distinct, no duplicates
#   - Prune on both count and sum dimensions
# ============================================================================
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

