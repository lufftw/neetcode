## Variant: Count of Smaller Numbers After Self (LeetCode 315)

> **Problem**: For each `nums[i]`, count how many `nums[j]` (j > i) are smaller than `nums[i]`.
> **Delta from Base**: Use BIT to count inversions with coordinate compression.
> **Role**: VARIANT demonstrating BIT for counting/frequency problems.

### Key Insight

Process array **right to left**. For each element:
1. Query: "How many elements smaller than current have we seen?"
2. Update: "Add current element to the data structure"

This requires **coordinate compression** since values can be large (-10^4 to 10^4).

### Coordinate Compression

```python
# Map values to ranks 1..n
sorted_unique = sorted(set(nums))
rank = {v: i + 1 for i, v in enumerate(sorted_unique)}

# Now use ranks instead of values in BIT
```

### Solution: Fenwick Tree with Coordinate Compression

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

### Why Right to Left?

| Direction | "Smaller after self" | Implementation |
|-----------|---------------------|----------------|
| Left to Right | Need to query "future" elements | ❌ Impossible |
| **Right to Left** | Seen elements = elements to the right | ✅ Natural |

### Alternative: Merge Sort with Counting

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

### Complexity

| Approach | Time | Space |
|----------|------|-------|
| BIT + Compression | O(n log n) | O(n) |
| Merge Sort | O(n log n) | O(n) |

### Trace Example (BIT)

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

