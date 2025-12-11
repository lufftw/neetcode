# solutions/0075_sort_colors.py
"""
================================================================================
LeetCode 75: Sort Colors
================================================================================

Problem: Given an array nums with n objects colored red, white, or blue (0, 1, 2),
         sort them in-place so that objects of the same color are adjacent,
         with the colors in the order red, white, and blue.

API Kernel: TwoPointersTraversal
Pattern: dutch_national_flag
Family: partitioning

--------------------------------------------------------------------------------
TWO POINTERS PATTERN: DUTCH NATIONAL FLAG (THREE-WAY PARTITION)
--------------------------------------------------------------------------------

This is the canonical Dutch National Flag problem, named after the Dutch flag's
three horizontal stripes. It partitions an array into three sections in one pass.

Three Pointers:
- LOW: Boundary for elements < pivot (0s)
- MID: Current element being examined
- HIGH: Boundary for elements > pivot (2s)

INVARIANT:
- nums[0:low] contains all 0s (red)
- nums[low:mid] contains all 1s (white)  
- nums[high+1:n] contains all 2s (blue)
- nums[mid:high+1] is unclassified

Why This Works:
    Each element is examined once. Based on its value:
    - 0: Swap with low, increment both low and mid (0 goes to red section)
    - 1: Just increment mid (1 is already in white section)
    - 2: Swap with high, decrement high (2 goes to blue section)
         Note: Don't increment mid — swapped element needs examination

--------------------------------------------------------------------------------
COMPLEXITY ANALYSIS
--------------------------------------------------------------------------------

Time:  O(n) - Each element examined once
Space: O(1) - In-place swaps only

================================================================================
"""
from typing import List


# ============================================================================
# Solution - O(n) Dutch National Flag Algorithm
# ============================================================================

class Solution:
    """
    Optimal one-pass solution using Dutch National Flag algorithm.
    
    Maintains three regions for 0s, 1s, and 2s while scanning through
    the array exactly once.
    """
    
    def sortColors(self, nums: List[int]) -> None:
        """
        Sort array containing only 0s, 1s, and 2s in-place.
        
        Args:
            nums: Array of integers (0, 1, or 2) to sort in-place
        """
        # POINTERS: Define three region boundaries
        low: int = 0              # Next position for 0
        mid: int = 0              # Current position being examined
        high: int = len(nums) - 1 # Next position for 2
        
        # Process until mid crosses high
        while mid <= high:
            if nums[mid] == 0:
                # CASE 0: Move to "red" section (beginning)
                # Swap with low and advance both pointers
                nums[low], nums[mid] = nums[mid], nums[low]
                low += 1
                mid += 1
                # We can increment mid because swapped element from low
                # is either 0 (already processed) or 1 (correct position)
            
            elif nums[mid] == 2:
                # CASE 2: Move to "blue" section (end)
                # Swap with high and decrement high only
                nums[mid], nums[high] = nums[high], nums[mid]
                high -= 1
                # DON'T increment mid — swapped element is unexamined
            
            else:
                # CASE 1: Already in correct section ("white")
                # Just advance mid
                mid += 1


# ============================================================================
# Alternative: Two-Pass Counting Sort
# ============================================================================

class SolutionCounting:
    """
    Alternative using counting sort approach.
    
    Two passes: first count each color, then overwrite array.
    Simpler to understand but requires two passes.
    """
    
    def sortColors(self, nums: List[int]) -> None:
        # Count occurrences of each color
        count = [0, 0, 0]
        for num in nums:
            count[num] += 1
        
        # Overwrite array with sorted colors
        index = 0
        for color in range(3):
            for _ in range(count[color]):
                nums[index] = color
                index += 1


# ============================================================================
# Alternative: Two-Pointer Partition (Two Passes)
# ============================================================================

class SolutionTwoPartition:
    """
    Alternative using two separate partition passes.
    
    First partition around 1 to separate 0s from {1,2}.
    Then partition the right part around 2 to separate 1s from 2s.
    """
    
    def sortColors(self, nums: List[int]) -> None:
        # First partition: move all 0s to the front
        write = 0
        for i in range(len(nums)):
            if nums[i] == 0:
                nums[write], nums[i] = nums[i], nums[write]
                write += 1
        
        # Second partition: move all 1s after the 0s
        for i in range(write, len(nums)):
            if nums[i] == 1:
                nums[write], nums[i] = nums[i], nums[write]
                write += 1


# ============================================================================
# Alternative: Generic K-Way Partition
# ============================================================================

class SolutionGeneric:
    """
    Generalized version that works for any number of distinct values.
    
    Uses counting sort approach, adaptable to more than 3 colors.
    """
    
    def sortColors(self, nums: List[int], k: int = 3) -> None:
        """Sort array with values in range [0, k-1]."""
        count = [0] * k
        for num in nums:
            count[num] += 1
        
        index = 0
        for value in range(k):
            for _ in range(count[value]):
                nums[index] = value
                index += 1


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format:
        Line 1: Space-separated integers (0, 1, or 2)
    
    Output format:
        Sorted array (space-separated)
    
    Example:
        Input:  2 0 2 1 1 0
        Output: 0 0 1 1 2 2
    """
    import sys
    
    line = sys.stdin.read().strip()
    nums = list(map(int, line.split())) if line else []
    
    solution = Solution()
    solution.sortColors(nums)
    
    print(' '.join(map(str, nums)))


if __name__ == "__main__":
    solve()

