# solutions/0922_sort_array_by_parity_ii.py
"""
Problem: Sort Array By Parity II
Link: https://leetcode.com/problems/sort-array-by-parity-ii/

Given an array of integers nums, half of the integers in nums are odd, and the other half are even.
Sort the array so that whenever nums[i] is odd, i is odd, and whenever nums[i] is even, i is even.
Return any answer array that satisfies this condition.

Example 1:
    Input: nums = [4,2,5,7]
    Output: [4,5,2,7]
    Explanation: [4,7,2,5], [2,5,4,7], [2,7,4,5] would also have been accepted.

Example 2:
    Input: nums = [2,3]
    Output: [2,3]

Constraints:
- 2 <= nums.length <= 2 * 10^4
- nums.length is even.
- Half of the integers in nums are even.
- 0 <= nums[i] <= 1000

Topics: Array, Two Pointers, Sorting

Follow-up: Could you solve it in-place?
"""
from typing import List
from _runner import get_solver


# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# Polymorphic pattern: each entry specifies class + method
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionTwoPointers",
        "method": "sortArrayByParityII",
        "complexity": "O(n) time, O(1) space",
        "description": "Two independent pointers for even and odd positions",
    },
    "two_pointers": {
        "class": "SolutionTwoPointers",
        "method": "sortArrayByParityII",
        "complexity": "O(n) time, O(1) space",
        "description": "Two independent pointers for even and odd positions",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================

def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output has even values at even indices, odd at odd indices.
    
    Args:
        actual: Program output (space-separated integers as string)
        expected: Expected output (None if from generator)
        input_data: Raw input string (space-separated integers)
    
    Returns:
        bool: True if parity matches indices
    """
    line = input_data.strip()
    nums = list(map(int, line.split())) if line else []
    
    # Parse actual output
    if isinstance(actual, str):
        actual_nums = list(map(int, actual.strip().split())) if actual.strip() else []
    elif isinstance(actual, list):
        actual_nums = actual
    else:
        return False
    
    # Check parity constraint
    for i, num in enumerate(actual_nums):
        if i % 2 == 0:
            if num % 2 != 0:
                return False
        else:
            if num % 2 != 1:
                return False
    
    # Check that all elements from original are present
    return sorted(actual_nums) == sorted(nums)


JUDGE_FUNC = judge


# ============================================
# Solution 1: Two Independent Pointers
# Time: O(n), Space: O(1)
#   - Find misplaced elements at even and odd positions
#   - Swap them when both found
#   - Optimal single-pass approach
# ============================================
class SolutionTwoPointers:
    """
    Optimal solution using two pointers for even and odd positions.
    
    Find misplaced elements at even and odd positions and swap them.
    """
    
    def sortArrayByParityII(self, nums: List[int]) -> List[int]:
        """
        Sort array so even indices have even values, odd indices have odd values.
        
        Args:
            nums: Array with equal count of even and odd integers
            
        Returns:
            Rearranged array satisfying the parity constraint
        """
        n: int = len(nums)
        
        # POINTERS: One for even positions, one for odd positions
        even_ptr: int = 0  # Points to even indices (0, 2, 4, ...)
        odd_ptr: int = 1   # Points to odd indices (1, 3, 5, ...)
        
        while even_ptr < n and odd_ptr < n:
            # Find misplaced odd number at even position
            while even_ptr < n and nums[even_ptr] % 2 == 0:
                even_ptr += 2
            
            # Find misplaced even number at odd position
            while odd_ptr < n and nums[odd_ptr] % 2 == 1:
                odd_ptr += 2
            
            # Swap misplaced elements if both found
            if even_ptr < n and odd_ptr < n:
                nums[even_ptr], nums[odd_ptr] = nums[odd_ptr], nums[even_ptr]
                even_ptr += 2
                odd_ptr += 2
        
        return nums


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format:
        Line 1: Space-separated integers
    
    Output format:
        Rearranged array with even indices having even values
    
    Example:
        Input:  4 2 5 7
        Output: 4 5 2 7  (or any valid arrangement)
    """
    import sys
    
    line = sys.stdin.read().strip()
    nums = list(map(int, line.split())) if line else []
    
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.sortArrayByParityII(nums)
    
    print(' '.join(map(str, result)))


if __name__ == "__main__":
    solve()
