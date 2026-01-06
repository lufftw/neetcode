## Variant: Minimum Cost to Make Valid Path (LeetCode 1368)

> **Problem**: Modify minimum arrows to create path from (0,0) to (m-1,n-1).
> **Delta from Base**: 0-1 BFS - edges cost 0 (follow arrow) or 1 (change arrow).
> **Role**: Demonstrates 0-1 BFS optimization.

### Problem Statement

Given a grid where each cell has an arrow (1=right, 2=left, 3=down, 4=up), find minimum cost to modify arrows to create a valid path from top-left to bottom-right. Modifying an arrow costs 1.

### Key Insight

**0-1 BFS**: When edge weights are only 0 or 1:
- Use deque instead of heap
- Add cost-0 edges to **front** of deque
- Add cost-1 edges to **back** of deque
- This maintains sorted order without heap overhead!

```
Edge cost = 0 if following current arrow direction
Edge cost = 1 if changing arrow direction
```

### Implementation

```python
class Solution:
    def minCost(self, grid: List[List[int]]) -> int:
        """
        0-1 BFS: Deque-based shortest path for binary edge weights.

        Time: O(mn)
        Space: O(mn)
        """
        from collections import deque

        rows, cols = len(grid), len(grid[0])

        # Direction mapping: 1=right, 2=left, 3=down, 4=up
        directions = {
            1: (0, 1),   # right
            2: (0, -1),  # left
            3: (1, 0),   # down
            4: (-1, 0)   # up
        }
        all_dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        dir_to_num = {(0, 1): 1, (0, -1): 2, (1, 0): 3, (-1, 0): 4}

        dist = [[float('inf')] * cols for _ in range(rows)]
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

        return dist[rows - 1][cols - 1]
```

### Why 0-1 BFS Works

```
Regular BFS queue:        0-1 BFS deque:
  [3, 4, 5, 6]             [3, 3, 4, 4, 5]
                            ↑ cost-0 edges added here
                                        ↑ cost-1 edges added here
```

The deque maintains the invariant that elements are sorted by cost!

### Key Difference from Base

| Aspect | Network Delay (Base) | 0-1 BFS |
|--------|---------------------|---------|
| Edge weights | Any non-negative | Only 0 or 1 |
| Data structure | Heap O(log n) | Deque O(1) |
| Complexity | O(E log V) | O(V + E) |

### Complexity Analysis

| Metric | Value |
|--------|-------|
| Time | O(mn) |
| Space | O(mn) |

---
