## Number of Provinces (LeetCode 547)

> **Problem**: Count connected components in an adjacency matrix graph.
> **Invariant**: Each union reduces component count by 1.
> **Role**: BASE TEMPLATE for Union-Find connectivity.

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "connected components" | → Union-Find or DFS |
| "adjacency matrix" | → Symmetric edges, union both (i,j) |
| "count groups" | → Track components during unions |

### Implementation

```python
# Pattern: union_find_connected_components
# See: docs/patterns/union_find/templates.md Section 1 (Base Template)

class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        """
        Count number of provinces (connected components).

        Key Insight:
        - Start with n components (each city is its own province)
        - Each successful union reduces count by 1
        - Final count = number of provinces

        Why Union-Find over DFS?
        - Same complexity O(n²) for this problem
        - Union-Find is more natural for connectivity queries
        - Easier to extend for dynamic edge additions
        """
        n = len(isConnected)
        parent = list(range(n))
        rank = [0] * n

        def find(x: int) -> int:
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x: int, y: int) -> bool:
            px, py = find(x), find(y)
            if px == py:
                return False
            if rank[px] < rank[py]:
                px, py = py, px
            parent[py] = px
            if rank[px] == rank[py]:
                rank[px] += 1
            return True

        components = n
        for i in range(n):
            for j in range(i + 1, n):  # Only upper triangle (symmetric)
                if isConnected[i][j] == 1:
                    if union(i, j):
                        components -= 1

        return components
```

### Trace Example

```
Input: isConnected = [[1,1,0],[1,1,0],[0,0,1]]

Cities: 0, 1, 2
Initial: components = 3, parent = [0, 1, 2]

Process edges:
- isConnected[0][1] = 1: union(0, 1) → success
  parent = [0, 0, 2], components = 2
- isConnected[0][2] = 0: skip
- isConnected[1][2] = 0: skip

Output: 2 (provinces: {0,1} and {2})
```

### Visual Representation

```
Adjacency Matrix:      Graph:
   0  1  2
0 [1, 1, 0]           0 --- 1
1 [1, 1, 0]
2 [0, 0, 1]           2 (isolated)

Union-Find Forest:
  0                   2
  |
  1

Result: 2 components
```

### Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n² × α(n)) ≈ O(n²) |
| Space | O(n) for parent/rank arrays |

### Related Problems

| Problem | Variation |
|---------|-----------|
| LC 200: Number of Islands | Grid-based components |
| LC 323: Number of Connected Components | Edge list input |
| LC 1319: Network Operations | Count components + edge requirement |


