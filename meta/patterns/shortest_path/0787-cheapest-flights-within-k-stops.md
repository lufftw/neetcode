## Variant: Cheapest Flights Within K Stops (LeetCode 787)

> **Problem**: Find cheapest flight path with at most K intermediate stops.
> **Delta from Base**: Add constraint on number of edges (stops).
> **Role**: Demonstrates Bellman-Ford / modified Dijkstra with step limit.

### Problem Statement

Find the cheapest price from `src` to `dst` with at most `k` stops. A stop is an intermediate city (not counting source or destination).

### Key Insight

Standard Dijkstra doesn't work because:
- A longer path (more stops) might be cheaper
- But we can't take paths with > k stops

**Two approaches:**
1. **Modified Dijkstra**: Track (cost, node, stops_remaining)
2. **Bellman-Ford**: Relax edges k+1 times

### Implementation (Modified Dijkstra)

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

### Implementation (Bellman-Ford)

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

### Key Difference from Base

| Aspect | Network Delay (Base) | K Stops |
|--------|---------------------|---------|
| State | Just node | (node, stops_used) |
| Termination | All nodes visited | Reach dst or exceed k |
| Algorithm | Pure Dijkstra | Modified Dijkstra or Bellman-Ford |

### Complexity Analysis

| Algorithm | Time | Space |
|-----------|------|-------|
| Modified Dijkstra | O(EK log(EK)) | O(NK) |
| Bellman-Ford | O(KE) | O(N) |

---
