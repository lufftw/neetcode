## Redundant Connection (LeetCode 684)

> **Problem**: Find the edge that creates a cycle in an undirected graph.
> **Invariant**: Union returns False when connecting already-connected nodes.
> **Role**: BASE TEMPLATE for cycle detection.

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "creates cycle" | → Union-Find: union returns False |
| "redundant edge" | → Edge connecting same component |
| "remove one edge" | → First (or last) edge creating cycle |

### Implementation

```python
# Pattern: union_find_cycle_detection
# See: docs/patterns/union_find/templates.md Section 2

class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        """
        Find the edge that creates a cycle.

        Key Insight:
        - Process edges in order
        - Union returns False if nodes already connected
        - That edge is redundant (creates a cycle)

        Why this works:
        - In a tree with n nodes, there are n-1 edges
        - Adding one more edge creates exactly one cycle
        - The edge connecting already-connected nodes is redundant
        """
        n = len(edges)
        parent = list(range(n + 1))  # 1-indexed
        rank = [0] * (n + 1)

        def find(x: int) -> int:
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x: int, y: int) -> bool:
            px, py = find(x), find(y)
            if px == py:
                return False  # Cycle detected!
            if rank[px] < rank[py]:
                px, py = py, px
            parent[py] = px
            if rank[px] == rank[py]:
                rank[px] += 1
            return True

        for u, v in edges:
            if not union(u, v):
                return [u, v]

        return []  # Should never reach here
```

### Trace Example

```
Input: edges = [[1,2],[1,3],[2,3]]

Process:
1. union(1, 2): success, parent = [0, 1, 1, 3]
2. union(1, 3): success, parent = [0, 1, 1, 1]
3. union(2, 3): find(2)=1, find(3)=1, SAME! Return [2,3]

Output: [2, 3]
```

### Visual Representation

```
Building graph:
Step 1: 1 --- 2         (union succeeds)
Step 2: 1 --- 2         (union succeeds)
        |
        3
Step 3: 1 --- 2         (union fails - cycle!)
        | \ /
        3

Edge [2,3] creates the cycle.
```

### Edge Case: Multiple Valid Answers

```
Problem says: Return the LAST edge that creates a cycle
(if multiple edges could be removed)

Input: [[1,2],[2,3],[3,4],[1,4],[1,5]]

Graph: 1-2-3-4-1 (cycle) + 1-5

Edge [1,4] creates the cycle.
If we check [3,4] first: no cycle yet
If we check [1,4] second: cycle detected!
```

### Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n × α(n)) ≈ O(n) |
| Space | O(n) for parent/rank arrays |

### Related Problems

| Problem | Variation |
|---------|-----------|
| LC 685: Redundant Connection II | Directed graph (harder) |
| LC 261: Graph Valid Tree | Check if exactly n-1 edges |
| LC 1319: Network Operations | Count extra edges |


