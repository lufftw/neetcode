## Variant: Minimum Obstacle Removal (LeetCode 2290)

> **Problem**: Find path removing minimum obstacles from (0,0) to (m-1,n-1).
> **Delta from Base**: Another 0-1 BFS problem; cost = cell value (0 or 1).
> **Role**: Reinforces 0-1 BFS pattern.

### Problem Statement

Given a grid where 0 = empty cell, 1 = obstacle, find minimum number of obstacles to remove to create a path from top-left to bottom-right.

### Key Insight

This is a cleaner 0-1 BFS example:
- Moving to empty cell (0) costs 0
- Moving to obstacle (1) costs 1 (removing it)

### Implementation

```python
class Solution:
    def minimumObstacles(self, grid: List[List[int]]) -> int:
        """
        0-1 BFS: Cost = grid value (0 for empty, 1 for obstacle).

        Time: O(mn)
        Space: O(mn)
        """
        from collections import deque

        rows, cols = len(grid), len(grid[0])

        dist = [[float('inf')] * cols for _ in range(rows)]
        dist[0][0] = 0

        dq: Deque[Tuple[int, int, int]] = deque([(0, 0, 0)])  # (cost, row, col)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while dq:
            cost, r, c = dq.popleft()

            if cost > dist[r][c]:
                continue

            if r == rows - 1 and c == cols - 1:
                return cost

            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                if 0 <= nr < rows and 0 <= nc < cols:
                    # Cost to enter cell = grid value (0 or 1)
                    new_cost = cost + grid[nr][nc]

                    if new_cost < dist[nr][nc]:
                        dist[nr][nc] = new_cost

                        if grid[nr][nc] == 0:
                            dq.appendleft((new_cost, nr, nc))  # Free move: front
                        else:
                            dq.append((new_cost, nr, nc))      # Remove obstacle: back

        return dist[rows - 1][cols - 1]
```

### Comparison: Dijkstra vs 0-1 BFS

```python
# Dijkstra approach (works but slower)
def dijkstra_version(grid):
    pq = [(0, 0, 0)]  # heap
    while pq:
        cost, r, c = heappop(pq)  # O(log n)
        ...
        heappush(pq, (new_cost, nr, nc))  # O(log n)

# 0-1 BFS approach (optimal)
def bfs_01_version(grid):
    dq = deque([(0, 0, 0)])  # deque
    while dq:
        cost, r, c = dq.popleft()  # O(1)
        ...
        if cost == 0:
            dq.appendleft(...)  # O(1)
        else:
            dq.append(...)  # O(1)
```

### Template: 0-1 BFS

```python
def bfs_01(grid):
    """
    0-1 BFS template for binary edge weights.
    """
    from collections import deque

    rows, cols = len(grid), len(grid[0])
    dist = [[float('inf')] * cols for _ in range(rows)]
    dist[0][0] = 0  # or cost of starting cell

    dq = deque([(initial_cost, 0, 0)])

    while dq:
        cost, r, c = dq.popleft()

        if cost > dist[r][c]:
            continue

        for nr, nc in neighbors(r, c):
            edge_cost = get_edge_cost(r, c, nr, nc)  # 0 or 1
            new_cost = cost + edge_cost

            if new_cost < dist[nr][nc]:
                dist[nr][nc] = new_cost
                if edge_cost == 0:
                    dq.appendleft((new_cost, nr, nc))
                else:
                    dq.append((new_cost, nr, nc))

    return dist[target_r][target_c]
```

### Complexity Analysis

| Metric | Value |
|--------|-------|
| Time | O(mn) |
| Space | O(mn) |

---
