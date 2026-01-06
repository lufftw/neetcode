# Segment Tree / Fenwick Tree Pattern

## API Kernel: `SegmentTreeFenwick`

> **Core Mechanism**: Efficient range queries with point/range updates in O(log n) time using tree-based data structures.

**Segment Tree / Fenwick Tree** patterns solve the dynamic variant of range query problems. While Prefix Sum handles static arrays with O(1) range queries, these patterns handle **mutable arrays** where both queries and updates must be efficient.

---

## Two Core Data Structures

| Structure | Build | Query | Update | Space | Best For |
|-----------|-------|-------|--------|-------|----------|
| **Segment Tree** | O(n) | O(log n) | O(log n) | O(4n) | Range min/max, lazy propagation, flexible ops |
| **Fenwick Tree (BIT)** | O(n log n) | O(log n) | O(log n) | O(n) | Prefix sums, simpler implementation |

---

## When Prefix Sum Fails

| Scenario | Prefix Sum | Segment Tree / BIT |
|----------|------------|-------------------|
| Static array, many queries | ✅ O(1) query | ❌ Overkill |
| **Update + Query interleaved** | ❌ O(n) update | ✅ O(log n) both |
| Range min/max queries | ❌ Not supported | ✅ Segment Tree |
| Coordinate compression needed | ❌ | ✅ BIT with compression |

---

## Core Pattern: Range Sum with Updates

The fundamental problem: Given array `nums`, support:
- `update(index, val)`: Set `nums[index] = val`
- `sumRange(left, right)`: Return sum of `nums[left..right]`

**Key Insight**: Both operations must be O(log n) or better.

---

## Binary Indexed Tree (Fenwick Tree) Mechanics

```
Index:     1    2    3    4    5    6    7    8
BIT[i]:   [a1] [a1+a2] [a3] [a1..a4] [a5] [a5+a6] [a7] [a1..a8]

lowbit(i) = i & (-i)  # Isolate rightmost set bit

Query prefix[i]: sum BIT[i], BIT[i-lowbit(i)], ... until 0
Update index i:  add to BIT[i], BIT[i+lowbit(i)], ... until > n
```

---

## Segment Tree Mechanics

```
           [0..7]
         /        \
      [0..3]      [4..7]
      /    \      /    \
   [0..1] [2..3] [4..5] [6..7]
   /  \   /  \   /  \   /  \
  [0] [1] [2] [3] [4] [5] [6] [7]

Node i: left = 2*i+1, right = 2*i+2
Query/Update: O(log n) by traversing relevant path
```

---

## Advanced Applications

| Application | Technique | Problems |
|-------------|-----------|----------|
| Count inversions | BIT + coordinate compression | LC 315 |
| Count range sums | Segment Tree + sorted merge | LC 327 |
| 2D range queries | 2D Segment Tree / BIT | LC 308 |

---

