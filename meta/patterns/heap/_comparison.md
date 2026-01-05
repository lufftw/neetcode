---

## Comparison with Similar Patterns

### Heap vs Sorting

| Aspect | Heap (Top-K) | Full Sort |
|--------|--------------|-----------|
| **Time** | O(n log k) | O(n log n) |
| **Space** | O(k) | O(n) |
| **Use When** | Only need k elements | Need all elements ordered |
| **Streaming** | ✅ Online algorithm | ❌ Requires all data |

### Heap vs Quickselect

| Aspect | Heap | Quickselect |
|--------|------|-------------|
| **Time (avg)** | O(n log k) | O(n) |
| **Time (worst)** | O(n log k) | O(n²) |
| **Space** | O(k) | O(1) in-place |
| **Stability** | Stable | Not stable |
| **Use When** | k is small, need all top-k | k is large (k ≈ n/2), only need kth |

### Two Heaps vs Sorted Container

| Aspect | Two Heaps | SortedList |
|--------|-----------|------------|
| **addNum** | O(log n) | O(log n) |
| **findMedian** | O(1) | O(1) |
| **Implementation** | Standard library | External dependency |
| **Memory** | 2 arrays | 1 sorted array |

### K-Way Merge: Heap vs Divide-and-Conquer

| Aspect | Min-Heap | Divide & Conquer |
|--------|----------|------------------|
| **Time** | O(N log k) | O(N log k) |
| **Space** | O(k) | O(1) iterative, O(log k) recursive |
| **Streaming** | ✅ Can process on-the-fly | ❌ Need all lists upfront |
| **Implementation** | Simpler | More code |


