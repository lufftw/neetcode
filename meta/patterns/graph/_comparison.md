---

## Pattern Comparison Matrix

### By Problem Type

| Problem Type | Best Pattern | Alternative | When to Switch |
|--------------|--------------|-------------|----------------|
| Count islands/regions | DFS flood fill | BFS | Large grid (avoid stack overflow) |
| Clone graph | DFS + hash map | BFS + hash map | Personal preference |
| Multi-source spread | Multi-source BFS | - | Always BFS for simultaneous spread |
| Bipartite check | BFS coloring | DFS coloring | Personal preference |
| Reachability | DFS | BFS, Union-Find | Multiple queries → Union-Find |
| Shortest path (unweighted) | BFS | - | Always BFS for shortest path |
| Shortest path (weighted) | Dijkstra | Bellman-Ford | Negative edges → Bellman-Ford |

### DFS vs BFS Selection

| Factor | Choose DFS | Choose BFS |
|--------|------------|------------|
| **Goal** | Existence, all paths | Shortest path, levels |
| **Memory** | O(depth) | O(width) |
| **Implementation** | Recursive (simpler) | Iterative (queue) |
| **Early termination** | Good | Good |
| **Level tracking** | Harder | Natural |
| **Cycle detection** | Postorder time | Layer check |

### By Data Structure

| Input | Pattern | Key Consideration |
|-------|---------|-------------------|
| Adjacency list | Standard DFS/BFS | Most common |
| Edge list | Build adj list first | O(E) preprocessing |
| Adjacency matrix | Iterate row for neighbors | O(V²) if dense |
| Grid | Implicit graph | 4/8 directional |

### Time/Space Complexity Summary

| Pattern | Time | Space |
|---------|------|-------|
| DFS (recursive) | O(V + E) | O(V) visited + O(V) stack |
| DFS (iterative) | O(V + E) | O(V) visited + O(V) stack |
| BFS | O(V + E) | O(V) visited + O(V) queue |
| Multi-source BFS | O(V + E) | O(V) for multiple sources |
| Union-Find | O(E × α(V)) | O(V) for parent array |


