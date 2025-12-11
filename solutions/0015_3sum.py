# solutions/0015_3sum.py
"""
================================================================================
LeetCode 15: 3Sum
================================================================================

Problem: Given an integer array nums, return all triplets [nums[i], nums[j], nums[k]]
         such that i != j != k and nums[i] + nums[j] + nums[k] == 0.
         The solution set must not contain duplicate triplets.

API Kernel: TwoPointersTraversal
Pattern: dedup_sorted_enumeration
Family: multi_sum_problems

--------------------------------------------------------------------------------
TWO POINTERS PATTERN: DEDUP + SORTED ENUMERATION
--------------------------------------------------------------------------------

This problem combines sorting, opposite pointers, and duplicate skipping into
a unified approach for finding all unique triplets.

Algorithm:
1. Sort the array to enable two-pointer search and deduplication
2. Fix the first element with an outer loop
3. Use opposite pointers to find pairs that sum to the complement
4. Skip duplicates at all three levels to avoid duplicate triplets

INVARIANT: After processing index i, all triplets starting with nums[i] have
           been found exactly once.

Key Deduplication Rules:
- Skip nums[i] if nums[i] == nums[i-1] (same first element)
- Skip nums[left] if nums[left] == nums[left+1] after finding a triplet
- Skip nums[right] if nums[right] == nums[right-1] after finding a triplet

--------------------------------------------------------------------------------
COMPLEXITY ANALYSIS
--------------------------------------------------------------------------------

Time:  O(n²) - O(n log n) sorting + O(n²) for nested iteration
Space: O(1) extra (excluding output and sorting space)

================================================================================
"""
from typing import List


# ============================================================================
# Solution - O(n²) Sort + Two Pointers
# ============================================================================

class Solution:
    """
    Optimal solution using sorting and two-pointer technique.
    
    The key insight is that sorting enables both efficient pair search
    and systematic duplicate avoidance.
    """
    
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """
        Find all unique triplets that sum to zero.
        
        Args:
            nums: List of integers
            
        Returns:
            List of triplets [a, b, c] where a + b + c = 0
        """
        n: int = len(nums)
        if n < 3:
            return []
        
        # SORT: Enable two-pointer search and deduplication
        nums.sort()
        
        result: List[List[int]] = []
        
        # OUTER LOOP: Fix the first element
        for i in range(n - 2):
            # DEDUP: Skip duplicate first elements
            # Must check i > 0 to avoid index out of bounds
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            
            # PRUNING: Early termination if smallest sum > 0
            # nums[i] is smallest in remaining array; if nums[i] > 0,
            # no triplet starting here can sum to 0
            if nums[i] > 0:
                break
            
            # PRUNING: Skip if largest possible sum < 0
            if nums[i] + nums[n - 2] + nums[n - 1] < 0:
                continue
            
            # TWO POINTERS: Find pairs summing to -nums[i]
            target: int = -nums[i]
            left: int = i + 1
            right: int = n - 1
            
            while left < right:
                current_sum: int = nums[left] + nums[right]
                
                if current_sum == target:
                    # FOUND: Record triplet
                    result.append([nums[i], nums[left], nums[right]])
                    
                    # DEDUP: Skip duplicate second elements
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    # DEDUP: Skip duplicate third elements
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    
                    # Move both pointers after recording
                    left += 1
                    right -= 1
                    
                elif current_sum < target:
                    # Sum too small: need larger values
                    left += 1
                else:
                    # Sum too large: need smaller values
                    right -= 1
        
        return result


# ============================================================================
# Alternative: Using Set for Deduplication
# ============================================================================

class SolutionWithSet:
    """
    Alternative using a set to handle deduplication.
    
    Simpler logic but slightly higher space usage due to set overhead.
    Useful when the duplicate-skipping logic is error-prone.
    """
    
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        n: int = len(nums)
        result_set: set = set()
        
        for i in range(n - 2):
            if nums[i] > 0:
                break
            
            target: int = -nums[i]
            left, right = i + 1, n - 1
            
            while left < right:
                current_sum = nums[left] + nums[right]
                
                if current_sum == target:
                    # Use tuple for hashability
                    result_set.add((nums[i], nums[left], nums[right]))
                    left += 1
                    right -= 1
                elif current_sum < target:
                    left += 1
                else:
                    right -= 1
        
        return [list(triplet) for triplet in result_set]


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format:
        Line 1: Space-separated integers
    
    Output format:
        Each line: a triplet as space-separated integers
    
    Example:
        Input:  -1 0 1 2 -1 -4
        Output: 
        -1 -1 2
        -1 0 1
    """
    import sys
    
    line = sys.stdin.read().strip()
    nums = list(map(int, line.split()))
    
    solution = Solution()
    result = solution.threeSum(nums)
    
    for triplet in result:
        print(' '.join(map(str, triplet)))


if __name__ == "__main__":
    solve()

