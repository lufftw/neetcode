---

## Quick Reference Templates

### Template 1: Kth Largest (Min-Heap of Size K)

```python
import heapq

def find_kth_largest(nums: List[int], k: int) -> int:
    """Find kth largest element. Time: O(n log k), Space: O(k)"""
    min_heap = []
    for num in nums:
        if len(min_heap) < k:
            heapq.heappush(min_heap, num)
        elif num > min_heap[0]:
            heapq.heapreplace(min_heap, num)
    return min_heap[0]
```

### Template 2: Top-K Frequent

```python
from collections import Counter
import heapq

def top_k_frequent(nums: List[int], k: int) -> List[int]:
    """Find k most frequent elements. Time: O(n + m log k)"""
    freq = Counter(nums)
    min_heap = []
    for element, count in freq.items():
        if len(min_heap) < k:
            heapq.heappush(min_heap, (count, element))
        elif count > min_heap[0][0]:
            heapq.heapreplace(min_heap, (count, element))
    return [elem for _, elem in min_heap]
```

### Template 3: Two Heaps for Median

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.lower = []  # max-heap (negated)
        self.upper = []  # min-heap

    def add(self, num: int) -> None:
        heapq.heappush(self.lower, -num)
        heapq.heappush(self.upper, -heapq.heappop(self.lower))
        if len(self.upper) > len(self.lower):
            heapq.heappush(self.lower, -heapq.heappop(self.upper))

    def median(self) -> float:
        if len(self.lower) > len(self.upper):
            return float(-self.lower[0])
        return (-self.lower[0] + self.upper[0]) / 2.0
```

### Template 4: K-Way Merge

```python
import heapq

def merge_k_sorted(lists: List[List[int]]) -> List[int]:
    """Merge k sorted lists. Time: O(N log k)"""
    min_heap = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(min_heap, (lst[0], i, 0))

    result = []
    while min_heap:
        val, list_idx, elem_idx = heapq.heappop(min_heap)
        result.append(val)
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(min_heap, (next_val, list_idx, elem_idx + 1))
    return result
```

### Template 5: Interval Scheduling (Meeting Rooms)

```python
import heapq

def min_rooms(intervals: List[List[int]]) -> int:
    """Minimum rooms for non-overlapping meetings. Time: O(n log n)"""
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[0])
    end_times = []
    for start, end in intervals:
        if end_times and end_times[0] <= start:
            heapq.heapreplace(end_times, end)
        else:
            heapq.heappush(end_times, end)
    return len(end_times)
```

### Template 6: Greedy Simulation

```python
import heapq

def simulate_max_heap(items: List[int]) -> int:
    """Process items by repeatedly taking largest. Time: O(n log n)"""
    max_heap = [-x for x in items]
    heapq.heapify(max_heap)

    while len(max_heap) > 1:
        largest = -heapq.heappop(max_heap)
        second = -heapq.heappop(max_heap)
        # Process largest and second
        result = process(largest, second)
        if result > 0:
            heapq.heappush(max_heap, -result)

    return -max_heap[0] if max_heap else 0
```

### Common Heap Operations Reference

```python
import heapq

# Create heap
heap = []                    # Empty heap
heapq.heapify(list)          # Convert list to heap O(n)

# Add element
heapq.heappush(heap, val)    # Add element O(log n)

# Remove smallest
smallest = heapq.heappop(heap)  # Remove and return O(log n)

# Peek smallest
smallest = heap[0]           # View without removing O(1)

# Push then pop (optimized)
heapq.heappushpop(heap, val) # Push val, pop smallest O(log n)

# Pop then push (optimized)
heapq.heapreplace(heap, val) # Pop smallest, push val O(log n)

# Max-heap using negation
max_heap = [-x for x in items]
heapq.heapify(max_heap)
largest = -heapq.heappop(max_heap)
```


