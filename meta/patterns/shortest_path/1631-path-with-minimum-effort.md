## Variant: Path With Minimum Effort (LeetCode 1631)

> **Problem**: Find path minimizing maximum absolute difference between adjacent cells.
> **Delta from Base**: Edge weight = height difference; minimize MAX edge, not SUM.
> **Role**: Demonstrates Dijkstra with minimax objective.

### Problem Statement

You are given a 2D grid of heights. Find a path from top-left to bottom-right minimizing the **maximum absolute difference** in heights between consecutive cells.

### Key Insight

**Minimax shortest path**: Instead of summing edge weights, we track the maximum edge weight on the path.

```
dist[node] = min over all paths of (max edge weight on path)
```

Dijkstra still works because:
- Priority = maximum edge so far (want to minimize)
- Once we reach a node, we've found the path with minimum "effort"

### Implementation

```python
class Solution:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        """
        Dijkstra's algorithm with minimax objective.

        Key change: dist[node] = min(max edge weight on any path to node)

        Time: O(mn log(mn))
        Space: O(mn)
        """
        from heapq import heappush, heappop

        rows, cols = len(heights), len(heights[0])

        # dist[r][c] = minimum effort to reach (r, c)
        dist = [[float('inf')] * cols for _ in range(rows)]
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

        return dist[rows - 1][cols - 1]
```

### Key Difference from Base

| Aspect | Network Delay (Base) | Minimum Effort |
|--------|---------------------|----------------|
| Objective | Minimize sum | Minimize max |
| Relaxation | `d + weight` | `max(d, weight)` |
| Graph | Explicit edges | Implicit grid |

### Complexity Analysis

| Metric | Value |
|--------|-------|
| Time | O(mn log(mn)) |
| Space | O(mn) |

---
