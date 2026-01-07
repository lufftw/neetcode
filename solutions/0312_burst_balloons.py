"""
312. Burst Balloons
https://leetcode.com/problems/burst-balloons/

Pattern: Interval DP - Last Operation
API Kernel: IntervalDP

Key insight: Think about which balloon to burst LAST in each interval.
If k is burst last in (i, j), then nums[i] and nums[j] are still boundaries.
"""
from typing import List
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "maxCoins",
        "complexity": "O(n³) time, O(n²) space",
        "description": "Interval DP with 'last to burst' approach",
    },
}


class Solution:
    def maxCoins(self, nums: List[int]) -> int:
        """
        Maximum coins from bursting all balloons.

        dp[i][j] = max coins from bursting all balloons in (i, j) exclusive

        For each k in (i, j):
        - If k is burst LAST, boundaries are nums[i] and nums[j]
        - coins = nums[i] * nums[k] * nums[j]
        - Total = dp[i][k] + dp[k][j] + coins
        """
        # Add virtual balloons at boundaries
        nums = [1] + nums + [1]
        n = len(nums)

        # dp[i][j] = max coins for interval (i, j) exclusive
        dp = [[0] * n for _ in range(n)]

        # Fill by interval length (from small to large)
        for length in range(2, n):  # length = j - i
            for i in range(n - length):
                j = i + length

                # Try each balloon k as the LAST to burst
                for k in range(i + 1, j):
                    coins = nums[i] * nums[k] * nums[j]
                    dp[i][j] = max(dp[i][j], dp[i][k] + dp[k][j] + coins)

        return dp[0][n - 1]


def solve():
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')
    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.maxCoins(nums)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
