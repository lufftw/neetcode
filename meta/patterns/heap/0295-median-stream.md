## Find Median from Data Stream (LeetCode 295)

> **Problem**: Design a data structure that supports adding numbers and finding the median.
> **Pattern**: Two heaps (max-heap for lower half, min-heap for upper half)
> **Role**: BASE TEMPLATE for streaming median problems.

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "median" | → Two heaps or sorted structure |
| "data stream" / "online" | → Efficient insertion, O(log n) |
| "running median" | → Maintain sorted halves |

### The Two-Heap Insight

```
All numbers seen: [1, 2, 3, 4, 5]

           median
              ↓
Lower half: [1, 2]  |  Upper half: [3, 4, 5]
   max-heap ↑           ↑ min-heap

Median = 3 (odd count: min-heap root)
    or = (2 + 3) / 2 = 2.5 (even count: average of roots)
```

### Implementation

```python
# Pattern: heap_median_stream
# See: docs/patterns/heap/templates.md Section 3

import heapq

class MedianFinder:
    """
    Maintain median of a data stream using two heaps.

    Data Structure Design:
    - lower_half (max-heap): stores smaller half of numbers
    - upper_half (min-heap): stores larger half of numbers

    Invariants:
    1. All elements in lower_half <= all elements in upper_half
    2. Size difference: |lower_half| - |upper_half| <= 1
    3. If odd count, lower_half has one more element

    Why Two Heaps?
    - Median requires knowing the middle element(s)
    - Heaps give O(1) access to extreme values
    - Max-heap for lower half → O(1) access to largest of smaller numbers
    - Min-heap for upper half → O(1) access to smallest of larger numbers
    """

    def __init__(self):
        # Max-heap for lower half (store negatives for max-heap behavior)
        self.lower_half: list[int] = []  # max-heap via negation
        # Min-heap for upper half
        self.upper_half: list[int] = []  # min-heap

    def addNum(self, num: int) -> None:
        """
        Add number while maintaining heap invariants.

        Strategy:
        1. Always add to lower_half first (max-heap)
        2. Move largest from lower to upper (balances the halves)
        3. If upper becomes larger, move smallest back to lower

        This ensures:
        - Elements are correctly partitioned (lower <= upper)
        - Sizes are balanced (lower has equal or one more)
        """
        # Step 1: Add to lower half (max-heap, store negative)
        heapq.heappush(self.lower_half, -num)

        # Step 2: Move largest from lower to upper
        # This ensures lower_half max <= upper_half min
        largest_lower = -heapq.heappop(self.lower_half)
        heapq.heappush(self.upper_half, largest_lower)

        # Step 3: Rebalance if upper has more elements
        if len(self.upper_half) > len(self.lower_half):
            smallest_upper = heapq.heappop(self.upper_half)
            heapq.heappush(self.lower_half, -smallest_upper)

    def findMedian(self) -> float:
        """
        Return median in O(1) time.

        Cases:
        - Odd count: median is the root of lower_half (the extra element)
        - Even count: median is average of both roots
        """
        if len(self.lower_half) > len(self.upper_half):
            # Odd count: lower has one more
            return float(-self.lower_half[0])
        else:
            # Even count: average of two middle elements
            return (-self.lower_half[0] + self.upper_half[0]) / 2.0
```

### Trace Example

```
Operations: addNum(1), addNum(2), findMedian(), addNum(3), findMedian()

addNum(1):
  lower = [-1], upper = []
  Move: lower = [], upper = [1]
  Rebalance: lower = [-1], upper = []

addNum(2):
  lower = [-2, -1], upper = []
  Move: lower = [-1], upper = [2]
  Balanced: len(lower) == len(upper)

findMedian():
  Even count → (1 + 2) / 2 = 1.5

addNum(3):
  lower = [-3, -1], upper = [2]
  Move: lower = [-1], upper = [2, 3]
  Rebalance: lower = [-2, -1], upper = [3]

findMedian():
  Odd count → -lower[0] = 2

Visual state after all operations:
  lower (max-heap): [2, 1]  →  max = 2
  upper (min-heap): [3]     →  min = 3
  Median = 2 ✓
```

### Alternative: Sorted List

```python
from sortedcontainers import SortedList

class MedianFinderSorted:
    """
    Alternative using sorted container.
    Time: O(log n) add, O(1) find
    """

    def __init__(self):
        self.sorted_nums = SortedList()

    def addNum(self, num: int) -> None:
        self.sorted_nums.add(num)

    def findMedian(self) -> float:
        n = len(self.sorted_nums)
        mid = n // 2
        if n % 2 == 1:
            return float(self.sorted_nums[mid])
        return (self.sorted_nums[mid - 1] + self.sorted_nums[mid]) / 2.0
```

### Complexity Analysis

| Operation | Two Heaps | Sorted List | Array (naive) |
|-----------|-----------|-------------|---------------|
| addNum | O(log n) | O(log n) | O(n) |
| findMedian | O(1) | O(1) | O(n log n) |
| Space | O(n) | O(n) | O(n) |

### Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Forgetting negation | Max-heap doesn't work | Always negate for max-heap |
| Wrong rebalance condition | Median incorrect | Check `len(upper) > len(lower)` |
| Integer division | Python 2 vs 3 | Use `/ 2.0` for float |


