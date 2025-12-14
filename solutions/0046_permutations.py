# solutions/0046_permutations.py
"""
Problem: Permutations
Link: https://leetcode.com/problems/permutations/

Given an array nums of distinct integers, return all possible permutations.

Sub-Pattern: Permutation Enumeration with used tracking
Key Insight: At each position in the permutation, try every element that
hasn't been used yet. Track usage with a boolean array.

This is the BASE TEMPLATE for the BacktrackingExploration API Kernel's
permutation sub-pattern.

Constraints:
- 1 <= nums.length <= 6
- -10 <= nums[i] <= 10
- All the integers of nums are unique
"""
from typing import List
from _runner import get_solver
import math


# ============================================================================
# JUDGE_FUNC - Custom validation for permutation problems
# ============================================================================
def judge(actual: List[List[int]], expected, input_data: str) -> bool:
    """
    Validate Permutations results.
    
    Checks:
    1. Each result is a valid permutation (same elements as input)
    2. No duplicate permutations
    3. Correct count (n! permutations)
    """
    nums = list(map(int, input_data.strip().split(',')))
    n = len(nums)
    nums_sorted = sorted(nums)
    
    # Each permutation should have same elements as input
    for perm in actual:
        if sorted(perm) != nums_sorted:
            return False
    
    # Check no duplicates
    perm_tuples = [tuple(p) for p in actual]
    if len(set(perm_tuples)) != len(actual):
        return False
    
    # Check correct count
    expected_count = math.factorial(n)
    if len(actual) != expected_count:
        return False
    
    return True


JUDGE_FUNC = judge


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "permute",
        "complexity": "O(n! × n) time, O(n) space",
        "description": "Backtracking with used array",
    },
}


# ============================================================================
# Solution 1: Backtracking with Used Array
# Time: O(n! × n), Space: O(n)
#   - Build permutation position by position
#   - At each position, try every unused element
#   - Track usage with boolean array; n! permutations × O(n) copy each
# ============================================================================
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        """
        Generate all permutations of distinct integers.
        
        Algorithm:
        - Build the permutation position by position
        - At each position, try every unused element
        - Track which elements are used with a boolean array
        - When path length equals nums length, we have a complete permutation
        
        Invariants:
        1. path contains elements from nums with no duplicates
        2. used[i] == True iff nums[i] is in path
        3. After backtracking, state is restored exactly
        
        Time Complexity: O(n! × n)
            - There are n! permutations
            - Each permutation takes O(n) to copy
        
        Space Complexity: O(n)
            - Recursion depth is n
            - Used array is O(n)
            - Output space not counted
        """
        results: List[List[int]] = []
        n = len(nums)
        
        # State: Current permutation being built
        path: List[int] = []
        
        # Tracking: Which elements are already in the current path
        # used[i] = True means nums[i] is already in path
        used: List[bool] = [False] * n
        
        def backtrack() -> None:
            # BASE CASE: Permutation is complete when path has all elements
            if len(path) == n:
                # Append a COPY of path (path will be modified later)
                results.append(path[:])
                return
            
            # RECURSIVE CASE: Try adding each unused element
            for i in range(n):
                # Skip elements already used in current permutation
                if used[i]:
                    continue
                
                # === CHOOSE ===
                # Add this element to the permutation
                path.append(nums[i])
                used[i] = True
                
                # === EXPLORE ===
                # Recursively fill the next position
                backtrack()
                
                # === UNCHOOSE ===
                # Remove the element to try other choices (backtrack)
                path.pop()
                used[i] = False
        
        backtrack()
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
    result = solver.permute(nums)
    
    print(result)


if __name__ == "__main__":
    solve()

