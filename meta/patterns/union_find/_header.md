# Union-Find Patterns: Complete Reference

> **API Kernel**: `UnionFindConnectivity`
> **Core Mechanism**: Maintain disjoint sets with efficient union and find operations using path compression and union by rank.

This document presents the **canonical Union-Find templates** covering connectivity queries, cycle detection, component counting, and equivalence grouping. Each implementation includes path compression and union by rank for near-constant time operations.

---

## Core Concepts

### Union-Find Data Structure

```python
class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))  # Initially, each node is its own parent
        self.rank = [0] * n           # Rank (tree depth upper bound)

    def find(self, x: int) -> int:
        """Find with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """Union by rank. Returns True if union performed (different sets)."""
        px, py = self.find(x), self.find(y)
        if px == py:
            return False  # Already in same set

        # Union by rank
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True
```

### Why Path Compression?

```python
# Without path compression:
#     1           After find(5): 1→2→3→4→5
#    /            Every find traverses full chain: O(n)
#   2
#  /
# 3
#  \
#   4
#    \
#     5

# With path compression:
#       1         After find(5): All nodes point to root
#    / | \ \      Subsequent finds: O(1)
#   2  3  4  5
```

### Why Union by Rank?

```python
# Without rank: Tree can become a linked list (O(n) per operation)
# With rank: Tree height stays O(log n)

# Union by rank: Always attach shorter tree under taller tree
# This keeps tree balanced
```

### Time Complexity Analysis

| Operation | Amortized Time |
|-----------|---------------|
| Find | O(α(n)) ≈ O(1) |
| Union | O(α(n)) ≈ O(1) |
| Connected | O(α(n)) ≈ O(1) |

Where α(n) is the inverse Ackermann function, which grows extremely slowly (α(n) ≤ 4 for any practical n).

### Pattern Variants

| Variant | Use When | Key Insight |
|---------|----------|-------------|
| **Connected Components** | Count/query connectivity | Each union reduces component count by 1 |
| **Cycle Detection** | Find redundant edges | Union returns False = cycle found |
| **Equivalence Grouping** | Group equivalent items | Map items to indices, then union |
| **Network Operations** | Min operations to connect | Components - 1 unions needed |

### Common Operations

```python
# Check if connected
def connected(self, x: int, y: int) -> bool:
    return self.find(x) == self.find(y)

# Count connected components
def count_components(self) -> int:
    return sum(1 for i, p in enumerate(self.parent) if self.find(i) == i)

# Get size of component (need to track sizes)
def __init__(self, n: int):
    self.parent = list(range(n))
    self.rank = [0] * n
    self.size = [1] * n  # Track component sizes

def union(self, x: int, y: int) -> bool:
    px, py = self.find(x), self.find(y)
    if px == py:
        return False
    if self.rank[px] < self.rank[py]:
        px, py = py, px
    self.parent[py] = px
    self.size[px] += self.size[py]  # Update size
    if self.rank[px] == self.rank[py]:
        self.rank[px] += 1
    return True
```


