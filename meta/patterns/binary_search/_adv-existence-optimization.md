## Existence vs Optimization Binary Search

> **Core Insight**: Is the problem asking "Does it exist?" or "What's the optimal value?"

### Two Fundamental Question Types

#### Type 1: Existence Query

**Question**: "Is target present?" / "Does a valid configuration exist?"

**Return Type**: `bool` or index (with -1 for not found)

**Template**:
```python
def exists(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return True  # or return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return False  # or return -1
```

**Characteristics**:
- Search terminates early on exact match
- Uses `left <= right` to check all candidates
- Often returns boolean or index

**Examples**: 704, 33, 81

#### Type 2: Optimization Query

**Question**: "What's the minimum/maximum valid value?"

**Return Type**: The actual value (int/float)

**Template**:
```python
def find_minimum(low, high, feasible):
    while low < high:
        mid = (low + high) // 2
        if feasible(mid):
            high = mid      # mid works, try smaller
        else:
            low = mid + 1   # mid doesn't work, need larger
    return low
```

**Characteristics**:
- Never terminates early (need to find optimal)
- Uses `left < right` to converge to answer
- Always returns a value (answer guaranteed to exist)

**Examples**: 875, 1011, 410, 774, 1283, 1482

### Side-by-Side Comparison

| Aspect | Existence | Optimization |
|--------|-----------|--------------|
| Question | "Is it there?" | "What's the best?" |
| Return type | `bool` / `int` (-1) | `int` / `float` |
| Early termination | Yes (on match) | No (need boundary) |
| Loop condition | `left <= right` | `left < right` |
| Search space | Array indices | Value range |
| Predicate | `arr[mid] == target` | `feasible(mid)` |

### Mapping to Template Choice

```
┌──────────────────────────────────────────────────────────┐
│  "Does X exist?"                                          │
│  ├── Yes → Use exact match template                       │
│  │         └── Returns: found index or -1                 │
│  │                                                        │
│  "What's the minimum/maximum X?"                          │
│  ├── Yes → Use first_true / last_true template            │
│  │         └── Returns: optimal value                     │
│  │                                                        │
│  Tip: Optimization often uses "first_true" for minimize   │
│       and "last_true" for maximize                        │
└──────────────────────────────────────────────────────────┘
```

### Why first_true vs last_true?

For **minimize** problems (find minimum valid value):
```python
# Find first speed where Koko can finish
# Predicate: can_finish(speed) returns True/False
# [F, F, F, T, T, T, T] → find first T
def first_true(lo, hi, predicate):
    while lo < hi:
        mid = (lo + hi) // 2
        if predicate(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

For **maximize** problems (find maximum valid value):
```python
# Find maximum pages per day such that reading finishes
# [T, T, T, T, F, F, F] → find last T
def last_true(lo, hi, predicate):
    while lo < hi:
        mid = (lo + hi + 1) // 2  # Bias right
        if predicate(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo
```

### Problem Classification

| Problem | Type | Return | Template |
|---------|------|--------|----------|
| 704 Binary Search | Existence | Index/-1 | Exact match |
| 33 Rotated Search | Existence | Index/-1 | Exact match + pivot |
| 81 Rotated (dupes) | Existence | bool | Exact match + linear fallback |
| 35 Search Insert | Optimization | Index | first_true (>= target) |
| 875 Koko Bananas | Optimization | Speed value | first_true (can finish) |
| 1011 Ship Packages | Optimization | Capacity | first_true (can ship) |
| 410 Split Array | Optimization | Max sum | first_true (can split) |


