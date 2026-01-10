"""
Problem: Maximum Subarray
Link: https://leetcode.com/problems/maximum-subarray/

Given an integer array nums, find the subarray with the largest sum,
and return its sum.

Example 1:
    Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
    Output: 6
    Explanation: The subarray [4,-1,2,1] has the largest sum 6.

Example 2:
    Input: nums = [1]
    Output: 1

Example 3:
    Input: nums = [5,4,-1,7,8]
    Output: 23

Constraints:
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4

Follow-up: Try coding a solution using divide and conquer approach.

Topics: Array, Divide And Conquer, Dynamic Programming
"""
import json
from typing import List
from _runner import get_solver


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionKadane",
        "method": "maxSubArray",
        "complexity": "O(n) time, O(1) space",
        "description": "Kadane's algorithm - optimal solution",
    },
    "kadane": {
        "class": "SolutionKadane",
        "method": "maxSubArray",
        "complexity": "O(n) time, O(1) space",
        "description": "Kadane's algorithm - optimal solution",
    },
    "dp": {
        "class": "SolutionDP",
        "method": "maxSubArray",
        "complexity": "O(n) time, O(n) space",
        "description": "Dynamic programming with explicit array",
    },
    "divide_conquer": {
        "class": "SolutionDivideConquer",
        "method": "maxSubArray",
        "complexity": "O(n log n) time, O(log n) space",
        "description": "Divide and conquer approach",
    },
}


# ============================================================================
# Solution 1: Kadane's Algorithm
# Time: O(n), Space: O(1)
#   - At each position, decide: extend current subarray or start new one
#   - Track maximum sum seen so far
#   - Optimal for this problem
# ============================================================================
class SolutionKadane:
    """
    Kadane's algorithm - the optimal O(n) solution.

    Key insight: At each position i, we make a simple decision:
    - Either extend the subarray ending at i-1 by including nums[i]
    - Or start a fresh subarray from i

    We choose whichever gives a larger sum:
        current_sum = max(nums[i], current_sum + nums[i])

    The global maximum is the largest current_sum we've seen.
    """

    def maxSubArray(self, nums: List[int]) -> int:
        # current_sum = max sum of subarray ending at current position
        # max_sum = max sum of any subarray seen so far
        current_sum = nums[0]
        max_sum = nums[0]

        for i in range(1, len(nums)):
            # Decision: extend current subarray or start fresh
            # If current_sum is negative, starting fresh is better
            current_sum = max(nums[i], current_sum + nums[i])

            # Update global maximum
            max_sum = max(max_sum, current_sum)

        return max_sum


# ============================================================================
# Solution 2: Dynamic Programming (Explicit)
# Time: O(n), Space: O(n)
#   - dp[i] = maximum sum of subarray ending at index i
#   - Same logic as Kadane but uses explicit array
#   - Easier to understand state transitions
# ============================================================================
class SolutionDP:
    """
    Dynamic programming with explicit dp array.

    State: dp[i] = maximum sum of subarray ending at index i
    Transition: dp[i] = max(nums[i], dp[i-1] + nums[i])
    Answer: max(dp)

    This is the same as Kadane's but stores all intermediate states,
    making it easier to understand but using O(n) space.
    """

    def maxSubArray(self, nums: List[int]) -> int:
        n = len(nums)

        # dp[i] = max sum of subarray ending at i
        dp = [0] * n
        dp[0] = nums[0]

        for i in range(1, n):
            # Either extend previous subarray or start new one
            dp[i] = max(nums[i], dp[i - 1] + nums[i])

        return max(dp)


# ============================================================================
# Solution 3: Divide and Conquer
# Time: O(n log n), Space: O(log n) for recursion stack
#   - Divide array into left and right halves
#   - Maximum subarray is either:
#     1. Entirely in left half
#     2. Entirely in right half
#     3. Crossing the midpoint
# ============================================================================
class SolutionDivideConquer:
    """
    Divide and conquer approach - as requested in the follow-up.

    The maximum subarray must be one of:
    1. Entirely in the left half
    2. Entirely in the right half
    3. Crossing the midpoint (spans both halves)

    We recursively solve left and right, then compute the crossing sum.
    The crossing sum is found by expanding from the midpoint in both directions.
    """

    def maxSubArray(self, nums: List[int]) -> int:
        def max_crossing_sum(left: int, mid: int, right: int) -> int:
            """Find max sum that crosses the midpoint."""
            # Expand left from mid
            left_sum = float('-inf')
            current = 0
            for i in range(mid, left - 1, -1):
                current += nums[i]
                left_sum = max(left_sum, current)

            # Expand right from mid+1
            right_sum = float('-inf')
            current = 0
            for i in range(mid + 1, right + 1):
                current += nums[i]
                right_sum = max(right_sum, current)

            return left_sum + right_sum

        def divide_conquer(left: int, right: int) -> int:
            """Find max subarray sum in nums[left:right+1]."""
            # Base case: single element
            if left == right:
                return nums[left]

            mid = (left + right) // 2

            # Maximum of three cases
            left_max = divide_conquer(left, mid)
            right_max = divide_conquer(mid + 1, right)
            cross_max = max_crossing_sum(left, mid, right)

            return max(left_max, right_max, cross_max)

        return divide_conquer(0, len(nums) - 1)


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: nums as JSON array

    Example:
        [-2,1,-3,4,-1,2,1,-5,4]
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')

    # Parse JSON array
    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.maxSubArray(nums)

    print(result)


if __name__ == "__main__":
    solve()
