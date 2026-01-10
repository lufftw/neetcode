"""
Problem: Swim in Rising Water
Link: https://leetcode.com/problems/swim-in-rising-water/

You are given an n x n integer matrix grid where each value grid[i][j] represents
the elevation at that point (i, j).

The rain starts to fall. At time t, the depth of the water everywhere is t. You
can swim from a square to another 4-directionally adjacent square if and only if
the elevation of both squares individually are at most t. You can swim infinite
distances in zero time. Of course, you must stay within the boundaries of the grid.

Return the least time until you can reach the bottom right square (n-1, n-1) if
you start at the top left square (0, 0).

Example 1:
    Input: grid = [[0,2],[1,3]]
    Output: 3

Example 2:
    Input: grid = [[0,1,2,3,4],[24,23,22,21,5],[12,13,14,15,16],[11,17,18,19,20],[10,9,8,7,6]]
    Output: 16

Constraints:
- n == grid.length
- n == grid[i].length
- 1 <= n <= 50
- 0 <= grid[i][j] < n^2
- Each value grid[i][j] is unique.

Topics: Array, Binary Search, DFS, BFS, Union Find, Heap Priority Queue, Matrix
"""

import json
import heapq
from typing import List
from _runner import get_solver


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionDijkstra",
        "method": "swimInWater",
        "complexity": "O(n^2 log n) time, O(n^2) space",
        "description": "Modified Dijkstra - minimize max elevation along path",
    },
    "binary_search": {
        "class": "SolutionBinarySearch",
        "method": "swimInWater",
        "complexity": "O(n^2 log(n^2)) time, O(n^2) space",
        "description": "Binary search on time + BFS/DFS to verify reachability",
    },
    "union_find": {
        "class": "SolutionUnionFind",
        "method": "swimInWater",
        "complexity": "O(n^2 log n) time, O(n^2) space",
        "description": "Process cells by elevation, union adjacent cells",
    },
}


# ============================================================================
# Solution 1: Modified Dijkstra's Algorithm
# Time: O(n^2 log n), Space: O(n^2)
#
# Key Insight:
#   This is a shortest path problem where the "cost" of a path is the maximum
#   elevation along that path (not the sum). We need to find the path from
#   (0,0) to (n-1,n-1) that minimizes this maximum elevation.
#
#   Dijkstra's algorithm works here because:
#   - We always expand the cell with the minimum "cost so far" (max elevation)
#   - Once we reach a cell, we've found the optimal way to reach it
#   - The min-heap ensures we process cells in order of their best reachable time
#
# Algorithm:
#   - Start with (max_elevation=grid[0][0], row=0, col=0) in min-heap
#   - Pop minimum, mark visited, update neighbors
#   - For each neighbor, the time to reach it is max(current_time, neighbor_elevation)
#   - Stop when we reach (n-1, n-1)
# ============================================================================
class SolutionDijkstra:
    """
    Modified Dijkstra finding the path that minimizes maximum elevation.

    Unlike standard Dijkstra which sums edge weights, here we track the
    maximum elevation seen along the path. This works because the time
    needed equals the maximum elevation on our chosen path.
    """

    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)

        # Directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # Min-heap: (time_to_reach, row, col)
        # time_to_reach = max elevation seen on path to this cell
        heap = [(grid[0][0], 0, 0)]
        visited = [[False] * n for _ in range(n)]

        while heap:
            time, row, col = heapq.heappop(heap)

            # Skip if already visited
            if visited[row][col]:
                continue
            visited[row][col] = True

            # Reached destination
            if row == n - 1 and col == n - 1:
                return time

            # Explore neighbors
            for dr, dc in directions:
                nr, nc = row + dr, col + dc

                if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc]:
                    # Time to reach neighbor = max of current time and neighbor's elevation
                    new_time = max(time, grid[nr][nc])
                    heapq.heappush(heap, (new_time, nr, nc))

        return -1  # Should never reach here for valid input


