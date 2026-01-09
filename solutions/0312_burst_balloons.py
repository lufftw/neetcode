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
    "memoization": {
        "class": "SolutionMemoization",
        "method": "maxCoins",
        "complexity": "O(n³) time, O(n²) space",
        "description": "Top-down recursive with memoization",
    },
}


# ============================================================================
# Solution 1: Interval DP (Last Operation)
# Time: O(n³), Space: O(n²)
#   - Think which balloon to burst LAST (not first)
#   - Add virtual balloons with value 1 at boundaries
#   - Fill DP table by increasing interval length
# ============================================================================
class Solution:
    def maxCoins(self, nums: List[int]) -> int:
        """
        Find maximum coins from bursting all balloons.

        Core insight: Think about which balloon to burst LAST in each interval.
        If k is burst last in (i, j), then nums[i] and nums[j] are still
        boundaries, giving coins = nums[i] * nums[k] * nums[j].

        Invariant: max_coins[i][j] contains optimal solution for the exclusive
        interval (i, j) when all balloons between i and j are burst.

        Args:
            nums: Array of balloon values

        Returns:
            Maximum coins obtainable
        """
        # Add virtual balloons at boundaries (value 1)
        nums = [1] + nums + [1]
        balloon_count = len(nums)

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


# ============================================================================
# Solution 2: Top-Down Memoization
# Time: O(n³), Space: O(n²)
#   - Recursive approach with memoization
#   - Directly models subproblem: max coins for interval (i, j)
#   - Same complexity as bottom-up
# ============================================================================
class SolutionMemoization:
    def maxCoins(self, nums: List[int]) -> int:
        """
        Find maximum coins using top-down memoization.

        Core insight: Recursively solve "what's max coins for interval (i, j)?"
        by trying each balloon as the last to burst and taking maximum.

        Invariant: memo[(left, right)] stores optimal solution for the exclusive
        interval (left, right) once computed.

        Args:
            nums: Array of balloon values

        Returns:
            Maximum coins obtainable
        """
        # Add virtual balloons at boundaries
        nums = [1] + nums + [1]
        n = len(nums)
        memo = {}

        def dp(left: int, right: int) -> int:
            # Base case: no balloons between left and right
            if left + 1 == right:
                return 0

            if (left, right) in memo:
                return memo[(left, right)]

            # Try each balloon as the LAST to burst in interval (left, right)
            max_coins = 0
            for last in range(left + 1, right):
                coins = nums[left] * nums[last] * nums[right]
                total = dp(left, last) + dp(last, right) + coins
                max_coins = max(max_coins, total)

            memo[(left, right)] = max_coins
            return max_coins

        return dp(0, n - 1)


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
