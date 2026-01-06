## Number of Operations to Make Network Connected (LeetCode 1319)

> **Problem**: Find minimum operations to connect all computers.
> **Invariant**: Need (components - 1) edges to connect all components.
> **Role**: VARIANT combining component counting with edge availability.

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "make all connected" | → Count components, need c-1 edges |
| "rearrange edges" | → Count redundant edges (extras) |
| "minimum operations" | → Move redundant edges to connect |

### Implementation

```python
# Pattern: union_find_network_connectivity
# See: docs/patterns/union_find/templates.md Section 4

class Solution:
    def makeConnected(self, n: int, connections: List[List[int]]) -> int:
        """
        Minimum cables to move to connect all computers.

        Key Insight:
        - Need at least n-1 edges to connect n nodes
        - Redundant edges (forming cycles) can be moved
        - Count components and check if enough redundant edges

        Algorithm:
        1. If edges < n-1: impossible (-1)
        2. Count components using Union-Find
        3. Need (components - 1) moves to connect all
        """
        if len(connections) < n - 1:
            return -1  # Not enough cables

        parent = list(range(n))
        rank = [0] * n

        def find(x: int) -> int:
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x: int, y: int) -> bool:
            px, py = find(x), find(y)
            if px == py:
                return False  # Redundant edge
            if rank[px] < rank[py]:
                px, py = py, px
            parent[py] = px
            if rank[px] == rank[py]:
                rank[px] += 1
            return True

        components = n
        for a, b in connections:
            if union(a, b):
                components -= 1

        return components - 1
```

### Trace Example

```
Input: n = 6, connections = [[0,1],[0,2],[0,3],[1,2],[1,3]]

Check: 5 edges >= 5 (n-1)? Yes, possible.

Process:
- union(0,1): success, components = 5
- union(0,2): success, components = 4
- union(0,3): success, components = 3
- union(1,2): find(1)=0, find(2)=0, SAME (redundant)
- union(1,3): find(1)=0, find(3)=0, SAME (redundant)

Components: {0,1,2,3}, {4}, {5}
Need: 3 - 1 = 2 operations

Output: 2
```

### Visual Representation

```
Initial:
0 --- 1           4        5
| \ / |
2   3

Operations needed:
- Move one redundant edge to connect {4}
- Move another redundant edge to connect {5}

After:
0 --- 1 --- 4 --- 5
| \ /
2   3
```

### Edge Cases

```python
# Not enough edges
n = 6, connections = [[0,1],[0,2],[0,3],[1,2]]
# 4 edges < 5 needed → return -1

# Already connected
n = 4, connections = [[0,1],[0,2],[1,2],[1,3],[2,3]]
# 1 component → return 0

# Worst case: all isolated
n = 4, connections = []
# 0 edges < 3 needed → return -1
```

### Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(E × α(n)) ≈ O(E) |
| Space | O(n) for parent/rank arrays |

### Related Problems

| Problem | Variation |
|---------|-----------|
| LC 547: Number of Provinces | Just count components |
| LC 1579: Remove Max Edges | Count edges to keep |
| LC 1101: Earliest Moment Friends Connected | Process edges in order |


