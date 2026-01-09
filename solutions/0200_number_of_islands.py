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
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Number of Islands solution."""
    import json
    import copy

    # Parse input
    grid = json.loads(input_data.strip())

    # If expected is available, compare directly
    if expected is not None:
        return actual == expected

    # Judge-only mode: compute expected using reference solution
    grid_copy = copy.deepcopy(grid)
    expected_count = _count_islands(grid_copy)
    return actual == expected_count


def _count_islands(grid):
    """Reference solution for validation."""
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return
        grid[r][c] = '0'
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)

    return count


JUDGE_FUNC = judge


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
    "dfs": {
        "class": "SolutionDFS",
        "method": "numIslands",
        "complexity": "O(m*n) time, O(m*n) space",
        "description": "DFS flood fill, recursive exploration",
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
    "union_find": {
        "class": "SolutionUnionFind",
        "method": "numIslands",
        "complexity": "O(m*n * α(m*n)) time, O(m*n) space",
        "description": "Union-Find (DSU) for connected components",
        "api_kernels": ["UnionFind"],
        "patterns": ["union_find_connected_components"],
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
        """
        Count number of islands in a 2D grid.

        Core insight: Each unvisited '1' starts a new island. Use DFS flood fill
        to mark all connected land cells as visited (sink them to '0'). Count
        how many times we initiate a new DFS.

        Invariant: After processing cell (r, c), all land cells connected to it
        have been marked '0'; island_count equals number of distinct islands
        discovered so far.

        Args:
            grid: 2D grid of '0' (water) and '1' (land)

        Returns:
            Number of islands (connected land components)
        """
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


# ============================================
# Solution 3: Union-Find (Disjoint Set Union)
# Time: O(m * n * α(m*n)), Space: O(m * n)
#   - α is inverse Ackermann, effectively O(1)
#   - Classic DSU pattern for connected components
#   - Does not modify input grid
# ============================================
class SolutionUnionFind:
    def numIslands(self, grid: List[List[str]]) -> int:
        """
        Count islands using Union-Find (Disjoint Set Union).

        Core insight: Model each land cell as a node. Union adjacent land cells.
        Final count of disjoint sets = number of islands.

        Key advantage: Does not modify input grid. Also foundation for
        dynamic connectivity problems (e.g., adding/removing edges).

        Args:
            grid: 2D grid of '0' (water) and '1' (land)

        Returns:
            Number of islands (connected components of land)
        """
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])

        # Union-Find data structure
        parent = {}
        rank = {}

        def find(x: int) -> int:
            """Find root with path compression."""
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x: int, y: int) -> None:
            """Union by rank."""
            root_x, root_y = find(x), find(y)
            if root_x == root_y:
                return
            # Attach smaller tree under larger tree
            if rank[root_x] < rank[root_y]:
                parent[root_x] = root_y
            elif rank[root_x] > rank[root_y]:
                parent[root_y] = root_x
            else:
                parent[root_y] = root_x
                rank[root_x] += 1

        # Initialize: each land cell is its own component
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1':
                    idx = r * cols + c
                    parent[idx] = idx
                    rank[idx] = 0

        # Union adjacent land cells (only right and down to avoid duplicates)
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1':
                    idx = r * cols + c
                    # Check right neighbor
                    if c + 1 < cols and grid[r][c + 1] == '1':
                        union(idx, idx + 1)
                    # Check down neighbor
                    if r + 1 < rows and grid[r + 1][c] == '1':
                        union(idx, idx + cols)

        # Count distinct roots (connected components)
        roots = set(find(idx) for idx in parent)
        return len(roots)


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
