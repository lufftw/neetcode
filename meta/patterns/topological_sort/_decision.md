## Decision Guide: When to Use Topological Sort

### Pattern Recognition Signals

Use Topological Sort when you see:

| Signal | Example Phrases |
|--------|-----------------|
| **Prerequisites/Dependencies** | "must complete X before Y", "depends on" |
| **Ordering with Constraints** | "valid order", "schedule tasks" |
| **Cycle Detection in DAG** | "is it possible to", "can all be completed" |
| **Build Order** | "compilation order", "dependency resolution" |

### Decision Flowchart

```
Problem involves ordering/dependencies?
├── Yes
│   ├── Is it a directed graph?
│   │   ├── Yes → Consider Topological Sort
│   │   │   ├── Just detect if order exists?
│   │   │   │   └── LC 207 style (return boolean)
│   │   │   ├── Need the actual order?
│   │   │   │   └── LC 210 style (return list)
│   │   │   ├── Find nodes not in cycles?
│   │   │   │   └── LC 802 style (safe states)
│   │   │   └── Multi-level dependencies?
│   │   │       └── LC 1203 style (nested topo)
│   │   │
│   │   └── No (undirected)
│   │       └── Consider Union-Find or other approaches
│   │
│   └── No ordering constraint
│       └── Different pattern (BFS, DFS, etc.)
│
└── No → Different pattern
```

### Related Patterns

| If you see... | Consider... |
|---------------|-------------|
| Shortest path in DAG | Topological Sort + DP |
| Strongly Connected Components | Kosaraju's or Tarjan's |
| Undirected cycle detection | Union-Find |
| Task scheduling with resources | Topological Sort + Heap |
| Longest path in DAG | Topological Sort + DP |

### Common Pitfalls

1. **Forgetting self-loops**: A node depending on itself is a cycle
2. **Wrong edge direction**: Prerequisite A→B means A must come BEFORE B
3. **Not handling disconnected components**: Process ALL unvisited nodes
4. **Stack overflow**: Use iterative version for deep graphs

---
