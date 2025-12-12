# solutions/0977_squares_of_a_sorted_array.py
"""
================================================================================
LeetCode 977: Squares of a Sorted Array
================================================================================

Problem: Given an integer array nums sorted in non-decreasing order, return an
         array of the squares of each number sorted in non-decreasing order.

API Kernel: TwoPointersTraversal
Pattern: merge_from_ends
Family: merge_pattern

--------------------------------------------------------------------------------
TWO POINTERS PATTERN: MERGE FROM ENDS
--------------------------------------------------------------------------------

This problem is a clever application of the merge pattern on a single array.

Key Insight:
    The input is sorted, but squaring can change the order because negative
    numbers become positive. However, the LARGEST squares are always at the ENDS:
    - Large negative numbers → large squares
    - Large positive numbers → large squares
    
    The smallest squares are somewhere in the middle (around zero).

Algorithm:
    Use opposite pointers from both ends. Compare absolute values (or squares),
    write the larger square to the result array from the END, and move the
    corresponding pointer inward.

INVARIANT: result[write+1:] contains the largest squares in sorted order.

This is essentially merging two sorted sequences:
- nums[0:k] reversed (negative numbers, largest first)
- nums[k:n] (positive numbers, largest last)

--------------------------------------------------------------------------------
COMPLEXITY ANALYSIS
--------------------------------------------------------------------------------

Time:  O(n) - Single pass through the array
Space: O(n) - Output array (or O(1) if output doesn't count)

================================================================================
"""
from typing import List
import os


# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# ============================================
SOLUTIONS = {
    "default": {
        "method": "solve_two_pointers",
        "complexity": "O(n) time, O(n) space",
        "description": "Two pointers from ends merging largest squares first",
    },
    "two_pointers": {
        "method": "solve_two_pointers",
        "complexity": "O(n) time, O(n) space",
        "description": "Two pointers from ends merging largest squares first",
    },
    "sort": {
        "method": "solve_sort",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Square all elements then sort (suboptimal)",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================

def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output is correctly sorted squares.
    
    Args:
        actual: Program output (space-separated integers as string)
        expected: Expected output (None if from generator)
        input_data: Raw input string (space-separated sorted integers)
    
    Returns:
        bool: True if correctly sorted squares
    """
    line = input_data.strip()
    nums = list(map(int, line.split())) if line else []
    
    # Compute correct answer
    correct = sorted(x * x for x in nums)
    
    # Parse actual output
    if isinstance(actual, str):
        actual_vals = list(map(int, actual.strip().split())) if actual.strip() else []
    elif isinstance(actual, list):
        actual_vals = actual
    else:
        return False
    
    return actual_vals == correct


JUDGE_FUNC = judge


# ============================================
# Solution 1: Two Pointers from Ends
# Time: O(n), Space: O(n)
#   - Compares absolute values at both ends
#   - Writes larger square to result from back to front
#   - Optimal single-pass approach
# ============================================
class SolutionTwoPointers:
    """
    Optimal solution using opposite pointers.
    
    Compares absolute values at both ends and writes the larger square
    to the result array from back to front.
    """
    
    def sortedSquares(self, nums: List[int]) -> List[int]:
        """
        Return array of squares in sorted order.
        
        Args:
            nums: Sorted array of integers
            
        Returns:
            Sorted array of squares
        """
        n: int = len(nums)
        result: List[int] = [0] * n
        
        # POINTERS: Start from both ends
        left: int = 0
        right: int = n - 1
        
        # WRITE: Fill result from the end (largest squares first)
        write: int = n - 1
        
        while left <= right:
            left_square: int = nums[left] * nums[left]
            right_square: int = nums[right] * nums[right]
            
            if left_square > right_square:
                result[write] = left_square
                left += 1
            else:
                result[write] = right_square
                right -= 1
            
            write -= 1
        
        return result


# ============================================
# Solution 2: Square Then Sort
# Time: O(n log n), Space: O(n)
#   - Simple approach: square all then sort
#   - O(n log n) instead of O(n)
#   - Useful for comparison or when simplicity is prioritized
# ============================================
class SolutionSort:
    """
    Simple sorting approach.
    
    Square all elements, then sort. O(n log n) instead of O(n).
    """
    
    def sortedSquares(self, nums: List[int]) -> List[int]:
        return sorted(x * x for x in nums)


# ============================================
# Wrapper functions for test_runner integration
# ============================================
def solve_two_pointers(nums: List[int]) -> List[int]:
    """Wrapper for SolutionTwoPointers."""
    return SolutionTwoPointers().sortedSquares(nums)


def solve_sort(nums: List[int]) -> List[int]:
    """Wrapper for SolutionSort."""
    return SolutionSort().sortedSquares(nums)


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format:
        Line 1: Space-separated integers (sorted array)
    
    Output format:
        Sorted squares (space-separated)
    
    Example:
        Input:  -4 -1 0 3 10
        Output: 0 1 9 16 100
    """
    import sys
    
    line = sys.stdin.read().strip()
    nums = list(map(int, line.split())) if line else []
    
    # Read environment variable to select which solution method to use
    method_name = os.environ.get('SOLUTION_METHOD', 'default')
    method_info = SOLUTIONS.get(method_name, SOLUTIONS['default'])
    method_func_name = method_info['method']
    
    # Dynamically call the selected solution method
    method_func = globals()[method_func_name]
    result = method_func(nums)
    
    print(' '.join(map(str, result)))


if __name__ == "__main__":
    solve()
