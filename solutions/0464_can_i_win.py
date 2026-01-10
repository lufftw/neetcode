"""
Problem: Can I Win
Link: https://leetcode.com/problems/can-i-win/

In the "100 game" two players take turns adding, to a running total, any integer
from 1 to 10. The player who first causes the running total to reach or exceed
100 wins.

What if we change the game so that players cannot re-use integers?

Given two integers maxChoosableInteger and desiredTotal, return true if the
first player to move can force a win, otherwise, return false.

Assume both players play optimally.

Example 1:
    Input: maxChoosableInteger = 10, desiredTotal = 11
    Output: false
    Explanation: No matter which integer the first player chooses, the first
                 player will lose. The first player can choose 1..10. If they
                 choose 1, the second player can win by choosing 10.

Example 2:
    Input: maxChoosableInteger = 10, desiredTotal = 0
    Output: true

Example 3:
    Input: maxChoosableInteger = 10, desiredTotal = 1
    Output: true

Constraints:
- 1 <= maxChoosableInteger <= 20
- 0 <= desiredTotal <= 300

Topics: Math, Dynamic Programming, Bit Manipulation, Memoization, Game Theory
"""
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "canIWin",
        "complexity": "O(2^n * n) time, O(2^n) space",
        "description": "Bitmask DP with memoization",
    },
}


# ============================================================================
# Solution: Bitmask DP with Memoization
# Time: O(2^n * n), Space: O(2^n) where n = maxChoosableInteger
#
# Core insight: The game state is fully determined by which numbers have been
# used. We use a bitmask to represent the set of available numbers.
#
# At each state, the current player wins if:
# 1. They can pick a number >= remaining total (immediate win), OR
# 2. They can pick any number such that the opponent LOSES in the resulting state
#
# Minimax principle: A player wins iff opponent loses in at least one branch.
# ============================================================================
class Solution:
    def canIWin(self, maxChoosableInteger: int, desiredTotal: int) -> bool:
        """
        Determine if first player can force a win in the modified 100 game.

        Key observations:
        1. If desiredTotal <= 0, first player wins immediately (no move needed)
        2. If sum(1..n) < desiredTotal, no one can ever reach it -> first loses
        3. Otherwise, use memoized game theory: current player wins if they can
           force opponent into a losing state.

        State representation: bitmask of used numbers (bit i = number i+1 used)
        - n numbers -> 2^n possible states
        - Each state explored once with O(n) work -> O(2^n * n) total

        Args:
            maxChoosableInteger: Maximum number that can be chosen (1 to this)
            desiredTotal: Target sum to reach or exceed

        Returns:
            True if first player can guarantee a win with optimal play
        """
        n = maxChoosableInteger
        total_sum = n * (n + 1) // 2

        # Edge case: already reached target
        if desiredTotal <= 0:
            return True

        # Edge case: impossible to reach target even using all numbers
        if total_sum < desiredTotal:
            return False

        # Memoization cache: used_mask -> can current player win?
        memo = {}

        def can_win(used_mask: int, remaining: int) -> bool:
            """
            Returns True if the current player can force a win.

            Args:
                used_mask: Bitmask of numbers already used
                remaining: How much more is needed to reach desiredTotal

            The current player tries each unused number:
            - If picking it reaches/exceeds remaining -> immediate win
            - Otherwise, recurse and check if opponent loses
            """
            if used_mask in memo:
                return memo[used_mask]

            # Try each unused number from 1 to n
            for num in range(1, n + 1):
                bit = 1 << (num - 1)

                if used_mask & bit:
                    continue  # Already used

                # Current player picks 'num'
                if num >= remaining:
                    # Immediate win: reached or exceeded target
                    memo[used_mask] = True
                    return True

                # Recurse: opponent plays with updated state
                # We win if opponent loses in this branch
                if not can_win(used_mask | bit, remaining - num):
                    memo[used_mask] = True
                    return True

            # No winning move found -> current player loses
            memo[used_mask] = False
            return False

        return can_win(0, desiredTotal)


def solve():
    """
    Input format:
    Line 1: maxChoosableInteger (integer)
    Line 2: desiredTotal (integer)
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')

    maxChoosableInteger = json.loads(lines[0])
    desiredTotal = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.canIWin(maxChoosableInteger, desiredTotal)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
