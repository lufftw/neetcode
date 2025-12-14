# solutions/0047_permutations_ii.py
"""
Problem: Permutations II
Link: https://leetcode.com/problems/permutations-ii/

Given a collection of numbers that might contain duplicates,
return all possible unique permutations.

Sub-Pattern: Permutation with duplicates (same-level deduplication)
Key Insight: Sort the array, then skip duplicate values at the same
tree level. The condition "!used[i-1]" ensures we only use the leftmost
occurrence of each duplicate at each level.

Delta from Base (LeetCode 46):
- Sort the input array to bring duplicates together
- Add deduplication: skip nums[i] if it equals nums[i-1] and !used[i-1]
"""
from typing import List
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "permuteUnique",
        "complexity": "O(n! × n) time, O(n) space",
        "description": "Backtracking with sorting and same-level deduplication",
    },
}


class Solution:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        """
        Generate all unique permutations when input may have duplicates.
        
        Algorithm:
        - Sort the array to bring duplicates together
        - Use same-level deduplication: skip a duplicate if its previous
          occurrence wasn't used (meaning we're at the same decision level)
        
        Deduplication Logic:
        - If nums[i] == nums[i-1] and used[i-1] == False, skip nums[i]
        - Why? If used[i-1] is False, we're choosing between i-1 and i
          at the same level. To avoid duplicate permutations, always
          choose the leftmost (i-1) first.
        - If used[i-1] is True, then i-1 is in an ancestor node, so
          choosing i is valid (different branch of the tree).
        
        Invariants:
        1. After sorting, duplicates are adjacent
        2. We always use duplicates in left-to-right order at each level
        3. This ensures each unique permutation is generated exactly once
        
        Time Complexity: O(n! × n) in worst case (all unique)
        Space Complexity: O(n) for recursion and used array
        """
        results: List[List[int]] = []
        n = len(nums)
        
        # CRITICAL: Sort to bring duplicates together
        # This is required for the deduplication logic to work
        nums.sort()
        
        path: List[int] = []
        used: List[bool] = [False] * n
        
        def backtrack() -> None:
            if len(path) == n:
                results.append(path[:])
                return
            
            for i in range(n):
                # Skip already used elements
                if used[i]:
                    continue
                
                # === DEDUPLICATION ===
                # Skip this duplicate if the previous identical element
                # is NOT used. This means we're at the same tree level
                # and should use the previous one instead.
                #
                # Example with [1, 1', 2]:
                # - When building position 0, we see 1 and 1'
                # - If we pick 1 first → valid path
                # - If we try to pick 1' first → skip (1 is unused, same level)
                # This ensures we always pick leftmost duplicate first at each level
                if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                    continue
                
                # === CHOOSE ===
                path.append(nums[i])
                used[i] = True
                
                # === EXPLORE ===
                backtrack()
                
                # === UNCHOOSE ===
                path.pop()
                used[i] = False
        
        backtrack()
        return results


def solve():
    """
    Input format:
    Line 1: nums (comma-separated)
    
    Example:
    1,1,2
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')
    
    nums = list(map(int, lines[0].split(',')))
    
    solver = get_solver(SOLUTIONS)
    result = solver.permuteUnique(nums)
    
    print(result)


if __name__ == "__main__":
    solve()

