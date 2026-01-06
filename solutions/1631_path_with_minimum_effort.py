# solutions/1631_path_with_minimum_effort.py
"""
Problem: Path With Minimum Effort
Link: https://leetcode.com/problems/path-with-minimum-effort/

You are given a 2D array of heights where heights[row][col] represents the
height of cell (row, col). Return the minimum effort required to travel from
the top-left cell to the bottom-right cell.

A route's effort is the maximum absolute difference in heights between two
consecutive cells of the route.

Example 1:
    Input: heights = [[1,2,2],[3,8,2],[5,3,5]]
    Output: 2
    Explanation: The route of [1,3,5,3,5] has a maximum absolute difference
    of 2 in consecutive cells.

Example 2:
    Input: heights = [[1,2,3],[3,8,4],[5,3,5]]
    Output: 1

Example 3:
    Input: heights = [[1,2,1,1,1],[1,2,1,2,1],[1,2,1,2,1],[1,2,1,2,1],[1,1,1,2,1]]
    Output: 0

Constraints:
- rows == heights.length
- columns == heights[i].length
- 1 <= rows, columns <= 100
- 1 <= heights[i][j] <= 10^6

Topics: Array, Binary Search, DFS, BFS, Union Find, Heap, Matrix
"""
from typing import List, Tuple
from heapq import heappush, heappop
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Path With Minimum Effort solution."""
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
    heights = json.loads(input_data.strip())
    expected_result = _minimum_effort(heights)
    return actual == expected_result


def _minimum_effort(heights: List[List[int]]) -> int:
    """Reference solution using minimax Dijkstra."""
    rows, cols = len(heights), len(heights[0])
    dist = [[float('inf')] * cols for _ in range(rows)]
    dist[0][0] = 0

    pq = [(0, 0, 0)]
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while pq:
        effort, r, c = heappop(pq)
        if effort > dist[r][c]:
            continue
        if r == rows - 1 and c == cols - 1:
            return effort
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                edge_effort = abs(heights[nr][nc] - heights[r][c])
                new_effort = max(effort, edge_effort)
                if new_effort < dist[nr][nc]:
                    dist[nr][nc] = new_effort
                    heappush(pq, (new_effort, nr, nc))

    return dist[rows - 1][cols - 1]


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionDijkstra",
        "method": "minimumEffortPath",
        "complexity": "O(mn log(mn)) time, O(mn) space",
        "description": "Minimax Dijkstra's algorithm",
        "api_kernels": ["ShortestPath"],
        "patterns": ["shortest_path_minimax"],
    },
}


# ============================================
# Solution: Minimax Dijkstra
# Time: O(mn log(mn)), Space: O(mn)
#   - Instead of summing edges, track max edge on path
#   - Dijkstra still works because we want to minimize the max
# ============================================
class SolutionDijkstra:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        rows, cols = len(heights), len(heights[0])

        # dist[r][c] = minimum effort to reach (r, c)
        dist: List[List[float]] = [[float('inf')] * cols for _ in range(rows)]
        dist[0][0] = 0

        # (effort, row, col)
        pq: List[Tuple[int, int, int]] = [(0, 0, 0)]
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while pq:
            effort, r, c = heappop(pq)

            if effort > dist[r][c]:
                continue

            if r == rows - 1 and c == cols - 1:
                return effort

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    # Edge weight = absolute height difference
                    edge_effort = abs(heights[nr][nc] - heights[r][c])
                    # New effort = max(path effort so far, this edge)
                    new_effort = max(effort, edge_effort)

                    if new_effort < dist[nr][nc]:
                        dist[nr][nc] = new_effort
                        heappush(pq, (new_effort, nr, nc))

        return int(dist[rows - 1][cols - 1])


def solve():
    """
    Input format (canonical JSON):
    Line 1: 2D array heights

    Output format:
    Integer: minimum effort
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    heights = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.minimumEffortPath(heights)

    print(result)


if __name__ == "__main__":
    solve()
