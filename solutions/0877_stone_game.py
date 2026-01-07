"""
Problem: Stone Game
Link: https://leetcode.com/problems/stone-game/

Alice and Bob play a game with piles of stones. There are an even number of piles
arranged in a row, and each pile has a positive integer number of stones piles[i].

The objective of the game is to end with the most stones. The total number of
stones across all the piles is odd, so there are no ties.

Alice and Bob take turns, with Alice starting first. Each turn, a player takes
the entire pile of stones either from the beginning or from the end of the row.
This continues until there are no more piles left.

Return true if Alice wins the game, or false if Bob wins.

Example 1:
    Input: piles = [5,3,4,5]
    Output: true
    Explanation: Alice can always win by taking 5 from either end.

Example 2:
    Input: piles = [3,7,2,3]
    Output: true

Constraints:
- 2 <= piles.length <= 500
- piles.length is even.
- 1 <= piles[i] <= 500
- sum(piles[i]) is odd.

Topics: Array, Math, Dynamic Programming, Game Theory
"""
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "stoneGame",
        "complexity": "O(1) time, O(1) space",
        "description": "Mathematical proof: Alice always wins with even piles",
    },
    "dp": {
        "class": "SolutionDP",
        "method": "stoneGame",
        "complexity": "O(n²) time, O(n²) space",
        "description": "Interval DP tracking score difference",
    },
}


# ============================================================================
# Solution: Mathematical (Alice Always Wins)
# Time: O(1), Space: O(1)
#   - With even number of piles, Alice can control which "color" she takes
#   - She can always guarantee taking the more valuable color
# ============================================================================
class Solution:
    def stoneGame(self, piles: list[int]) -> bool:
        """
        Alice always wins when there's an even number of piles.

        Mathematical proof:
        1. Color piles alternately: even-indexed vs odd-indexed
        2. One color must have strictly more stones (sum is odd)
        3. Alice can always take ALL piles of her chosen color:
           - If even-indexed has more, she takes left first
           - This forces Bob to expose another even-indexed pile
           - Alice continues taking even-indexed piles

        Since Alice can guarantee the larger half, she always wins.
        """
        return True


# ============================================================================
# Solution: Interval DP (Educational)
# Time: O(n²), Space: O(n²)
#   - dp[i][j] = max score difference for current player on piles[i..j]
#   - At each state, try taking left or right pile
#   - Subtract opponent's best outcome (minimax)
# ============================================================================
class SolutionDP:
    def stoneGame(self, piles: list[int]) -> bool:
        """
        Track score difference from current player's perspective.

        dp(left, right) = max(
            piles[left] - dp(left+1, right),   # take left
            piles[right] - dp(left, right-1)   # take right
        )

        The subtraction accounts for perspective switch:
        - What opponent gains from their turn is our loss
        - So we subtract their best outcome

        Alice wins if dp(0, n-1) > 0.
        """
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def dp(left: int, right: int) -> int:
            if left > right:
                return 0

            take_left = piles[left] - dp(left + 1, right)
            take_right = piles[right] - dp(left, right - 1)

            return max(take_left, take_right)

        return dp(0, len(piles) - 1) > 0


def solve():
    """
    Input format:
    Line 1: piles (JSON array of integers)
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')

    piles = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.stoneGame(piles)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
