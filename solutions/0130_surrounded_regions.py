# solutions/0130_surrounded_regions.py
"""
Problem 0130 - Surrounded Regions

Given an m x n matrix board containing 'X' and 'O', capture all regions
that are 4-directionally surrounded by 'X'.

A region is captured by flipping all 'O's into 'X's in that surrounded region.

LeetCode Constraints:
- m == board.length
- n == board[i].length
- 1 <= m, n <= 200
- board[i][j] is 'X' or 'O'

Key Insight:
An 'O' is NOT captured if and only if it's connected to a border 'O'.
So instead of finding surrounded regions, we find border-connected 'O's.

Algorithm:
1. Start DFS/BFS from all border 'O's
2. Mark all reachable 'O's as safe (temporarily change to 'S')
3. Iterate through board: 'O' -> 'X', 'S' -> 'O'

This inverts the problem from "find surrounded" to "find not surrounded".

Solution Approaches:
1. DFS from borders: O(m*n) time, O(m*n) space (recursion stack)
2. BFS from borders: O(m*n) time, O(m*n) space (queue)
"""
from typing import List
from collections import deque
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionDFS",
        "method": "solve",
        "complexity": "O(m*n) time, O(m*n) space",
        "description": "DFS from border O's, mark safe, flip remaining",
    },
    "bfs": {
        "class": "SolutionBFS",
        "method": "solve",
        "complexity": "O(m*n) time, O(m*n) space",
        "description": "BFS from border O's using queue",
    },
}


class SolutionDFS:
    """
    DFS approach marking border-connected cells.

    Phase 1: For each 'O' on the border, DFS to mark all connected
    'O's as 'S' (safe). These cells are NOT surrounded.

    Phase 2: Scan the entire board:
    - 'O' cells (not marked safe) -> 'X' (captured)
    - 'S' cells -> 'O' (restore safe cells)

    The key insight is that surrounded means "not reachable from border".
    """

    def solve(self, board: List[List[str]]) -> None:
        if not board or not board[0]:
            return

        m, n = len(board), len(board[0])

        def dfs(row: int, col: int) -> None:
            """Mark cell and all connected O's as safe."""
            if row < 0 or row >= m or col < 0 or col >= n:
                return
            if board[row][col] != "O":
                return

            board[row][col] = "S"  # Mark as safe
            dfs(row + 1, col)
            dfs(row - 1, col)
            dfs(row, col + 1)
            dfs(row, col - 1)

        # Phase 1: Mark all border-connected O's as safe
        for i in range(m):
            dfs(i, 0)       # Left border
            dfs(i, n - 1)   # Right border

        for j in range(n):
            dfs(0, j)       # Top border
            dfs(m - 1, j)   # Bottom border

        # Phase 2: Capture surrounded O's and restore safe cells
        for i in range(m):
            for j in range(n):
                if board[i][j] == "O":
                    board[i][j] = "X"  # Captured
                elif board[i][j] == "S":
                    board[i][j] = "O"  # Restore safe


class SolutionBFS:
    """
    BFS approach using queue.

    Same logic as DFS, but explores in breadth-first order.
    Collects all border O's first, then processes them level by level.

    Avoids potential stack overflow on large grids with deep recursion.
    """

    def solve(self, board: List[List[str]]) -> None:
        if not board or not board[0]:
            return

        m, n = len(board), len(board[0])
        queue: deque = deque()

        # Collect all border O's
        for i in range(m):
            if board[i][0] == "O":
                queue.append((i, 0))
                board[i][0] = "S"
            if board[i][n - 1] == "O":
                queue.append((i, n - 1))
                board[i][n - 1] = "S"

        for j in range(n):
            if board[0][j] == "O":
                queue.append((0, j))
                board[0][j] = "S"
            if board[m - 1][j] == "O":
                queue.append((m - 1, j))
                board[m - 1][j] = "S"

        # BFS to mark all connected O's
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while queue:
            row, col = queue.popleft()

            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if 0 <= nr < m and 0 <= nc < n and board[nr][nc] == "O":
                    board[nr][nc] = "S"
                    queue.append((nr, nc))

        # Capture and restore
        for i in range(m):
            for j in range(n):
                if board[i][j] == "O":
                    board[i][j] = "X"
                elif board[i][j] == "S":
                    board[i][j] = "O"


def solve():
    import sys
    import json

    data = sys.stdin.read().strip()
    board = json.loads(data)

    solver = get_solver(SOLUTIONS)
    solver.solve(board)

    print(json.dumps(board, separators=(",", ":")))


if __name__ == "__main__":
    solve()
