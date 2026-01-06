## Base Template: Network Delay Time (LeetCode 743)

> **Problem**: Find time for signal to reach all nodes from source.
> **Pattern**: Classic Dijkstra's algorithm.
> **Role**: BASE TEMPLATE for shortest path patterns.

### Problem Statement

You are given a network of `n` nodes labeled from `1` to `n`. You are given `times`, where `times[i] = (ui, vi, wi)` represents a directed edge from `ui` to `vi` with time `wi`.

Send a signal from node `k`. Return the minimum time for all nodes to receive the signal. Return `-1` if impossible.

### Key Insight

This is the **canonical Dijkstra problem**:
- Find shortest paths from source to ALL nodes
- Answer = maximum of all shortest paths (time for last node to receive)

### Implementation

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

### Algorithm Trace

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

### Complexity Analysis

| Metric | Value |
|--------|-------|
| Time | O((V + E) log V) |
| Space | O(V + E) |

---
