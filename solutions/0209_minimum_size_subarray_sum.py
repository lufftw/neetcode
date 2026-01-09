# solutions/0209_minimum_size_subarray_sum.py
"""
Problem: Minimum Size Subarray Sum
Link: https://leetcode.com/problems/minimum-size-subarray-sum/

Given an array of positive integers nums and a positive integer target, return the minimal length of a subarray whose sum is greater than or equal to target. If there is no such subarray, return 0 instead.

Example 1:
    Input: target = 7, nums = [2,3,1,2,4,3]
    Output: 2
    Explanation: The subarray [4,3] has the minimal length under the problem constraint.

Example 2:
    Input: target = 4, nums = [1,4,4]
    Output: 1

Example 3:
    Input: target = 11, nums = [1,1,1,1,1,1,1,1]
    Output: 0

Constraints:
- 1 <= target <= 10^9
- 1 <= nums.length <= 10^5
- 1 <= nums[i] <= 10^4

Topics: Array, Binary Search, Sliding Window, Prefix Sum

Follow-up: If you have figured out the O(n) solution, try coding another solution of which the time complexity is O(n log(n)).
"""
from typing import List
from _runner import get_solver


# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# Polymorphic pattern: each entry specifies class + method
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "minSubArrayLen",
        "complexity": "O(n) time, O(1) space",
        "description": "Sliding window approach",
    },
    "sliding_window": {
        "class": "Solution",
        "method": "minSubArrayLen",
        "complexity": "O(n) time, O(1) space",
        "description": "Optimal sliding window, each element visited twice",
    },
    "binary_search": {
        "class": "SolutionBinarySearch",
        "method": "minSubArrayLen",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Prefix sum + binary search (follow-up solution)",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================

def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result using reference implementation.
    """
    import json
    lines = input_data.strip().split('\n')
    target = int(lines[0])
    nums = json.loads(lines[1]) if len(lines) > 1 else []
    
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
# Solution 1: Sliding Window
# Time: O(n), Space: O(1)
#   - Each element added and removed at most once
#   - Only tracking sum and pointers
# ============================================================================

class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        """
        Find the minimal length of a subarray whose sum is >= target.

        Core insight: Works because all elements are positive — adding always
        increases sum, removing always decreases. This monotonicity enables
        sliding window. (With negatives, need prefix sum + monotonic deque.)

        Invariant: window_sum = sum of nums[left..right].

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
# Solution 2: Binary Search with Prefix Sum
# Time: O(n log n), Space: O(n)
#   - Build prefix sum array
#   - For each starting position, binary search for ending position
#   - Follow-up solution demonstrating O(n log n) approach
# ============================================================================

class SolutionBinarySearch:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        """
        Find minimal subarray length using prefix sum + binary search.

        Core insight: For positive numbers, prefix sum is monotonically increasing.
        For each starting index i, binary search for smallest j where
        prefix[j] - prefix[i] >= target, i.e., prefix[j] >= prefix[i] + target.

        This is the O(n log n) follow-up solution.

        Args:
            target: Target sum to reach or exceed
            nums: Array of positive integers

        Returns:
            Minimum length of valid subarray, or 0 if none exists
        """
        import bisect

        n = len(nums)
        if n == 0:
            return 0

        # Build prefix sum array: prefix[i] = sum(nums[0:i])
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + nums[i]

        min_length = float('inf')

        # For each starting position i, find smallest j where prefix[j] >= prefix[i] + target
        for i in range(n):
            # Need prefix[j] >= prefix[i] + target
            required = prefix[i] + target

            # Binary search for leftmost j where prefix[j] >= required
            j = bisect.bisect_left(prefix, required)

            if j <= n:
                min_length = min(min_length, j - i)

        return min_length if min_length != float('inf') else 0


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    import json
    """
    Input format:
        Line 1: target (integer)
        Line 2: nums (space-separated integers)
    
    Output format:
        Single integer: minimum length of valid subarray, or 0
    """
    import sys
    import json
    
    lines = sys.stdin.read().strip().split('\n')
    target = int(lines[0])
    nums = json.loads(lines[1]) if len(lines) > 1 else []
    
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.minSubArrayLen(target, nums)
    
    print(result)


if __name__ == "__main__":
    solve()

