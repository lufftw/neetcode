# Segment Tree / Fenwick Tree: Intuition Guide

## The Mental Model

Imagine you're managing a **scoreboard** that tracks scores for a league of players. Users can:
1. **Update** any player's score at any time
2. **Query** the total score of players ranked 5 through 15

With a simple array, updates are O(1) but range queries are O(n). With prefix sums, queries are O(1) but updates are O(n). **Segment Tree and Fenwick Tree give you O(log n) for both.**

---

## The Core Insight

Both data structures exploit the same fundamental idea:

> **Break the problem into log(n) pieces that can be precomputed and combined.**

### Fenwick Tree (Binary Indexed Tree)

Think of it as **layered partial sums** where each layer covers exponentially larger ranges:

```
Index:  1    2    3    4    5    6    7    8
        │    │    │    │    │    │    │    │
Layer 0: [1]  [2]  [3]  [4]  [5]  [6]  [7]  [8]   ← single elements
Layer 1: └─[1-2]  └─[3-4]  └─[5-6]  └─[7-8]       ← pairs
Layer 2:    └───[1-4]        └───[5-8]            ← groups of 4
Layer 3:        └───────[1-8]                     ← all 8
```

The magic: `lowbit(i) = i & (-i)` tells you which layer an index belongs to.

### Segment Tree

Think of it as a **binary tree** where each node stores aggregate info for a range:

```
              [sum 1-8]
             /         \
      [sum 1-4]       [sum 5-8]
       /     \         /     \
   [1-2]   [3-4]   [5-6]   [7-8]
   / \     / \     / \     / \
  1   2   3   4   5   6   7   8
```

Queries and updates only touch O(log n) nodes.

---

## Pattern Recognition Signals

### Signal: "Update + Range Query"

When you see both in the same problem:
- `update(index, value)` - modify a single element
- `query(left, right)` - get aggregate of range

**Think**: Segment Tree or Fenwick Tree

### Signal: "Count elements smaller/greater"

When you need to count inversions or relative ordering:
- "Count of smaller numbers after self"
- "Count inversions in array"

**Think**: BIT with coordinate compression, process right-to-left

### Signal: "Count subarrays/pairs with property"

When counting based on prefix sum differences:
- "Count subarrays with sum in [lower, upper]"
- "Count pairs where condition involves sum"

**Think**: Merge sort with counting or BIT with range queries

---

## Common Pitfalls

### 1. Forgetting BIT is 1-indexed

BIT uses indices 1 to n, not 0 to n-1. Always add 1 when converting.

```python
# Wrong
bit.update(i, val)  # if i can be 0

# Correct
bit.update(i + 1, val)
```

### 2. Using BIT for min/max queries

BIT only works for **prefix-aggregatable** operations (sum, count). For min/max, use Segment Tree.

### 3. Forgetting coordinate compression

When values are large (e.g., -10^9 to 10^9) but count is small, compress coordinates:

```python
sorted_unique = sorted(set(values))
rank = {v: i + 1 for i, v in enumerate(sorted_unique)}
```

### 4. Off-by-one in merge sort counting

In merge sort-based counting, left array has smaller indices, right has larger. The counting happens **before** merging when arrays are still sorted.

---

## Practice Progression

### Level 1: Foundation
1. **LC 307** (Range Sum Query - Mutable) - Build both BIT and Segment Tree

### Level 2: Coordinate Compression
2. **LC 315** (Count of Smaller Numbers After Self) - BIT with compression

### Level 3: Advanced Counting
3. **LC 327** (Count of Range Sum) - Merge sort with counting

### Level 4: Extensions (Optional)
4. **LC 308** (Range Sum Query 2D - Mutable) - 2D Segment Tree

---

## Key Templates to Memorize

### Fenwick Tree Core Operations

```python
def lowbit(x):
    return x & (-x)

def update(i, delta):  # Add delta to index i
    while i <= n:
        tree[i] += delta
        i += lowbit(i)

def prefix_sum(i):  # Sum of [1..i]
    total = 0
    while i > 0:
        total += tree[i]
        i -= lowbit(i)
    return total
```

### Right-to-Left Counting Pattern

```python
result = []
for num in reversed(nums):
    rank = rank_map[num]
    count = bit.query(rank - 1)  # Count smaller
    result.append(count)
    bit.update(rank, 1)  # Add current
return result[::-1]
```

---

## When NOT to Use These

| Scenario | Better Alternative |
|----------|-------------------|
| Static array, many queries | Prefix Sum (simpler) |
| Single range query | Just compute directly |
| Queries only, no updates | Sparse Table for min/max |
| Small n (< 100) | Brute force is fine |

---

## Summary

| Structure | Best For | Key Insight |
|-----------|----------|-------------|
| **Fenwick Tree** | Range sums with updates | `lowbit(i)` magic |
| **Segment Tree** | Any associative operation | Binary tree decomposition |
| **Merge Sort** | Counting pairs/inversions | Count during merge |

Master LC 307 first. The BIT template is the foundation for everything else.
