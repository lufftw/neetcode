---

## Decision Framework

### Quick Reference Decision Tree

```
START: Given connectivity/grouping problem
│
├─ "Count connected components"?
│   └─ YES → Union-Find with component counter
│            (LC 547, 1319 pattern)
│
├─ "Find cycle" or "redundant edge"?
│   └─ YES → Union-Find: union returns False = cycle
│            (LC 684 pattern)
│
├─ "Merge/group by common element"?
│   └─ YES → Map elements to indices, union on match
│            (LC 721 pattern)
│
├─ "Equality + inequality constraints"?
│   └─ YES → Two-pass: equalities first, then check inequalities
│            (LC 990 pattern)
│
├─ "Connect all with minimum operations"?
│   └─ YES → Count components, need c-1 moves
│            Check if enough extra edges
│            (LC 1319 pattern)
│
└─ "Path between nodes" or "shortest path"?
    └─ NO → Union-Find can help
    └─ YES → Use DFS/BFS instead
```

### Feature Selection Guide

```
Need to track component sizes?
  → Add size[] array, update in union()

Need weighted relationships (like a/b = 2)?
  → Use weighted Union-Find with ratio tracking

Need to handle string keys (not just indices)?
  → Use dict for parent instead of list
  → Or map strings to indices first

Need to count redundant edges?
  → Count when union() returns False
```

### Common Mistakes to Avoid

| Mistake | Why Wrong | Correct Approach |
|---------|-----------|------------------|
| Not using path compression | O(n) per find | Always compress path |
| Forgetting to update rank/size | Unbalanced trees | Update after linking |
| Processing order wrong | Wrong answer | Equalities before inequalities |
| Using 0-indexed for 1-indexed input | Off-by-one | Match problem indexing |
| Not checking if enough edges | Wrong answer for impossible | Check edges >= n-1 |

### Index Mapping Patterns

```python
# 1-indexed nodes (LC 684)
parent = list(range(n + 1))  # Extra slot for 1-indexing

# Character indices (LC 990)
x = ord(char) - ord('a')  # 'a'->0, 'b'->1, etc.

# String to index mapping (LC 721)
string_to_idx = {}
for i, s in enumerate(strings):
    if s not in string_to_idx:
        string_to_idx[s] = len(string_to_idx)

# Coordinate to index (grid problems)
idx = row * cols + col
```

### Complexity Expectations

| Operation | Expected Complexity |
|-----------|-------------------|
| Initialize | O(n) |
| Find (with path compression) | O(α(n)) ≈ O(1) |
| Union (with rank) | O(α(n)) ≈ O(1) |
| Process all edges | O(E × α(n)) |
| Count components | O(n) |


