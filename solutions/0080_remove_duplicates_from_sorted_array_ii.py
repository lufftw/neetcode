# solutions/0080_remove_duplicates_from_sorted_array_ii.py
"""
================================================================================
LeetCode 80: Remove Duplicates from Sorted Array II
================================================================================

Problem: Given a sorted array nums, remove some duplicates in-place such that
         each unique element appears at most twice. Return the new length.

API Kernel: TwoPointersTraversal
Pattern: same_direction_writer_k_allowed
Family: in_place_array_modification

--------------------------------------------------------------------------------
TWO POINTERS PATTERN: SAME-DIRECTION WITH K-ALLOWANCE
--------------------------------------------------------------------------------

This problem generalizes the basic deduplication pattern to allow up to K copies.

DELTA from Remove Duplicates (LeetCode 26):
- Instead of "different from nums[write-1]", check "different from nums[write-K]"
- K=2 for this problem (each element appears at most twice)
- Generalizes to any K by changing the lookback distance

INVARIANT: nums[0:write] contains at most K copies of each unique element.

Key Insight:
    We can allow K copies by checking nums[write-K] instead of nums[write-1].
    If the current element equals nums[write-K], we already have K copies,
    so we skip it. Otherwise, we write it.

Why This Works:
    If nums[read] == nums[write-K], then nums[write-K], ..., nums[write-1] are
    all equal (since array is sorted), meaning we already have K copies.

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
    Optimal solution allowing at most 2 copies of each element.
    
    The key insight is that we compare with nums[write_index - 2] to determine
    if we already have 2 copies of the current value.
    """
    
    def removeDuplicates(self, nums: List[int]) -> int:
        """
        Remove duplicates allowing at most 2 copies of each element.
        
        Args:
            nums: Sorted array of integers (modified in-place)
            
        Returns:
            New length with at most 2 copies per unique element
        """
        n: int = len(nums)
        if n <= 2:
            return n
        
        # WRITE POINTER: Start at 2 (first two elements always kept)
        write_index: int = 2
        
        # READ POINTER: Start scanning from index 2
        for read_index in range(2, n):
            # CHECK CONDITION: Keep if different from element 2 positions back
            # If nums[read] != nums[write-2], we don't yet have 2 copies
            if nums[read_index] != nums[write_index - 2]:
                nums[write_index] = nums[read_index]
                write_index += 1
        
        return write_index


# ============================================================================
# Alternative: Generalized K-Copies Solution
# ============================================================================

class SolutionKCopies:
    """
    Generalized solution that allows up to K copies of each element.
    
    This template can solve the K=1 case (original problem) and K=2 case
    (this problem) with a single parameter change.
    """
    
    def removeDuplicates(self, nums: List[int], k: int = 2) -> int:
        """
        Remove duplicates allowing at most k copies of each element.
        
        Args:
            nums: Sorted array of integers
            k: Maximum allowed copies (default 2)
            
        Returns:
            New length with at most k copies per unique element
        """
        n: int = len(nums)
        if n <= k:
            return n
        
        write_index: int = k
        
        for read_index in range(k, n):
            # Compare with element k positions back
            if nums[read_index] != nums[write_index - k]:
                nums[write_index] = nums[read_index]
                write_index += 1
        
        return write_index


# ============================================================================
# Alternative: Explicit Counter Approach
# ============================================================================

class SolutionCounter:
    """
    Alternative using explicit count tracking.
    
    More verbose but may be clearer for understanding the logic.
    """
    
    def removeDuplicates(self, nums: List[int]) -> int:
        if len(nums) <= 2:
            return len(nums)
        
        write_index: int = 1
        count: int = 1
        
        for read_index in range(1, len(nums)):
            if nums[read_index] == nums[read_index - 1]:
                count += 1
            else:
                count = 1
            
            # Keep element if we haven't seen it twice yet
            if count <= 2:
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
        Line 1: New length
        Line 2: Modified array (first k elements)
    
    Example:
        Input:  1 1 1 2 2 3
        Output:
        5
        1 1 2 2 3
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

