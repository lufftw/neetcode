## Rotting Oranges (LeetCode 994)

> **Problem**: Find minimum time for all oranges to rot (multi-source BFS).
> **Pattern**: Multi-source BFS for simultaneous propagation
> **Key Insight**: All rotten oranges spread simultaneously each minute.

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "minimum time/minutes" | → BFS level = time |
| "spread simultaneously" | → Multi-source BFS |
| "propagation from multiple sources" | → Initialize queue with all sources |

### Implementation

```python
# Pattern: graph_bfs_multi_source
# See: docs/patterns/graph/templates.md Section 4

from collections import deque

class SolutionBFS:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        """
        Find minimum minutes for all oranges to rot using multi-source BFS.

        Key Insight:
        - All rotten oranges spread at the same time (level = minute)
        - BFS naturally processes level by level
        - Initialize queue with ALL rotten oranges (multi-source)
        - Each BFS level = 1 minute of spreading

        Why BFS, not DFS?
        - BFS processes by "wavefront" (distance from sources)
        - Each wavefront = 1 minute
        - Time = number of wavefronts = BFS depth
        """
        if not grid or not grid[0]:
            return -1

        rows, cols = len(grid), len(grid[0])
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        # Initialize: find all rotten oranges and count fresh
        queue: deque[tuple[int, int]] = deque()
        fresh_count = 0

        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 2:
                    queue.append((row, col))
                elif grid[row][col] == 1:
                    fresh_count += 1

        # Edge case: no fresh oranges
        if fresh_count == 0:
            return 0

        minutes = 0

        # Multi-source BFS: process level by level
        while queue:
            minutes += 1
            level_size = len(queue)

            for _ in range(level_size):
                row, col = queue.popleft()

                for dr, dc in directions:
                    nr, nc = row + dr, col + dc

                    # Check bounds and if fresh orange
                    if (0 <= nr < rows and 0 <= nc < cols and
                        grid[nr][nc] == 1):
                        # Rot the orange
                        grid[nr][nc] = 2
                        fresh_count -= 1
                        queue.append((nr, nc))

        # Check if all oranges rotted
        return minutes - 1 if fresh_count == 0 else -1
```

### Trace Example

```
Initial grid:
  2 1 1
  1 1 0
  0 1 1

Minute 0: Queue = [(0,0)]
  Fresh count = 6

Minute 1: Process (0,0), rot neighbors
  2 2 1
  2 1 0
  0 1 1
  Queue = [(0,1), (1,0)]
  Fresh = 4

Minute 2: Process (0,1), (1,0)
  2 2 2
  2 2 0
  0 1 1
  Queue = [(0,2), (1,1)]
  Fresh = 2

Minute 3: Process (0,2), (1,1)
  2 2 2
  2 2 0
  0 2 1
  Queue = [(2,1)]
  Fresh = 1

Minute 4: Process (2,1)
  2 2 2
  2 2 0
  0 2 2
  Queue = [(2,2)]
  Fresh = 0

Result: 4 minutes
```

### Edge Cases

```python
# Case 1: Fresh orange unreachable
#   2 1 1
#   0 1 1
#   1 0 1   ← (2,0) is isolated
# Return: -1

# Case 2: No fresh oranges
#   2 2 2
#   0 2 0
# Return: 0

# Case 3: All fresh oranges adjacent to rotten
#   2 1
#   1 2
# Return: 1
```

### Why -1 at the End?

```python
# After BFS completes:
# - minutes counted from 1 (first spreading)
# - But initial state is minute 0
# - Need to subtract 1 from final count

# Alternative: Start minutes = -1, increment before processing
minutes = -1
while queue:
    minutes += 1
    # process level...
```

### Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(m × n) - each cell visited once |
| Space | O(m × n) - worst case all oranges in queue |


