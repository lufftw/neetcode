# solutions/0078_subsets.py
"""
Problem: Subsets
Link: https://leetcode.com/problems/subsets/

Given an integer array nums of unique elements, return all possible subsets (the power set).
The solution set must not contain duplicate subsets. Return the solution in any order.

Example 1:
    Input: nums = [1,2,3]
    Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]

Example 2:
    Input: nums = [0]
    Output: [[],[0]]

Constraints:
- 1 <= nums.length <= 10
- -10 <= nums[i] <= 10
- All the numbers of nums are unique.

Topics: Array, Backtracking, Bit Manipulation
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
    "bitmask": {
        "class": "SolutionBitmask",
        "method": "subsets",
        "complexity": "O(n × 2^n) time, O(1) extra space",
        "description": "Bitmask enumeration - iterate all 2^n masks",
    },
}


# ============================================================================
# JUDGE_FUNC - Validate subsets
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Subsets results."""
    import json
    nums = json.loads(input_data.strip())
    n = len(nums)
    nums_set = set(nums)
    
    # Each subset should only contain elements from nums
    for subset in actual:
        for num in subset:
            if num not in nums_set:
                return False
    
    # Check no duplicate subsets
    sorted_subsets = [tuple(sorted(s)) for s in actual]
    if len(set(sorted_subsets)) != len(actual):
        return False
    
    # Check correct count: 2^n subsets
    if len(actual) != (1 << n):
        return False
    
    return True


JUDGE_FUNC = judge


# ============================================================================
# Solution 1: Backtracking with Start-Index Canonicalization
# Time: O(n × 2^n), Space: O(n)
#   - Use start_index to enforce canonical ordering
#   - Collect at every node (not just leaves)
#   - 2^n subsets, O(n) to copy each
# ============================================================================
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


# ============================================================================
# Solution 2: Bitmask Enumeration
# Time: O(n × 2^n), Space: O(1) extra (excluding output)
#   - Each integer 0 to 2^n-1 represents a unique subset
#   - Bit i set means include nums[i]
#   - Iterate and decode each mask
# ============================================================================
class SolutionBitmask:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        """
        Generate all subsets using bitmask enumeration.

        Key Insight:
        - There are 2^n subsets of an n-element set
        - Each integer from 0 to 2^n-1 uniquely represents a subset
        - Bit i being set (1) means include nums[i]

        Example for nums = [1, 2, 3]:
            mask=0 (000): []
            mask=1 (001): [1]
            mask=2 (010): [2]
            mask=3 (011): [1, 2]
            mask=4 (100): [3]
            mask=5 (101): [1, 3]
            mask=6 (110): [2, 3]
            mask=7 (111): [1, 2, 3]

        Time: O(n × 2^n) - iterate 2^n masks, decode each in O(n)
        Space: O(1) extra - no recursion stack
        """
        n = len(nums)
        result = []

        # Iterate all 2^n possible masks
        for mask in range(1 << n):
            # Decode mask to subset
            subset = []
            for i in range(n):
                if mask & (1 << i):  # Check if bit i is set
                    subset.append(nums[i])
            result.append(subset)

        return result


def solve():
    import json
    """
    Input format:
    Line 1: nums (comma-separated)
    
    Example:
    1,2,3
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')
    
    nums = json.loads(lines[0])
    
    solver = get_solver(SOLUTIONS)
    result = solver.subsets(nums)
    
    print(result)


if __name__ == "__main__":
    solve()

