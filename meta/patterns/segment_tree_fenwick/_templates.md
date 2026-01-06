## Quick Reference Templates

### Fenwick Tree (Binary Indexed Tree)

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

### Segment Tree (Range Sum)

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

### Coordinate Compression Pattern

```python
def compress_coordinates(values: List[int]) -> dict[int, int]:
    """Map values to ranks 1..n for BIT usage."""
    sorted_unique = sorted(set(values))
    return {v: i + 1 for i, v in enumerate(sorted_unique)}
```

### Count Inversions Pattern (Right-to-Left)

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

### Merge Sort with Counting Pattern

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

