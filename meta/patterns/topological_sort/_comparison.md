## Pattern Comparison

### Kahn's Algorithm vs DFS Postorder

| Aspect | Kahn's (BFS) | DFS Postorder |
|--------|--------------|---------------|
| **Approach** | Process nodes with in-degree 0 | Explore deeply, add on backtrack |
| **Data Structure** | Queue + in-degree array | Recursion stack + color array |
| **Cycle Detection** | `len(result) < n` | Back edge (GRAY → GRAY) |
| **Order Production** | Natural forward order | Reverse of postorder |
| **Parallelism** | Easily parallelizable | Sequential by nature |
| **Best For** | Streaming/online processing | Simple implementation |

### Problem Variant Comparison

| Problem | Core Task | Key Modification |
|---------|-----------|------------------|
| LC 207 | Detect if order exists | Return boolean only |
| LC 210 | Find valid order | Collect nodes during traversal |
| LC 802 | Find safe nodes | DFS color or reverse Kahn's |
| LC 1203 | Multi-level ordering | Two-level topo sort |

### When to Choose Which Algorithm

```
Choose Kahn's (BFS) when:
├── Need to process in batches/levels
├── Parallelization is important
├── Need to handle dynamic insertions
└── Prefer iterative over recursive

Choose DFS when:
├── Simpler implementation preferred
├── Need to find all topological orderings
├── Stack depth is not a concern
└── Already doing other DFS operations
```

---
