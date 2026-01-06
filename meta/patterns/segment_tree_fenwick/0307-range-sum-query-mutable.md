## Base Template: Range Sum Query - Mutable (LeetCode 307)

> **Problem**: Given an integer array `nums`, handle multiple queries: (1) update element at index, (2) query sum of range [left, right].
> **Invariant**: After each update, the data structure correctly represents the current array state.
> **Role**: BASE TEMPLATE for `SegmentTreeFenwick` API Kernel.

### Why This Problem?

This is the canonical "update + range query" problem. It demonstrates why Prefix Sum fails (O(n) updates) and why we need Segment Tree or Fenwick Tree (O(log n) both).

### Solution 1: Fenwick Tree (Binary Indexed Tree)

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

### Solution 2: Segment Tree

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

### Complexity Analysis

| Operation | Fenwick Tree | Segment Tree |
|-----------|-------------|--------------|
| Build | O(n log n) | O(n) |
| Update | O(log n) | O(log n) |
| Query | O(log n) | O(log n) |
| Space | O(n) | O(4n) |

### Trace Example (Fenwick Tree)

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

