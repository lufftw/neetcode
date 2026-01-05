## Is Graph Bipartite? (LeetCode 785)

> **Problem**: Determine if a graph can be 2-colored (bipartite).
> **Pattern**: BFS/DFS with node coloring
> **Key Insight**: Alternate colors at each level; conflict = not bipartite.

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "two groups" / "bipartite" | → Two-coloring problem |
| "no edges within group" | → Adjacent nodes must differ |
| "can be divided" | → Graph coloring BFS/DFS |

### Implementation

```python
# Pattern: graph_bipartite
# See: docs/patterns/graph/templates.md Section 5

from collections import deque

class SolutionBFS:
    def isBipartite(self, graph: List[List[int]]) -> bool:
        """
        Check if graph is bipartite using BFS coloring.

        Key Insight:
        - Bipartite = can assign 2 colors so no adjacent nodes share color
        - BFS processes level by level
        - Alternate colors at each level
        - If we try to color a node that's already colored differently → conflict

        Why BFS?
        - Natural level-by-level processing
        - Each level gets opposite color
        - Easy to detect conflicts
        """
        n = len(graph)
        # -1 = uncolored, 0 = color A, 1 = color B
        color: list[int] = [-1] * n

        def bfs(start: int) -> bool:
            """BFS coloring from start node. Returns False if conflict."""
            queue: deque[int] = deque([start])
            color[start] = 0  # Start with color 0

            while queue:
                node = queue.popleft()

                for neighbor in graph[node]:
                    if color[neighbor] == -1:
                        # Uncolored: assign opposite color
                        color[neighbor] = 1 - color[node]
                        queue.append(neighbor)
                    elif color[neighbor] == color[node]:
                        # Same color as current node → conflict
                        return False

            return True

        # Check all components (graph may be disconnected)
        for node in range(n):
            if color[node] == -1:
                if not bfs(node):
                    return False

        return True
```

### Trace Example

```
Graph: [[1,3], [0,2], [1,3], [0,2]]
Adjacency:
    0 --- 1
    |     |
    3 --- 2

BFS from node 0:
1. Color 0 with color A (0)
2. Visit neighbors 1, 3: color with B (1)
3. Visit neighbor of 1 (which is 2): color with A (0)
4. Visit neighbor of 3 (which is 2): already colored A ✓
5. Check neighbor of 2 (which is 3): already colored B ✓

Colors: [A, B, A, B] = [0, 1, 0, 1]
No conflicts → Bipartite!

Non-bipartite example:
    0 --- 1
     \   /
      \ /
       2

Coloring attempt:
1. Color 0 with A
2. Color 1, 2 with B
3. Check edge 1-2: both B → CONFLICT!
Not bipartite.
```

### DFS Alternative

```python
class SolutionDFS:
    def isBipartite(self, graph: List[List[int]]) -> bool:
        """DFS approach - recursive coloring."""
        n = len(graph)
        color: list[int] = [-1] * n

        def dfs(node: int, c: int) -> bool:
            """Try to color node with color c. Returns False if conflict."""
            if color[node] != -1:
                return color[node] == c  # Check for conflict

            color[node] = c

            for neighbor in graph[node]:
                if not dfs(neighbor, 1 - c):
                    return False

            return True

        for node in range(n):
            if color[node] == -1:
                if not dfs(node, 0):
                    return False

        return True
```

### Why Disconnected Graph Check?

```python
# Graph may have multiple components
# Example: graph = [[1], [0], [3], [2]]
#   0 -- 1    2 -- 3
#
# Must check EACH component separately
# Only need to start BFS/DFS from uncolored nodes

for node in range(n):
    if color[node] == -1:  # New component
        if not bfs(node):
            return False
```

### Complexity Analysis

| Approach | Time | Space |
|----------|------|-------|
| BFS | O(V + E) | O(V) for color array + queue |
| DFS | O(V + E) | O(V) for color array + recursion |

### Related Problems

| Problem | Connection |
|---------|------------|
| LC 886: Possible Bipartition | Same pattern with edge list input |
| LC 207: Course Schedule | Graph cycle detection variant |


