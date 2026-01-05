# Heap / Priority Queue Patterns: Complete Reference

> **API Kernel**: `HeapTopK`
> **Core Mechanism**: Maintain a bounded collection of elements with efficient access to extreme values (min/max).

This document presents the **canonical heap templates** for top-k selection, streaming median, k-way merge, and greedy scheduling problems. Each implementation follows consistent naming conventions and includes detailed logic explanations.

---

## Core Concepts

### The Heap Property

A heap is a complete binary tree satisfying the heap property:
- **Min-Heap**: Parent ≤ children (root is minimum)
- **Max-Heap**: Parent ≥ children (root is maximum)

```
Min-Heap Example:
        1           Operations:
       / \          - push: O(log n)
      3   2         - pop: O(log n)
     / \            - peek: O(1)
    5   4           - heapify: O(n)
```

### Python heapq Module

Python's `heapq` implements a **min-heap**. For max-heap behavior, negate values:

```python
import heapq

# Min-heap (default)
min_heap = []
heapq.heappush(min_heap, 5)
smallest = heapq.heappop(min_heap)

# Max-heap (negate values)
max_heap = []
heapq.heappush(max_heap, -5)  # Store negative
largest = -heapq.heappop(max_heap)  # Negate on retrieval
```

### Universal Heap Template

```python
def heap_top_k(elements: Iterable[T], k: int, key: Callable = None) -> List[T]:
    """
    Find top-k elements efficiently.

    Strategy: Maintain a min-heap of size k.
    - Elements larger than heap root replace the root
    - After processing, heap contains k largest elements

    Time: O(n log k), Space: O(k)

    Why min-heap for max problem?
    - Min-heap root is the smallest of the k largest
    - Easy to check if new element should enter the set
    - If new_element > root, it belongs in top-k; evict root
    """
    min_heap = []

    for element in elements:
        val = key(element) if key else element

        if len(min_heap) < k:
            heapq.heappush(min_heap, (val, element))
        elif val > min_heap[0][0]:
            heapq.heapreplace(min_heap, (val, element))

    return [item[1] for item in min_heap]
```

### Pattern Variants

| Variant | API Kernel | Use When | Key Insight |
|---------|------------|----------|-------------|
| **Kth Element** | `HeapTopK` | Find kth largest/smallest | Min-heap of size k, root is answer |
| **Top-K** | `HeapTopK` | Find k largest/smallest elements | Same as kth, return all k elements |
| **Streaming Median** | `HeapTopK` | Maintain median over stream | Two heaps: max-heap for lower, min-heap for upper |
| **K-Way Merge** | `KWayMerge` | Merge k sorted sequences | Min-heap of k heads, always pop smallest |
| **Interval Scheduling** | `HeapTopK` | Meeting rooms, overlapping intervals | Min-heap of end times for greedy assignment |
| **Task Scheduler** | `HeapTopK` | Schedule with cooldown constraints | Max-heap for greedy selection by frequency |
| **Greedy Simulation** | `HeapTopK` | Repeatedly process largest/smallest | Max-heap for repeated extraction |

### Heap Size Strategies

| Strategy | When to Use | Time Complexity |
|----------|-------------|-----------------|
| **Size k min-heap** | Top-k largest, kth largest | O(n log k) |
| **Size k max-heap** | Top-k smallest, kth smallest | O(n log k) |
| **Full heap** | Need all elements ordered | O(n log n) |
| **Two heaps** | Running median, balanced partition | O(n log n) |


