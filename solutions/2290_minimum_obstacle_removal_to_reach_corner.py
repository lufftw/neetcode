# solutions/2290_minimum_obstacle_removal_to_reach_corner.py
"""
Problem: Minimum Obstacle Removal to Reach Corner
Link: https://leetcode.com/problems/minimum-obstacle-removal-to-reach-corner/

You are given a 0-indexed 2D integer array grid of size m x n. Each cell has
one of two values:
- 0 represents an empty cell,
- 1 represents an obstacle that may be removed.

You can move up, down, left, or right from and to an empty cell.

Return the minimum number of obstacles to remove so you can move from the
upper left corner (0, 0) to the lower right corner (m - 1, n - 1).

Example 1:
    Input: grid = [[0,1,1],[1,1,0],[1,1,0]]
    Output: 2
    Explanation: We can remove the obstacles at (0, 1) and (0, 2) to create
    a path from (0, 0) to (2, 2).

Example 2:
    Input: grid = [[0,1,0,0,0],[0,1,0,1,0],[0,0,0,1,0]]
    Output: 0

Constraints:
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 10^5
- 2 <= m * n <= 10^5
- grid[i][j] is either 0 or 1.
- grid[0][0] == grid[m - 1][n - 1] == 0

Topics: Array, BFS, Graph, Heap, Matrix, Shortest Path
"""
from typing import List, Tuple, Deque
from collections import deque
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Minimum Obstacle Removal solution."""
    import json

    # Normalize actual
    if isinstance(actual, str):
        actual = int(actual)

    # If expected is available, compare directly
    if expected is not None:
        if isinstance(expected, str):
            expected = int(expected)
        return actual == expected

    # Judge-only mode: compute expected using reference solution
    grid = json.loads(input_data.strip())
    expected_result = _min_obstacles(grid)
    return actual == expected_result


def _min_obstacles(grid: List[List[int]]) -> int:
    """Reference solution using 0-1 BFS."""
    rows, cols = len(grid), len(grid[0])
    dist = [[float('inf')] * cols for _ in range(rows)]
    dist[0][0] = 0

    dq = deque([(0, 0, 0)])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while dq:
        cost, r, c = dq.popleft()
        if cost > dist[r][c]:
            continue
        if r == rows - 1 and c == cols - 1:
            return cost

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                new_cost = cost + grid[nr][nc]
                if new_cost < dist[nr][nc]:
                    dist[nr][nc] = new_cost
                    if grid[nr][nc] == 0:
                        dq.appendleft((new_cost, nr, nc))
                    else:
                        dq.append((new_cost, nr, nc))

    return dist[rows - 1][cols - 1]


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution01BFS",
        "method": "minimumObstacles",
        "complexity": "O(mn) time, O(mn) space",
        "description": "0-1 BFS with deque",
        "api_kernels": ["ShortestPath"],
        "patterns": ["shortest_path_01_bfs"],
    },
}


# ============================================
# Solution: 0-1 BFS
# Time: O(mn), Space: O(mn)
#   - Cost = grid value (0 for empty, 1 for obstacle)
#   - Cost-0 edges added to front, cost-1 to back
# ============================================
class Solution01BFS:
    def minimumObstacles(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])

        dist: List[List[float]] = [[float('inf')] * cols for _ in range(rows)]
        dist[0][0] = 0

        dq: Deque[Tuple[int, int, int]] = deque([(0, 0, 0)])  # (cost, row, col)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while dq:
            cost, r, c = dq.popleft()

            if cost > dist[r][c]:
                continue

            if r == rows - 1 and c == cols - 1:
                return cost

            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                if 0 <= nr < rows and 0 <= nc < cols:
                    # Cost to enter cell = grid value (0 or 1)
                    new_cost = cost + grid[nr][nc]

                    if new_cost < dist[nr][nc]:
                        dist[nr][nc] = new_cost

                        if grid[nr][nc] == 0:
                            dq.appendleft((new_cost, nr, nc))  # Free move: front
                        else:
                            dq.append((new_cost, nr, nc))      # Remove obstacle: back

        return int(dist[rows - 1][cols - 1])


def solve():
    """
    Input format (canonical JSON):
    Line 1: 2D array grid

    Output format:
    Integer: minimum obstacles to remove
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    grid = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.minimumObstacles(grid)

    print(result)


if __name__ == "__main__":
    solve()
