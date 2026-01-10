"""
Problem: Minimum Number of Visited Cells in a Grid
Link: https://leetcode.com/problems/minimum-number-of-visited-cells-in-a-grid/

From (i,j), can move to:
- (i, k) where j < k <= j + grid[i][j] (right)
- (k, j) where i < k <= i + grid[i][j] (down)

Find minimum cells to visit from (0,0) to (m-1, n-1).

Constraints:
- 1 <= m, n <= 10^5
- 1 <= m * n <= 10^5
- 0 <= grid[i][j] < m * n

Topics: DP, Heap, Segment Tree
"""
from typing import List
import heapq
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "minimumVisitedCells",
        "complexity": "O(m*n*log(m*n)) time, O(m*n) space",
        "description": "DP with heap optimization",
    },
}


# JUDGE_FUNC for generated tests
def _reference(grid: List[List[int]]) -> int:
    """Reference implementation using heap-optimized DP."""
    m, n = len(grid), len(grid[0])
    if m == 1 and n == 1:
        return 1

    INF = float('inf')
    dist = [[INF] * n for _ in range(m)]
    dist[0][0] = 1

    # row_heaps[i] = min-heap of (dist, max_reachable_col, col) for row i
    # col_heaps[j] = min-heap of (dist, max_reachable_row, row) for col j
    row_heaps = [[] for _ in range(m)]
    col_heaps = [[] for _ in range(n)]

    # Initialize from (0,0)
    if grid[0][0] > 0:
        heapq.heappush(row_heaps[0], (1, grid[0][0], 0))
        heapq.heappush(col_heaps[0], (1, grid[0][0], 0))

    for i in range(m):
        for j in range(n):
            # Find min dist from cells in same row that can reach (i, j)
            while row_heaps[i] and row_heaps[i][0][1] < j:
                heapq.heappop(row_heaps[i])
            if row_heaps[i]:
                dist[i][j] = min(dist[i][j], row_heaps[i][0][0] + 1)

            # Find min dist from cells in same column that can reach (i, j)
            while col_heaps[j] and col_heaps[j][0][1] < i:
                heapq.heappop(col_heaps[j])
            if col_heaps[j]:
                dist[i][j] = min(dist[i][j], col_heaps[j][0][0] + 1)

            # Special case for starting cell
            if i == 0 and j == 0:
                dist[i][j] = 1

            # If we can reach this cell, add it to heaps
            if dist[i][j] < INF and grid[i][j] > 0:
                max_col = j + grid[i][j]
                max_row = i + grid[i][j]
                heapq.heappush(row_heaps[i], (dist[i][j], max_col, j))
                heapq.heappush(col_heaps[j], (dist[i][j], max_row, i))

    return dist[m-1][n-1] if dist[m-1][n-1] < INF else -1


def judge(actual, expected, input_data: str) -> bool:
    import json
    grid = json.loads(input_data.strip())
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(grid)


JUDGE_FUNC = judge


# ============================================================================
# Solution: DP with Heap Optimization
# Time: O(m*n*log(m*n)), Space: O(m*n)
#   - Process cells left-to-right, top-to-bottom
#   - Use heaps to efficiently find minimum distance predecessor
# ============================================================================
class Solution:
    # Key insight: For each cell (i,j), find minimum distance from:
    #   1. Cells (i, k) where k < j and k + grid[i][k] >= j
    #   2. Cells (k, j) where k < i and k + grid[k][j] >= i
    #
    # Optimization: Use min-heaps keyed by (dist, max_reach)
    # Lazy deletion: pop entries where max_reach < current position

    def minimumVisitedCells(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        if m == 1 and n == 1:
            return 1

        INF = float('inf')
        dist = [[INF] * n for _ in range(m)]
        dist[0][0] = 1

        # row_heaps[i]: (dist, max_col_reachable, col) for cells in row i
        # col_heaps[j]: (dist, max_row_reachable, row) for cells in col j
        row_heaps = [[] for _ in range(m)]
        col_heaps = [[] for _ in range(n)]

        # Initialize from (0,0)
        if grid[0][0] > 0:
            heapq.heappush(row_heaps[0], (1, grid[0][0], 0))
            heapq.heappush(col_heaps[0], (1, grid[0][0], 0))

        for i in range(m):
            for j in range(n):
                # Clean up entries that can't reach (i, j)
                while row_heaps[i] and row_heaps[i][0][1] < j:
                    heapq.heappop(row_heaps[i])
                if row_heaps[i]:
                    dist[i][j] = min(dist[i][j], row_heaps[i][0][0] + 1)

                while col_heaps[j] and col_heaps[j][0][1] < i:
                    heapq.heappop(col_heaps[j])
                if col_heaps[j]:
                    dist[i][j] = min(dist[i][j], col_heaps[j][0][0] + 1)

                # Starting cell
                if i == 0 and j == 0:
                    dist[i][j] = 1

                # Add this cell to heaps if reachable and has moves
                if dist[i][j] < INF and grid[i][j] > 0:
                    heapq.heappush(row_heaps[i], (dist[i][j], j + grid[i][j], j))
                    heapq.heappush(col_heaps[j], (dist[i][j], i + grid[i][j], i))

        return dist[m-1][n-1] if dist[m-1][n-1] < INF else -1


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: grid (JSON 2D array)

    Example:
        [[3,4,2,1],[4,2,3,1],[2,1,0,0],[2,4,0,0]]
        -> 4
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')
    grid = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.minimumVisitedCells(grid)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
