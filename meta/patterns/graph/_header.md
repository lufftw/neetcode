# Graph Traversal Patterns: Complete Reference

> **API Kernel**: `GraphDFS`, `GraphBFS`
> **Core Mechanism**: Systematically explore all reachable nodes in a graph using depth-first or breadth-first strategies.

This document presents the **canonical graph traversal templates** covering DFS, BFS, connected components, bipartite checking, and shortest path problems. Each implementation follows consistent naming conventions and includes detailed logic explanations.

---

## Core Concepts

### Graph Representation

```python
# Adjacency List (most common for sparse graphs)
graph: dict[int, list[int]] = {
    0: [1, 2],      # Node 0 connects to nodes 1 and 2
    1: [0, 3],
    2: [0, 3],
    3: [1, 2]
}

# Edge List
edges: list[tuple[int, int]] = [(0, 1), (0, 2), (1, 3), (2, 3)]

# Adjacency Matrix (dense graphs)
matrix: list[list[int]] = [
    [0, 1, 1, 0],   # Node 0's connections
    [1, 0, 0, 1],   # Node 1's connections
    [1, 0, 0, 1],   # Node 2's connections
    [0, 1, 1, 0]    # Node 3's connections
]

# Grid as implicit graph
grid: list[list[int]] = [
    [1, 1, 0],
    [1, 1, 0],
    [0, 0, 1]
]
# Neighbors: (row±1, col±1) for 4-directional, add diagonals for 8-directional
```

### DFS vs BFS

| Aspect | DFS | BFS |
|--------|-----|-----|
| **Data Structure** | Stack (or recursion) | Queue |
| **Exploration** | Deep first, backtrack | Level by level |
| **Memory** | O(height) for recursion | O(width) for queue |
| **Use Cases** | Pathfinding, cycles, components | Shortest path, levels |
| **When to Choose** | Existence queries, all paths | Distance/level queries |

### Universal DFS Template

```python
def dfs(node: int, graph: dict, visited: set) -> None:
    """
    DFS template using recursion.

    Core invariant:
    - visited set prevents revisiting nodes
    - Process node BEFORE recursing (preorder) or AFTER (postorder)
    """
    if node in visited:
        return

    visited.add(node)

    # Process current node (preorder position)

    for neighbor in graph[node]:
        dfs(neighbor, graph, visited)

    # Process current node (postorder position)
```

### Universal BFS Template

```python
from collections import deque

def bfs(start: int, graph: dict) -> None:
    """
    BFS template using queue.

    Core invariant:
    - Nodes at distance d are processed before nodes at distance d+1
    - visited set prevents revisiting and infinite loops
    """
    visited: set[int] = {start}
    queue: deque[int] = deque([start])

    while queue:
        node = queue.popleft()

        # Process current node

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)  # Mark visited BEFORE adding to queue
                queue.append(neighbor)
```

### Pattern Variants

| Variant | API Kernel | Use When | Key Insight |
|---------|------------|----------|-------------|
| **Connected Components** | `GraphDFS` | Count/identify separate groups | DFS from each unvisited node |
| **Clone Graph** | `GraphDFS` | Deep copy graph structure | Map old nodes to new nodes |
| **Multi-source BFS** | `GraphBFS` | Propagation from multiple starts | Initialize queue with all sources |
| **Bipartite Check** | `GraphBFS` | Two-coloring problem | Alternate colors at each level |
| **Shortest Path** | `GraphBFS` | Unweighted graph distance | BFS guarantees shortest path |
| **Grid Traversal** | `GridBFSMultiSource` | 2D grid as graph | 4-directional neighbors |

### Grid Traversal Helpers

```python
# 4-directional movement
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def get_neighbors(row: int, col: int, rows: int, cols: int) -> list[tuple[int, int]]:
    """Get valid 4-directional neighbors."""
    neighbors = []
    for dr, dc in DIRECTIONS:
        nr, nc = row + dr, col + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

# 8-directional movement (includes diagonals)
DIRECTIONS_8 = [(0, 1), (0, -1), (1, 0), (-1, 0),
                (1, 1), (1, -1), (-1, 1), (-1, -1)]
```

### When BFS Guarantees Shortest Path

BFS finds shortest path ONLY when:
1. **Unweighted graph**: All edges have equal weight (or weight = 1)
2. **Non-negative weights**: No negative edges

For weighted graphs, use Dijkstra's algorithm instead.


