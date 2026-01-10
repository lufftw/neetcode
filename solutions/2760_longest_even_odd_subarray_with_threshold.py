"""
Problem: Longest Even Odd Subarray With Threshold
Link: https://leetcode.com/problems/longest-even-odd-subarray-with-threshold/

You are given a 0-indexed integer array nums and an integer threshold.

Find the length of the longest subarray of nums starting at index l and ending
at index r (0 <= l <= r < nums.length) that satisfies the following conditions:

1. nums[l] % 2 == 0 (starts with even number)
2. For all i in [l, r], nums[i] <= threshold
3. For all i in [l, r-1], nums[i] % 2 != nums[i+1] % 2 (alternating parity)

Return the length of the longest such subarray.

Example 1:
    Input: nums = [3,2,5,4], threshold = 5
    Output: 3
    Explanation: Subarray [2,5,4] starts with even, all <= 5, alternating parity.

Example 2:
    Input: nums = [1,2], threshold = 2
    Output: 1
    Explanation: Subarray [2] is the longest valid subarray.

Example 3:
    Input: nums = [2,3,4,5], threshold = 4
    Output: 3
    Explanation: Subarray [2,3,4] satisfies all conditions.

Constraints:
- 1 <= nums.length <= 100
- 1 <= nums[i] <= 100
- 1 <= threshold <= 100

Topics: Array, Sliding Window
"""
from typing import List
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "longestAlternatingSubarray",
        "complexity": "O(n) time, O(1) space",
        "description": "Single pass with state tracking",
    },
}


# ============================================================================
# Solution: Single Pass with State Tracking
# Time: O(n), Space: O(1)
#
# Key insight: Scan through array, tracking current valid subarray length.
# Reset when:
# - Element exceeds threshold
# - Found even number (potential new start)
# - Parity doesn't alternate
#
# When current element breaks the chain but is even and <= threshold,
# start a new subarray from this position.
# ============================================================================
class Solution:
    def longestAlternatingSubarray(self, nums: List[int], threshold: int) -> int:
        """
        Find longest subarray starting with even, alternating parity, all <= threshold.

        We iterate through the array maintaining:
        - current_len: length of current valid subarray
        - last_parity: parity (0/1) of last element in current subarray

        At each position, we either:
        1. Extend current subarray if conditions met
        2. Start new subarray if current element is even and <= threshold
        3. Reset if current element > threshold

        Args:
            nums: Input array
            threshold: Maximum allowed value

        Returns:
            Length of longest valid subarray
        """
        n = len(nums)
        result = 0
        i = 0

        while i < n:
            # Look for a valid starting point (even and <= threshold)
            if nums[i] % 2 == 0 and nums[i] <= threshold:
                # Found valid start, extend as far as possible
                start = i
                i += 1

                while (i < n and
                       nums[i] <= threshold and
                       nums[i] % 2 != nums[i - 1] % 2):
                    i += 1

                # Update result with this subarray length
                result = max(result, i - start)
            else:
                # Not a valid starting point, move on
                i += 1

        return result


def solve():
    """
    Input format:
    Line 1: nums (JSON array)
    Line 2: threshold (integer)
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')

    nums = json.loads(lines[0])
    threshold = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.longestAlternatingSubarray(nums, threshold)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
