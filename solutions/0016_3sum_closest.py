# solutions/0016_3sum_closest.py
"""
================================================================================
LeetCode 16: 3Sum Closest
================================================================================

Problem: Given an integer array nums and an integer target, find three integers
         in nums such that the sum is closest to target. Return the sum.
         You may assume that each input would have exactly one solution.

API Kernel: TwoPointersTraversal
Pattern: opposite_pointers_closest
Family: multi_sum_problems

--------------------------------------------------------------------------------
TWO POINTERS PATTERN: OPPOSITE POINTERS (CLOSEST VARIANT)
--------------------------------------------------------------------------------

This problem is a variant of 3Sum where instead of finding exact matches,
we track the closest sum seen so far.

DELTA from 3Sum:
- No deduplication needed (we return a single value, not all triplets)
- Track |current_sum - target| instead of checking equality
- Update closest_sum when a closer sum is found

INVARIANT: closest_sum is the sum nearest to target among all triplets
           examined so far.

Key Insight:
    The two-pointer technique still works because:
    - If current_sum < target, we need a larger sum → move left pointer right
    - If current_sum > target, we need a smaller sum → move right pointer left
    - If current_sum == target, we found the optimal → return immediately

--------------------------------------------------------------------------------
COMPLEXITY ANALYSIS
--------------------------------------------------------------------------------

Time:  O(n²) - O(n log n) sorting + O(n²) for nested iteration
Space: O(1) extra (excluding sorting space)

================================================================================
"""
from typing import List
from _runner import get_solver


# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionTwoPointers",
        "method": "threeSumClosest",
        "complexity": "O(n²) time, O(1) extra space",
        "description": "Sort + two pointers tracking closest sum",
    },
    "two_pointers": {
        "class": "SolutionTwoPointers",
        "method": "threeSumClosest",
        "complexity": "O(n²) time, O(1) extra space",
        "description": "Sort + two pointers tracking closest sum",
    },
    "optimized": {
        "class": "SolutionTwoPointersOptimized",
        "method": "threeSumClosest",
        "complexity": "O(n²) time, O(1) extra space",
        "description": "Two pointers with additional pruning strategies",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================

def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output is the closest sum to target.
    
    Args:
        actual: Program output (integer as string or int)
        expected: Expected output (None if from generator)
        input_data: Raw input string (Line 1: nums, Line 2: target)
    
    Returns:
        bool: True if correct closest sum
    """
    lines = input_data.strip().split('\n')
    nums = list(map(int, lines[0].split())) if lines[0] else []
    target = int(lines[1]) if len(lines) > 1 else 0
    
    # Compute correct answer
    correct = _brute_force_closest(nums, target)
    
    try:
        actual_val = int(actual) if not isinstance(actual, int) else actual
        return actual_val == correct
    except (ValueError, TypeError):
        return False


def _brute_force_closest(nums: List[int], target: int) -> int:
    """O(n³) brute force solution for verification."""
    n = len(nums)
    if n < 3:
        return sum(nums) if n == 3 else 0
    
    closest_sum = nums[0] + nums[1] + nums[2]
    min_diff = abs(closest_sum - target)
    
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                current_sum = nums[i] + nums[j] + nums[k]
                diff = abs(current_sum - target)
                if diff < min_diff:
                    min_diff = diff
                    closest_sum = current_sum
    
    return closest_sum


JUDGE_FUNC = judge


# ============================================
# Solution 1: Sort + Two Pointers
# Time: O(n²), Space: O(1) extra
#   - O(n log n) sorting + O(n²) nested iteration
#   - Tracks closest sum seen so far
#   - No deduplication needed (single value result)
# ============================================
class SolutionTwoPointers:
    """
    Optimal solution tracking the closest sum using two pointers.
    
    Similar structure to 3Sum, but simplified by tracking a single
    closest value instead of collecting all exact matches.
    """
    
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        """
        Find the sum of three integers closest to target.
        
        Args:
            nums: List of integers
            target: Target sum to approach
            
        Returns:
            Sum of the triplet closest to target
        """
        n: int = len(nums)
        
        # SORT: Enable two-pointer search
        nums.sort()
        
        # Initialize with first possible triplet sum
        closest_sum: int = nums[0] + nums[1] + nums[2]
        
        # OUTER LOOP: Fix the first element
        for i in range(n - 2):
            # SKIP DUPLICATES: Optional optimization
            # Unlike 3Sum, skipping duplicates here is purely for efficiency
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            
            # TWO POINTERS: Search for closest pair sum
            left: int = i + 1
            right: int = n - 1
            
            while left < right:
                current_sum: int = nums[i] + nums[left] + nums[right]
                
                # EXACT MATCH: Cannot get closer than this
                if current_sum == target:
                    return target
                
                # UPDATE CLOSEST: Check if current sum is closer
                if abs(current_sum - target) < abs(closest_sum - target):
                    closest_sum = current_sum
                
                # MOVE POINTERS: Adjust based on sum comparison
                if current_sum < target:
                    # Sum too small: need larger values
                    left += 1
                else:
                    # Sum too large: need smaller values
                    right -= 1
        
        return closest_sum


# ============================================
# Solution 2: Two Pointers with Additional Pruning
# Time: O(n²), Space: O(1) extra
#   - Same time complexity with bounds checking
#   - May skip iterations that cannot improve closest sum
#   - Better constant factors in practice
# ============================================
class SolutionTwoPointersOptimized:
    """
    Optimized version with additional pruning strategies.
    
    Includes bounds checking to skip iterations that cannot improve
    the current closest sum.
    """
    
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        nums.sort()
        n: int = len(nums)
        closest_sum: int = nums[0] + nums[1] + nums[2]
        
        for i in range(n - 2):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            
            # PRUNING: Check bounds for this fixed element
            # Minimum possible sum with nums[i]
            min_sum: int = nums[i] + nums[i + 1] + nums[i + 2]
            if min_sum > target:
                # All remaining sums will be >= min_sum
                if abs(min_sum - target) < abs(closest_sum - target):
                    closest_sum = min_sum
                break
            
            # Maximum possible sum with nums[i]
            max_sum: int = nums[i] + nums[n - 2] + nums[n - 1]
            if max_sum < target:
                # All sums with this i will be <= max_sum
                if abs(max_sum - target) < abs(closest_sum - target):
                    closest_sum = max_sum
                continue
            
            # Two-pointer search
            left, right = i + 1, n - 1
            
            while left < right:
                current_sum = nums[i] + nums[left] + nums[right]
                
                if current_sum == target:
                    return target
                
                if abs(current_sum - target) < abs(closest_sum - target):
                    closest_sum = current_sum
                
                if current_sum < target:
                    left += 1
                else:
                    right -= 1
        
        return closest_sum


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format:
        Line 1: Space-separated integers (nums)
        Line 2: Target integer
    
    Output format:
        Single integer: closest sum
    
    Example:
        Input:
        -1 2 1 -4
        1
        Output: 2
    """
    import sys
    
    lines = sys.stdin.read().strip().split('\n')
    nums = list(map(int, lines[0].split()))
    target = int(lines[1])
    
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.threeSumClosest(nums, target)
    
    print(result)


if __name__ == "__main__":
    solve()
