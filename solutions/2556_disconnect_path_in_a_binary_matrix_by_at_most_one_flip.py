"""
Problem: Disconnect Path in a Binary Matrix by at Most One Flip
Link: https://leetcode.com/problems/disconnect-path-in-a-binary-matrix-by-at-most-one-flip/

Can flip at most one cell (not start/end) to disconnect path from (0,0) to (m-1,n-1).
Movement: only right or down through cells with value 1.

Constraints:
- 1 <= m, n <= 1000
- 1 <= m * n <= 10^5
- grid[0][0] == grid[m-1][n-1] == 1

Topics: Array, Dynamic Programming, DFS, BFS, Matrix
"""
from typing import List
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "isPossibleToCutPath",
        "complexity": "O(m * n) time, O(m + n) space",
        "description": "Two DFS passes to check for vertex-disjoint paths",
    },
}


# JUDGE_FUNC for generated tests
def _reference(grid: List[List[int]]) -> bool:
    """Reference implementation."""
    import copy
    g = copy.deepcopy(grid)
    m, n = len(g), len(g[0])

    def dfs(r, c):
        if r == m - 1 and c == n - 1:
            return True
        if r >= m or c >= n or g[r][c] == 0:
            return False
        g[r][c] = 0
        return dfs(r + 1, c) or dfs(r, c + 1)

    if not dfs(0, 0):
        return True
    g[0][0] = 1
    return not dfs(0, 0)


def judge(actual, expected, input_data: str) -> bool:
    grid = json.loads(input_data.strip().split('\n')[0])
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(grid)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Two DFS Passes
# Time: O(m * n), Space: O(m + n) for recursion stack
# ============================================================================
class Solution:
    # Key insight:
    #   - If 2 vertex-disjoint paths exist (sharing only start/end), can't disconnect
    #   - Otherwise, all paths share some intermediate cell → flip it to disconnect
    #
    # Algorithm:
    #   1. DFS to find first path, mark all visited cells as 0
    #   2. Restore start cell (can't flip it)
    #   3. DFS again - if path still exists, two disjoint paths exist
    #
    # Why this works:
    #   - First DFS "removes" cells on its path
    #   - If second DFS succeeds, it found a completely different route
    #   - Movement is only right/down, so no revisiting same cell in DFS

    def isPossibleToCutPath(self, grid: List[List[int]]) -> bool:
        m, n = len(grid), len(grid[0])

        def dfs(r: int, c: int) -> bool:
            if r == m - 1 and c == n - 1:
                return True
            if r >= m or c >= n or grid[r][c] == 0:
                return False
            grid[r][c] = 0  # Mark as visited
            return dfs(r + 1, c) or dfs(r, c + 1)

        # First pass: find one path
        if not dfs(0, 0):
            return True  # No path exists at all

        # Restore start (we can't flip it)
        grid[0][0] = 1

        # Second pass: check if another disjoint path exists
        return not dfs(0, 0)


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: grid (JSON 2D array)

    Example:
        [[1,1,1],[1,0,0],[1,1,1]]
        -> true
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    grid = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.isPossibleToCutPath(grid)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
