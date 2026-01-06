## Pattern Comparison

### Algorithm Selection Guide

| Problem Type | Algorithm | Time | When to Use |
|--------------|-----------|------|-------------|
| General weighted | Dijkstra | O((V+E) log V) | Non-negative weights |
| Binary weights (0/1) | 0-1 BFS | O(V + E) | Weights only 0 or 1 |
| Limited steps/edges | Bellman-Ford | O(K × E) | Need to limit path length |
| Unweighted | BFS | O(V + E) | All edges cost 1 |
| Negative edges | Bellman-Ford | O(V × E) | Negative weights present |

### Problem Variant Comparison

| Problem | Edge Weight | Objective | Special Constraint |
|---------|-------------|-----------|-------------------|
| LC 743 | Given | Min sum to all | None |
| LC 1631 | Height diff | Min max edge | Implicit grid graph |
| LC 787 | Given | Min sum to dst | At most K stops |
| LC 1368 | 0 or 1 | Min sum | 0-1 BFS applicable |
| LC 2290 | 0 or 1 | Min sum | 0-1 BFS applicable |

### Implementation Patterns

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
