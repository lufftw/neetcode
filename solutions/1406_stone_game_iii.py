"""
Problem: Stone Game III
Link: https://leetcode.com/problems/stone-game-iii/

Alice and Bob continue their games with piles of stones. There are several
stones arranged in a row, and each stone has an associated value which is
an integer given in the array stoneValue.

Alice and Bob take turns, with Alice starting first. On each player's turn,
that player can take 1, 2, or 3 stones from the first remaining stones in
the row.

The score of each player is the sum of the values of the stones taken. The
score of each player is 0 initially.

The objective of the game is to end with the highest score, and the winner
is the player with the highest score and there could be a tie.

Return "Alice" if Alice will win, "Bob" if Bob will win, or "Tie" if they
will end the game with the same score.

Example 1:
    Input: stoneValue = [1,2,3,7]
    Output: "Bob"

Example 2:
    Input: stoneValue = [1,2,3,-9]
    Output: "Alice"

Example 3:
    Input: stoneValue = [1,2,3,6]
    Output: "Tie"

Constraints:
- 1 <= stoneValue.length <= 5 * 10^4
- -1000 <= stoneValue[i] <= 1000

Topics: Array, Math, Dynamic Programming, Game Theory
"""
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "stoneGameIII",
        "complexity": "O(n) time, O(n) space",
        "description": "Linear DP tracking score difference",
    },
    "space_optimized": {
        "class": "SolutionSpaceOptimized",
        "method": "stoneGameIII",
        "complexity": "O(n) time, O(1) space",
        "description": "Rolling array with only 4 values",
    },
}


# ============================================================================
# Solution: Linear DP
# Time: O(n), Space: O(n)
#   - dp[i] = max score difference for current player starting from index i
#   - Each turn: take 1, 2, or 3 stones from front
#   - Subtract opponent's best outcome for minimax
# ============================================================================
class Solution:
    def stoneGameIII(self, stoneValue: list[int]) -> str:
        """
        Return winner: "Alice", "Bob", or "Tie".

        dp(start) = max score difference current player can achieve
                    starting from index start.

        At each turn, try taking 1, 2, or 3 stones:
        - Gain the sum of stones taken
        - Subtract opponent's best outcome from remaining position

        Alice wins if dp(0) > 0, Bob wins if dp(0) < 0, tie if dp(0) == 0.
        """
        n = len(stoneValue)

        from functools import lru_cache

        @lru_cache(maxsize=None)
        def dp(start: int) -> int:
            if start >= n:
                return 0

            best = float('-inf')
            stones_taken = 0

            for take in range(1, 4):
                if start + take > n:
                    break

                stones_taken += stoneValue[start + take - 1]

                # Score gained minus opponent's best outcome
                value = stones_taken - dp(start + take)
                best = max(best, value)

            return best

        diff = dp(0)

        if diff > 0:
            return "Alice"
        elif diff < 0:
            return "Bob"
        else:
            return "Tie"


# ============================================================================
# Solution: Space Optimized (Rolling Array)
# Time: O(n), Space: O(1)
#   - Only need dp[i+1], dp[i+2], dp[i+3] to compute dp[i]
#   - Use array of size 4 with modular indexing
# ============================================================================
class SolutionSpaceOptimized:
    def stoneGameIII(self, stoneValue: list[int]) -> str:
        """
        Bottom-up DP with O(1) space using rolling array.

        Since we only need 3 future values, use dp[i % 4].
        """
        n = len(stoneValue)
        dp = [0] * 4  # Rolling array

        for i in range(n - 1, -1, -1):
            best = float('-inf')
            stones = 0

            for take in range(1, 4):
                if i + take > n:
                    break
                stones += stoneValue[i + take - 1]
                value = stones - dp[(i + take) % 4]
                best = max(best, value)

            dp[i % 4] = best

        diff = dp[0]

        if diff > 0:
            return "Alice"
        elif diff < 0:
            return "Bob"
        else:
            return "Tie"


def solve():
    """
    Input format:
    Line 1: stoneValue (JSON array of integers)
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')

    stoneValue = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.stoneGameIII(stoneValue)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
