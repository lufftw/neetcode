## Advanced: Count of Range Sum (LeetCode 327)

> **Problem**: Count subarrays where `lower <= sum(nums[i..j]) <= upper`.
> **Delta from Base**: Combine prefix sum with BIT/Segment Tree for range counting.
> **Role**: ADVANCED combining prefix sum insight with range data structures.

### Key Insight

For subarray sum `[i..j]` to be in `[lower, upper]`:
- `lower <= prefix[j+1] - prefix[i] <= upper`
- Rearrange: `prefix[j+1] - upper <= prefix[i] <= prefix[j+1] - lower`

For each `j`, count how many previous `prefix[i]` fall in `[prefix[j+1]-upper, prefix[j+1]-lower]`.

### The Challenge

1. Prefix sums can be **large** and **negative** → need coordinate compression
2. Need to count elements in a **range** efficiently → BIT or Segment Tree
3. Process **left to right**, adding prefix sums as we go

### Solution: Merge Sort (Cleaner for This Problem)

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

### Solution: BIT with Coordinate Compression

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

### Why Merge Sort Works

During merge:
- `left` array = prefix sums with smaller original indices
- `right` array = prefix sums with larger original indices
- We count valid `(left[i], right[j])` pairs where `left[i] + lower <= right[j] <= left[i] + upper`

Since both arrays are **sorted**, we can use two-pointer technique for efficient counting.

### Complexity

| Approach | Time | Space |
|----------|------|-------|
| Merge Sort | O(n log n) | O(n) |
| BIT + Compression | O(n log n) | O(n) |

### Trace Example (Merge Sort)

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

