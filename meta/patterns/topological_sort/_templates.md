## Quick Reference Templates

### Template 1: Kahn's Algorithm (BFS)

```python
def topological_sort_kahn(n: int, edges: List[Tuple[int, int]]) -> List[int]:
    """
    Kahn's algorithm for topological sort.
    edges: List of (from, to) pairs meaning from → to

    Returns:
        List of nodes in topological order, or [] if cycle exists.
    """
    from collections import deque

    # Build graph and in-degrees
    graph: List[List[int]] = [[] for _ in range(n)]
    in_degree: List[int] = [0] * n

    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    # Initialize with in-degree 0 nodes
    queue: deque[int] = deque([i for i in range(n) if in_degree[i] == 0])
    result: List[int] = []

    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return result if len(result) == n else []
```

### Template 2: DFS Postorder

```python
def topological_sort_dfs(n: int, edges: List[Tuple[int, int]]) -> List[int]:
    """
    DFS-based topological sort.
    edges: List of (from, to) pairs meaning from → to

    Returns:
        List of nodes in topological order, or [] if cycle exists.
    """
    WHITE, GRAY, BLACK = 0, 1, 2

    graph: List[List[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)

    color: List[int] = [WHITE] * n
    result: List[int] = []
    has_cycle = False

    def dfs(node: int) -> None:
        nonlocal has_cycle
        if has_cycle:
            return

        color[node] = GRAY

        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                has_cycle = True
                return
            if color[neighbor] == WHITE:
                dfs(neighbor)

        color[node] = BLACK
        result.append(node)

    for node in range(n):
        if color[node] == WHITE:
            dfs(node)
            if has_cycle:
                return []

    return result[::-1]
```

### Template 3: Cycle Detection Only

```python
def has_cycle(n: int, edges: List[Tuple[int, int]]) -> bool:
    """
    Check if directed graph has a cycle.
    Returns True if cycle exists.
    """
    from collections import deque

    graph: List[List[int]] = [[] for _ in range(n)]
    in_degree: List[int] = [0] * n

    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    queue: deque[int] = deque([i for i in range(n) if in_degree[i] == 0])
    visited = 0

    while queue:
        node = queue.popleft()
        visited += 1

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return visited != n  # True if cycle exists
```

### Template 4: Safe Nodes (LC 802 Style)

```python
def find_safe_nodes(graph: List[List[int]]) -> List[int]:
    """
    Find nodes that are not part of any cycle.
    graph[i] = list of nodes reachable from i.
    """
    n = len(graph)
    WHITE, GRAY, BLACK = 0, 1, 2
    color: List[int] = [WHITE] * n

    def is_safe(node: int) -> bool:
        if color[node] == GRAY:
            return False
        if color[node] == BLACK:
            return True

        color[node] = GRAY

        for neighbor in graph[node]:
            if not is_safe(neighbor):
                return False

        color[node] = BLACK
        return True

    return [i for i in range(n) if is_safe(i)]
```

### Complexity Summary

| Algorithm | Time | Space |
|-----------|------|-------|
| Kahn's (BFS) | O(V + E) | O(V + E) |
| DFS Postorder | O(V + E) | O(V + E) |
| Cycle Detection | O(V + E) | O(V + E) |
| Safe Nodes | O(V + E) | O(V) |

---
