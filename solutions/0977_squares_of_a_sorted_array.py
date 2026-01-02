# solutions/0977_squares_of_a_sorted_array.py
"""
Problem: Squares of a Sorted Array
Link: https://leetcode.com/problems/squares-of-a-sorted-array/

Given an integer array nums sorted in non-decreasing order, return an array of the squares of each number sorted in non-decreasing order.

Example 1:
    Input: nums = [-4,-1,0,3,10]
    Output: [0,1,9,16,100]
    Explanation: After squaring, the array becomes [16,1,0,9,100].
                 After sorting, it becomes [0,1,9,16,100].

Example 2:
    Input: nums = [-7,-3,2,3,11]
    Output: [4,9,9,49,121]

Constraints:
- 1 <= nums.length <= 10^4
- -10^4 <= nums[i] <= 10^4
- nums is sorted in non-decreasing order.

Topics: Array, Two Pointers, Sorting

Follow-up: Squaring each element and sorting the new array is very trivial, could you find an O(n) solution using a different approach?
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
        "method": "sortedSquares",
        "complexity": "O(n) time, O(n) space",
        "description": "Two pointers from ends merging largest squares first",
    },
    "two_pointers": {
        "class": "SolutionTwoPointers",
        "method": "sortedSquares",
        "complexity": "O(n) time, O(n) space",
        "description": "Two pointers from ends merging largest squares first",
    },
    "sort": {
        "class": "SolutionSort",
        "method": "sortedSquares",
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
    import json
    line = input_data.strip()
    nums = json.loads(line) if line else []
    
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


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    import json
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
    import json
    
    line = sys.stdin.read().strip()
    nums = json.loads(line) if line else []
    
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.sortedSquares(nums)
    
    print(' '.join(map(str, result)))


if __name__ == "__main__":
    solve()
