---

## Pattern Decision Guide

### Quick Decision Tree

```
Graph Problem?
├── Need shortest path?
│   ├── Unweighted → BFS
│   ├── Non-negative weights → Dijkstra
│   └── Negative weights → Bellman-Ford
├── Count components?
│   └── DFS/BFS from each unvisited → Count DFS calls
├── Clone/copy structure?
│   └── DFS/BFS + hash map (old → new)
├── Spread from multiple sources?
│   └── Multi-source BFS (queue all sources)
├── Bipartite/two-coloring?
│   └── BFS/DFS with alternating colors
├── Reachability (can reach X from Y)?
│   ├── Single query → DFS/BFS
│   └── Multiple queries → Union-Find
└── Cycle detection?
    ├── Undirected → Union-Find or DFS with parent tracking
    └── Directed → DFS with coloring (white/gray/black)
```

### Signal-to-Pattern Mapping

| Problem Signal | Pattern | Template |
|----------------|---------|----------|
| "count islands" | Connected components | LC 200 |
| "minimum time/distance" | BFS shortest path | LC 994 |
| "spread simultaneously" | Multi-source BFS | LC 994 |
| "reach both X and Y" | Two BFS + intersection | LC 417 |
| "deep copy" / "clone" | DFS + hash map | LC 133 |
| "two groups" / "divide" | Bipartite check | LC 785 |
| "can reach" / "visit all" | DFS reachability | LC 841 |
| "connected or not" | Union-Find / DFS | LC 1971 |

### Common Mistakes to Avoid

| Mistake | Problem | Solution |
|---------|---------|----------|
| Using DFS for shortest path | Won't find shortest | Use BFS instead |
| Not handling disconnected graphs | Missing components | Loop over all nodes |
| Not marking visited before enqueue | Duplicate processing | Mark when adding to queue |
| Modifying graph during traversal | Unexpected behavior | Use separate visited set |
| Stack overflow on large grids | Recursion limit | Use iterative DFS/BFS |

### Grid-Specific Considerations

```python
# Grid traversal setup
rows, cols = len(grid), len(grid[0])
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def is_valid(r: int, c: int) -> bool:
    return 0 <= r < rows and 0 <= c < cols

# Common patterns:
# - Mark visited in-place: grid[r][c] = '#' or '0'
# - Use visited set: visited.add((r, c))
# - Check condition: grid[r][c] == target_value
```


