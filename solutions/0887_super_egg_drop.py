"""
Problem: Super Egg Drop
Link: https://leetcode.com/problems/super-egg-drop/

Find minimum moves to determine critical floor with k eggs and n floors.

Constraints:
- 1 <= k <= 100
- 1 <= n <= 10^4

Topics: Math, Binary Search, Dynamic Programming
"""
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "superEggDrop",
        "complexity": "O(k * log n) time, O(k) space",
        "description": "DP reformulation: floors checkable with m moves and k eggs",
    },
}


# JUDGE_FUNC for generated tests
def _reference(k: int, n: int) -> int:
    """Reference implementation."""
    dp = [0] * (k + 1)
    m = 0
    while dp[k] < n:
        m += 1
        new_dp = [0] * (k + 1)
        for j in range(1, k + 1):
            new_dp[j] = dp[j - 1] + dp[j] + 1
        dp = new_dp
    return m


def judge(actual, expected, input_data: str) -> bool:
    lines = input_data.strip().split('\n')
    k = int(lines[0])
    n = int(lines[1])
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(k, n)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Reformulated DP
# Time: O(k * log n), Space: O(k)
# ============================================================================
class Solution:
    # Classic formulation: dp[k][n] = min moves with k eggs and n floors
    # This leads to O(k * n^2) or O(k * n * log n) with binary search.
    #
    # Optimal reformulation: dp[m][k] = max floors checkable with m moves, k eggs
    #
    # Recurrence:
    #   When we drop at floor x:
    #   - Egg breaks: check dp[m-1][k-1] floors below
    #   - Egg survives: check dp[m-1][k] floors above
    #   Total checkable = dp[m-1][k-1] + 1 + dp[m-1][k]
    #
    # We want minimum m such that dp[m][k] >= n.
    #
    # Since dp is monotonically increasing in m, we can iterate m from 1.

    def superEggDrop(self, k: int, n: int) -> int:
        # dp[j] = max floors checkable with current m moves and j eggs
        dp = [0] * (k + 1)

        m = 0  # Number of moves
        while dp[k] < n:
            m += 1
            # Update from right to left to use old values
            new_dp = [0] * (k + 1)
            for j in range(1, k + 1):
                # dp[m][j] = dp[m-1][j-1] + dp[m-1][j] + 1
                new_dp[j] = dp[j - 1] + dp[j] + 1
            dp = new_dp

        return m


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: k (number of eggs)
        Line 2: n (number of floors)

    Example:
        1
        2
        -> 2
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    k = int(lines[0])
    n = int(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.superEggDrop(k, n)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
