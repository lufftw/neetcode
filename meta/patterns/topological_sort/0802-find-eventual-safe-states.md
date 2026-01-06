## Variant: Find Eventual Safe States (LeetCode 802)

> **Problem**: Find all nodes that eventually lead only to terminal nodes.
> **Delta from Base**: Work on reversed graph; find nodes NOT in any cycle.
> **Role**: Demonstrates reverse topological analysis and safe state detection.

### Problem Statement

There is a directed graph of `n` nodes with each node labeled from `0` to `n - 1`. The graph is represented by a 0-indexed 2D integer array `graph` where `graph[i]` is an integer array of nodes adjacent to node `i`.

A node is a **terminal node** if there are no outgoing edges. A node is a **safe node** if every possible path starting from that node leads to a terminal node (or another safe node).

Return an array containing all the safe nodes in ascending order.

### Key Insight

A node is **safe** if and only if it's NOT part of a cycle and all paths from it lead to terminal nodes.

**Approach 1 (DFS)**: Color-based cycle detection. Nodes that finish (BLACK) without finding a cycle are safe.

**Approach 2 (Reverse + Kahn)**: Reverse graph direction, then terminal nodes have out-degree 0. Run Kahn's from terminals.

### Implementation (DFS Three-Color)

```python
class Solution:
    def eventualSafeNodes(self, graph: List[List[int]]) -> List[int]:
        """
        Find nodes not in any cycle using three-color DFS.
        Safe = reaches BLACK state without encountering GRAY.
        """
        n = len(graph)
        WHITE, GRAY, BLACK = 0, 1, 2
        color: List[int] = [WHITE] * n

        def is_safe(node: int) -> bool:
            if color[node] == GRAY:
                return False  # In cycle
            if color[node] == BLACK:
                return True   # Already verified safe

            color[node] = GRAY

            for neighbor in graph[node]:
                if not is_safe(neighbor):
                    return False  # Leads to cycle

            color[node] = BLACK
            return True

        return [node for node in range(n) if is_safe(node)]
```

### Implementation (Reverse Graph + Kahn's)

```python
class SolutionKahn:
    def eventualSafeNodes(self, graph: List[List[int]]) -> List[int]:
        """
        Reverse graph, then run Kahn's from terminal nodes.
        Nodes reachable in reverse = safe nodes.
        """
        n = len(graph)

        # Build reverse graph and out-degree
        reverse_graph: List[List[int]] = [[] for _ in range(n)]
        out_degree: List[int] = [0] * n

        for node in range(n):
            out_degree[node] = len(graph[node])
            for neighbor in graph[node]:
                reverse_graph[neighbor].append(node)

        # Start with terminal nodes (out-degree 0)
        queue: deque[int] = deque()
        for node in range(n):
            if out_degree[node] == 0:
                queue.append(node)

        safe: List[bool] = [False] * n

        while queue:
            node = queue.popleft()
            safe[node] = True

            # Process predecessors in reverse graph
            for pred in reverse_graph[node]:
                out_degree[pred] -= 1
                if out_degree[pred] == 0:
                    queue.append(pred)

        return [node for node in range(n) if safe[node]]
```

### Complexity Analysis

| Approach | Time | Space |
|----------|------|-------|
| DFS Three-Color | O(V + E) | O(V) |
| Reverse + Kahn | O(V + E) | O(V + E) |

### Trace Example

```
Input: graph = [[1,2],[2,3],[5],[0],[5],[],[]]
       0 → 1, 2
       1 → 2, 3
       2 → 5
       3 → 0  (creates cycle: 0→1→3→0)
       4 → 5
       5 → (terminal)
       6 → (terminal)

DFS from 0:
  0 (GRAY) → 1 (GRAY) → 2 (GRAY) → 5 (GRAY→BLACK, safe)
           ← 2 (BLACK, safe)
           → 3 (GRAY) → 0 (GRAY!) → CYCLE!
  0, 1, 3 are NOT safe

DFS from 2: Already BLACK, safe
DFS from 4: 4→5 (BLACK), 4 is safe
DFS from 5, 6: Terminal, safe

Answer: [2, 4, 5, 6]
```

---
