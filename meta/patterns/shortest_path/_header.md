# Shortest Path Patterns

> **API Kernel**: `ShortestPath`
>
> **Core Mechanism**: Find minimum-cost path in weighted graphs using priority-based exploration.

## Pattern Overview

Shortest path algorithms find the minimum-cost route between nodes in a graph. The choice of algorithm depends on edge weights and constraints.

### Algorithm Family

| Algorithm | Edge Weights | Best For |
|-----------|--------------|----------|
| **Dijkstra** | Non-negative | General weighted graphs |
| **0-1 BFS** | Only 0 or 1 | Binary edge weights |
| **Bellman-Ford** | Any (including negative) | Negative edges, limited steps |
| **BFS** | Unweighted (all = 1) | Unit cost graphs |

### Universal Template Structure

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

### Key Invariant

> **At each step, the node with minimum distance is finalized (for non-negative weights).**

This greedy property is why Dijkstra works: once we pop a node from the heap, we've found its shortest path.

---
