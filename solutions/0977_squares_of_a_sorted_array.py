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


# ============================================================================
# Solution - O(n) Opposite Pointers (Write from End)
# ============================================================================

class Solution:
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


# ============================================================================
# Alternative: Using Absolute Values (Equivalent Logic)
# ============================================================================

class SolutionAbsolute:
    """
    Alternative using absolute values for comparison.
    
    Equivalent to comparing squares, but may be clearer for understanding.
    """
    
    def sortedSquares(self, nums: List[int]) -> List[int]:
        n = len(nums)
        result = [0] * n
        
        left, right = 0, n - 1
        write = n - 1
        
        while left <= right:
            if abs(nums[left]) > abs(nums[right]):
                result[write] = nums[left] ** 2
                left += 1
            else:
                result[write] = nums[right] ** 2
                right -= 1
            write -= 1
        
        return result


# ============================================================================
# Alternative: Find Split Point Then Merge
# ============================================================================

class SolutionSplit:
    """
    Alternative: find where negatives end, then merge two sequences.
    
    More explicit about the "merge two sorted sequences" structure.
    """
    
    def sortedSquares(self, nums: List[int]) -> List[int]:
        n = len(nums)
        
        # Find the split point (first non-negative number)
        split = 0
        while split < n and nums[split] < 0:
            split += 1
        
        # Two pointers: left goes backward through negatives, right goes forward
        left = split - 1
        right = split
        result = []
        
        # Merge: smaller squares first
        while left >= 0 and right < n:
            left_sq = nums[left] ** 2
            right_sq = nums[right] ** 2
            
            if left_sq <= right_sq:
                result.append(left_sq)
                left -= 1
            else:
                result.append(right_sq)
                right += 1
        
        # Remaining elements
        while left >= 0:
            result.append(nums[left] ** 2)
            left -= 1
        
        while right < n:
            result.append(nums[right] ** 2)
            right += 1
        
        return result


# ============================================================================
# Alternative: Simple Sort (Suboptimal)
# ============================================================================

class SolutionSort:
    """
    Simple sorting approach.
    
    Square all elements, then sort. O(n log n) instead of O(n).
    """
    
    def sortedSquares(self, nums: List[int]) -> List[int]:
        return sorted(x * x for x in nums)


# ============================================================================
# Alternative: Using Deque for Bidirectional Building
# ============================================================================

class SolutionDeque:
    """
    Alternative using deque for bidirectional insertion.
    
    Builds result by appending to the end (largest squares first).
    """
    
    def sortedSquares(self, nums: List[int]) -> List[int]:
        from collections import deque
        
        result = deque()
        left, right = 0, len(nums) - 1
        
        while left <= right:
            if abs(nums[left]) > abs(nums[right]):
                result.appendleft(nums[left] ** 2)
                left += 1
            else:
                result.appendleft(nums[right] ** 2)
                right -= 1
        
        return list(result)


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
    
    solution = Solution()
    result = solution.sortedSquares(nums)
    
    print(' '.join(map(str, result)))


if __name__ == "__main__":
    solve()