# ============================================================================
# Solution 2: Binary Search + BFS
# Time: O(n^2 log(n^2)), Space: O(n^2)
#
# Key Insight:
#   The answer has a monotonic property: if we can reach the destination at
#   time T, we can also reach it at any time T' > T. This allows binary search.
#
#   Binary search on the time value, and for each candidate time, use BFS/DFS
#   to check if we can reach (n-1, n-1) from (0, 0) using only cells with
#   elevation <= T.
#
# Algorithm:
#   - Binary search T in range [max(grid[0][0], grid[n-1][n-1]), n^2-1]
#   - For each T, BFS to check if path exists using cells with elevation <= T
#   - Find minimum T where path exists
# ============================================================================
class SolutionBinarySearch:
    """
    Binary search on time combined with BFS reachability check.

    We leverage the monotonic property: if reachable at time T, then
    reachable at all times > T. Binary search finds the minimum T.
    """

    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        def can_reach(max_time: int) -> bool:
            """Check if we can reach (n-1, n-1) using cells with elevation <= max_time."""
            if grid[0][0] > max_time:
                return False

            visited = [[False] * n for _ in range(n)]
            queue = [(0, 0)]
            visited[0][0] = True

            while queue:
                row, col = queue.pop()

                if row == n - 1 and col == n - 1:
                    return True

                for dr, dc in directions:
                    nr, nc = row + dr, col + dc

                    if (0 <= nr < n and 0 <= nc < n and
                        not visited[nr][nc] and grid[nr][nc] <= max_time):
                        visited[nr][nc] = True
                        queue.append((nr, nc))

            return False

        # Binary search on time
        # Minimum possible: must be at least max of start and end elevations
        # Maximum possible: n^2 - 1 (largest elevation in grid)
        left = max(grid[0][0], grid[n-1][n-1])
        right = n * n - 1

        while left < right:
            mid = (left + right) // 2

            if can_reach(mid):
                right = mid  # Try smaller time
            else:
                left = mid + 1  # Need more time

        return left


# ============================================================================
# Solution 3: Union-Find (Kruskal-like approach)
# Time: O(n^2 log n) for sorting, O(n^2 * α(n^2)) for union-find operations
# Space: O(n^2)
#
# Key Insight:
#   Process cells in order of increasing elevation. At each step, union the
#   current cell with its already-processed neighbors. The answer is the
#   elevation of the cell when (0,0) and (n-1,n-1) become connected.
#
# Algorithm:
#   - Create list of (elevation, row, col) for all cells, sort by elevation
#   - Process cells in order, unioning with neighbors that have been processed
#   - Stop when start and end are in the same connected component
# ============================================================================
class SolutionUnionFind:
    """
    Union-Find approach processing cells by elevation.

    This is similar to Kruskal's MST algorithm. We process cells from
    lowest to highest elevation, connecting them to already-processed
    neighbors. The moment start and end connect gives our answer.
    """

    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # Union-Find with path compression and union by rank
        parent = list(range(n * n))
        rank = [0] * (n * n)

        def find(x: int) -> int:
            if parent[x] != x:
                parent[x] = find(parent[x])  # Path compression
            return parent[x]

        def union(x: int, y: int) -> None:
            px, py = find(x), find(y)
            if px == py:
                return
            # Union by rank
            if rank[px] < rank[py]:
                px, py = py, px
            parent[py] = px
            if rank[px] == rank[py]:
                rank[px] += 1

        def cell_id(row: int, col: int) -> int:
            return row * n + col

        # Create sorted list of cells by elevation
        cells = []
        for i in range(n):
            for j in range(n):
                cells.append((grid[i][j], i, j))
        cells.sort()

        # Track which cells have been processed
        processed = [[False] * n for _ in range(n)]

        start_id = cell_id(0, 0)
        end_id = cell_id(n - 1, n - 1)

        for elevation, row, col in cells:
            processed[row][col] = True

            # Union with already-processed neighbors
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if 0 <= nr < n and 0 <= nc < n and processed[nr][nc]:
                    union(cell_id(row, col), cell_id(nr, nc))

            # Check if start and end are connected
            if find(start_id) == find(end_id):
                return elevation

        return -1  # Should never reach here


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: grid as JSON 2D array

    Example:
        [[0,2],[1,3]]
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')

    grid = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.swimInWater(grid)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
