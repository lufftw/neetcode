# Segment Tree / Fenwick Tree Pattern

## Table of Contents

1. [API Kernel: `SegmentTreeFenwick`](#1-api-kernel-segmenttreefenwick)
2. [Two Core Data Structures](#2-two-core-data-structures)
3. [When Prefix Sum Fails](#3-when-prefix-sum-fails)
4. [Core Pattern: Range Sum with Updates](#4-core-pattern-range-sum-with-updates)
5. [Binary Indexed Tree (Fenwick Tree) Mechanics](#5-binary-indexed-tree-fenwick-tree-mechanics)
6. [Segment Tree Mechanics](#6-segment-tree-mechanics)
7. [Advanced Applications](#7-advanced-applications)
8. [Base Template: Range Sum Query - Mutable (LeetCode 307)](#8-base-template-range-sum-query---mutable-leetcode-307)
9. [Variant: Count of Smaller Numbers After Self (LeetCode 315)](#9-variant-count-of-smaller-numbers-after-self-leetcode-315)
10. [Advanced: Count of Range Sum (LeetCode 327)](#10-advanced-count-of-range-sum-leetcode-327)
11. [Pattern Comparison](#11-pattern-comparison)
12. [Decision Flowchart](#12-decision-flowchart)
13. [Quick Reference Templates](#13-quick-reference-templates)

---

## 1. API Kernel: `SegmentTreeFenwick`

> **Core Mechanism**: Efficient range queries with point/range updates in O(log n) time using tree-based data structures.

**Segment Tree / Fenwick Tree** patterns solve the dynamic variant of range query problems. While Prefix Sum handles static arrays with O(1) range queries, these patterns handle **mutable arrays** where both queries and updates must be efficient.

---

## 2. Two Core Data Structures

| Structure | Build | Query | Update | Space | Best For |
|-----------|-------|-------|--------|-------|----------|
| **Segment Tree** | O(n) | O(log n) | O(log n) | O(4n) | Range min/max, lazy propagation, flexible ops |
| **Fenwick Tree (BIT)** | O(n log n) | O(log n) | O(log n) | O(n) | Prefix sums, simpler implementation |

---

## 3. When Prefix Sum Fails

| Scenario | Prefix Sum | Segment Tree / BIT |
|----------|------------|-------------------|
| Static array, many queries | ✅ O(1) query | ❌ Overkill |
| **Update + Query interleaved** | ❌ O(n) update | ✅ O(log n) both |
| Range min/max queries | ❌ Not supported | ✅ Segment Tree |
| Coordinate compression needed | ❌ | ✅ BIT with compression |

---

## 4. Core Pattern: Range Sum with Updates

The fundamental problem: Given array `nums`, support:
- `update(index, val)`: Set `nums[index] = val`
- `sumRange(left, right)`: Return sum of `nums[left..right]`

**Key Insight**: Both operations must be O(log n) or better.

---

## 5. Binary Indexed Tree (Fenwick Tree) Mechanics

```
Index:     1    2    3    4    5    6    7    8
BIT[i]:   [a1] [a1+a2] [a3] [a1..a4] [a5] [a5+a6] [a7] [a1..a8]

lowbit(i) = i & (-i)  # Isolate rightmost set bit

Query prefix[i]: sum BIT[i], BIT[i-lowbit(i)], ... until 0
Update index i:  add to BIT[i], BIT[i+lowbit(i)], ... until > n
```

---

## 6. Segment Tree Mechanics

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

## 7. Advanced Applications

| Application | Technique | Problems |
|-------------|-----------|----------|
| Count inversions | BIT + coordinate compression | LC 315 |
| Count range sums | Segment Tree + sorted merge | LC 327 |
| 2D range queries | 2D Segment Tree / BIT | LC 308 |

---

## 8. Base Template: Range Sum Query - Mutable (LeetCode 307)

> **Problem**: Given an integer array `nums`, handle multiple queries: (1) update element at index, (2) query sum of range [left, right].
> **Invariant**: After each update, the data structure correctly represents the current array state.
> **Role**: BASE TEMPLATE for `SegmentTreeFenwick` API Kernel.

### 8.1 Why This Problem?

This is the canonical "update + range query" problem. It demonstrates why Prefix Sum fails (O(n) updates) and why we need Segment Tree or Fenwick Tree (O(log n) both).

### 8.2 Solution 1: Fenwick Tree (Binary Indexed Tree)

```python
class NumArray:
    def __init__(self, nums: List[int]) -> None:
        self.n = len(nums)
        self.nums = nums[:]
        self.tree = [0] * (self.n + 1)  # 1-indexed

        # Build BIT in O(n log n)
        for i, num in enumerate(nums):
            self._add(i + 1, num)

    def _lowbit(self, x: int) -> int:
        """Get rightmost set bit."""
        return x & (-x)

    def _add(self, i: int, delta: int) -> None:
        """Add delta to index i (1-indexed)."""
        while i <= self.n:
            self.tree[i] += delta
            i += self._lowbit(i)

    def _prefix_sum(self, i: int) -> int:
        """Get prefix sum [1..i]."""
        total = 0
        while i > 0:
            total += self.tree[i]
            i -= self._lowbit(i)
        return total

    def update(self, index: int, val: int) -> None:
        delta = val - self.nums[index]
        self.nums[index] = val
        self._add(index + 1, delta)

    def sumRange(self, left: int, right: int) -> int:
        return self._prefix_sum(right + 1) - self._prefix_sum(left)
```

### 8.3 Solution 2: Segment Tree

```python
class NumArray:
    def __init__(self, nums: List[int]) -> None:
        self.n = len(nums)
        self.tree = [0] * (4 * self.n)  # 4n space for safety
        self.nums = nums
        if nums:
            self._build(0, 0, self.n - 1)

    def _build(self, node: int, start: int, end: int) -> None:
        if start == end:
            self.tree[node] = self.nums[start]
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2
            self._build(left_child, start, mid)
            self._build(right_child, mid + 1, end)
            self.tree[node] = self.tree[left_child] + self.tree[right_child]

    def update(self, index: int, val: int) -> None:
        self._update(0, 0, self.n - 1, index, val)

    def _update(self, node: int, start: int, end: int, idx: int, val: int) -> None:
        if start == end:
            self.tree[node] = val
            self.nums[idx] = val
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2
            if idx <= mid:
                self._update(left_child, start, mid, idx, val)
            else:
                self._update(right_child, mid + 1, end, idx, val)
            self.tree[node] = self.tree[left_child] + self.tree[right_child]

    def sumRange(self, left: int, right: int) -> int:
        return self._query(0, 0, self.n - 1, left, right)

    def _query(self, node: int, start: int, end: int, l: int, r: int) -> int:
        if r < start or l > end:
            return 0  # Out of range
        if l <= start and end <= r:
            return self.tree[node]  # Fully covered
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        return (self._query(left_child, start, mid, l, r) +
                self._query(right_child, mid + 1, end, l, r))
```

### 8.4 Complexity Analysis

| Operation | Fenwick Tree | Segment Tree |
|-----------|-------------|--------------|
| Build | O(n log n) | O(n) |
| Update | O(log n) | O(log n) |
| Query | O(log n) | O(log n) |
| Space | O(n) | O(4n) |

### 8.5 Trace Example (Fenwick Tree)

```
nums = [1, 3, 5, 7, 9, 11]
BIT:   [0, 1, 4, 5, 16, 9, 20]  (1-indexed)

sumRange(1, 3):
  prefix[4] - prefix[1]
  = (16) - (1)
  = 15 ✓ (3 + 5 + 7 = 15)

update(2, 6):  # nums[2] = 5 → 6, delta = 1
  _add(3, 1): tree[3] += 1, tree[4] += 1
  BIT: [0, 1, 4, 6, 17, 9, 21]
```

---

## 9. Variant: Count of Smaller Numbers After Self (LeetCode 315)

> **Problem**: For each `nums[i]`, count how many `nums[j]` (j > i) are smaller than `nums[i]`.
> **Delta from Base**: Use BIT to count inversions with coordinate compression.
> **Role**: VARIANT demonstrating BIT for counting/frequency problems.

### 9.1 Key Insight

Process array **right to left**. For each element:
1. Query: "How many elements smaller than current have we seen?"
2. Update: "Add current element to the data structure"

This requires **coordinate compression** since values can be large (-10^4 to 10^4).

### 9.2 Coordinate Compression

```python
# Map values to ranks 1..n
sorted_unique = sorted(set(nums))
rank = {v: i + 1 for i, v in enumerate(sorted_unique)}

# Now use ranks instead of values in BIT
```

### 9.3 Solution: Fenwick Tree with Coordinate Compression

```python
class Solution:
    def countSmaller(self, nums: List[int]) -> List[int]:
        if not nums:
            return []

        # Coordinate compression
        sorted_unique = sorted(set(nums))
        rank_map = {v: i + 1 for i, v in enumerate(sorted_unique)}
        n = len(sorted_unique)

        # BIT for counting
        tree = [0] * (n + 1)

        def lowbit(x: int) -> int:
            return x & (-x)

        def update(i: int) -> None:
            """Increment count at rank i."""
            while i <= n:
                tree[i] += 1
                i += lowbit(i)

        def query(i: int) -> int:
            """Count elements with rank <= i."""
            total = 0
            while i > 0:
                total += tree[i]
                i -= lowbit(i)
            return total

        result = []
        # Process right to left
        for num in reversed(nums):
            rank = rank_map[num]
            # Count elements smaller than current (rank - 1)
            count = query(rank - 1)
            result.append(count)
            # Add current element
            update(rank)

        return result[::-1]
```

### 9.4 Why Right to Left?

| Direction | "Smaller after self" | Implementation |
|-----------|---------------------|----------------|
| Left to Right | Need to query "future" elements | ❌ Impossible |
| **Right to Left** | Seen elements = elements to the right | ✅ Natural |

### 9.5 Alternative: Merge Sort with Counting

```python
class Solution:
    def countSmaller(self, nums: List[int]) -> List[int]:
        counts = [0] * len(nums)
        indexed = [(num, i) for i, num in enumerate(nums)]

        def merge_sort(arr):
            if len(arr) <= 1:
                return arr

            mid = len(arr) // 2
            left = merge_sort(arr[:mid])
            right = merge_sort(arr[mid:])
            return merge(left, right)

        def merge(left, right):
            result = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i][0] <= right[j][0]:
                    # Count: j elements in right are smaller
                    counts[left[i][1]] += j
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            while i < len(left):
                counts[left[i][1]] += j
                result.append(left[i])
                i += 1
            result.extend(right[j:])
            return result

        merge_sort(indexed)
        return counts
```

### 9.6 Complexity

| Approach | Time | Space |
|----------|------|-------|
| BIT + Compression | O(n log n) | O(n) |
| Merge Sort | O(n log n) | O(n) |

### 9.7 Trace Example (BIT)

```
nums = [5, 2, 6, 1]
ranks: {1:1, 2:2, 5:3, 6:4}

Process right to left:
  i=3: num=1, rank=1, query(0)=0, update(1)  → count=0
  i=2: num=6, rank=4, query(3)=1, update(4)  → count=1
  i=1: num=2, rank=2, query(1)=1, update(2)  → count=1
  i=0: num=5, rank=3, query(2)=2, update(3)  → count=2

Result (reversed): [2, 1, 1, 0] ✓
```

---

## 10. Advanced: Count of Range Sum (LeetCode 327)

> **Problem**: Count subarrays where `lower <= sum(nums[i..j]) <= upper`.
> **Delta from Base**: Combine prefix sum with BIT/Segment Tree for range counting.
> **Role**: ADVANCED combining prefix sum insight with range data structures.

### 10.1 Key Insight

For subarray sum `[i..j]` to be in `[lower, upper]`:
- `lower <= prefix[j+1] - prefix[i] <= upper`
- Rearrange: `prefix[j+1] - upper <= prefix[i] <= prefix[j+1] - lower`

For each `j`, count how many previous `prefix[i]` fall in `[prefix[j+1]-upper, prefix[j+1]-lower]`.

### 10.2 The Challenge

1. Prefix sums can be **large** and **negative** → need coordinate compression
2. Need to count elements in a **range** efficiently → BIT or Segment Tree
3. Process **left to right**, adding prefix sums as we go

### 10.3 Solution: Merge Sort (Cleaner for This Problem)

```python
class Solution:
    def countRangeSum(self, nums: List[int], lower: int, upper: int) -> int:
        # Compute prefix sums
        prefix = [0]
        for num in nums:
            prefix.append(prefix[-1] + num)

        self.count = 0

        def merge_sort(arr: List[int]) -> List[int]:
            if len(arr) <= 1:
                return arr

            mid = len(arr) // 2
            left = merge_sort(arr[:mid])
            right = merge_sort(arr[mid:])
            return merge(left, right)

        def merge(left: List[int], right: List[int]) -> List[int]:
            # Count valid pairs (i from left, j from right means i < j in original)
            j_low = j_high = 0
            for prefix_i in left:
                # Find range [prefix_i + lower, prefix_i + upper] in right
                while j_low < len(right) and right[j_low] < prefix_i + lower:
                    j_low += 1
                while j_high < len(right) and right[j_high] <= prefix_i + upper:
                    j_high += 1
                self.count += j_high - j_low

            # Standard merge
            result = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            result.extend(left[i:])
            result.extend(right[j:])
            return result

        merge_sort(prefix)
        return self.count
```

### 10.4 Solution: BIT with Coordinate Compression

```python
class Solution:
    def countRangeSum(self, nums: List[int], lower: int, upper: int) -> int:
        # Compute prefix sums
        prefix = [0]
        for num in nums:
            prefix.append(prefix[-1] + num)

        # Collect all values we need to query
        all_values = set(prefix)
        for p in prefix:
            all_values.add(p - lower)
            all_values.add(p - upper)

        # Coordinate compression
        sorted_vals = sorted(all_values)
        rank = {v: i + 1 for i, v in enumerate(sorted_vals)}
        n = len(sorted_vals)

        # BIT
        tree = [0] * (n + 1)

        def lowbit(x):
            return x & (-x)

        def update(i):
            while i <= n:
                tree[i] += 1
                i += lowbit(i)

        def query(i):
            total = 0
            while i > 0:
                total += tree[i]
                i -= lowbit(i)
            return total

        def range_query(l, r):
            if l > r:
                return 0
            return query(r) - query(l - 1)

        count = 0
        for p in prefix:
            # Count prefix sums in [p - upper, p - lower]
            lo = rank.get(p - upper, 0)
            hi = rank.get(p - lower, 0)
            if lo and hi:
                count += range_query(lo, hi)
            # Add current prefix sum
            update(rank[p])

        return count
```

### 10.5 Why Merge Sort Works

During merge:
- `left` array = prefix sums with smaller original indices
- `right` array = prefix sums with larger original indices
- We count valid `(left[i], right[j])` pairs where `left[i] + lower <= right[j] <= left[i] + upper`

Since both arrays are **sorted**, we can use two-pointer technique for efficient counting.

### 10.6 Complexity

| Approach | Time | Space |
|----------|------|-------|
| Merge Sort | O(n log n) | O(n) |
| BIT + Compression | O(n log n) | O(n) |

### 10.7 Trace Example (Merge Sort)

```
nums = [-2, 5, -1], lower = -2, upper = 2
prefix = [0, -2, 3, 2]

After merge sort counts all valid pairs:
  (prefix[0]=0, prefix[1]=-2): diff=-2 ✓
  (prefix[0]=0, prefix[3]=2): diff=2 ✓
  (prefix[1]=-2, prefix[3]=2): diff=4 ✗
  (prefix[2]=3, prefix[3]=2): diff=-1 ✓

Result: 3 ✓
```

---

## 11. Pattern Comparison

| Problem | Pattern | Data Structure | Key Technique |
|---------|---------|----------------|---------------|
| LC 307 | Range Sum + Update | BIT or Segment Tree | Direct point update |
| LC 315 | Count Inversions | BIT + Compression | Right-to-left counting |
| LC 327 | Range Sum Count | Merge Sort or BIT | Prefix sum + range counting |

### 11.1 When to Use Which

| Scenario | Best Choice | Why |
|----------|-------------|-----|
| Simple range sum with updates | **Fenwick Tree** | Simpler, less code |
| Range min/max queries | **Segment Tree** | BIT only works for prefix sums |
| Counting/frequency with compression | **BIT** | Natural fit for prefix queries |
| 2D range queries | **2D Segment Tree** | More flexible than 2D BIT |

### 11.2 Complexity Summary

| Problem | Time Complexity | Space Complexity |
|---------|-----------------|------------------|
| LC 307 | O(n) build + O(log n) ops | O(n) |
| LC 315 | O(n log n) | O(n) |
| LC 327 | O(n log n) | O(n) |

---

## 12. Decision Flowchart

```
                    Range Query Problem?
                           │
                           ▼
              ┌─────────────────────────┐
              │   Is the array mutable   │
              │   (updates + queries)?   │
              └─────────────────────────┘
                    │             │
                   YES            NO
                    │             │
                    ▼             ▼
           Segment Tree    Prefix Sum
           or Fenwick Tree  (O(1) query)
                    │
                    ▼
        ┌────────────────────────┐
        │  What type of query?   │
        └────────────────────────┘
              │         │
         Range Sum   Range Min/Max
              │         │
              ▼         ▼
         Fenwick    Segment Tree
          Tree      (BIT doesn't
                     support this)
```

### 12.1 Key Decision Points

| Signal | Use This |
|--------|----------|
| "update element" + "query range sum" | BIT or Segment Tree |
| "update element" + "query range min/max" | Segment Tree only |
| "count elements in range" | BIT with coordinate compression |
| "count inversions" | BIT (process right-to-left) or Merge Sort |
| "count subarrays with sum in [L, R]" | Merge Sort with counting |

### 12.2 Problem Pattern Recognition

| If you see... | Think... |
|---------------|----------|
| `update(index, val)` + `sumRange(left, right)` | BIT (simpler) |
| Values too large, need compression | Coordinate compression + BIT |
| "count smaller after self" | BIT right-to-left |
| "count pairs satisfying condition" | Merge Sort with counting |
| 2D array with updates | 2D Segment Tree |

---

## 13. Quick Reference Templates

### 13.1 Fenwick Tree (Binary Indexed Tree)

```python
class FenwickTree:
    """Fenwick Tree for range sum queries with point updates."""

    def __init__(self, n: int) -> None:
        self.n = n
        self.tree = [0] * (n + 1)  # 1-indexed

    def _lowbit(self, x: int) -> int:
        """Get rightmost set bit."""
        return x & (-x)

    def update(self, i: int, delta: int) -> None:
        """Add delta to index i (1-indexed)."""
        while i <= self.n:
            self.tree[i] += delta
            i += self._lowbit(i)

    def prefix_sum(self, i: int) -> int:
        """Get prefix sum [1..i]."""
        total = 0
        while i > 0:
            total += self.tree[i]
            i -= self._lowbit(i)
        return total

    def range_sum(self, l: int, r: int) -> int:
        """Get range sum [l..r]."""
        return self.prefix_sum(r) - self.prefix_sum(l - 1)
```

### 13.2 Segment Tree (Range Sum)

```python
class SegmentTree:
    """Segment Tree for range sum queries with point updates."""

    def __init__(self, nums: List[int]) -> None:
        self.n = len(nums)
        self.tree = [0] * (4 * self.n)
        self.nums = nums
        if nums:
            self._build(0, 0, self.n - 1)

    def _build(self, node: int, start: int, end: int) -> None:
        if start == end:
            self.tree[node] = self.nums[start]
        else:
            mid = (start + end) // 2
            self._build(2 * node + 1, start, mid)
            self._build(2 * node + 2, mid + 1, end)
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]

    def update(self, idx: int, val: int) -> None:
        self._update(0, 0, self.n - 1, idx, val)

    def _update(self, node: int, start: int, end: int, idx: int, val: int) -> None:
        if start == end:
            self.tree[node] = val
            self.nums[idx] = val
        else:
            mid = (start + end) // 2
            if idx <= mid:
                self._update(2 * node + 1, start, mid, idx, val)
            else:
                self._update(2 * node + 2, mid + 1, end, idx, val)
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]

    def query(self, l: int, r: int) -> int:
        return self._query(0, 0, self.n - 1, l, r)

    def _query(self, node: int, start: int, end: int, l: int, r: int) -> int:
        if r < start or l > end:
            return 0
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return (self._query(2 * node + 1, start, mid, l, r) +
                self._query(2 * node + 2, mid + 1, end, l, r))
```

### 13.3 Coordinate Compression Pattern

```python
def compress_coordinates(values: List[int]) -> dict[int, int]:
    """Map values to ranks 1..n for BIT usage."""
    sorted_unique = sorted(set(values))
    return {v: i + 1 for i, v in enumerate(sorted_unique)}
```

### 13.4 Count Inversions Pattern (Right-to-Left)

```python
def count_smaller_after_self(nums: List[int]) -> List[int]:
    """Count elements smaller than nums[i] to its right."""
    # Coordinate compression
    rank = compress_coordinates(nums)
    n = len(rank)
    bit = FenwickTree(n)

    result = []
    for num in reversed(nums):
        r = rank[num]
        # Query: count of elements with rank < r
        count = bit.prefix_sum(r - 1)
        result.append(count)
        # Update: add current element
        bit.update(r, 1)

    return result[::-1]
```

### 13.5 Merge Sort with Counting Pattern

```python
def merge_sort_count(arr: List[int], count_condition) -> int:
    """Merge sort that counts pairs satisfying a condition."""
    total_count = 0

    def merge_sort(arr):
        nonlocal total_count
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])

        # Count valid pairs before merging
        # Left elements have smaller original indices
        # Right elements have larger original indices
        # Use two pointers for efficient counting
        # ... (problem-specific counting logic)

        # Standard merge
        return merge(left, right)

    merge_sort(arr)
    return total_count
```



---



*Document generated for NeetCode Practice Framework — API Kernel: segment_tree_fenwick*
