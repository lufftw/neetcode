# solutions/0922_sort_array_by_parity_ii.py
"""
================================================================================
LeetCode 922: Sort Array By Parity II
================================================================================

Problem: Given an array of integers nums, half of the integers in nums are odd,
         and the other half are even. Sort the array so that whenever
         nums[i] is odd, i is odd, and whenever nums[i] is even, i is even.
         Return any answer array that satisfies this condition.

API Kernel: TwoPointersTraversal
Pattern: interleaved_partition
Family: partitioning

--------------------------------------------------------------------------------
TWO POINTERS PATTERN: INTERLEAVED PARTITION
--------------------------------------------------------------------------------

This problem requires a specific interleaving pattern where:
- Even indices (0, 2, 4, ...) must contain even values
- Odd indices (1, 3, 5, ...) must contain odd values

DELTA from Sort By Parity (LeetCode 905):
- Position-dependent constraint instead of simple grouping
- Need two separate pointers: one for even indices, one for odd indices

Algorithm:
1. Use pointer i for even positions (0, 2, 4, ...)
2. Use pointer j for odd positions (1, 3, 5, ...)
3. When i finds an odd number at even position, and j finds an even number
   at odd position, swap them

INVARIANT:
- All even positions < i contain even numbers
- All odd positions < j contain odd numbers

--------------------------------------------------------------------------------
COMPLEXITY ANALYSIS
--------------------------------------------------------------------------------

Time:  O(n) - Each position examined once
Space: O(1) - In-place swaps

================================================================================
"""
from typing import List


# ============================================================================
# Solution - O(n) Two Independent Pointers
# ============================================================================

class Solution:
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
# Alternative: Single Pass with Two Pointers
# ============================================================================

class SolutionSinglePass:
    """
    Alternative single-pass approach.
    
    Process even indices; when finding an odd number, find an even number
    at an odd position to swap with.
    """
    
    def sortArrayByParityII(self, nums: List[int]) -> List[int]:
        n = len(nums)
        odd_ptr = 1  # Pointer to search for even numbers at odd positions
        
        for even_ptr in range(0, n, 2):
            # Check if current even position has odd number
            if nums[even_ptr] % 2 == 1:
                # Find even number at odd position
                while nums[odd_ptr] % 2 == 1:
                    odd_ptr += 2
                
                # Swap
                nums[even_ptr], nums[odd_ptr] = nums[odd_ptr], nums[even_ptr]
        
        return nums


# ============================================================================
# Alternative: New Array Approach
# ============================================================================

class SolutionNewArray:
    """
    Alternative creating a new array.
    
    Uses O(n) extra space but simpler logic.
    """
    
    def sortArrayByParityII(self, nums: List[int]) -> List[int]:
        n = len(nums)
        result = [0] * n
        
        even_idx = 0
        odd_idx = 1
        
        for num in nums:
            if num % 2 == 0:
                result[even_idx] = num
                even_idx += 2
            else:
                result[odd_idx] = num
                odd_idx += 2
        
        return result


# ============================================================================
# Alternative: Two-Pass Segregate Then Interleave
# ============================================================================

class SolutionTwoPass:
    """
    Alternative: first segregate evens/odds, then interleave.
    
    Less efficient but conceptually simple.
    """
    
    def sortArrayByParityII(self, nums: List[int]) -> List[int]:
        evens = [x for x in nums if x % 2 == 0]
        odds = [x for x in nums if x % 2 == 1]
        
        result = []
        for i in range(len(evens)):
            result.append(evens[i])
            result.append(odds[i])
        
        return result


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
    
    solution = Solution()
    result = solution.sortArrayByParityII(nums)
    
    print(' '.join(map(str, result)))


if __name__ == "__main__":
    solve()

