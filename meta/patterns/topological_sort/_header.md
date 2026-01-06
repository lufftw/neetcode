# Topological Sort Patterns: Complete Reference

> **API Kernel**: `TopologicalSort`
> **Core Mechanism**: Order nodes in a DAG such that for every directed edge u→v, u comes before v.

## Core Concepts

### The Topological Order Principle

A **topological order** is a linear ordering of vertices in a Directed Acyclic Graph (DAG) where for every directed edge (u, v), vertex u appears before vertex v.

**Key Properties**:
- Only exists for DAGs (no cycles)
- May have multiple valid orderings
- Detecting a cycle = no valid topological order exists

### Two Canonical Algorithms

#### 1. Kahn's Algorithm (BFS / In-degree)

Process nodes with in-degree 0 first, then reduce neighbors' in-degrees:

```python
def kahn_topological_sort(num_nodes: int, edges: List[List[int]]) -> List[int]:
    """
    BFS-based topological sort using in-degree counting.
    Returns empty list if cycle detected.
    """
    # Build adjacency list and in-degree count
    graph: List[List[int]] = [[] for _ in range(num_nodes)]
    in_degree: List[int] = [0] * num_nodes

    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    # Initialize queue with all nodes having in-degree 0
    queue: deque[int] = deque()
    for node in range(num_nodes):
        if in_degree[node] == 0:
            queue.append(node)

    topo_order: List[int] = []

    while queue:
        node = queue.popleft()
        topo_order.append(node)

        # Reduce in-degree of neighbors
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # If not all nodes processed, cycle exists
    if len(topo_order) != num_nodes:
        return []  # Cycle detected

    return topo_order
```

#### 2. DFS Postorder (with Cycle Detection)

DFS explores deeply, adding nodes to result in reverse postorder:

```python
def dfs_topological_sort(num_nodes: int, edges: List[List[int]]) -> List[int]:
    """
    DFS-based topological sort using postorder reversal.
    Returns empty list if cycle detected.

    State colors:
    - WHITE (0): Unvisited
    - GRAY (1): In current DFS path (cycle detection)
    - BLACK (2): Fully processed
    """
    WHITE, GRAY, BLACK = 0, 1, 2

    # Build adjacency list
    graph: List[List[int]] = [[] for _ in range(num_nodes)]
    for u, v in edges:
        graph[u].append(v)

    color: List[int] = [WHITE] * num_nodes
    topo_order: List[int] = []
    has_cycle = False

    def dfs(node: int) -> None:
        nonlocal has_cycle
        if has_cycle:
            return

        color[node] = GRAY  # Mark as being processed

        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                has_cycle = True  # Back edge = cycle
                return
            if color[neighbor] == WHITE:
                dfs(neighbor)

        color[node] = BLACK  # Mark as fully processed
        topo_order.append(node)  # Postorder: add after all descendants

    for node in range(num_nodes):
        if color[node] == WHITE:
            dfs(node)
            if has_cycle:
                return []

    return topo_order[::-1]  # Reverse for topological order
```

### Cycle Detection

**Using Kahn's Algorithm**:
- If `len(result) < num_nodes`, a cycle exists
- Nodes in cycle never reach in-degree 0

**Using DFS**:
- Back edge (visiting a GRAY node) indicates cycle
- Three-color marking: WHITE → GRAY → BLACK

### Pattern Variants

| Variant | Key Modification | Example Problem |
|---------|-----------------|-----------------|
| Cycle Detection | Return boolean instead of order | LC 207 |
| Full Order | Return one valid topological order | LC 210 |
| Safe States | Reverse graph, find nodes not in cycles | LC 802 |
| Multi-Level | Nested topological sort | LC 1203 |

---
