---

## Code Templates Summary

### Template 1: Basic Union-Find Class

```python
class UnionFind:
    """Standard Union-Find with path compression and union by rank."""

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        self.components -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)
```

### Template 2: Inline Functions (Competitive)

```python
def solve(n: int, edges: List[List[int]]) -> int:
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

    # Use find() and union() here
```

### Template 3: With Size Tracking

```python
class UnionFindWithSize:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        # Union by size
        if self.size[px] < self.size[py]:
            px, py = py, px
        self.parent[py] = px
        self.size[px] += self.size[py]
        return True

    def get_size(self, x: int) -> int:
        return self.size[self.find(x)]
```

### Template 4: Cycle Detection (LC 684)

```python
def find_redundant_edge(edges: List[List[int]]) -> List[int]:
    n = len(edges)
    parent = list(range(n + 1))

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    for u, v in edges:
        pu, pv = find(u), find(v)
        if pu == pv:
            return [u, v]  # Cycle found!
        parent[pv] = pu

    return []
```

### Template 5: Constraint Satisfaction (LC 990)

```python
def check_equations(equations: List[str]) -> bool:
    parent = list(range(26))

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    # Pass 1: Union equals
    for eq in equations:
        if eq[1] == '=':
            x, y = ord(eq[0]) - ord('a'), ord(eq[3]) - ord('a')
            parent[find(y)] = find(x)

    # Pass 2: Check not-equals
    for eq in equations:
        if eq[1] == '!':
            x, y = ord(eq[0]) - ord('a'), ord(eq[3]) - ord('a')
            if find(x) == find(y):
                return False

    return True
```

### Pattern Selection Cheat Sheet

| Problem Signal | Template | Key Modification |
|---------------|----------|-----------------|
| "count components" | Template 1 | Track component count |
| "find cycle" | Template 4 | Return edge when union fails |
| "group by common" | Template 1 | Map items to indices |
| "equality constraints" | Template 5 | Two-pass processing |
| "component sizes" | Template 3 | Use size instead of rank |


