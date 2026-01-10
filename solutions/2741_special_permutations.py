"""
Problem: Special Permutations
Link: https://leetcode.com/problems/special-permutations/

Count permutations where adjacent elements satisfy: one divides the other.

Constraints:
- 2 <= nums.length <= 14
- 1 <= nums[i] <= 10^9
- All nums[i] are distinct

Topics: Array, Dynamic Programming, Bit Manipulation, Bitmask
"""
from typing import List
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "specialPerm",
        "complexity": "O(n^2 * 2^n) time, O(n * 2^n) space",
        "description": "Bitmask DP tracking used elements and last element",
    },
}


# JUDGE_FUNC for generated tests
def _reference(nums: List[int]) -> int:
    """Reference implementation."""
    MOD = 10**9 + 7
    n = len(nums)
    dp = [[0] * n for _ in range(1 << n)]
    for i in range(n):
        dp[1 << i][i] = 1
    for mask in range(1, 1 << n):
        for last in range(n):
            if not (mask & (1 << last)) or dp[mask][last] == 0:
                continue
            for j in range(n):
                if mask & (1 << j):
                    continue
                if nums[j] % nums[last] == 0 or nums[last] % nums[j] == 0:
                    dp[mask | (1 << j)][j] = (dp[mask | (1 << j)][j] + dp[mask][last]) % MOD
    return sum(dp[(1 << n) - 1]) % MOD


def judge(actual, expected, input_data: str) -> bool:
    nums = json.loads(input_data.strip())
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(nums)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Bitmask DP
# Time: O(n^2 * 2^n), Space: O(n * 2^n)
# ============================================================================
class Solution:
    # Key insight: n <= 14, so bitmask DP is feasible
    #
    # State: dp[mask][last] = count of special permutations
    #        using elements in mask, ending with nums[last]
    #
    # Transition: for each unused j where divisibility holds,
    #            dp[mask | (1<<j)][j] += dp[mask][last]
    #
    # Answer: sum of dp[full_mask][*]

    def specialPerm(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)

        # dp[mask][last] = count
        dp = [[0] * n for _ in range(1 << n)]

        # Base case: single element permutations
        for i in range(n):
            dp[1 << i][i] = 1

        # Fill DP
        for mask in range(1, 1 << n):
            for last in range(n):
                if not (mask & (1 << last)):
                    continue
                if dp[mask][last] == 0:
                    continue

                for j in range(n):
                    if mask & (1 << j):  # already used
                        continue
                    # Check divisibility
                    if nums[j] % nums[last] == 0 or nums[last] % nums[j] == 0:
                        new_mask = mask | (1 << j)
                        dp[new_mask][j] = (dp[new_mask][j] + dp[mask][last]) % MOD

        # Sum all full permutations
        full_mask = (1 << n) - 1
        return sum(dp[full_mask]) % MOD


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: nums (JSON array)

    Example:
        [2,3,6]
        -> 2
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.specialPerm(nums)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
