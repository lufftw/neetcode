## Find if Path Exists in Graph (LeetCode 1971)

> **Problem**: Determine if a path exists between source and destination.
> **Pattern**: DFS/BFS reachability OR Union-Find
> **Key Insight**: Standard connectivity check - multiple valid approaches.

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "path exists between" | → Reachability query |
| "undirected graph" | → Bidirectional edges |
| "source to destination" | → Point-to-point connectivity |

### Implementation

```python
# Pattern: graph_dfs_reachability
# See: docs/patterns/graph/templates.md Section 1

from collections import defaultdict

class SolutionDFS:
    def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        """
        Check if path exists from source to destination using DFS.

        Key Insight:
        - Build adjacency list from edge list
        - DFS from source
        - Return True if we reach destination

        Early termination: Stop as soon as destination is found.
        """
        if source == destination:
            return True

        # Build adjacency list
        graph: dict[int, list[int]] = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)  # Undirected

        visited: set[int] = set()

        def dfs(node: int) -> bool:
            if node == destination:
                return True

            visited.add(node)

            for neighbor in graph[node]:
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True

            return False

        return dfs(source)
```

### Trace Example

```
n = 6, edges = [[0,1],[0,2],[3,5],[5,4],[4,3]]
source = 0, destination = 5

Graph:
  0 -- 1
  |
  2

  3 -- 5
   \  /
    4

Components: {0, 1, 2} and {3, 4, 5}

DFS from 0:
1. Visit 0, neighbors: 1, 2
2. Visit 1, neighbors: 0 (visited)
3. Visit 2, neighbors: 0 (visited)
4. Exhausted component, destination 5 not found

Result: False (different components)

If destination = 2:
DFS from 0:
1. Visit 0, neighbors: 1, 2
2. Visit 1... or
2. Visit 2 → FOUND!

Result: True
```

### BFS Alternative

```python
from collections import deque, defaultdict

class SolutionBFS:
    def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        """BFS approach with early termination."""
        if source == destination:
            return True

        graph: dict[int, list[int]] = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        visited: set[int] = {source}
        queue: deque[int] = deque([source])

        while queue:
            node = queue.popleft()

            for neighbor in graph[node]:
                if neighbor == destination:
                    return True
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return False
```

### Union-Find Alternative

```python
class SolutionUnionFind:
    def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        """
        Union-Find approach - check if source and destination are in same component.

        When to use Union-Find vs DFS/BFS:
        - Single query: DFS/BFS is simpler
        - Multiple queries: Union-Find is more efficient (preprocess once)
        - Dynamic connectivity: Union-Find handles edge additions
        """
        parent = list(range(n))
        rank = [0] * n

        def find(x: int) -> int:
            if parent[x] != x:
                parent[x] = find(parent[x])  # Path compression
            return parent[x]

        def union(x: int, y: int) -> None:
            px, py = find(x), find(y)
            if px == py:
                return
            # Union by rank
            if rank[px] < rank[py]:
                px, py = py, px
            parent[py] = px
            if rank[px] == rank[py]:
                rank[px] += 1

        # Union all edges
        for u, v in edges:
            union(u, v)

        # Check if same component
        return find(source) == find(destination)
```

### Approach Comparison

| Approach | Time | Space | Best For |
|----------|------|-------|----------|
| DFS | O(V + E) | O(V + E) | Single query, simple implementation |
| BFS | O(V + E) | O(V + E) | Single query, shortest path needed |
| Union-Find | O(E × α(n)) | O(V) | Multiple queries, dynamic graphs |

α(n) = inverse Ackermann function, effectively constant

### When to Choose Each

```python
# DFS: Simple reachability, recursive thinking
# - Easy to implement
# - Good for single query
# - Natural for exploring all paths

# BFS: Need shortest path or level information
# - Guaranteed shortest path in unweighted graph
# - Good for single query
# - Level-by-level exploration

# Union-Find: Multiple connectivity queries
# - Preprocess graph once
# - O(α(n)) per query after preprocessing
# - Handles edge additions efficiently
```

### Complexity Analysis

| Approach | Time | Space |
|----------|------|-------|
| DFS | O(V + E) | O(V + E) graph + O(V) visited + recursion |
| BFS | O(V + E) | O(V + E) graph + O(V) visited + queue |
| Union-Find | O(E × α(n)) | O(V) for parent/rank arrays |

### Related Problems

| Problem | Connection |
|---------|------------|
| LC 200: Number of Islands | Count connected components |
| LC 547: Number of Provinces | Same as Number of Islands |
| LC 684: Redundant Connection | Union-Find cycle detection |


