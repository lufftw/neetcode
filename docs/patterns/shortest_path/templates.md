# Shortest Path Patterns

> **API Kernel**: `ShortestPath`
>
> **Core Mechanism**: Find minimum-cost path in weighted graphs using priority-based exploration.

## Table of Contents

1. [Pattern Overview](#1-pattern-overview)
2. [Base Template: Network Delay Time (LeetCode 743)](#2-base-template-network-delay-time-leetcode-743)
3. [Variant: Path With Minimum Effort (LeetCode 1631)](#3-variant-path-with-minimum-effort-leetcode-1631)
4. [Variant: Cheapest Flights Within K Stops (LeetCode 787)](#4-variant-cheapest-flights-within-k-stops-leetcode-787)
5. [Variant: Minimum Cost to Make Valid Path (LeetCode 1368)](#5-variant-minimum-cost-to-make-valid-path-leetcode-1368)
6. [Variant: Minimum Obstacle Removal (LeetCode 2290)](#6-variant-minimum-obstacle-removal-leetcode-2290)
7. [Pattern Comparison](#7-pattern-comparison)
8. [Decision Guide: When to Use Shortest Path Algorithms](#8-decision-guide-when-to-use-shortest-path-algorithms)
9. [Quick Reference Templates](#9-quick-reference-templates)

---

## 1. Pattern Overview

Shortest path algorithms find the minimum-cost route between nodes in a graph. The choice of algorithm depends on edge weights and constraints.

### 1.1 Algorithm Family

| Algorithm | Edge Weights | Best For |
|-----------|--------------|----------|
| **Dijkstra** | Non-negative | General weighted graphs |
| **0-1 BFS** | Only 0 or 1 | Binary edge weights |
| **Bellman-Ford** | Any (including negative) | Negative edges, limited steps |
| **BFS** | Unweighted (all = 1) | Unit cost graphs |

### 1.2 Universal Template Structure

```python
def shortest_path(graph, start, end):
    """
    Generic shortest path framework.

    Components:
    1. Distance array: dist[node] = minimum cost to reach node
    2. Priority structure: heap (Dijkstra) or deque (0-1 BFS)
    3. Relaxation: if new_cost < dist[neighbor], update
    """
    dist = {start: 0}  # or [inf] * n with dist[start] = 0
    pq = [(0, start)]  # (cost, node)

    while pq:
        cost, node = heappop(pq)

        if cost > dist.get(node, inf):
            continue  # Already found better path

        if node == end:
            return cost

        for neighbor, weight in graph[node]:
            new_cost = cost + weight
            if new_cost < dist.get(neighbor, inf):
                dist[neighbor] = new_cost
                heappush(pq, (new_cost, neighbor))

    return -1  # Unreachable
```

### 1.3 Key Invariant

> **At each step, the node with minimum distance is finalized (for non-negative weights).**

This greedy property is why Dijkstra works: once we pop a node from the heap, we've found its shortest path.

---

## 2. Base Template: Network Delay Time (LeetCode 743)

> **Problem**: Find time for signal to reach all nodes from source.
> **Pattern**: Classic Dijkstra's algorithm.
> **Role**: BASE TEMPLATE for shortest path patterns.

### 2.1 Problem Statement

You are given a network of `n` nodes labeled from `1` to `n`. You are given `times`, where `times[i] = (ui, vi, wi)` represents a directed edge from `ui` to `vi` with time `wi`.

Send a signal from node `k`. Return the minimum time for all nodes to receive the signal. Return `-1` if impossible.

### 2.2 Key Insight

This is the **canonical Dijkstra problem**:
- Find shortest paths from source to ALL nodes
- Answer = maximum of all shortest paths (time for last node to receive)

### 2.3 Implementation

```python
class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        """
        Dijkstra's algorithm for single-source shortest paths.

        Time: O((V + E) log V) with binary heap
        Space: O(V + E)
        """
        from heapq import heappush, heappop

        # Build adjacency list
        graph: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
        for u, v, w in times:
            graph[u].append((v, w))

        # Dijkstra's algorithm
        dist: Dict[int, int] = {}
        pq: List[Tuple[int, int]] = [(0, k)]  # (distance, node)

        while pq:
            d, node = heappop(pq)

            if node in dist:
                continue  # Already processed

            dist[node] = d

            for neighbor, weight in graph[node]:
                if neighbor not in dist:
                    heappush(pq, (d + weight, neighbor))

        # Check if all nodes reachable
        if len(dist) != n:
            return -1

        return max(dist.values())
```

### 2.4 Algorithm Trace

```
Input: times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2

Graph:
  2 --1--> 1
  2 --1--> 3 --1--> 4

Dijkstra from node 2:
  Step 1: Pop (0, 2), dist[2] = 0
          Push (1, 1), (1, 3)

  Step 2: Pop (1, 1), dist[1] = 1
          No outgoing edges

  Step 3: Pop (1, 3), dist[3] = 1
          Push (2, 4)

  Step 4: Pop (2, 4), dist[4] = 2

Final: dist = {2: 0, 1: 1, 3: 1, 4: 2}
Answer: max(0, 1, 1, 2) = 2
```

### 2.5 Complexity Analysis

| Metric | Value |
|--------|-------|
| Time | O((V + E) log V) |
| Space | O(V + E) |

---

## 3. Variant: Path With Minimum Effort (LeetCode 1631)

> **Problem**: Find path minimizing maximum absolute difference between adjacent cells.
> **Delta from Base**: Edge weight = height difference; minimize MAX edge, not SUM.
> **Role**: Demonstrates Dijkstra with minimax objective.

### 3.1 Problem Statement

You are given a 2D grid of heights. Find a path from top-left to bottom-right minimizing the **maximum absolute difference** in heights between consecutive cells.

### 3.2 Key Insight

**Minimax shortest path**: Instead of summing edge weights, we track the maximum edge weight on the path.

```
dist[node] = min over all paths of (max edge weight on path)
```

Dijkstra still works because:
- Priority = maximum edge so far (want to minimize)
- Once we reach a node, we've found the path with minimum "effort"

### 3.3 Implementation

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

### 3.4 Key Difference from Base

| Aspect | Network Delay (Base) | Minimum Effort |
|--------|---------------------|----------------|
| Objective | Minimize sum | Minimize max |
| Relaxation | `d + weight` | `max(d, weight)` |
| Graph | Explicit edges | Implicit grid |

### 3.5 Complexity Analysis

| Metric | Value |
|--------|-------|
| Time | O(mn log(mn)) |
| Space | O(mn) |

---

## 4. Variant: Cheapest Flights Within K Stops (LeetCode 787)

> **Problem**: Find cheapest flight path with at most K intermediate stops.
> **Delta from Base**: Add constraint on number of edges (stops).
> **Role**: Demonstrates Bellman-Ford / modified Dijkstra with step limit.

### 4.1 Problem Statement

Find the cheapest price from `src` to `dst` with at most `k` stops. A stop is an intermediate city (not counting source or destination).

### 4.2 Key Insight

Standard Dijkstra doesn't work because:
- A longer path (more stops) might be cheaper
- But we can't take paths with > k stops

**Two approaches:**
1. **Modified Dijkstra**: Track (cost, node, stops_remaining)
2. **Bellman-Ford**: Relax edges k+1 times

### 4.3 Implementation (Modified Dijkstra)

```python
class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]],
                          src: int, dst: int, k: int) -> int:
        """
        Modified Dijkstra with state = (node, stops_used).

        Time: O(E * K * log(E * K))
        Space: O(N * K)
        """
        from heapq import heappush, heappop

        # Build graph
        graph: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
        for u, v, price in flights:
            graph[u].append((v, price))

        # dist[node][stops] = min cost to reach node using exactly stops edges
        # We track minimum cost for each (node, stops) state
        dist: Dict[Tuple[int, int], int] = {}

        # (cost, node, stops_used)
        pq: List[Tuple[int, int, int]] = [(0, src, 0)]

        while pq:
            cost, node, stops = heappop(pq)

            if node == dst:
                return cost

            if stops > k:
                continue  # Too many stops

            if (node, stops) in dist and dist[(node, stops)] <= cost:
                continue

            dist[(node, stops)] = cost

            for neighbor, price in graph[node]:
                new_cost = cost + price
                new_stops = stops + 1

                # Only continue if we haven't found a better path to this state
                if (neighbor, new_stops) not in dist:
                    heappush(pq, (new_cost, neighbor, new_stops))

        return -1
```

### 4.4 Implementation (Bellman-Ford)

```python
class SolutionBellmanFord:
    def findCheapestPrice(self, n: int, flights: List[List[int]],
                          src: int, dst: int, k: int) -> int:
        """
        Bellman-Ford: Relax all edges k+1 times.

        Time: O(K * E)
        Space: O(N)
        """
        INF = float('inf')
        dist = [INF] * n
        dist[src] = 0

        # Relax edges k+1 times (k stops = k+1 edges)
        for _ in range(k + 1):
            # Use copy to avoid using updated values in same iteration
            new_dist = dist.copy()

            for u, v, price in flights:
                if dist[u] != INF:
                    new_dist[v] = min(new_dist[v], dist[u] + price)

            dist = new_dist

        return dist[dst] if dist[dst] != INF else -1
```

### 4.5 Key Difference from Base

| Aspect | Network Delay (Base) | K Stops |
|--------|---------------------|---------|
| State | Just node | (node, stops_used) |
| Termination | All nodes visited | Reach dst or exceed k |
| Algorithm | Pure Dijkstra | Modified Dijkstra or Bellman-Ford |

### 4.6 Complexity Analysis

| Algorithm | Time | Space |
|-----------|------|-------|
| Modified Dijkstra | O(EK log(EK)) | O(NK) |
| Bellman-Ford | O(KE) | O(N) |

---

## 5. Variant: Minimum Cost to Make Valid Path (LeetCode 1368)

> **Problem**: Modify minimum arrows to create path from (0,0) to (m-1,n-1).
> **Delta from Base**: 0-1 BFS - edges cost 0 (follow arrow) or 1 (change arrow).
> **Role**: Demonstrates 0-1 BFS optimization.

### 5.1 Problem Statement

Given a grid where each cell has an arrow (1=right, 2=left, 3=down, 4=up), find minimum cost to modify arrows to create a valid path from top-left to bottom-right. Modifying an arrow costs 1.

### 5.2 Key Insight

**0-1 BFS**: When edge weights are only 0 or 1:
- Use deque instead of heap
- Add cost-0 edges to **front** of deque
- Add cost-1 edges to **back** of deque
- This maintains sorted order without heap overhead!

```
Edge cost = 0 if following current arrow direction
Edge cost = 1 if changing arrow direction
```

### 5.3 Implementation

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

### 5.4 Why 0-1 BFS Works

```
Regular BFS queue:        0-1 BFS deque:
  [3, 4, 5, 6]             [3, 3, 4, 4, 5]
                            ↑ cost-0 edges added here
                                        ↑ cost-1 edges added here
```

The deque maintains the invariant that elements are sorted by cost!

### 5.5 Key Difference from Base

| Aspect | Network Delay (Base) | 0-1 BFS |
|--------|---------------------|---------|
| Edge weights | Any non-negative | Only 0 or 1 |
| Data structure | Heap O(log n) | Deque O(1) |
| Complexity | O(E log V) | O(V + E) |

### 5.6 Complexity Analysis

| Metric | Value |
|--------|-------|
| Time | O(mn) |
| Space | O(mn) |

---

## 6. Variant: Minimum Obstacle Removal (LeetCode 2290)

> **Problem**: Find path removing minimum obstacles from (0,0) to (m-1,n-1).
> **Delta from Base**: Another 0-1 BFS problem; cost = cell value (0 or 1).
> **Role**: Reinforces 0-1 BFS pattern.

### 6.1 Problem Statement

Given a grid where 0 = empty cell, 1 = obstacle, find minimum number of obstacles to remove to create a path from top-left to bottom-right.

### 6.2 Key Insight

This is a cleaner 0-1 BFS example:
- Moving to empty cell (0) costs 0
- Moving to obstacle (1) costs 1 (removing it)

### 6.3 Implementation

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

### 6.4 Comparison: Dijkstra vs 0-1 BFS

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

### 6.5 Template: 0-1 BFS

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

### 6.6 Complexity Analysis

| Metric | Value |
|--------|-------|
| Time | O(mn) |
| Space | O(mn) |

---

## 7. Pattern Comparison

### 7.1 Algorithm Selection Guide

| Problem Type | Algorithm | Time | When to Use |
|--------------|-----------|------|-------------|
| General weighted | Dijkstra | O((V+E) log V) | Non-negative weights |
| Binary weights (0/1) | 0-1 BFS | O(V + E) | Weights only 0 or 1 |
| Limited steps/edges | Bellman-Ford | O(K × E) | Need to limit path length |
| Unweighted | BFS | O(V + E) | All edges cost 1 |
| Negative edges | Bellman-Ford | O(V × E) | Negative weights present |

### 7.2 Problem Variant Comparison

| Problem | Edge Weight | Objective | Special Constraint |
|---------|-------------|-----------|-------------------|
| LC 743 | Given | Min sum to all | None |
| LC 1631 | Height diff | Min max edge | Implicit grid graph |
| LC 787 | Given | Min sum to dst | At most K stops |
| LC 1368 | 0 or 1 | Min sum | 0-1 BFS applicable |
| LC 2290 | 0 or 1 | Min sum | 0-1 BFS applicable |

### 7.3 Implementation Patterns

```
Dijkstra (LC 743):
├── Data structure: Min-heap
├── State: (cost, node)
├── Relaxation: new_cost = cost + weight
└── Complexity: O((V+E) log V)

Minimax Dijkstra (LC 1631):
├── Data structure: Min-heap
├── State: (max_effort, row, col)
├── Relaxation: new_effort = max(effort, edge_weight)
└── Complexity: O((V+E) log V)

Modified Dijkstra with K (LC 787):
├── Data structure: Min-heap
├── State: (cost, node, stops_used)
├── Relaxation: new_cost = cost + weight, stops + 1
└── Complexity: O(EK log(EK))

0-1 BFS (LC 1368, 2290):
├── Data structure: Deque
├── State: (cost, row, col)
├── Relaxation: cost-0 → front, cost-1 → back
└── Complexity: O(V + E)
```

---

## 8. Decision Guide: When to Use Shortest Path Algorithms

### 8.1 Pattern Recognition Signals

Use Shortest Path when you see:

| Signal | Example Phrases |
|--------|-----------------|
| **Minimum cost/time** | "shortest time", "minimum cost", "cheapest" |
| **Path in weighted graph** | "edge weights", "travel time", "price" |
| **Grid navigation** | "minimum moves", "reach destination" |
| **Optimization on graph** | "find optimal route", "best path" |

### 8.2 Decision Flowchart

```
Need shortest path in graph?
├── Yes
│   ├── What are the edge weights?
│   │   ├── Unweighted (all = 1)?
│   │   │   └── Use BFS
│   │   ├── Binary (0 or 1)?
│   │   │   └── Use 0-1 BFS (deque)
│   │   ├── Non-negative?
│   │   │   ├── Need to limit path length?
│   │   │   │   ├── Yes → Modified Dijkstra or Bellman-Ford
│   │   │   │   └── No → Dijkstra
│   │   │   └── Minimax objective (minimize max edge)?
│   │   │       └── Dijkstra with max() relaxation
│   │   └── Negative weights?
│   │       └── Bellman-Ford
│   │
│   └── What's the objective?
│       ├── Minimize sum of edges → Standard shortest path
│       ├── Minimize max edge → Minimax Dijkstra
│       └── Count/enumerate paths → DP or DFS
│
└── No → Different pattern (DFS, BFS exploration, etc.)
```

### 8.3 Algorithm Trade-offs

| Algorithm | Pros | Cons |
|-----------|------|------|
| **Dijkstra** | Works for any non-negative weights | O(log V) per operation |
| **0-1 BFS** | O(1) per operation | Only for 0/1 weights |
| **Bellman-Ford** | Handles negative edges, path limit | O(V × E) or O(K × E) |
| **BFS** | Simple, O(1) per operation | Only for unweighted |

### 8.4 Common Pitfalls

1. **Using BFS for weighted graphs**: BFS only works when all edges have equal weight.

2. **Not handling disconnected nodes**: Check if target is reachable.

3. **Wrong priority in 0-1 BFS**: Cost-0 edges go to FRONT, cost-1 to BACK.

4. **Forgetting to skip processed nodes**: In Dijkstra, skip if `cost > dist[node]`.

5. **Using Dijkstra with negative edges**: Will give wrong results; use Bellman-Ford.

### 8.5 Related Patterns

| If you see... | Consider... |
|---------------|-------------|
| Shortest path in DAG | Topological Sort + DP |
| All-pairs shortest path | Floyd-Warshall |
| Longest path in DAG | Negate weights or DP |
| Path with constraints | State-space Dijkstra |
| MST (connect all nodes) | Prim's or Kruskal's |

---

## 9. Quick Reference Templates

### 9.1 Template 1: Dijkstra's Algorithm

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

### 9.2 Template 2: 0-1 BFS

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

### 9.3 Template 3: Bellman-Ford (K iterations)

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

### 9.4 Template 4: Minimax Dijkstra

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

### 9.5 Complexity Summary

| Algorithm | Time | Space |
|-----------|------|-------|
| Dijkstra | O((V + E) log V) | O(V + E) |
| 0-1 BFS | O(V + E) | O(V) |
| Bellman-Ford (full) | O(V × E) | O(V) |
| Bellman-Ford (K iter) | O(K × E) | O(V) |
| Minimax Dijkstra | O((V + E) log V) | O(V) |

---



---



*Document generated for NeetCode Practice Framework — API Kernel: ShortestPath*
