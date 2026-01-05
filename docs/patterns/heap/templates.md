# Heap / Priority Queue Patterns: Complete Reference

> **API Kernel**: `HeapTopK`
> **Core Mechanism**: Maintain a bounded collection of elements with efficient access to extreme values (min/max).

This document presents the **canonical heap templates** for top-k selection, streaming median, k-way merge, and greedy scheduling problems. Each implementation follows consistent naming conventions and includes detailed logic explanations.

---

## Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Base Template: Kth Largest Element (LeetCode 215)](#2-base-template-kth-largest-element-leetcode-215)
3. [Top K Frequent Elements (LeetCode 347)](#3-top-k-frequent-elements-leetcode-347)
4. [Find Median from Data Stream (LeetCode 295)](#4-find-median-from-data-stream-leetcode-295)
5. [Merge K Sorted Lists (LeetCode 23)](#5-merge-k-sorted-lists-leetcode-23)
6. [Meeting Rooms II (LeetCode 253)](#6-meeting-rooms-ii-leetcode-253)
7. [Task Scheduler (LeetCode 621)](#7-task-scheduler-leetcode-621)
8. [Last Stone Weight (LeetCode 1046)](#8-last-stone-weight-leetcode-1046)
9. [Comparison with Similar Patterns](#9-comparison-with-similar-patterns)
10. [Decision Flowchart](#10-decision-flowchart)
11. [Quick Reference Templates](#11-quick-reference-templates)

---

## 1. Core Concepts

### 1.1 The Heap Property

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

### 1.2 Python heapq Module

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

### 1.3 Universal Heap Template

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

### 1.4 Pattern Variants

| Variant | API Kernel | Use When | Key Insight |
|---------|------------|----------|-------------|
| **Kth Element** | `HeapTopK` | Find kth largest/smallest | Min-heap of size k, root is answer |
| **Top-K** | `HeapTopK` | Find k largest/smallest elements | Same as kth, return all k elements |
| **Streaming Median** | `HeapTopK` | Maintain median over stream | Two heaps: max-heap for lower, min-heap for upper |
| **K-Way Merge** | `KWayMerge` | Merge k sorted sequences | Min-heap of k heads, always pop smallest |
| **Interval Scheduling** | `HeapTopK` | Meeting rooms, overlapping intervals | Min-heap of end times for greedy assignment |
| **Task Scheduler** | `HeapTopK` | Schedule with cooldown constraints | Max-heap for greedy selection by frequency |
| **Greedy Simulation** | `HeapTopK` | Repeatedly process largest/smallest | Max-heap for repeated extraction |

### 1.5 Heap Size Strategies

| Strategy | When to Use | Time Complexity |
|----------|-------------|-----------------|
| **Size k min-heap** | Top-k largest, kth largest | O(n log k) |
| **Size k max-heap** | Top-k smallest, kth smallest | O(n log k) |
| **Full heap** | Need all elements ordered | O(n log n) |
| **Two heaps** | Running median, balanced partition | O(n log n) |

---

## 2. Base Template: Kth Largest Element (LeetCode 215)

> **Problem**: Find the kth largest element in an unsorted array.
> **Invariant**: Min-heap of size k contains the k largest elements; root is the kth largest.
> **Role**: BASE TEMPLATE for `HeapTopK` API Kernel.

### 2.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "kth largest/smallest" | → Heap of size k |
| "without sorting" | → Quickselect or heap |
| "stream of numbers" | → Online algorithm with heap |

### 2.2 Implementation

```python
# Pattern: heap_kth_element
# See: docs/patterns/heap/templates.md Section 1 (Base Template)

class SolutionHeap:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        """
        Find kth largest using min-heap of size k.

        Key Insight:
        - Maintain k largest elements seen so far in a min-heap
        - Root of min-heap = smallest of the k largest = kth largest

        Why min-heap for max problem?
        - When new element > root, it belongs in top-k
        - Replace root (smallest of k largest) with new element
        - After n elements, root is exactly the kth largest
        """
        import heapq

        # Min-heap stores k largest elements
        min_heap: list[int] = []

        for num in nums:
            if len(min_heap) < k:
                # Phase 1: Fill heap until size k
                heapq.heappush(min_heap, num)
            elif num > min_heap[0]:
                # Phase 2: New element larger than kth largest
                # Replace the current kth largest
                heapq.heapreplace(min_heap, num)

        # Root is the kth largest element
        return min_heap[0]
```

### 2.3 Trace Example

```
Input: nums = [3, 2, 1, 5, 6, 4], k = 2

Step-by-step heap evolution:
num=3: heap=[3]          (fill phase, size < k)
num=2: heap=[2, 3]       (fill phase, size = k)
num=1: heap=[2, 3]       (1 < 2, skip)
num=5: heap=[3, 5]       (5 > 2, replace root)
num=6: heap=[5, 6]       (6 > 3, replace root)
num=4: heap=[5, 6]       (4 < 5, skip)

Result: heap[0] = 5 (2nd largest)

Visual verification:
Sorted descending: [6, 5, 4, 3, 2, 1]
                       ↑
                   2nd largest = 5 ✓
```

### 2.4 Alternative: Quickselect

```python
class SolutionQuickselect:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        """
        Quickselect algorithm: O(n) average, O(n²) worst.

        Partition-based selection without full sorting.
        Use random pivot to avoid worst-case on sorted input.
        """
        import random

        target_idx = k - 1  # kth largest at index k-1 in descending order

        def partition(left: int, right: int) -> int:
            # Random pivot to avoid O(n²) on sorted arrays
            pivot_idx = random.randint(left, right)
            pivot_val = nums[pivot_idx]
            nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]

            store_idx = left
            for i in range(left, right):
                if nums[i] >= pivot_val:  # >= for descending order
                    nums[store_idx], nums[i] = nums[i], nums[store_idx]
                    store_idx += 1

            nums[store_idx], nums[right] = nums[right], nums[store_idx]
            return store_idx

        left, right = 0, len(nums) - 1
        while left <= right:
            pivot_idx = partition(left, right)
            if pivot_idx == target_idx:
                return nums[pivot_idx]
            elif pivot_idx < target_idx:
                left = pivot_idx + 1
            else:
                right = pivot_idx - 1

        return nums[left]
```

### 2.5 Complexity Comparison

| Approach | Time (Average) | Time (Worst) | Space |
|----------|----------------|--------------|-------|
| Min-heap size k | O(n log k) | O(n log k) | O(k) |
| Quickselect | O(n) | O(n²) | O(1) |
| Sorting | O(n log n) | O(n log n) | O(n) |

### 2.6 When to Use Each

| Scenario | Best Approach |
|----------|---------------|
| k is small (k << n) | Min-heap O(n log k) ≈ O(n) |
| k ≈ n/2 | Quickselect O(n) |
| Need top-k elements, not just kth | Min-heap |
| Streaming data | Min-heap (online algorithm) |
| Memory constrained | Quickselect (in-place) |

---

## 3. Top K Frequent Elements (LeetCode 347)

> **Problem**: Given an integer array, return the k most frequent elements.
> **Variant**: heap_top_k with frequency as sort key
> **Delta from 215**: Sort by frequency instead of value; bucket sort alternative.

### 3.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "k most frequent" | → Count frequencies, then top-k selection |
| "top k by some metric" | → Heap with custom comparator |
| "unique answer guaranteed" | → No tie-breaking needed |

### 3.2 Implementation

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

### 3.3 Trace Example

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

### 3.4 Alternative: Bucket Sort

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

### 3.5 Complexity Comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Min-heap | O(n + m log k) | O(m + k) | m = unique elements |
| Bucket sort | O(n) | O(n) | Better when m is large |
| Quickselect | O(n) avg | O(m) | In-place on frequency array |
| Sorting | O(n + m log m) | O(m) | Simple but slower |

### 3.6 When to Use Each

| Scenario | Best Approach |
|----------|---------------|
| General case | Heap O(n + m log k) |
| k is large (k ≈ m) | Bucket sort O(n) |
| Memory constrained | Quickselect |
| Need sorted output | Sort by frequency |

---

## 4. Find Median from Data Stream (LeetCode 295)

> **Problem**: Design a data structure that supports adding numbers and finding the median.
> **Pattern**: Two heaps (max-heap for lower half, min-heap for upper half)
> **Role**: BASE TEMPLATE for streaming median problems.

### 4.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "median" | → Two heaps or sorted structure |
| "data stream" / "online" | → Efficient insertion, O(log n) |
| "running median" | → Maintain sorted halves |

### 4.2 The Two-Heap Insight

```
All numbers seen: [1, 2, 3, 4, 5]

           median
              ↓
Lower half: [1, 2]  |  Upper half: [3, 4, 5]
   max-heap ↑           ↑ min-heap

Median = 3 (odd count: min-heap root)
    or = (2 + 3) / 2 = 2.5 (even count: average of roots)
```

### 4.3 Implementation

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

### 4.4 Trace Example

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

### 4.5 Alternative: Sorted List

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

### 4.6 Complexity Analysis

| Operation | Two Heaps | Sorted List | Array (naive) |
|-----------|-----------|-------------|---------------|
| addNum | O(log n) | O(log n) | O(n) |
| findMedian | O(1) | O(1) | O(n log n) |
| Space | O(n) | O(n) | O(n) |

### 4.7 Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Forgetting negation | Max-heap doesn't work | Always negate for max-heap |
| Wrong rebalance condition | Median incorrect | Check `len(upper) > len(lower)` |
| Integer division | Python 2 vs 3 | Use `/ 2.0` for float |

---

## 5. Merge K Sorted Lists (LeetCode 23)

> **Problem**: Merge k sorted linked lists into one sorted list.
> **Pattern**: K-way merge using min-heap
> **Role**: BASE TEMPLATE for `KWayMerge` API Kernel.

### 5.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "merge k sorted" | → K-way merge with heap |
| "k sorted arrays/lists" | → Min-heap of k heads |
| "external merge sort" | → Same pattern at scale |

### 5.2 The K-Way Merge Insight

```
k=3 sorted lists:
  List 0: 1 → 4 → 5
  List 1: 1 → 3 → 4
  List 2: 2 → 6

Min-heap of heads: [(1, 0), (1, 1), (2, 2)]
                       ↑
                  Pop smallest, push successor

Result: 1 → 1 → 2 → 3 → 4 → 4 → 5 → 6
```

### 5.3 Implementation

```python
# Pattern: merge_k_sorted_heap
# See: docs/patterns/heap/templates.md Section 4

import heapq
from typing import List, Optional

class ListNode:
    def __init__(self, val: int = 0, next: 'ListNode' = None):
        self.val = val
        self.next = next

class SolutionHeap:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        """
        Merge k sorted lists using min-heap.

        Key Insight:
        - At any point, the next element in the merged list is the
          smallest among all current list heads
        - Min-heap gives O(log k) access to the smallest head
        - After popping, push the successor node

        Why (val, index, node) tuple?
        - val: primary sort key
        - index: tie-breaker (ListNode not comparable)
        - node: reference to actual node for result building
        """
        if not lists:
            return None

        # Min-heap: (node_value, list_index, node)
        # list_index breaks ties when values are equal
        min_heap: list[tuple[int, int, ListNode]] = []

        # Initialize heap with all non-empty list heads
        for i, node in enumerate(lists):
            if node:
                heapq.heappush(min_heap, (node.val, i, node))

        # Dummy head simplifies list construction
        dummy = ListNode(0)
        tail = dummy

        while min_heap:
            # Pop the smallest node
            val, i, node = heapq.heappop(min_heap)

            # Append to result
            tail.next = node
            tail = tail.next

            # Push successor if exists
            if node.next:
                heapq.heappush(min_heap, (node.next.val, i, node.next))

        return dummy.next
```

### 5.4 Trace Example

```
Input: lists = [[1,4,5], [1,3,4], [2,6]]

Initial heap: [(1, 0, Node1), (1, 1, Node1'), (2, 2, Node2)]

Step 1: Pop (1, 0, Node1), push (4, 0, Node4)
  Result: 1 →
  Heap: [(1, 1, Node1'), (2, 2, Node2), (4, 0, Node4)]

Step 2: Pop (1, 1, Node1'), push (3, 1, Node3)
  Result: 1 → 1 →
  Heap: [(2, 2, Node2), (4, 0, Node4), (3, 1, Node3)]

Step 3: Pop (2, 2, Node2), push (6, 2, Node6)
  Result: 1 → 1 → 2 →
  Heap: [(3, 1, Node3), (4, 0, Node4), (6, 2, Node6)]

... continue until heap empty ...

Final: 1 → 1 → 2 → 3 → 4 → 4 → 5 → 6
```

### 5.5 Alternative: Divide and Conquer

```python
class SolutionDivideConquer:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        """
        Merge by repeatedly combining pairs.

        Analysis:
        - Each round: merge k/2 pairs → k/2 lists remain
        - After log(k) rounds: 1 list remains
        - Total: N elements × log(k) rounds = O(N log k)
        """
        if not lists:
            return None

        while len(lists) > 1:
            merged = []
            for i in range(0, len(lists), 2):
                l1 = lists[i]
                l2 = lists[i + 1] if i + 1 < len(lists) else None
                merged.append(self._merge_two(l1, l2))
            lists = merged

        return lists[0]

    def _merge_two(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        tail = dummy

        while l1 and l2:
            if l1.val <= l2.val:
                tail.next = l1
                l1 = l1.next
            else:
                tail.next = l2
                l2 = l2.next
            tail = tail.next

        tail.next = l1 if l1 else l2
        return dummy.next
```

### 5.6 Complexity Comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Min-heap | O(N log k) | O(k) | N = total nodes, k = lists |
| Divide & Conquer | O(N log k) | O(1) | In-place merge |
| Sequential merge | O(Nk) | O(1) | Merge one at a time |
| Greedy (compare k) | O(Nk) | O(1) | Compare all k heads each step |

### 5.7 Related Problems

| Problem | Variation |
|---------|-----------|
| LC 88: Merge Sorted Array | k=2, in-place |
| LC 21: Merge Two Lists | k=2, linked list |
| LC 378: Kth in Sorted Matrix | K-way merge on rows |
| LC 373: K Pairs with Smallest Sums | Virtual K-way merge |

---

## 6. Meeting Rooms II (LeetCode 253)

> **Problem**: Given an array of meeting time intervals, find the minimum number of conference rooms required.
> **Pattern**: Greedy assignment with min-heap of end times
> **Variant**: Interval scheduling with heap

### 6.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "minimum rooms/resources" | → Greedy with heap |
| "overlapping intervals" | → Sort + track end times |
| "schedule tasks" | → Min-heap for earliest available |

### 6.2 The Greedy Insight

```
Meetings: [[0,30], [5,10], [15,20]]

Timeline:
0   5   10  15  20  25  30
|-------- Meeting 0 --------|
    |- M1 -|
            |-M2-|

At t=5: Meeting 1 starts, Meeting 0 still running → need 2 rooms
At t=15: Meeting 2 starts, Meeting 0 still running → need 2 rooms

Minimum rooms = 2 (max concurrent meetings)
```

### 6.3 Implementation

```python
# Pattern: heap_interval_scheduling
# See: docs/patterns/heap/templates.md Section 5

import heapq

class SolutionHeap:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        """
        Find minimum meeting rooms using min-heap of end times.

        Key Insight:
        - Sort meetings by start time (process chronologically)
        - Min-heap tracks when each room becomes free (end times)
        - For each meeting: if starts after earliest end, reuse room
        - Otherwise, allocate new room

        Why min-heap of end times?
        - We need the room that frees up earliest
        - If new meeting starts >= earliest end, room can be reused
        - Pop the old end time, push new end time
        """
        if not intervals:
            return 0

        # Sort by start time
        intervals.sort(key=lambda x: x[0])

        # Min-heap of end times (when rooms become free)
        end_times: list[int] = []

        for start, end in intervals:
            # Check if earliest-ending room is now free
            if end_times and end_times[0] <= start:
                # Room is free, reuse it (pop old end, push new end)
                heapq.heapreplace(end_times, end)
            else:
                # All rooms busy, allocate new room
                heapq.heappush(end_times, end)

        # Number of rooms = size of heap
        return len(end_times)
```

### 6.4 Trace Example

```
Input: intervals = [[0,30], [5,10], [15,20]]

After sorting (already sorted by start): [[0,30], [5,10], [15,20]]

Process [0, 30]:
  end_times = [30]
  Rooms needed: 1

Process [5, 10]:
  Earliest end = 30, but meeting starts at 5 (5 < 30)
  Cannot reuse, allocate new room
  end_times = [10, 30]
  Rooms needed: 2

Process [15, 20]:
  Earliest end = 10, meeting starts at 15 (15 >= 10)
  Reuse room! Replace 10 with 20
  end_times = [20, 30]
  Rooms needed: 2

Result: 2 rooms
```

### 6.5 Alternative: Sweep Line

```python
class SolutionSweepLine:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        """
        Sweep line: track events at each time point.

        Events:
        - +1 at start time (meeting begins)
        - -1 at end time (meeting ends)

        Max concurrent events = max rooms needed.
        """
        events = []
        for start, end in intervals:
            events.append((start, 1))   # Meeting starts
            events.append((end, -1))    # Meeting ends

        # Sort by time; if same time, process ends before starts
        # (room frees up before new meeting uses it)
        events.sort(key=lambda x: (x[0], x[1]))

        max_rooms = 0
        current_rooms = 0

        for time, delta in events:
            current_rooms += delta
            max_rooms = max(max_rooms, current_rooms)

        return max_rooms
```

### 6.6 Complexity Comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Min-heap | O(n log n) | O(n) | Sort + heap ops |
| Sweep line | O(n log n) | O(n) | Sort events |
| Brute force | O(n²) | O(1) | Check all pairs |

### 6.7 Related Problems

| Problem | Variation |
|---------|-----------|
| LC 252: Meeting Rooms | Just check if any overlap |
| LC 56: Merge Intervals | Merge overlapping intervals |
| LC 435: Non-overlapping Intervals | Min removals for no overlap |
| LC 1094: Car Pooling | Range update + capacity check |

---

## 7. Task Scheduler (LeetCode 621)

> **Problem**: Schedule tasks with cooldown constraint n between same tasks. Return minimum time units.
> **Pattern**: Greedy scheduling with max-heap
> **Variant**: Heap + greedy for optimal ordering

### 7.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "minimum time to complete" | → Greedy scheduling |
| "cooldown period" | → Track availability |
| "most frequent first" | → Max-heap by count |

### 7.2 The Greedy Insight

```
Tasks: A A A B B B, n = 2

Greedy: Always schedule most frequent available task

Optimal schedule:
A B _ A B _ A B
1 2 3 4 5 6 7 8

Total time = 8 units

Why most frequent first?
- Reduces idle time by distributing high-frequency tasks
- Idle slots appear when no task is available (all in cooldown)
```

### 7.3 Implementation

```python
# Pattern: heap_task_scheduler
# See: docs/patterns/heap/templates.md Section 6

import heapq
from collections import Counter, deque

class SolutionHeap:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        """
        Schedule tasks with cooldown using max-heap.

        Strategy:
        1. Greedily pick most frequent available task
        2. Track cooldown using a queue (task becomes available at time t)
        3. If no task available, idle (time still advances)

        Why max-heap?
        - We want to process high-frequency tasks first
        - This minimizes idle time at the end
        - Max-heap gives O(log k) access to most frequent
        """
        # Count task frequencies
        task_counts = Counter(tasks)

        # Max-heap of remaining counts (negate for max-heap)
        max_heap = [-count for count in task_counts.values()]
        heapq.heapify(max_heap)

        # Queue of (available_time, remaining_count) for tasks in cooldown
        cooldown_queue: deque[tuple[int, int]] = deque()

        time = 0

        while max_heap or cooldown_queue:
            time += 1

            # Check if any task exits cooldown
            if cooldown_queue and cooldown_queue[0][0] == time:
                available_time, remaining = cooldown_queue.popleft()
                heapq.heappush(max_heap, -remaining)

            if max_heap:
                # Execute most frequent available task
                count = -heapq.heappop(max_heap)
                count -= 1

                if count > 0:
                    # Task has more instances, put in cooldown
                    cooldown_queue.append((time + n + 1, count))
            # else: idle (no task available)

        return time
```

### 7.4 Trace Example

```
Input: tasks = ['A','A','A','B','B','B'], n = 2

Initial:
  Counts: A=3, B=3
  max_heap: [-3, -3]
  cooldown_queue: []

Time 1: Pop A (count=3→2), cooldown until time=4
  heap: [-3], queue: [(4, 2)]

Time 2: Pop B (count=3→2), cooldown until time=5
  heap: [], queue: [(4, 2), (5, 2)]

Time 3: Idle (heap empty, queue not ready)
  heap: [], queue: [(4, 2), (5, 2)]

Time 4: A exits cooldown, pop A (count=2→1)
  heap: [-2], queue: [(5, 2), (7, 1)]
  Actually: A exits, push to heap, then pop

... continue ...

Final time = 8
```

### 7.5 Alternative: Math Formula

```python
class SolutionMath:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        """
        Mathematical approach based on most frequent task.

        Observation:
        - Most frequent task determines the "frame"
        - Frame: chunks of size (n+1) with one instance of max-freq task

        Formula:
        - frames = (max_freq - 1)
        - frame_size = n + 1
        - base_time = frames * frame_size
        - Add tasks with max_freq (they fill the last partial frame)

        Edge case:
        - If total tasks > formula result, no idle needed
        """
        task_counts = Counter(tasks)
        max_freq = max(task_counts.values())
        max_freq_count = sum(1 for count in task_counts.values() if count == max_freq)

        # Formula: (max_freq - 1) frames × (n + 1) slots + max_freq_count final slots
        formula_time = (max_freq - 1) * (n + 1) + max_freq_count

        # Actual time is max of formula and total tasks
        return max(formula_time, len(tasks))
```

### 7.6 Visual Explanation of Formula

```
tasks = [A,A,A,A,B,B,B,C,C], n = 2, max_freq = 4 (task A)

Formula visualization:
Frame 1: A _ _
Frame 2: A _ _
Frame 3: A _ _
Frame 4: A

Slots per frame = n + 1 = 3
Frames (excluding last) = max_freq - 1 = 3
Base slots = 3 × 3 = 9
Plus final A = 1

Total slots = 10 (minimum, may need more if many tasks)
```

### 7.7 Complexity Comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Max-heap | O(n × m) | O(k) | n=cooldown, m=total tasks, k=unique |
| Math formula | O(n) | O(k) | Count frequencies only |

### 7.8 Related Problems

| Problem | Variation |
|---------|-----------|
| LC 767: Reorganize String | No same adjacent chars |
| LC 358: Rearrange String k Distance | k-distance apart |
| LC 1834: Single-Threaded CPU | Task scheduling with priority |

---

## 8. Last Stone Weight (LeetCode 1046)

> **Problem**: Smash two heaviest stones repeatedly, return weight of last stone (or 0).
> **Pattern**: Greedy simulation with max-heap
> **Variant**: Simple heap operations for repeated selection

### 8.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "repeatedly pick largest/smallest" | → Max/min-heap |
| "simulation" | → Heap for efficient selection |
| "until one/none left" | → Process until heap size ≤ 1 |

### 8.2 Implementation

```python
# Pattern: heap_greedy_simulation
# See: docs/patterns/heap/templates.md Section 7

import heapq

class SolutionHeap:
    def lastStoneWeight(self, stones: List[int]) -> int:
        """
        Simulate stone smashing using max-heap.

        Game Rules:
        1. Pick two heaviest stones x, y (x <= y)
        2. If x == y: both destroyed
        3. If x != y: stone of weight y - x remains

        Why max-heap?
        - Need repeated access to two largest elements
        - Python heapq is min-heap, so negate values
        - O(log n) per operation vs O(n) for linear search
        """
        # Convert to max-heap (negate all values)
        max_heap = [-stone for stone in stones]
        heapq.heapify(max_heap)  # O(n) heapify

        # Simulate until 0 or 1 stone remains
        while len(max_heap) > 1:
            # Pop two largest (remember to negate)
            largest = -heapq.heappop(max_heap)
            second = -heapq.heappop(max_heap)

            # If different weights, push the difference
            if largest != second:
                heapq.heappush(max_heap, -(largest - second))

        # Return last stone weight (or 0 if no stones left)
        return -max_heap[0] if max_heap else 0
```

### 8.3 Trace Example

```
Input: stones = [2, 7, 4, 1, 8, 1]

Initial max-heap: [-8, -7, -4, -1, -2, -1]
Displayed as max-heap: [8, 7, 4, 1, 2, 1]

Round 1: Pop 8, 7; difference = 1
  heap: [4, 2, 1, 1, 1]

Round 2: Pop 4, 2; difference = 2
  heap: [2, 1, 1, 1]

Round 3: Pop 2, 1; difference = 1
  heap: [1, 1, 1]

Round 4: Pop 1, 1; equal, both destroyed
  heap: [1]

Result: 1
```

### 8.4 Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n log n) |
| Space | O(n) for heap |

**Time breakdown**:
- Heapify: O(n)
- Each smash: 2 pops + 0-1 push = O(log n)
- Total smashes: at most n-1 (each reduces count by at least 1)
- Total: O(n) + O(n log n) = O(n log n)

### 8.5 Related Problems

| Problem | Variation |
|---------|-----------|
| LC 1167: Min Cost to Connect Sticks | Sum instead of difference |
| LC 973: K Closest Points | Top-k by distance |
| LC 703: Kth Largest Element in Stream | Maintain kth largest online |

---

---

## 9. Comparison with Similar Patterns

### 9.1 Heap vs Sorting

| Aspect | Heap (Top-K) | Full Sort |
|--------|--------------|-----------|
| **Time** | O(n log k) | O(n log n) |
| **Space** | O(k) | O(n) |
| **Use When** | Only need k elements | Need all elements ordered |
| **Streaming** | ✅ Online algorithm | ❌ Requires all data |

### 9.2 Heap vs Quickselect

| Aspect | Heap | Quickselect |
|--------|------|-------------|
| **Time (avg)** | O(n log k) | O(n) |
| **Time (worst)** | O(n log k) | O(n²) |
| **Space** | O(k) | O(1) in-place |
| **Stability** | Stable | Not stable |
| **Use When** | k is small, need all top-k | k is large (k ≈ n/2), only need kth |

### 9.3 Two Heaps vs Sorted Container

| Aspect | Two Heaps | SortedList |
|--------|-----------|------------|
| **addNum** | O(log n) | O(log n) |
| **findMedian** | O(1) | O(1) |
| **Implementation** | Standard library | External dependency |
| **Memory** | 2 arrays | 1 sorted array |

### 9.4 K-Way Merge: Heap vs Divide-and-Conquer

| Aspect | Min-Heap | Divide & Conquer |
|--------|----------|------------------|
| **Time** | O(N log k) | O(N log k) |
| **Space** | O(k) | O(1) iterative, O(log k) recursive |
| **Streaming** | ✅ Can process on-the-fly | ❌ Need all lists upfront |
| **Implementation** | Simpler | More code |

---

---

## 10. Decision Flowchart

Use this flowchart to determine which heap pattern applies:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    HEAP PATTERN SELECTION                               │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │ What are you finding/doing?   │
                    └───────────────────────────────┘
                                    │
          ┌─────────────────────────┼─────────────────────────┐
          │                         │                         │
          ▼                         ▼                         ▼
   ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
   │ Kth element  │         │   Merging    │         │  Scheduling  │
   │ or Top-K     │         │   sorted     │         │  or greedy   │
   └──────────────┘         └──────────────┘         └──────────────┘
          │                         │                         │
          ▼                         ▼                         ▼
   ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
   │ Static or    │         │ How many     │         │ What type?   │
   │ streaming?   │         │ sequences?   │         └──────────────┘
   └──────────────┘         └──────────────┘                 │
          │                         │               ┌────────┼────────┐
    ┌─────┴─────┐             ┌─────┴─────┐         │        │        │
    │           │             │           │         ▼        ▼        ▼
    ▼           ▼             ▼           ▼      Interval  Task    Repeated
 Static    Streaming       k = 2       k > 2    overlap  cooldown  largest
    │           │             │           │         │        │        │
    ▼           ▼             ▼           ▼         ▼        ▼        ▼
┌────────┐ ┌────────┐   ┌────────┐  ┌────────┐ ┌────────┐┌────────┐┌────────┐
│heap_   │ │heap_   │   │two     │  │merge_k │ │heap_   ││heap_   ││heap_   │
│kth_    │ │median_ │   │pointer │  │_sorted_│ │interval││task_   ││greedy_ │
│element │ │stream  │   │merge   │  │heap    │ │schedule││schedule││sim     │
│        │ │        │   │        │  │        │ │        ││r       ││        │
│LC 215  │ │LC 295  │   │LC 21   │  │LC 23   │ │LC 253  ││LC 621  ││LC 1046 │
│LC 347  │ │        │   │LC 88   │  │        │ │        ││        ││        │
└────────┘ └────────┘   └────────┘  └────────┘ └────────┘└────────┘└────────┘
```

### 10.1 Quick Decision Table

| Clue in Problem | Pattern | Key Data Structure |
|-----------------|---------|-------------------|
| "kth largest/smallest" | heap_kth_element | Min-heap size k |
| "top k frequent" | heap_top_k | Min-heap + frequency map |
| "running/streaming median" | heap_median_stream | Two heaps (max + min) |
| "merge k sorted" | merge_k_sorted_heap | Min-heap of heads |
| "minimum rooms/resources" | heap_interval_scheduling | Min-heap of end times |
| "schedule with cooldown" | heap_task_scheduler | Max-heap + cooldown queue |
| "repeatedly process largest" | heap_greedy_simulation | Max-heap |

### 10.2 Pattern Checklist

Before implementing, verify:

- [ ] **Is heap the right choice?**
  - Need repeated access to min/max? → Heap
  - Need kth element only once? → Consider quickselect
  - Need all elements sorted? → Just sort

- [ ] **Which heap type?**
  - Finding largest/max → Min-heap of size k
  - Finding smallest/min → Max-heap of size k
  - Merging sorted → Min-heap
  - Greedy simulation → Max or min depending on problem

- [ ] **Edge cases identified?**
  - Empty input
  - k > n elements
  - Duplicate values
  - Tie-breaking rules

---

---

## 11. Quick Reference Templates

### 11.1 Template 1: Kth Largest (Min-Heap of Size K)

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

### 11.2 Template 2: Top-K Frequent

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

### 11.3 Template 3: Two Heaps for Median

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

### 11.4 Template 4: K-Way Merge

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

### 11.5 Template 5: Interval Scheduling (Meeting Rooms)

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

### 11.6 Template 6: Greedy Simulation

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

### 11.7 Common Heap Operations Reference

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



---



*Document generated for NeetCode Practice Framework — API Kernel: HeapTopK*
