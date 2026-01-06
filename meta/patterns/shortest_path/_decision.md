## Decision Guide: When to Use Shortest Path Algorithms

### Pattern Recognition Signals

Use Shortest Path when you see:

| Signal | Example Phrases |
|--------|-----------------|
| **Minimum cost/time** | "shortest time", "minimum cost", "cheapest" |
| **Path in weighted graph** | "edge weights", "travel time", "price" |
| **Grid navigation** | "minimum moves", "reach destination" |
| **Optimization on graph** | "find optimal route", "best path" |

### Decision Flowchart

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

### Algorithm Trade-offs

| Algorithm | Pros | Cons |
|-----------|------|------|
| **Dijkstra** | Works for any non-negative weights | O(log V) per operation |
| **0-1 BFS** | O(1) per operation | Only for 0/1 weights |
| **Bellman-Ford** | Handles negative edges, path limit | O(V × E) or O(K × E) |
| **BFS** | Simple, O(1) per operation | Only for unweighted |

### Common Pitfalls

1. **Using BFS for weighted graphs**: BFS only works when all edges have equal weight.

2. **Not handling disconnected nodes**: Check if target is reachable.

3. **Wrong priority in 0-1 BFS**: Cost-0 edges go to FRONT, cost-1 to BACK.

4. **Forgetting to skip processed nodes**: In Dijkstra, skip if `cost > dist[node]`.

5. **Using Dijkstra with negative edges**: Will give wrong results; use Bellman-Ford.

### Related Patterns

| If you see... | Consider... |
|---------------|-------------|
| Shortest path in DAG | Topological Sort + DP |
| All-pairs shortest path | Floyd-Warshall |
| Longest path in DAG | Negate weights or DP |
| Path with constraints | State-space Dijkstra |
| MST (connect all nodes) | Prim's or Kruskal's |

---
