# solutions/0283_move_zeroes.py
"""
================================================================================
LeetCode 283: Move Zeroes
================================================================================

Problem: Given an integer array nums, move all 0's to the end of it while
         maintaining the relative order of the non-zero elements.
         Note: You must do this in-place without making a copy of the array.

API Kernel: TwoPointersTraversal
Pattern: same_direction_writer
Family: in_place_array_modification

--------------------------------------------------------------------------------
TWO POINTERS PATTERN: SAME-DIRECTION (READER/WRITER)
--------------------------------------------------------------------------------

This problem is a two-phase application of the same-direction pattern:
1. Phase 1: Move all non-zero elements to the front (standard writer pattern)
2. Phase 2: Fill remaining positions with zeros

DELTA from Remove Element (LeetCode 27):
- Same core logic: keep non-zero elements
- Additional step: fill remaining positions with zeros (not just return count)

INVARIANT: nums[0:write] contains all non-zero elements from nums[0:read]
           in their original relative order.

Alternative Approach (Swap-based):
    Instead of overwriting and filling, we can SWAP non-zero elements forward.
    This preserves zeros in their new positions automatically.

--------------------------------------------------------------------------------
COMPLEXITY ANALYSIS
--------------------------------------------------------------------------------

Time:  O(n) - Single pass (or two passes for fill approach)
Space: O(1) - In-place modification

================================================================================
"""
from typing import List


# ============================================================================
# Solution - O(n) Same-Direction with Fill
# ============================================================================

class Solution:
    """
    Optimal solution using reader/writer pattern with zero-fill phase.
    
    This approach minimizes writes when there are few zeros, as we only
    write non-zero elements once each.
    """
    
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Move all zeros to the end while maintaining relative order of non-zeros.
        
        Args:
            nums: Array of integers (modified in-place)
        """
        n: int = len(nums)
        
        # PHASE 1: Move all non-zero elements to the front
        write_index: int = 0
        
        for read_index in range(n):
            if nums[read_index] != 0:
                nums[write_index] = nums[read_index]
                write_index += 1
        
        # PHASE 2: Fill remaining positions with zeros
        for i in range(write_index, n):
            nums[i] = 0


# ============================================================================
# Alternative: Swap-Based Approach
# ============================================================================

class SolutionSwap:
    """
    Alternative using swaps instead of overwrite + fill.
    
    Each non-zero element is swapped with the element at write_index.
    Zeros naturally accumulate at the end through swapping.
    
    This approach uses more writes when zeros are sparse, but is more
    intuitive and works in a single pass.
    """
    
    def moveZeroes(self, nums: List[int]) -> None:
        write_index: int = 0
        
        for read_index in range(len(nums)):
            if nums[read_index] != 0:
                # SWAP: Exchange non-zero with position at write_index
                # This moves zeros toward the end
                nums[write_index], nums[read_index] = nums[read_index], nums[write_index]
                write_index += 1


# ============================================================================
# Alternative: Optimized Swap (Avoid Self-Swap)
# ============================================================================

class SolutionOptimizedSwap:
    """
    Optimized swap version that avoids unnecessary self-swaps.
    
    When write_index == read_index, swapping is unnecessary.
    This optimization helps when zeros are rare.
    """
    
    def moveZeroes(self, nums: List[int]) -> None:
        write_index: int = 0
        
        for read_index in range(len(nums)):
            if nums[read_index] != 0:
                if write_index != read_index:
                    nums[write_index], nums[read_index] = nums[read_index], nums[write_index]
                write_index += 1


# ============================================================================
# Alternative: Snowball Method (Count Zeros)
# ============================================================================

class SolutionSnowball:
    """
    Snowball method: track the "snowball" of zeros rolling through the array.
    
    As we encounter zeros, the snowball grows. When we encounter a non-zero,
    we swap it with the front of the snowball.
    
    Conceptually different but equivalent to the swap approach.
    """
    
    def moveZeroes(self, nums: List[int]) -> None:
        snowball_size: int = 0  # Number of zeros accumulated
        
        for i in range(len(nums)):
            if nums[i] == 0:
                snowball_size += 1
            elif snowball_size > 0:
                # Swap current element with front of snowball
                nums[i - snowball_size], nums[i] = nums[i], nums[i - snowball_size]


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format:
        Line 1: Space-separated integers
    
    Output format:
        Space-separated integers (zeros moved to end)
    
    Example:
        Input:  0 1 0 3 12
        Output: 1 3 12 0 0
    """
    import sys
    
    line = sys.stdin.read().strip()
    if not line:
        return
    
    nums = list(map(int, line.split()))
    
    solution = Solution()
    solution.moveZeroes(nums)
    
    print(' '.join(map(str, nums)))


if __name__ == "__main__":
    solve()

