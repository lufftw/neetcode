## Top K Frequent Elements (LeetCode 347)

> **Problem**: Given an integer array, return the k most frequent elements.
> **Variant**: heap_top_k with frequency as sort key
> **Delta from 215**: Sort by frequency instead of value; bucket sort alternative.

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "k most frequent" | → Count frequencies, then top-k selection |
| "top k by some metric" | → Heap with custom comparator |
| "unique answer guaranteed" | → No tie-breaking needed |

### Implementation

```python
# Pattern: heap_top_k
# See: docs/patterns/heap/templates.md Section 2

from collections import Counter
import heapq

class SolutionHeap:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        """
        Find k most frequent elements using min-heap.

        Two-Phase Approach:
        1. Count frequencies: O(n)
        2. Top-k selection: O(m log k) where m = unique elements

        Why min-heap for max-frequency?
        - Store (frequency, element) tuples
        - Heap root = smallest frequency among top-k
        - Elements with higher frequency replace root
        """
        # Phase 1: Count frequencies
        frequency_map: dict[int, int] = Counter(nums)

        # Phase 2: Maintain min-heap of size k
        min_heap: list[tuple[int, int]] = []  # (frequency, element)

        for element, freq in frequency_map.items():
            if len(min_heap) < k:
                heapq.heappush(min_heap, (freq, element))
            elif freq > min_heap[0][0]:
                heapq.heapreplace(min_heap, (freq, element))

        # Extract elements (frequency is index 0, element is index 1)
        return [element for freq, element in min_heap]
```

### Trace Example

```
Input: nums = [1, 1, 1, 2, 2, 3], k = 2

Phase 1 - Count frequencies:
frequency_map = {1: 3, 2: 2, 3: 1}

Phase 2 - Min-heap selection:
(1, 3): heap = [(3, 1)]              (size < k)
(2, 2): heap = [(2, 2), (3, 1)]      (size = k, sorted by freq)
(3, 1): 1 < 2, skip                  (freq too low)

Result: [2, 1] or [1, 2] (order doesn't matter)
```

### Alternative: Bucket Sort

```python
class SolutionBucket:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        """
        Bucket sort approach: O(n) time.

        Key Insight:
        - Frequency is bounded: 1 <= freq <= n
        - Use array index as frequency bucket
        - Iterate from highest frequency bucket

        Why O(n)?
        - At most n distinct elements
        - At most n buckets (frequency 1 to n)
        - Single pass through buckets
        """
        frequency_map: dict[int, int] = Counter(nums)

        # Bucket: index = frequency, value = list of elements with that frequency
        # Frequency can be at most len(nums)
        buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]

        for element, freq in frequency_map.items():
            buckets[freq].append(element)

        # Collect k elements starting from highest frequency
        result: list[int] = []
        for freq in range(len(nums), 0, -1):
            for element in buckets[freq]:
                result.append(element)
                if len(result) == k:
                    return result

        return result
```

### Complexity Comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Min-heap | O(n + m log k) | O(m + k) | m = unique elements |
| Bucket sort | O(n) | O(n) | Better when m is large |
| Quickselect | O(n) avg | O(m) | In-place on frequency array |
| Sorting | O(n + m log m) | O(m) | Simple but slower |

### When to Use Each

| Scenario | Best Approach |
|----------|---------------|
| General case | Heap O(n + m log k) |
| k is large (k ≈ m) | Bucket sort O(n) |
| Memory constrained | Quickselect |
| Need sorted output | Sort by frequency |


