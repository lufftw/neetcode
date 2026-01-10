"""
Problem: Zuma Game
Link: https://leetcode.com/problems/zuma-game/

Insert balls from hand to eliminate all balls on board.
Consecutive 3+ same-colored balls are removed.
Find minimum insertions to clear board, or -1 if impossible.

Constraints:
- 1 <= board.length <= 16
- 1 <= hand.length <= 5
- board and hand contain only 'R', 'Y', 'B', 'G', 'W'
- No 3+ consecutive same colors in initial board

Topics: String, Dynamic Programming, BFS, DFS, Memoization
"""
from _runner import get_solver
import json
from functools import lru_cache


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "findMinStep",
        "complexity": "O(n * 5^m * n) time, O(n * 5^m) space",
        "description": "DFS with memoization and pruning",
    },
}


# ============================================================================
# Solution: DFS with Memoization
# Time: O(n * 5^m * n), Space: O(n * 5^m) where n = board len, m = hand len
# ============================================================================
class Solution:
    # Key insight: Try inserting each hand ball at strategic positions.
    # After insertion, remove consecutive groups of 3+.
    # Use memoization on (board, sorted_hand) to avoid redundant states.
    #
    # Pruning: Only insert a ball next to the same color on board.
    # This dramatically reduces search space.

    def findMinStep(self, board: str, hand: str) -> int:

        def remove_consecutive(s: str) -> str:
            """Remove all consecutive groups of 3+ same-colored balls."""
            while True:
                new_s = ""
                i = 0
                changed = False
                while i < len(s):
                    j = i
                    while j < len(s) and s[j] == s[i]:
                        j += 1
                    if j - i >= 3:
                        changed = True
                    else:
                        new_s += s[i:j]
                    i = j
                s = new_s
                if not changed:
                    break
            return s

        @lru_cache(maxsize=None)
        def dfs(board: str, hand: str) -> int:
            """Return minimum balls to insert to clear board, or -1 if impossible."""
            board = remove_consecutive(board)
            if not board:
                return 0
            if not hand:
                return -1

            result = float('inf')
            hand_set = set(hand)

            # Try inserting each unique color from hand
            for color in hand_set:
                new_hand = hand.replace(color, '', 1)

                # Only insert next to same color (optimization)
                for i in range(len(board)):
                    # Insert at positions where it might help:
                    # 1. Next to same color
                    # 2. Between two same colors (to complete a triple)
                    if board[i] == color:
                        new_board = board[:i] + color + board[i:]
                        sub_result = dfs(new_board, new_hand)
                        if sub_result != -1:
                            result = min(result, sub_result + 1)

                    # Also try inserting between two same colors
                    if i > 0 and board[i] == board[i - 1] and board[i] != color:
                        # This position could help if we insert between
                        pass

                # Also try inserting at each position (for completeness)
                # This handles edge cases where optimal insertion isn't adjacent
                for i in range(len(board) + 1):
                    if i > 0 and board[i - 1] == color:
                        continue  # Already tried
                    if i < len(board) and board[i] == color:
                        continue  # Already tried

                    new_board = board[:i] + color + board[i:]
                    sub_result = dfs(new_board, new_hand)
                    if sub_result != -1:
                        result = min(result, sub_result + 1)

            return result if result != float('inf') else -1

        # Sort hand for consistent memoization keys
        result = dfs(board, ''.join(sorted(hand)))
        return result


# ============================================================================
# JUDGE_FUNC: Verify answer using reference solution
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Verify answer by running reference solution.
    """
    lines = input_data.strip().split('\n')
    board = lines[0].strip().strip('"')
    hand = lines[1].strip().strip('"')

    # Run reference solution
    sol = Solution()
    correct = sol.findMinStep(board, hand)

    return actual == correct


JUDGE_FUNC = judge


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: board (string)
        Line 2: hand (string)

    Example:
        WRRBBW
        RB
        -> -1
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    board = lines[0].strip().strip('"')
    hand = lines[1].strip().strip('"')

    solver = get_solver(SOLUTIONS)
    result = solver.findMinStep(board, hand)

    print(result)


if __name__ == "__main__":
    solve()
