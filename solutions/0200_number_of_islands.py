# solutions/0200_number_of_islands.py
"""
Problem: Number of Islands
Link: https://leetcode.com/problems/number-of-islands/

Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water),
return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands horizontally
or vertically. You may assume all four edges of the grid are all surrounded by water.

Example 1:
    Input: grid = [
      ["1","1","1","1","0"],
      ["1","1","0","1","0"],
      ["1","1","0","0","0"],
      ["0","0","0","0","0"]
    ]
    Output: 1

Example 2:
    Input: grid = [
      ["1","1","0","0","0"],
      ["1","1","0","0","0"],
      ["0","0","1","0","0"],
      ["0","0","0","1","1"]
    ]
    Output: 3

Constraints:
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 300
- grid[i][j] is '0' or '1'.

Topics: Array, DFS, BFS, Union Find, Matrix
"""
from typing import List
from collections import deque
from _runner import get_solver


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionDFS",
        "method": "numIslands",
        "complexity": "O(m*n) time, O(m*n) space",
        "description": "DFS flood fill approach",
        "api_kernels": ["GraphDFS"],
        "patterns": ["graph_dfs_connected_components"],
    },
    "bfs": {
        "class": "SolutionBFS",
        "method": "numIslands",
        "complexity": "O(m*n) time, O(min(m,n)) space",
        "description": "BFS flood fill approach",
        "api_kernels": ["GraphBFS"],
        "patterns": ["graph_bfs_connected_components"],
    },
}


# ============================================
# Solution 1: DFS (Depth-First Search)
# Time: O(m * n), Space: O(m * n) worst case recursion
#   - Each cell visited once
#   - Mark visited by changing '1' to '0'
#   - DFS explores entire island, then count++
# ============================================
class SolutionDFS:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        island_count = 0

        def dfs(row: int, col: int) -> None:
            """Flood fill: mark all connected land cells."""
            # Boundary check and water/visited check
            if (row < 0 or row >= rows or
                col < 0 or col >= cols or
                grid[row][col] != '1'):
                return

            # Mark as visited (sink the land)
            grid[row][col] = '0'

            # Explore 4 directions
            dfs(row + 1, col)  # Down
            dfs(row - 1, col)  # Up
            dfs(row, col + 1)  # Right
            dfs(row, col - 1)  # Left

        # Main loop: find and count islands
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == '1':
                    island_count += 1
                    dfs(row, col)  # Mark entire island as visited

        return island_count


# ============================================
# Solution 2: BFS (Breadth-First Search)
# Time: O(m * n), Space: O(min(m, n)) for queue
#   - Each cell visited once
#   - BFS explores level by level (not needed here, just alternative)
# ============================================
class SolutionBFS:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        island_count = 0
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        def bfs(start_row: int, start_col: int) -> None:
            queue = deque([(start_row, start_col)])
            grid[start_row][start_col] = '0'

            while queue:
                row, col = queue.popleft()
                for dr, dc in directions:
                    nr, nc = row + dr, col + dc
                    if (0 <= nr < rows and 0 <= nc < cols and
                        grid[nr][nc] == '1'):
                        grid[nr][nc] = '0'
                        queue.append((nr, nc))

        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == '1':
                    island_count += 1
                    bfs(row, col)

        return island_count


def solve():
    """
    Input format (canonical JSON):
    Line 1: 2D array grid (e.g. [["1","1","0"],["1","0","0"]])

    Output format:
    Integer: number of islands
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    grid = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.numIslands(grid)

    print(result)


if __name__ == "__main__":
    solve()
