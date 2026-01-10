# solutions/0695_max_area_of_island.py
"""
Problem 0695 - Max Area of Island

Given an m x n binary matrix grid, find the maximum area of an island.
An island is a group of 1's (land) connected 4-directionally.
Return 0 if there is no island.

LeetCode Constraints:
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 50
- grid[i][j] is either 0 or 1

Key Insight:
This is a connected components problem on a 2D grid.
For each unvisited land cell, explore its entire connected component
using DFS or BFS, counting cells as we go. Track the maximum.

The key optimization is marking visited cells in-place by setting
them to 0 (water), avoiding extra space for a visited set.

Solution Approaches:
1. DFS recursive: clean code, implicit stack via recursion
2. DFS iterative: explicit stack, avoids stack overflow on deep recursion
3. BFS: uses queue, explores level by level
"""
from typing import List
from collections import deque
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionDFS",
        "method": "maxAreaOfIsland",
        "complexity": "O(m*n) time, O(m*n) space",
        "description": "Recursive DFS with in-place marking",
    },
    "iterative": {
        "class": "SolutionIterativeDFS",
        "method": "maxAreaOfIsland",
        "complexity": "O(m*n) time, O(m*n) space",
        "description": "Iterative DFS using explicit stack",
    },
    "bfs": {
        "class": "SolutionBFS",
        "method": "maxAreaOfIsland",
        "complexity": "O(m*n) time, O(m*n) space",
        "description": "BFS traversal using queue",
    },
}


class SolutionDFS:
    """
    Recursive DFS approach.

    For each cell that is land (1), start a DFS to explore the entire
    connected island. Mark cells as visited by changing 1 to 0.

    The DFS returns the area of the island it explores.
    Track the maximum area seen across all starting points.

    In-place modification avoids O(m*n) extra space for visited set,
    though recursion stack can be O(m*n) in worst case (snake pattern).
    """

    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0

        m, n = len(grid), len(grid[0])
        max_area = 0

        def dfs(row: int, col: int) -> int:
            # Base case: out of bounds or water
            if row < 0 or row >= m or col < 0 or col >= n or grid[row][col] == 0:
                return 0

            # Mark as visited (sink the land)
            grid[row][col] = 0

            # Explore all 4 directions and sum areas
            area = 1  # Count this cell
            area += dfs(row + 1, col)
            area += dfs(row - 1, col)
            area += dfs(row, col + 1)
            area += dfs(row, col - 1)

            return area

        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    max_area = max(max_area, dfs(i, j))

        return max_area


class SolutionIterativeDFS:
    """
    Iterative DFS using explicit stack.

    Same logic as recursive DFS, but uses an explicit stack to avoid
    potential stack overflow on very large/deep islands.

    The stack stores (row, col) coordinates to visit.
    Pop a cell, mark it, count it, and push unvisited neighbors.
    """

    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0

        m, n = len(grid), len(grid[0])
        max_area = 0
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    area = 0
                    stack = [(i, j)]
                    grid[i][j] = 0  # Mark starting cell

                    while stack:
                        row, col = stack.pop()
                        area += 1

                        for dr, dc in directions:
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                                grid[nr][nc] = 0  # Mark before pushing
                                stack.append((nr, nc))

                    max_area = max(max_area, area)

        return max_area


class SolutionBFS:
    """
    BFS approach using queue.

    Explores the island level by level (by distance from start).
    Functionally equivalent to DFS for finding area, but explores
    in breadth-first order rather than depth-first.

    Uses deque for efficient O(1) popleft operations.
    """

    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0

        m, n = len(grid), len(grid[0])
        max_area = 0
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    area = 0
                    queue = deque([(i, j)])
                    grid[i][j] = 0  # Mark starting cell

                    while queue:
                        row, col = queue.popleft()
                        area += 1

                        for dr, dc in directions:
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                                grid[nr][nc] = 0  # Mark before enqueuing
                                queue.append((nr, nc))

                    max_area = max(max_area, area)

        return max_area


def solve():
    import sys
    import json

    data = sys.stdin.read().strip()
    grid = json.loads(data)

    solver = get_solver(SOLUTIONS)
    result = solver.maxAreaOfIsland(grid)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
