"""
Problem: Split Array With Same Average
Link: https://leetcode.com/problems/split-array-with-same-average/

Split array into two non-empty parts with same average.
Return true if possible.

Constraints:
- 1 <= nums.length <= 30
- 0 <= nums[i] <= 10^4

Topics: Array, Math, DP, Bitmask, Meet in the Middle
"""
from typing import List
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "splitArraySameAverage",
        "complexity": "O(n * S * n/2) time, O(n * S) space",
        "description": "DP checking if subset of size k can sum to S*k/n",
    },
}


# JUDGE_FUNC for generated tests
def _reference(nums: List[int]) -> bool:
    """Brute force for small inputs."""
    n = len(nums)
    if n == 1:
        return False

    total = sum(nums)

    # Try all non-empty proper subsets
    for mask in range(1, (1 << n) - 1):
        subset_sum = 0
        subset_size = 0
        for i in range(n):
            if mask & (1 << i):
                subset_sum += nums[i]
                subset_size += 1

        # Check if average of subset == average of total
        # subset_sum / subset_size == total / n
        # subset_sum * n == total * subset_size
        if subset_sum * n == total * subset_size:
            return True

    return False


def judge(actual, expected, input_data: str) -> bool:
    lines = input_data.strip().split('\n')
    nums = json.loads(lines[0])
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    if len(nums) <= 20:
        return actual == _reference(nums)
    return isinstance(actual, bool)


JUDGE_FUNC = judge


# ============================================================================
# Solution: DP on Subset Sum with Size
# Time: O(n * S * n/2), Space: O(n * S)
# ============================================================================
class Solution:
    # Key insight:
    #   If avg(A) == avg(B) == avg(nums) = S/n, then for subset A of size k:
    #   sum(A)/k = S/n → sum(A) = S*k/n
    #
    #   This requires S*k % n == 0 for valid k.
    #   Check for each valid k from 1 to n//2 if such subset exists.
    #
    # DP: dp[k][s] = True if we can select k elements summing to s
    # Optimization: only track sizes, use set for sums at each size

    def splitArraySameAverage(self, nums: List[int]) -> bool:
        n = len(nums)
        if n == 1:
            return False

        total = sum(nums)

        # Early termination: check if any valid k exists
        possible = False
        for k in range(1, n // 2 + 1):
            if (total * k) % n == 0:
                possible = True
                break
        if not possible:
            return False

        # DP: dp[k] = set of achievable sums with exactly k elements
        dp = [set() for _ in range(n // 2 + 1)]
        dp[0].add(0)

        for num in nums:
            # Iterate in reverse to avoid using same element twice
            for k in range(min(len(dp) - 1, n // 2), 0, -1):
                for s in dp[k - 1]:
                    dp[k].add(s + num)

        # Check if any valid subset exists
        for k in range(1, n // 2 + 1):
            if (total * k) % n == 0:
                target = (total * k) // n
                if target in dp[k]:
                    return True

        return False


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: nums (JSON array)

    Example:
        [1,2,3,4,5,6,7,8]
        -> true
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.splitArraySameAverage(nums)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
