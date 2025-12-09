# solutions/0209_minimum_size_subarray_sum.py
"""
================================================================================
LeetCode 209: Minimum Size Subarray Sum
================================================================================

Problem: Given an array of positive integers nums and a positive integer target,
         return the minimal length of a subarray whose sum is >= target.
         If there is no such subarray, return 0.

API Kernel: SubstringSlidingWindow
Pattern: sliding_window_cost_bounded
Family: substring_window (numeric variant)

--------------------------------------------------------------------------------
RELATIONSHIP TO BASE KERNEL (LeetCode 3)
--------------------------------------------------------------------------------

Base (LeetCode 3):
    - String input, track character frequencies/positions
    - Maximize window

This Variant (LeetCode 209):
    - Numeric array input
    - Track running sum (simpler than frequency map!)
    - Minimize window with sum >= target

Delta from Base:
    - State is a single integer (sum) instead of a map
    - Condition is numeric comparison (sum >= target)
    - Goal is to minimize, so we contract WHILE valid (like LeetCode 76)

Key Insight:
    Since all numbers are positive, adding elements always increases sum,
    and removing elements always decreases sum. This monotonicity enables
    the sliding window approach.

--------------------------------------------------------------------------------
COMPLEXITY ANALYSIS
--------------------------------------------------------------------------------

Time:  O(n) - Each element added and removed at most once
Space: O(1) - Only tracking sum and pointers

================================================================================
"""
from typing import List


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================

def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result using reference implementation.
    """
    lines = input_data.strip().split('\n')
    target = int(lines[0])
    nums = list(map(int, lines[1].split())) if len(lines) > 1 else []
    
    correct = _find_min_subarray(target, nums)
    
    try:
        actual_val = int(actual) if not isinstance(actual, int) else actual
        return actual_val == correct
    except (ValueError, TypeError):
        return False


def _find_min_subarray(target: int, nums: List[int]) -> int:
    """Reference implementation for verification."""
    n = len(nums)
    if n == 0:
        return 0
    
    window_sum = 0
    left = 0
    min_length = float('inf')
    
    for right, num in enumerate(nums):
        window_sum += num
        
        while window_sum >= target:
            min_length = min(min_length, right - left + 1)
            window_sum -= nums[left]
            left += 1
    
    return min_length if min_length != float('inf') else 0


JUDGE_FUNC = judge


# ============================================================================
# Solution - O(n) Sliding Window
# ============================================================================

class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        """
        Find the minimal length of a subarray whose sum is >= target.
        
        Args:
            target: Target sum to reach or exceed
            nums: Array of positive integers
            
        Returns:
            Minimum length of valid subarray, or 0 if none exists
        """
        n = len(nums)
        if n == 0:
            return 0
        
        # STATE: Running sum of current window
        window_sum: int = 0
        
        # WINDOW boundaries
        left: int = 0
        
        # ANSWER: Track minimum valid window length
        min_length: int = float('inf')
        
        for right, num in enumerate(nums):
            # EXPAND: Add element to window sum
            window_sum += num
            
            # CONTRACT: While sum satisfies target, try to minimize window
            while window_sum >= target:
                current_length = right - left + 1
                min_length = min(min_length, current_length)
                
                # Try to shrink
                window_sum -= nums[left]
                left += 1
        
        return min_length if min_length != float('inf') else 0


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format:
        Line 1: target (integer)
        Line 2: nums (space-separated integers)
    
    Output format:
        Single integer: minimum length of valid subarray, or 0
    """
    import sys
    
    lines = sys.stdin.read().strip().split('\n')
    target = int(lines[0])
    nums = list(map(int, lines[1].split())) if len(lines) > 1 else []
    
    solution = Solution()
    result = solution.minSubArrayLen(target, nums)
    
    print(result)


if __name__ == "__main__":
    solve()

