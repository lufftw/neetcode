## Quick Reference Templates

### Template 1: Dijkstra's Algorithm

```python
def dijkstra(n: int, edges: List[Tuple[int, int, int]], src: int) -> List[int]:
    """
    Single-source shortest paths with non-negative weights.
    edges: List of (from, to, weight)

    Returns:
        dist[i] = shortest distance from src to i (-1 if unreachable)
    """
    from heapq import heappush, heappop
    from collections import defaultdict

    graph: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))

    dist: List[int] = [float('inf')] * n
    dist[src] = 0
    pq: List[Tuple[int, int]] = [(0, src)]  # (distance, node)

    while pq:
        d, node = heappop(pq)

        if d > dist[node]:
            continue  # Already found better path

        for neighbor, weight in graph[node]:
            new_dist = d + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heappush(pq, (new_dist, neighbor))

    return [d if d != float('inf') else -1 for d in dist]
```

### Template 2: 0-1 BFS

```python
def bfs_01(grid: List[List[int]], start: Tuple[int, int],
           end: Tuple[int, int]) -> int:
    """
    Shortest path with binary edge weights (0 or 1).

    Returns:
        Minimum cost from start to end, or -1 if unreachable.
    """
    from collections import deque

    rows, cols = len(grid), len(grid[0])
    sr, sc = start
    er, ec = end

    dist = [[float('inf')] * cols for _ in range(rows)]
    dist[sr][sc] = 0

    dq: Deque[Tuple[int, int, int]] = deque([(0, sr, sc)])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while dq:
        cost, r, c = dq.popleft()

        if cost > dist[r][c]:
            continue

        if r == er and c == ec:
            return cost

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                # Define edge_cost based on problem
                edge_cost = grid[nr][nc]  # or custom logic
                new_cost = cost + edge_cost

                if new_cost < dist[nr][nc]:
                    dist[nr][nc] = new_cost
                    if edge_cost == 0:
                        dq.appendleft((new_cost, nr, nc))
                    else:
                        dq.append((new_cost, nr, nc))

    return -1 if dist[er][ec] == float('inf') else dist[er][ec]
```

### Template 3: Bellman-Ford (K iterations)

```python
def bellman_ford_k(n: int, edges: List[Tuple[int, int, int]],
                   src: int, k: int) -> List[int]:
    """
    Shortest paths with at most k edges.
    edges: List of (from, to, weight)

    Returns:
        dist[i] = shortest distance from src to i using <= k edges
    """
    INF = float('inf')
    dist = [INF] * n
    dist[src] = 0

    for _ in range(k):
        new_dist = dist.copy()
        for u, v, w in edges:
            if dist[u] != INF:
                new_dist[v] = min(new_dist[v], dist[u] + w)
        dist = new_dist

    return [d if d != INF else -1 for d in dist]
```

### Template 4: Minimax Dijkstra

```python
def dijkstra_minimax(grid: List[List[int]]) -> int:
    """
    Find path minimizing the maximum edge weight.

    Returns:
        Minimum possible maximum edge weight from (0,0) to (m-1,n-1)
    """
    from heapq import heappush, heappop

    rows, cols = len(grid), len(grid[0])
    dist = [[float('inf')] * cols for _ in range(rows)]
    dist[0][0] = 0

    pq: List[Tuple[int, int, int]] = [(0, 0, 0)]  # (max_weight, row, col)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while pq:
        max_w, r, c = heappop(pq)

        if max_w > dist[r][c]:
            continue

        if r == rows - 1 and c == cols - 1:
            return max_w

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                edge_weight = abs(grid[nr][nc] - grid[r][c])
                new_max = max(max_w, edge_weight)

                if new_max < dist[nr][nc]:
                    dist[nr][nc] = new_max
                    heappush(pq, (new_max, nr, nc))

    return dist[rows - 1][cols - 1]
```

### Complexity Summary

| Algorithm | Time | Space |
|-----------|------|-------|
| Dijkstra | O((V + E) log V) | O(V + E) |
| 0-1 BFS | O(V + E) | O(V) |
| Bellman-Ford (full) | O(V × E) | O(V) |
| Bellman-Ford (K iter) | O(K × E) | O(V) |
| Minimax Dijkstra | O((V + E) log V) | O(V) |

---
