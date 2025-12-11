# solutions/0027_remove_element.py
"""
================================================================================
LeetCode 27: Remove Element
================================================================================

Problem: Given an integer array nums and an integer val, remove all occurrences
         of val in nums in-place. The order of elements may be changed.
         Return the number of elements not equal to val.

API Kernel: TwoPointersTraversal
Pattern: same_direction_writer
Family: in_place_array_modification

--------------------------------------------------------------------------------
TWO POINTERS PATTERN: SAME-DIRECTION (READER/WRITER)
--------------------------------------------------------------------------------

This problem uses the same-direction pattern with a simple keep condition:
keep the element if it's not equal to the target value.

DELTA from Remove Duplicates (LeetCode 26):
- Condition changes from "different from last written" to "not equal to val"
- Array need not be sorted
- Write index starts at 0 (no guaranteed first element to keep)

INVARIANT: nums[0:write] contains all elements != val from nums[0:read].

Algorithm:
1. Scan through array with read pointer
2. If current element != val, copy to write position and increment write
3. Return write (count of elements kept)

--------------------------------------------------------------------------------
COMPLEXITY ANALYSIS
--------------------------------------------------------------------------------

Time:  O(n) - Single pass through the array
Space: O(1) - In-place modification

================================================================================
"""
from typing import List


# ============================================================================
# Solution - O(n) Same-Direction Pointers
# ============================================================================

class Solution:
    """
    Optimal solution using reader/writer pointer pattern.
    
    Simple and efficient: elements not equal to val are copied forward,
    effectively "overwriting" the vals.
    """
    
    def removeElement(self, nums: List[int], val: int) -> int:
        """
        Remove all occurrences of val in-place.
        
        Args:
            nums: Array of integers (modified in-place)
            val: Value to remove
            
        Returns:
            Number of elements remaining (not equal to val)
        """
        # WRITE POINTER: Position for next element to keep
        write_index: int = 0
        
        # READ POINTER: Scan through all elements
        for read_index in range(len(nums)):
            # CHECK CONDITION: Keep if not equal to val
            if nums[read_index] != val:
                nums[write_index] = nums[read_index]
                write_index += 1
        
        return write_index


# ============================================================================
# Alternative: Two-Pointer from Both Ends
# ============================================================================

class SolutionTwoEnds:
    """
    Alternative using pointers from both ends.
    
    More efficient when val is rare: we swap val elements with elements
    from the end, minimizing total writes.
    
    Useful when:
    - Elements to remove are rare
    - We want to minimize write operations
    """
    
    def removeElement(self, nums: List[int], val: int) -> int:
        left: int = 0
        right: int = len(nums) - 1
        
        while left <= right:
            if nums[left] == val:
                # Swap with element from end
                nums[left] = nums[right]
                right -= 1
                # Don't increment left - need to check swapped element
            else:
                left += 1
        
        return left


# ============================================================================
# Alternative: Functional Style with Filter
# ============================================================================

class SolutionFunctional:
    """
    Functional-style solution using list comprehension.
    
    Note: This creates a new list, so it doesn't strictly satisfy the
    "in-place" requirement. Shown for comparison purposes.
    """
    
    def removeElement(self, nums: List[int], val: int) -> int:
        # Create filtered list
        kept = [x for x in nums if x != val]
        
        # Copy back (to satisfy interface requirements)
        for i, x in enumerate(kept):
            nums[i] = x
        
        return len(kept)


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format:
        Line 1: Space-separated integers (array)
        Line 2: Value to remove
    
    Output format:
        Line 1: Number of remaining elements
        Line 2: Remaining elements (space-separated)
    
    Example:
        Input:
        3 2 2 3
        3
        Output:
        2
        2 2
    """
    import sys
    
    lines = sys.stdin.read().strip().split('\n')
    nums = list(map(int, lines[0].split())) if lines[0] else []
    val = int(lines[1])
    
    solution = Solution()
    k = solution.removeElement(nums, val)
    
    print(k)
    if k > 0:
        print(' '.join(map(str, nums[:k])))


if __name__ == "__main__":
    solve()

