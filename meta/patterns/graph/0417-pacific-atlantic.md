## Pacific Atlantic Water Flow (LeetCode 417)

> **Problem**: Find cells that can flow to both Pacific and Atlantic oceans.
> **Pattern**: Multi-source BFS/DFS from ocean borders
> **Key Insight**: Reverse the flow direction - find cells reachable FROM ocean.

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "flow from multiple sources" | → Multi-source BFS |
| "reach both destinations" | → Intersection of two reachability sets |
| "reverse direction" | → Start from destination, not source |

### Implementation

```python
# Pattern: graph_bfs_multi_source
# See: docs/patterns/graph/templates.md Section 3

from collections import deque

class SolutionBFS:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        """
        Find cells that can reach both oceans using reverse BFS.

        Key Insight:
        - Forward: Check if water from cell reaches ocean (complex)
        - Reverse: Check if ocean can reach cell going UPHILL (simpler)

        Why reverse direction?
        - Ocean borders are known sources
        - Multi-source BFS finds all reachable cells efficiently
        - Intersection gives cells reaching both oceans
        """
        if not heights or not heights[0]:
            return []

        rows, cols = len(heights), len(heights[0])
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        def bfs(sources: list[tuple[int, int]]) -> set[tuple[int, int]]:
            """Multi-source BFS to find all reachable cells."""
            reachable: set[tuple[int, int]] = set(sources)
            queue: deque[tuple[int, int]] = deque(sources)

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

        # Return intersection
        return list(pacific_reach & atlantic_reach)
```

### Trace Example

```
Heights:
  1 2 2 3 5   (Pacific top)
  3 2 3 4 4
  2 4 5 3 1
  6 7 1 4 5
  5 1 1 2 4   (Atlantic bottom)
  P         A
  (left)    (right)

Pacific reachable (going uphill from ocean):
  ✓ ✓ ✓ ✓ ✓
  ✓ ✓ ✓ ✓ ✓
  ✓ ✓ ✓ . .
  ✓ ✓ . . .
  ✓ . . . .

Atlantic reachable:
  . . . ✓ ✓
  . . . ✓ ✓
  . ✓ ✓ ✓ ✓
  ✓ ✓ ✓ ✓ ✓
  ✓ ✓ ✓ ✓ ✓

Intersection (both oceans):
  [[0,4], [1,3], [1,4], [2,2], [3,0], [3,1], [4,0]]
```

### DFS Alternative

```python
class SolutionDFS:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        """DFS approach - recursive from ocean borders."""
        if not heights:
            return []

        rows, cols = len(heights), len(heights[0])
        pacific: set[tuple[int, int]] = set()
        atlantic: set[tuple[int, int]] = set()

        def dfs(row: int, col: int, reachable: set, prev_height: int) -> None:
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

        return list(pacific & atlantic)
```

### Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(m × n) - each cell visited at most twice |
| Space | O(m × n) for reachable sets |


