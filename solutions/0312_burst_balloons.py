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


# ============================================================================
# Solution 1: Interval DP (Last Operation)
# Time: O(n³), Space: O(n²)
#   - Key: think which balloon to burst LAST (not first)
#   - State: max_coins[i][j] = max coins for bursting all in (i, j) exclusive
#   - Base case: max_coins[i][i+1] = 0 (no balloons between adjacent)
#   - Transition: max_coins[i][j] = max over k of: left + right + nums[i]*nums[k]*nums[j]
# ============================================================================
class Solution:
    def maxCoins(self, nums: List[int]) -> int:
        # Add virtual balloons at boundaries (value 1)
        nums = [1] + nums + [1]
        balloon_count = len(nums)

        # max_coins[i][j] = max coins for bursting all in interval (i, j) exclusive
        max_coins: list[list[int]] = [
            [0] * balloon_count for _ in range(balloon_count)
        ]

        # Fill by interval length (small to large)
        for interval_len in range(2, balloon_count):
            for start in range(balloon_count - interval_len):
                end = start + interval_len

                # Try each balloon as the LAST to burst in this interval
                for last_burst in range(start + 1, end):
                    coins = nums[start] * nums[last_burst] * nums[end]
                    total = max_coins[start][last_burst] + max_coins[last_burst][end] + coins
                    max_coins[start][end] = max(max_coins[start][end], total)

        return max_coins[0][balloon_count - 1]


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
