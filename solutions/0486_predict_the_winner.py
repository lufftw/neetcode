"""
Problem: Predict the Winner
Link: https://leetcode.com/problems/predict-the-winner/

You are given an integer array nums. Two players are playing a game with this
array: player 1 and player 2.

Player 1 and player 2 take turns, with player 1 starting first. Both players
start the game with a score of 0. At each turn, the player takes one of the
numbers from either end of the array (i.e., nums[0] or nums[nums.length - 1])
which reduces the size of the array by 1. The player adds the chosen number
to their score.

Return true if Player 1 can win the game. If the scores of both players are
equal, then player 1 is still the winner, and you should also return true.

Example 1:
    Input: nums = [1,5,2]
    Output: false
    Explanation: Player 1 can choose 1 or 2. If he chooses 2, nums = [1,5],
                 Player 2 chooses 5, and Player 1 gets 1.
                 Player 1 = 2 + 1 = 3, Player 2 = 5. Player 2 wins.

Example 2:
    Input: nums = [1,5,233,7]
    Output: true
    Explanation: Player 1 can choose 1 first, then Player 2 gets choice of 5 or 7,
                 Player 1 gets 233, and so on.

Constraints:
- 1 <= nums.length <= 20
- 0 <= nums[i] <= 10^7

Topics: Array, Math, Dynamic Programming, Recursion, Game Theory
"""
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "predictTheWinner",
        "complexity": "O(n²) time, O(n²) space",
        "description": "Interval DP tracking score difference",
    },
    "space_optimized": {
        "class": "SolutionSpaceOptimized",
        "method": "predictTheWinner",
        "complexity": "O(n²) time, O(n) space",
        "description": "Bottom-up DP with linear space",
    },
}


# ============================================================================
# Solution: Interval DP
# Time: O(n²), Space: O(n²)
#   - dp[i][j] = max score difference for current player on nums[i..j]
#   - Player 1 wins if dp[0][n-1] >= 0 (tie counts as win)
# ============================================================================
class Solution:
    def predictTheWinner(self, nums: list[int]) -> bool:
        """
        Return True if Player 1 can win or tie.

        dp(left, right) = max score difference current player can achieve
                          from nums[left..right].

        At each state, current player tries both ends:
        - Take left: gain nums[left], opponent gets dp(left+1, right)
        - Take right: gain nums[right], opponent gets dp(left, right-1)

        Since opponent's gain is our loss, we subtract their outcome.

        Player 1 wins if dp(0, n-1) >= 0 (tie counts as P1 win).
        """
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def dp(left: int, right: int) -> int:
            if left > right:
                return 0

            take_left = nums[left] - dp(left + 1, right)
            take_right = nums[right] - dp(left, right - 1)

            return max(take_left, take_right)

        return dp(0, len(nums) - 1) >= 0


# ============================================================================
# Solution: Bottom-Up with Space Optimization
# Time: O(n²), Space: O(n)
#   - Process intervals by increasing length
#   - Only need one row of previous values
# ============================================================================
class SolutionSpaceOptimized:
    def predictTheWinner(self, nums: list[int]) -> bool:
        """
        Bottom-up DP with O(n) space.

        dp[j] represents score difference for interval ending at j.
        Process by interval length, reusing the same array.
        """
        n = len(nums)
        dp = nums[:]  # Base case: single element intervals

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                # dp[j] currently holds value for interval (i+1, j)
                take_left = nums[i] - dp[j]
                # dp[j-1] holds value for interval (i, j-1)
                take_right = nums[j] - dp[j - 1]
                dp[j] = max(take_left, take_right)

        return dp[n - 1] >= 0


def solve():
    """
    Input format:
    Line 1: nums (JSON array of integers)
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')

    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.predictTheWinner(nums)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
