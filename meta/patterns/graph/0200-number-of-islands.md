## Base Template: Number of Islands (LeetCode 200)

> **Problem**: Count the number of islands in a 2D binary grid.
> **Invariant**: Each DFS marks all cells of one island as visited.
> **Role**: BASE TEMPLATE for connected components on grid.

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "count islands/regions" | → Connected components with DFS/BFS |
| "2D grid" | → Grid as implicit graph |
| "connected 4-directionally" | → 4-directional neighbors |

### Implementation

```python
# Pattern: graph_dfs_connected_components
# See: docs/patterns/graph/templates.md Section 1 (Base Template)

class SolutionDFS:
    def numIslands(self, grid: List[List[str]]) -> int:
        """
        Count islands using DFS to mark connected land cells.

        Key Insight:
        - Each unvisited '1' starts a new island
        - DFS from that cell marks all connected '1's as visited
        - Number of DFS calls = number of islands

        Why mark in-place?
        - Change '1' to '0' to mark as visited
        - Avoids separate visited set (saves space)
        - Alternatively, use visited set if grid shouldn't be modified
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
```

### Trace Example

```
Input grid:
  1 1 0 0 0
  1 1 0 0 0
  0 0 1 0 0
  0 0 0 1 1

Step 1: Start at (0,0), DFS marks island 1:
  0 0 0 0 0
  0 0 0 0 0
  0 0 1 0 0
  0 0 0 1 1
  island_count = 1

Step 2: Find (2,2), DFS marks island 2:
  0 0 0 0 0
  0 0 0 0 0
  0 0 0 0 0
  0 0 0 1 1
  island_count = 2

Step 3: Find (3,3), DFS marks island 3:
  0 0 0 0 0
  0 0 0 0 0
  0 0 0 0 0
  0 0 0 0 0
  island_count = 3

Result: 3 islands
```

### BFS Alternative

```python
from collections import deque

class SolutionBFS:
    def numIslands(self, grid: List[List[str]]) -> int:
        """BFS approach - iterative, uses explicit queue."""
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
```

### Complexity Analysis

| Approach | Time | Space |
|----------|------|-------|
| DFS | O(m × n) | O(m × n) recursion stack worst case |
| BFS | O(m × n) | O(min(m, n)) queue size |

### Related Problems

| Problem | Variation |
|---------|-----------|
| LC 695: Max Area of Island | Track area during DFS |
| LC 463: Island Perimeter | Count boundary edges |
| LC 827: Making A Large Island | Try flipping each 0 |


