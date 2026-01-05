## Strict vs Non-Strict Inequality Strategy

> **Core Insight**: The choice between `<` and `<=` is not about "which is correct" — it's about **invariant definition**.

### The Real Pain Point

Many developers memorize `while left <= right` but don't understand **when to use `<` vs `<=`**. This leads to:
- Off-by-one errors
- Infinite loops
- Wrong boundary detection

### Two Canonical Loop Styles

#### Style 1: `while left <= right` (Closed Interval)

```python
# Invariant: answer is in [left, right] (inclusive both ends)
left, right = 0, len(arr) - 1
while left <= right:
    mid = (left + right) // 2
    if condition(mid):
        right = mid - 1  # Exclude mid, search [left, mid-1]
    else:
        left = mid + 1   # Exclude mid, search [mid+1, right]
# Loop ends when left > right (empty interval)
```

**Use when:**
- Finding exact match
- Need to check every element
- Return -1 if not found

**Examples:** 704 (Binary Search), 33 (Search in Rotated)

#### Style 2: `while left < right` (Half-Open Interval)

```python
# Invariant: answer is in [left, right) or [left, right]
left, right = 0, len(arr)  # Note: right = len(arr), not len(arr)-1
while left < right:
    mid = (left + right) // 2
    if condition(mid):
        right = mid        # Keep mid in range, search [left, mid]
    else:
        left = mid + 1     # Exclude mid, search [mid+1, right]
# Loop ends when left == right (single candidate)
```

**Use when:**
- Finding boundary (first/last true)
- Answer guaranteed to exist
- Need the boundary position

**Examples:** 34 (First/Last Position), 35 (Search Insert), 875 (Koko Bananas)

### Decision Matrix

| Question | Style 1 (`<=`) | Style 2 (`<`) |
|----------|---------------|---------------|
| Interval type | Closed `[l, r]` | Half-open `[l, r)` |
| Initial right | `len(arr) - 1` | `len(arr)` |
| When found | Move both boundaries | Move one boundary |
| Loop ends | `left > right` | `left == right` |
| Best for | Exact match | Boundary finding |

### Why This Matters for Duplicates

With duplicates (LC 34, 81), the inequality choice determines:
- Whether you find **first** or **last** occurrence
- Whether boundary **includes** or **excludes** target

```python
# Find FIRST occurrence of target
while left < right:
    mid = (left + right) // 2
    if arr[mid] >= target:  # Include mid in left part
        right = mid
    else:
        left = mid + 1

# Find LAST occurrence of target
while left < right:
    mid = (left + right + 1) // 2  # Bias right to avoid infinite loop
    if arr[mid] <= target:  # Include mid in right part
        left = mid
    else:
        right = mid - 1
```

### The Infinite Loop Trap

When `left < right` and you do `left = mid` (without +1), you risk infinite loop:

```
┌─────────────────────────────────────────────────┐
│  left = 3, right = 4                            │
│  mid = (3 + 4) // 2 = 3                         │
│  If left = mid → left = 3 (no progress!)        │
│                                                 │
│  Solution: Use mid = (left + right + 1) // 2    │
│  mid = (3 + 4 + 1) // 2 = 4                     │
│  Now left = mid → left = 4 (progress!)          │
└─────────────────────────────────────────────────┘
```

### Covered Problems

| Problem | Inequality | Why |
|---------|-----------|-----|
| 34 First/Last Position | `<` | Finding boundaries with duplicates |
| 81 Rotated with Duplicates | `<=` | Need to check all, worst case linear |
| 875 Koko Eating Bananas | `<` | Finding minimum feasible answer |
| 1011 Ship Packages | `<` | Finding minimum capacity |
| 410 Split Array | `<` | Minimizing maximum sum |


