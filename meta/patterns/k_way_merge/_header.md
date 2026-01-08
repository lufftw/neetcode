# K-Way Merge: Complete Reference

> **API Kernel**: `KWayMerge`
> **Core Mechanism**: Efficiently merge K sorted sequences by maintaining a heap of current heads, always extracting the global minimum.

This document presents the **canonical K-way merge templates** covering heap-based merge, divide-and-conquer approaches, and the fundamental two-pointer merge. Each implementation follows consistent naming conventions and includes detailed logic explanations.

---

## Core Concepts

### The K-Way Merge Problem

Given K sorted sequences, produce a single sorted sequence containing all elements.

**Naive approach**: Concatenate all sequences, then sort → O(N log N)
**Optimal approach**: Use the sorted property → O(N log K)

### The Key Insight

> **At any moment, the next element in the merged result must be the smallest among all K current heads.**

We maintain a min-heap of size K, containing the "head" (next unprocessed element) of each sequence. Each extraction gives us the global minimum, and we push the successor from that sequence.

```
Lists:          Heap (heads):       Output:
[1,4,5]             1                  []
[1,3,4]   →         1    →    pop 1 → [1]
[2,6]               2

After pop 1 from list[0], push 4:
[4,5]               1
[1,3,4]   →         2    →    pop 1 → [1,1]
[2,6]               4
```

### Universal K-Way Merge Template

```python
import heapq
from typing import List, Iterator, TypeVar, Callable

T = TypeVar('T')

def k_way_merge(sequences: List[List[T]], key: Callable[[T], any] = None) -> Iterator[T]:
    """
    Merge K sorted sequences using a min-heap.

    Core invariant:
    - Heap contains exactly one element from each non-empty sequence
    - Heap root is always the global minimum among current heads
    - Each element is pushed and popped exactly once

    Args:
        sequences: List of sorted sequences
        key: Optional key function for comparison

    Yields:
        Elements in sorted order
    """
    # Initialize heap with (value, sequence_index, element_index)
    # sequence_index breaks ties (avoids comparing elements directly)
    heap = []

    for i, seq in enumerate(sequences):
        if seq:  # Skip empty sequences
            val = key(seq[0]) if key else seq[0]
            heapq.heappush(heap, (val, i, 0))

    while heap:
        _, seq_idx, elem_idx = heapq.heappop(heap)
        yield sequences[seq_idx][elem_idx]

        # Push successor from same sequence if available
        next_idx = elem_idx + 1
        if next_idx < len(sequences[seq_idx]):
            next_val = sequences[seq_idx][next_idx]
            val = key(next_val) if key else next_val
            heapq.heappush(heap, (val, seq_idx, next_idx))
```

### Pattern Variants

| Variant | Data Structure | Time | Space | Best When |
|---------|---------------|------|-------|-----------|
| **Heap-based** | Min-heap | O(N log K) | O(K) | K is large |
| **Divide-and-conquer** | Recursive merge | O(N log K) | O(1) + stack | K is moderate |
| **Two-pointer merge** | Arrays | O(N) | O(1) | K = 2 |

### Two-Pointer Merge (K=2 Base Case)

```python
def merge_two_sorted(list1: List[T], list2: List[T]) -> List[T]:
    """
    Merge two sorted lists using two pointers.

    This is the building block for divide-and-conquer K-way merge.
    """
    result = []
    i = j = 0

    while i < len(list1) and j < len(list2):
        if list1[i] <= list2[j]:
            result.append(list1[i])
            i += 1
        else:
            result.append(list2[j])
            j += 1

    # Append remaining elements
    result.extend(list1[i:])
    result.extend(list2[j:])

    return result
```

### Linked List Adaptation

For linked lists, the pattern is identical but uses node pointers:

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_k_lists(lists: List[ListNode]) -> ListNode:
    """
    K-way merge for linked lists.

    Heap entry: (node.val, list_index, node)
    - list_index breaks ties (nodes aren't comparable)
    """
    heap = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))

    dummy = ListNode()
    tail = dummy

    while heap:
        val, idx, node = heapq.heappop(heap)
        tail.next = node
        tail = tail.next

        if node.next:
            heapq.heappush(heap, (node.next.val, idx, node.next))

    return dummy.next
```

### Complexity Analysis

For merging K sequences with total N elements:

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Heap-based | O(N log K) | O(K) | Each element: 1 push + 1 pop |
| Divide-and-conquer | O(N log K) | O(log K) stack | Pair-wise merge in log K rounds |
| Naive (sort all) | O(N log N) | O(N) | Ignores sorted property |

When K is small (e.g., 2), two-pointer merge is O(N) and simpler.


