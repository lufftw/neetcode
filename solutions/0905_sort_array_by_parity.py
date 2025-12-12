# solutions/0905_sort_array_by_parity.py
"""
================================================================================
LeetCode 905: Sort Array By Parity
================================================================================

Problem: Given an integer array nums, move all the even integers at the beginning
         of the array followed by all the odd integers. Return any array that
         satisfies this condition.

API Kernel: TwoPointersTraversal
Pattern: two_way_partition
Family: partitioning

--------------------------------------------------------------------------------
TWO POINTERS PATTERN: TWO-WAY PARTITION
--------------------------------------------------------------------------------

This is a simplified partition problem with only two categories (even/odd).

DELTA from Dutch National Flag (LeetCode 75):
- Only 2 categories instead of 3
- Only need 2 pointers instead of 3
- Can use either same-direction or opposite pointers approach

Two Approaches:
1. OPPOSITE POINTERS: Start from both ends, swap when left is odd and right is even
2. SAME-DIRECTION (Writer): Move evens to front using reader/writer pattern

INVARIANT (Opposite Pointers):
- nums[0:left] contains only even numbers
- nums[right+1:n] contains only odd numbers

--------------------------------------------------------------------------------
COMPLEXITY ANALYSIS
--------------------------------------------------------------------------------

Time:  O(n) - Each element examined once
Space: O(1) - In-place swaps

================================================================================
"""
from typing import List
from _runner import get_solver


# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# Polymorphic pattern: each entry specifies class + method
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionOppositePointers",
        "method": "sortArrayByParity",
        "complexity": "O(n) time, O(1) space",
        "description": "Opposite pointers swapping evens and odds",
    },
    "opposite_pointers": {
        "class": "SolutionOppositePointers",
        "method": "sortArrayByParity",
        "complexity": "O(n) time, O(1) space",
        "description": "Opposite pointers swapping evens and odds",
    },
    "writer": {
        "class": "SolutionWriter",
        "method": "sortArrayByParity",
        "complexity": "O(n) time, O(1) space",
        "description": "Same-direction reader/writer pattern",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================

def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output has evens before odds.
    
    Args:
        actual: Program output (space-separated integers as string, list, or single int)
        expected: Expected output (None if from generator)
        input_data: Raw input string (space-separated integers)
    
    Returns:
        bool: True if evens come before odds
    """
    line = input_data.strip()
    nums = list(map(int, line.split())) if line else []
    
    # Parse actual output - handle int (from ast.literal_eval), str, or list
    if isinstance(actual, int):
        actual_nums = [actual]
    elif isinstance(actual, str):
        actual_nums = list(map(int, actual.strip().split())) if actual.strip() else []
    elif isinstance(actual, list):
        actual_nums = actual
    else:
        return False
    
    # Check if evens come before odds
    if not actual_nums:
        return actual_nums == nums
    
    # Find first odd index
    first_odd_idx = None
    for i, num in enumerate(actual_nums):
        if num % 2 == 1:
            first_odd_idx = i
            break
    
    # If no odds, all evens is valid
    if first_odd_idx is None:
        return len(actual_nums) == len(nums)
    
    # Check all before first_odd_idx are even, all after are odd
    for i in range(first_odd_idx):
        if actual_nums[i] % 2 == 1:
            return False
    
    for i in range(first_odd_idx, len(actual_nums)):
        if actual_nums[i] % 2 == 0:
            return False
    
    # Check that all elements from original are present
    return sorted(actual_nums) == sorted(nums)


JUDGE_FUNC = judge


# ============================================
# Solution 1: Opposite Pointers
# Time: O(n), Space: O(1)
#   - Even numbers migrate to left, odd to right
#   - In-place swaps
#   - Optimal single-pass approach
# ============================================
class SolutionOppositePointers:
    """
    Optimal solution using opposite pointers.
    
    Even numbers migrate to the left, odd numbers to the right.
    """
    
    def sortArrayByParity(self, nums: List[int]) -> List[int]:
        """
        Move all even numbers before all odd numbers.
        
        Args:
            nums: Array of integers
            
        Returns:
            Array with evens before odds (modified in-place)
        """
        left: int = 0
        right: int = len(nums) - 1
        
        while left < right:
            # Find next odd number from left
            while left < right and nums[left] % 2 == 0:
                left += 1
            
            # Find next even number from right
            while left < right and nums[right] % 2 == 1:
                right -= 1
            
            # Swap odd (at left) with even (at right)
            if left < right:
                nums[left], nums[right] = nums[right], nums[left]
                left += 1
                right -= 1
        
        return nums


# ============================================
# Solution 2: Same-Direction Writer Pattern
# Time: O(n), Space: O(1)
#   - Move all even numbers to front by swapping
#   - Single pass with write pointer
#   - Alternative approach with same complexity
# ============================================
class SolutionWriter:
    """
    Alternative using same-direction reader/writer pattern.
    
    Move all even numbers to the front by swapping with write position.
    """
    
    def sortArrayByParity(self, nums: List[int]) -> List[int]:
        write_index: int = 0
        
        for read_index in range(len(nums)):
            if nums[read_index] % 2 == 0:
                # Even number: swap to write position
                nums[write_index], nums[read_index] = nums[read_index], nums[write_index]
                write_index += 1
        
        return nums


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format:
        Line 1: Space-separated integers
    
    Output format:
        Rearranged array (evens before odds)
    
    Example:
        Input:  3 1 2 4
        Output: 2 4 3 1  (or any valid arrangement)
    """
    import sys
    
    line = sys.stdin.read().strip()
    nums = list(map(int, line.split())) if line else []
    
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.sortArrayByParity(nums)
    
    print(' '.join(map(str, result)))


if __name__ == "__main__":
    solve()
