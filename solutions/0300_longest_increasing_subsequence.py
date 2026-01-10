# solutions/0300_longest_increasing_subsequence.py
"""
Problem: Longest Increasing Subsequence
https://leetcode.com/problems/longest-increasing-subsequence/

Given an integer array nums, return the length of the longest strictly
increasing subsequence.

Constraints:
- 1 <= nums.length <= 2500
- -10^4 <= nums[i] <= 10^4
"""
from typing import List
import bisect
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionBinarySearch",
        "method": "lengthOfLIS",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Binary search with patience sorting tails array",
    },
    "dp": {
        "class": "SolutionDP",
        "method": "lengthOfLIS",
        "complexity": "O(n^2) time, O(n) space",
        "description": "Dynamic programming with quadratic scan",
    },
}


class SolutionBinarySearch:
    """
    Binary search approach using patience sorting insight.

    We maintain a "tails" array where tails[i] is the smallest ending
    element of all increasing subsequences of length i+1. This array
    is always sorted, enabling binary search for updates.

    For each element, we either extend the longest subsequence (append)
    or replace an existing tail (binary search). This is equivalent to
    patience sorting from solitaire - each pile's top card is tails[i].
    """

    def lengthOfLIS(self, nums: List[int]) -> int:
        # tails[i] = smallest ending element of LIS of length i+1
        # This array is always sorted, enabling O(log n) updates
        tails = []

        for num in nums:
            # Binary search for leftmost position where tails[pos] >= num
            # This finds where to place num to maintain sorted property
            pos = bisect.bisect_left(tails, num)

            if pos == len(tails):
                # num is larger than all tails - extend longest LIS
                tails.append(num)
            else:
                # Replace tails[pos] with smaller ending value
                # This doesn't change LIS length but enables longer future LIS
                tails[pos] = num

        # Length of tails array = length of LIS
        return len(tails)


class SolutionDP:
    """
    Classic dynamic programming with O(n^2) complexity.

    dp[i] represents the length of the longest increasing subsequence
    ending at index i. For each position, we scan all previous positions
    to find valid extensions.

    This approach is more intuitive but less efficient than binary search.
    Each element must check all predecessors, giving quadratic time.
    """

    def lengthOfLIS(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0

        # dp[i] = length of LIS ending at index i
        # Base case: each element forms LIS of length 1
        dp = [1] * n

        for i in range(1, n):
            # Check all previous elements for valid extensions
            for j in range(i):
                # If nums[j] < nums[i], we can extend LIS ending at j
                if nums[j] < nums[i]:
                    dp[i] = max(dp[i], dp[j] + 1)

        # Answer is maximum LIS length ending at any position
        return max(dp)


def judge(actual, expected, input_data: str) -> bool:
    """
    Validate LIS length using binary search reference implementation.
    """
    import json

    nums = json.loads(input_data.strip())

    # Compute expected LIS length using binary search
    tails = []
    for num in nums:
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num

    expected_len = len(tails)
    return actual == expected_len


JUDGE_FUNC = judge


def solve():
    import sys
    import json

    lines = sys.stdin.read().strip().split("\n")

    # Parse input: array
    nums = json.loads(lines[0])

    # Get solver and find LIS length
    solver = get_solver(SOLUTIONS)
    result = solver.lengthOfLIS(nums)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
