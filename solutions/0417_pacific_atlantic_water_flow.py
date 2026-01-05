# solutions/0417_pacific_atlantic_water_flow.py
"""
Problem: Pacific Atlantic Water Flow
Link: https://leetcode.com/problems/pacific-atlantic-water-flow/

There is an m x n rectangular island that borders both the Pacific Ocean and Atlantic Ocean.
The Pacific Ocean touches the island's left and top edges, and the Atlantic Ocean touches the
island's right and bottom edges.

The island is partitioned into a grid of square cells. You are given an m x n integer matrix
heights where heights[r][c] represents the height above sea level of the cell at coordinate (r, c).

The island receives a lot of rain, and the rain water can flow to neighboring cells directly
north, south, east, and west if the neighboring cell's height is less than or equal to the
current cell's height. Water can flow from any cell adjacent to an ocean into the ocean.

Return a 2D list of grid coordinates result where result[i] = [ri, ci] denotes that rain water
can flow from cell (ri, ci) to both the Pacific and Atlantic oceans.

Example 1:
    Input: heights = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]
    Output: [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]

Example 2:
    Input: heights = [[1]]
    Output: [[0,0]]

Constraints:
- m == heights.length
- n == heights[r].length
- 1 <= m, n <= 200
- 0 <= heights[r][c] <= 10^5

Topics: Array, DFS, BFS, Matrix
"""
from typing import List, Set, Tuple
from collections import deque
from _runner import get_solver


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionBFS",
        "method": "pacificAtlantic",
        "complexity": "O(m*n) time, O(m*n) space",
        "description": "Multi-source BFS from ocean borders",
        "api_kernels": ["GraphBFS"],
        "patterns": ["graph_bfs_multi_source"],
    },
    "dfs": {
        "class": "SolutionDFS",
        "method": "pacificAtlantic",
        "complexity": "O(m*n) time, O(m*n) space",
        "description": "DFS from ocean borders",
        "api_kernels": ["GraphDFS"],
        "patterns": ["graph_dfs_reachability"],
    },
}

# Use sorted comparison since result can be in any order
COMPARE_MODE = "sorted"


# ============================================
# Solution 1: Multi-source BFS
# Time: O(m * n), Space: O(m * n)
#   - Reverse direction: find cells reachable FROM ocean
#   - Start from ocean borders, go uphill
#   - Intersection gives cells reaching both oceans
# ============================================
class SolutionBFS:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        if not heights or not heights[0]:
            return []

        rows, cols = len(heights), len(heights[0])
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        def bfs(sources: List[Tuple[int, int]]) -> Set[Tuple[int, int]]:
            """Multi-source BFS to find all reachable cells."""
            reachable: Set[Tuple[int, int]] = set(sources)
            queue: deque[Tuple[int, int]] = deque(sources)

            while queue:
                row, col = queue.popleft()

                for dr, dc in directions:
                    nr, nc = row + dr, col + dc
                    # Can flow uphill (from ocean's perspective)
                    if (0 <= nr < rows and 0 <= nc < cols and
                        (nr, nc) not in reachable and
                        heights[nr][nc] >= heights[row][col]):
                        reachable.add((nr, nc))
                        queue.append((nr, nc))

            return reachable

        # Pacific: top row + left column
        pacific_sources = (
            [(0, col) for col in range(cols)] +
            [(row, 0) for row in range(rows)]
        )

        # Atlantic: bottom row + right column
        atlantic_sources = (
            [(rows - 1, col) for col in range(cols)] +
            [(row, cols - 1) for row in range(rows)]
        )

        # Find cells reachable from each ocean
        pacific_reach = bfs(pacific_sources)
        atlantic_reach = bfs(atlantic_sources)

        # Return intersection as list of lists
        return [[r, c] for r, c in pacific_reach & atlantic_reach]


# ============================================
# Solution 2: DFS from ocean borders
# Time: O(m * n), Space: O(m * n)
#   - Same concept, recursive approach
# ============================================
class SolutionDFS:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        if not heights:
            return []

        rows, cols = len(heights), len(heights[0])
        pacific: Set[Tuple[int, int]] = set()
        atlantic: Set[Tuple[int, int]] = set()

        def dfs(row: int, col: int, reachable: Set, prev_height: int) -> None:
            if (row < 0 or row >= rows or col < 0 or col >= cols or
                (row, col) in reachable or heights[row][col] < prev_height):
                return

            reachable.add((row, col))
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                dfs(row + dr, col + dc, reachable, heights[row][col])

        # DFS from ocean borders
        for col in range(cols):
            dfs(0, col, pacific, 0)
            dfs(rows - 1, col, atlantic, 0)

        for row in range(rows):
            dfs(row, 0, pacific, 0)
            dfs(row, cols - 1, atlantic, 0)

        return [[r, c] for r, c in pacific & atlantic]


def solve():
    """
    Input format (canonical JSON):
    Line 1: 2D array heights

    Output format:
    2D array of coordinates
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    heights = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.pacificAtlantic(heights)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
