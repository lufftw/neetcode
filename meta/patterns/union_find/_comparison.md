---

## Pattern Comparison

### Union-Find vs DFS/BFS for Connectivity

| Aspect | Union-Find | DFS/BFS |
|--------|------------|---------|
| Build time | O(E × α(n)) | O(V + E) |
| Query time | O(α(n)) | O(V + E) |
| Dynamic edges | ✓ Efficient | ✗ Rebuild needed |
| Path info | ✗ Just connectivity | ✓ Can find path |
| Memory | O(V) | O(V + E) for adj list |

### When to Use Union-Find

```python
# ✓ USE Union-Find when:
# - Multiple connectivity queries after building
# - Dynamic edge additions (but not deletions!)
# - Only need "are X and Y connected?" not "what's the path?"
# - Detecting cycles during graph construction

# ✗ DON'T USE Union-Find when:
# - Need to find actual path between nodes
# - Need to handle edge deletions
# - Single connectivity query (DFS is simpler)
# - Need shortest path (BFS is better)
```

### Problem Type Recognition

| Problem Type | Key Signal | Approach |
|--------------|------------|----------|
| **Count components** | "how many groups" | Track count during unions |
| **Cycle detection** | "redundant edge", "creates cycle" | Union returns False |
| **Equivalence grouping** | "same group if share X" | Map items → indices |
| **Network connectivity** | "connect all", "minimum operations" | Components - 1 edges needed |
| **Constraint satisfaction** | "a==b", "a!=b" | Equality first, then check inequality |

### Code Pattern Comparison

```python
# BASIC UNION-FIND (most problems)
def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]

def union(x, y):
    px, py = find(x), find(y)
    if px == py: return False
    parent[py] = px
    return True

# WITH RANK (balanced trees)
def union_by_rank(x, y):
    px, py = find(x), find(y)
    if px == py: return False
    if rank[px] < rank[py]: px, py = py, px
    parent[py] = px
    if rank[px] == rank[py]: rank[px] += 1
    return True

# WITH SIZE TRACKING
def union_with_size(x, y):
    px, py = find(x), find(y)
    if px == py: return False
    if size[px] < size[py]: px, py = py, px
    parent[py] = px
    size[px] += size[py]
    return True
```

### Optimization Techniques

| Technique | Effect | When Needed |
|-----------|--------|-------------|
| Path compression | Find → O(α(n)) | Always use |
| Union by rank | Balanced trees | Competitive programming |
| Union by size | Track component sizes | Size-related queries |
| Weighted Union-Find | Handle weighted relationships | Division evaluation |


