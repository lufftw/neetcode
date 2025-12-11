# solutions/0026_remove_duplicates_from_sorted_array.py
"""
================================================================================
LeetCode 26: Remove Duplicates from Sorted Array
================================================================================

Problem: Given an integer array nums sorted in non-decreasing order, remove the
         duplicates in-place such that each unique element appears only once.
         Return the number of unique elements (k), with the first k elements of
         nums containing the unique elements in their original order.

API Kernel: TwoPointersTraversal
Pattern: same_direction_writer
Family: in_place_array_modification

--------------------------------------------------------------------------------
TWO POINTERS PATTERN: SAME-DIRECTION (READER/WRITER)
--------------------------------------------------------------------------------

This is the canonical same-direction two-pointer pattern for in-place modification.

Pointer Roles:
- READ pointer (fast): Scans through all elements
- WRITE pointer (slow): Marks where the next unique element should be placed

INVARIANT: nums[0:write] contains all unique elements seen in nums[0:read].

Key Insight:
    Since the array is SORTED, duplicates are always adjacent. We only need to
    compare nums[read] with nums[write-1] (the last written element).

Algorithm:
1. Start write at 1 (first element is always unique)
2. For each read position from 1 to n-1:
   - If nums[read] != nums[write-1], copy to write position and increment write
3. Return write (the count of unique elements)

--------------------------------------------------------------------------------
COMPLEXITY ANALYSIS
--------------------------------------------------------------------------------

Time:  O(n) - Single pass through the array
Space: O(1) - In-place modification, only two indices

================================================================================
"""
from typing import List


# ============================================================================
# Solution - O(n) Same-Direction Pointers
# ============================================================================

class Solution:
    """
    Optimal solution using reader/writer pointer pattern.
    
    Maintains the invariant that nums[0:write_index] contains exactly
    one copy of each unique value seen so far.
    """
    
    def removeDuplicates(self, nums: List[int]) -> int:
        """
        Remove duplicates in-place, keeping one copy of each unique element.
        
        Args:
            nums: Sorted array of integers (modified in-place)
            
        Returns:
            Number of unique elements (new logical length)
        """
        if len(nums) == 0:
            return 0
        
        # WRITE POINTER: Position where next unique element will be placed
        # Start at 1 because nums[0] is always kept (first element is unique)
        write_index: int = 1
        
        # READ POINTER: Scan through array looking for new unique values
        for read_index in range(1, len(nums)):
            # CHECK CONDITION: Is this a new unique value?
            # Compare with the last written element (nums[write_index - 1])
            if nums[read_index] != nums[write_index - 1]:
                # WRITE: Copy unique value to write position
                nums[write_index] = nums[read_index]
                write_index += 1
        
        # write_index now equals the count of unique elements
        return write_index


# ============================================================================
# Alternative: Using Enumerate (Slightly More Pythonic)
# ============================================================================

class SolutionEnumerate:
    """
    Alternative using enumerate for cleaner iteration.
    
    Functionally identical but may be more readable for some developers.
    """
    
    def removeDuplicates(self, nums: List[int]) -> int:
        if not nums:
            return 0
        
        write_index: int = 1
        
        for read_index, value in enumerate(nums):
            if read_index > 0 and value != nums[write_index - 1]:
                nums[write_index] = value
                write_index += 1
        
        return write_index


# ============================================================================
# Alternative: Generic Template Form
# ============================================================================

class SolutionTemplate:
    """
    Template-based solution showing the general pattern structure.
    
    This form can be easily adapted for similar problems by changing
    the keep_condition function.
    """
    
    def removeDuplicates(self, nums: List[int]) -> int:
        if not nums:
            return 0
        
        def should_keep(read_idx: int, write_idx: int) -> bool:
            """Condition: keep element if it's different from last written."""
            return nums[read_idx] != nums[write_idx - 1]
        
        write_index: int = 1  # First element always kept
        
        for read_index in range(1, len(nums)):
            if should_keep(read_index, write_index):
                nums[write_index] = nums[read_index]
                write_index += 1
        
        return write_index


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format:
        Line 1: Space-separated integers (sorted array)
    
    Output format:
        Line 1: Number of unique elements
        Line 2: The unique elements (space-separated)
    
    Example:
        Input:  1 1 2
        Output: 
        2
        1 2
    """
    import sys
    
    line = sys.stdin.read().strip()
    if not line:
        print(0)
        return
    
    nums = list(map(int, line.split()))
    
    solution = Solution()
    k = solution.removeDuplicates(nums)
    
    print(k)
    if k > 0:
        print(' '.join(map(str, nums[:k])))


if __name__ == "__main__":
    solve()

