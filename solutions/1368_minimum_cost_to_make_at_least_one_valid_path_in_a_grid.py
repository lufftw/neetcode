# solutions/1368_minimum_cost_to_make_at_least_one_valid_path_in_a_grid.py
"""
Problem: Minimum Cost to Make at Least One Valid Path in a Grid
Link: https://leetcode.com/problems/minimum-cost-to-make-at-least-one-valid-path-in-a-grid/

Given an m x n grid. Each cell of the grid has a sign pointing to the next cell
you should visit if you are currently in this cell. The sign can be:
1 = go right, 2 = go left, 3 = go down, 4 = go up

Notice that there could be some signs on the cells of the grid that point outside
the grid.

You will initially start at the upper left cell (0, 0). A valid path in the grid
is a path that starts from (0, 0) and ends at (m-1, n-1) following the signs.

Return the minimum cost to make the grid have at least one valid path.

Example 1:
    Input: grid = [[1,1,1,1],[2,2,2,2],[1,1,1,1],[2,2,2,2]]
    Output: 3

Example 2:
    Input: grid = [[1,1,3],[3,2,2],[1,1,4]]
    Output: 0

Example 3:
    Input: grid = [[1,2],[4,3]]
    Output: 1

Constraints:
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 100
- 1 <= grid[i][j] <= 4

Topics: Array, BFS, Graph, Heap, Matrix, Shortest Path
"""
from typing import List, Tuple, Deque
from collections import deque
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Minimum Cost Valid Path solution."""
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
    expected_result = _min_cost(grid)
    return actual == expected_result


def _min_cost(grid: List[List[int]]) -> int:
    """Reference solution using 0-1 BFS."""
    rows, cols = len(grid), len(grid[0])
    directions = {1: (0, 1), 2: (0, -1), 3: (1, 0), 4: (-1, 0)}
    dir_to_num = {(0, 1): 1, (0, -1): 2, (1, 0): 3, (-1, 0): 4}
    all_dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    dist = [[float('inf')] * cols for _ in range(rows)]
    dist[0][0] = 0

    dq = deque([(0, 0, 0)])

    while dq:
        cost, r, c = dq.popleft()
        if cost > dist[r][c]:
            continue
        if r == rows - 1 and c == cols - 1:
            return cost

        current_arrow = grid[r][c]

        for dr, dc in all_dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                edge_cost = 0 if dir_to_num[(dr, dc)] == current_arrow else 1
                new_cost = cost + edge_cost
                if new_cost < dist[nr][nc]:
                    dist[nr][nc] = new_cost
                    if edge_cost == 0:
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
        "method": "minCost",
        "complexity": "O(mn) time, O(mn) space",
        "description": "0-1 BFS with deque",
        "api_kernels": ["ShortestPath"],
        "patterns": ["shortest_path_01_bfs"],
    },
}


# ============================================
# Solution: 0-1 BFS
# Time: O(mn), Space: O(mn)
#   - Cost 0: follow arrow direction (add to front)
#   - Cost 1: change direction (add to back)
#   - Deque maintains sorted order without heap
# ============================================
class Solution01BFS:
    def minCost(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])

        # Direction mapping: 1=right, 2=left, 3=down, 4=up
        dir_to_num = {(0, 1): 1, (0, -1): 2, (1, 0): 3, (-1, 0): 4}
        all_dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        dist: List[List[float]] = [[float('inf')] * cols for _ in range(rows)]
        dist[0][0] = 0

        dq: Deque[Tuple[int, int, int]] = deque([(0, 0, 0)])  # (cost, row, col)

        while dq:
            cost, r, c = dq.popleft()

            if cost > dist[r][c]:
                continue

            if r == rows - 1 and c == cols - 1:
                return cost

            current_arrow = grid[r][c]

            for dr, dc in all_dirs:
                nr, nc = r + dr, c + dc

                if 0 <= nr < rows and 0 <= nc < cols:
                    # Cost 0 if this direction matches the arrow
                    edge_cost = 0 if dir_to_num[(dr, dc)] == current_arrow else 1
                    new_cost = cost + edge_cost

                    if new_cost < dist[nr][nc]:
                        dist[nr][nc] = new_cost

                        if edge_cost == 0:
                            dq.appendleft((new_cost, nr, nc))  # Front for cost 0
                        else:
                            dq.append((new_cost, nr, nc))      # Back for cost 1

        return int(dist[rows - 1][cols - 1])


def solve():
    """
    Input format (canonical JSON):
    Line 1: 2D array grid

    Output format:
    Integer: minimum cost
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    grid = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.minCost(grid)

    print(result)


if __name__ == "__main__":
    solve()
