# K-Way Merge: Complete Reference

> **API Kernel**: `KWayMerge`
> **Core Mechanism**: Efficiently merge K sorted sequences by maintaining a heap of current heads, always extracting the global minimum.

This document presents the **canonical K-way merge templates** covering heap-based merge, divide-and-conquer approaches, and the fundamental two-pointer merge. Each implementation follows consistent naming conventions and includes detailed logic explanations.

---

## Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Problem Link](#2-problem-link)
3. [Difficulty](#3-difficulty)
4. [Tags](#4-tags)
5. [Pattern](#5-pattern)
6. [API Kernel](#6-api-kernel)
7. [Problem Summary](#7-problem-summary)
8. [Key Insight](#8-key-insight)
9. [Template Mapping](#9-template-mapping)
10. [Alternative: Divide and Conquer](#10-alternative-divide-and-conquer)
11. [Complexity](#11-complexity)
12. [Why This Problem First?](#12-why-this-problem-first)
13. [Common Mistakes](#13-common-mistakes)
14. [Related Problems](#14-related-problems)
15. [Problem Link](#15-problem-link)
16. [Difficulty](#16-difficulty)
17. [Tags](#17-tags)
18. [Pattern](#18-pattern)
19. [API Kernel](#19-api-kernel)
20. [Problem Summary](#20-problem-summary)
21. [Key Insight](#21-key-insight)
22. [Template Mapping](#22-template-mapping)
23. [Alternative: Recursive](#23-alternative-recursive)
24. [Complexity](#24-complexity)
25. [Why This Problem Second?](#25-why-this-problem-second)
26. [Common Mistakes](#26-common-mistakes)
27. [Related Problems](#27-related-problems)
28. [Problem Link](#28-problem-link)
29. [Difficulty](#29-difficulty)
30. [Tags](#30-tags)
31. [Pattern](#31-pattern)
32. [API Kernel](#32-api-kernel)
33. [Problem Summary](#33-problem-summary)
34. [Key Insight](#34-key-insight)
35. [Template Mapping](#35-template-mapping)
36. [Complexity](#36-complexity)
37. [Why This Problem Third?](#37-why-this-problem-third)
38. [Delta from Linked List Merge](#38-delta-from-linked-list-merge)
39. [Common Mistakes](#39-common-mistakes)
40. [Related Problems](#40-related-problems)
41. [Problem Comparison](#41-problem-comparison)
42. [Approach Comparison](#42-approach-comparison)
43. [Pattern Evolution](#43-pattern-evolution)
44. [Code Structure Comparison](#44-code-structure-comparison)
45. [Decision Tree](#45-decision-tree)
46. [Pattern Selection Guide](#46-pattern-selection-guide)
47. [Quick Pattern Recognition](#47-quick-pattern-recognition)
48. [Complexity Trade-offs](#48-complexity-trade-offs)
49. [Universal Templates](#49-universal-templates)

---

## 1. Core Concepts

### 1.1 The K-Way Merge Problem

Given K sorted sequences, produce a single sorted sequence containing all elements.

**Naive approach**: Concatenate all sequences, then sort → O(N log N)
**Optimal approach**: Use the sorted property → O(N log K)

### 1.2 The Key Insight

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

### 1.3 Universal K-Way Merge Template

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

### 1.4 Pattern Variants

| Variant | Data Structure | Time | Space | Best When |
|---------|---------------|------|-------|-----------|
| **Heap-based** | Min-heap | O(N log K) | O(K) | K is large |
| **Divide-and-conquer** | Recursive merge | O(N log K) | O(1) + stack | K is moderate |
| **Two-pointer merge** | Arrays | O(N) | O(1) | K = 2 |

### 1.5 Two-Pointer Merge (K=2 Base Case)

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

### 1.6 Linked List Adaptation

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

### 1.7 Complexity Analysis

For merging K sequences with total N elements:

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Heap-based | O(N log K) | O(K) | Each element: 1 push + 1 pop |
| Divide-and-conquer | O(N log K) | O(log K) stack | Pair-wise merge in log K rounds |
| Naive (sort all) | O(N log N) | O(N) | Ignores sorted property |

When K is small (e.g., 2), two-pointer merge is O(N) and simpler.

---

# 23. Merge k Sorted Lists

## 2. Problem Link
https://leetcode.com/problems/merge-k-sorted-lists/

## 3. Difficulty
Hard

## 4. Tags
- Linked List
- Divide and Conquer
- Heap (Priority Queue)
- Merge Sort

## 5. Pattern
KWayMerge - Heap-based

## 6. API Kernel
`KWayMerge`

## 7. Problem Summary

Given an array of K linked lists, each sorted in ascending order, merge all lists into one sorted linked list.

## 8. Key Insight

This is the **canonical K-way merge problem**. The heap maintains K "heads" (current nodes from each list), and we repeatedly extract the minimum and advance that list's pointer.

```
Lists: [1→4→5], [1→3→4], [2→6]
Heap:  {1, 1, 2}  (current heads)

Pop min=1 (list 0), push 4:
Heap:  {1, 2, 4}
Result: 1→

Pop min=1 (list 1), push 3:
Heap:  {2, 3, 4}
Result: 1→1→

...continue until heap empty...
```

## 9. Template Mapping

```python
import heapq
from typing import List, Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        # Min-heap: (value, list_index, node)
        # list_index is tie-breaker (nodes aren't comparable)
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

## 10. Alternative: Divide and Conquer

```python
class SolutionDivideConquer:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if not lists:
            return None

        while len(lists) > 1:
            merged = []
            for i in range(0, len(lists), 2):
                l1 = lists[i]
                l2 = lists[i + 1] if i + 1 < len(lists) else None
                merged.append(self._mergeTwoLists(l1, l2))
            lists = merged

        return lists[0]

    def _mergeTwoLists(self, l1, l2):
        dummy = ListNode()
        tail = dummy
        while l1 and l2:
            if l1.val <= l2.val:
                tail.next = l1
                l1 = l1.next
            else:
                tail.next = l2
                l2 = l2.next
            tail = tail.next
        tail.next = l1 or l2
        return dummy.next
```

## 11. Complexity
- Heap: O(N log K) time, O(K) space
- Divide-and-conquer: O(N log K) time, O(1) extra space (excluding recursion)

## 12. Why This Problem First?

Merge K Sorted Lists is the **canonical K-way merge** because:

1. **Direct pattern application**: Multiple sorted sequences → one sorted output
2. **Requires heap for efficiency**: O(N log K) vs O(NK) naive
3. **Tie-breaker pattern**: Using index to avoid comparing ListNode objects
4. **Foundation for streaming**: Same technique works for iterators/streams

## 13. Common Mistakes

1. **Comparing ListNode objects directly** - Python can't compare custom objects; use index as tie-breaker
2. **Not handling empty lists** - Check `if node:` before adding to heap
3. **Using O(NK) greedy approach** - Comparing all K heads each time is too slow

## 14. Related Problems
- LC 21: Merge Two Sorted Lists (K=2 base case)
- LC 88: Merge Sorted Array (array version)
- LC 378: Kth Smallest Element in a Sorted Matrix
- LC 373: Find K Pairs with Smallest Sums

---

# 21. Merge Two Sorted Lists

## 15. Problem Link
https://leetcode.com/problems/merge-two-sorted-lists/

## 16. Difficulty
Easy

## 17. Tags
- Linked List
- Recursion

## 18. Pattern
KWayMerge - Two Pointer (K=2)

## 19. API Kernel
`MergeSortedSequences`

## 20. Problem Summary

Merge two sorted linked lists and return the merged list as a sorted list.

## 21. Key Insight

This is the **K=2 special case** of K-way merge. When K=2, we don't need a heap - simple two-pointer comparison suffices. This is also the building block for divide-and-conquer K-way merge.

```
list1: 1 → 2 → 4
list2: 1 → 3 → 4

Step by step:
1 <= 1: pick list1[0] → [1]
1 <= 2: pick list2[0] → [1,1]
2 <= 3: pick list1[1] → [1,1,2]
3 <= 4: pick list2[1] → [1,1,2,3]
4 <= 4: pick list1[2] → [1,1,2,3,4]
append remaining list2[2] → [1,1,2,3,4,4]
```

## 22. Template Mapping

```python
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        # Dummy node simplifies edge cases
        dummy = ListNode()
        tail = dummy

        # Two-pointer merge: compare heads, advance smaller
        while list1 and list2:
            if list1.val <= list2.val:
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next

        # Attach remaining (at most one list has elements)
        tail.next = list1 if list1 else list2

        return dummy.next
```

## 23. Alternative: Recursive

```python
class SolutionRecursive:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        if not list1:
            return list2
        if not list2:
            return list1

        if list1.val <= list2.val:
            list1.next = self.mergeTwoLists(list1.next, list2)
            return list1
        else:
            list2.next = self.mergeTwoLists(list1, list2.next)
            return list2
```

## 24. Complexity
- Iterative: O(n + m) time, O(1) space
- Recursive: O(n + m) time, O(n + m) stack space

## 25. Why This Problem Second?

Merge Two Sorted Lists establishes the **two-pointer merge foundation**:

1. **Simplest merge case**: Only two sequences to compare
2. **No heap overhead**: Direct comparison is optimal for K=2
3. **Building block**: Used in divide-and-conquer K-way merge
4. **Dummy node pattern**: Avoids special-casing the head

## 26. Common Mistakes

1. **Special-casing the first node** - Use dummy node instead
2. **Forgetting to attach remaining elements** - After loop, one list may have elements
3. **Returning wrong node** - Return `dummy.next`, not `dummy`

## 27. Related Problems
- LC 23: Merge K Sorted Lists (generalization)
- LC 88: Merge Sorted Array (array version)
- LC 148: Sort List (uses merge as subroutine)

---

# 88. Merge Sorted Array

## 28. Problem Link
https://leetcode.com/problems/merge-sorted-array/

## 29. Difficulty
Easy

## 30. Tags
- Array
- Two Pointers
- Sorting

## 31. Pattern
KWayMerge - In-Place Backward Merge

## 32. API Kernel
`MergeSortedSequences`

## 33. Problem Summary

Merge nums2 into nums1 in-place. nums1 has enough space (length m + n) to hold additional elements.

## 34. Key Insight

**Merge from the end** to avoid overwriting elements we haven't processed yet. Start filling from position m+n-1, comparing largest elements first.

```
nums1 = [1,2,3,_,_,_], m = 3
nums2 = [2,5,6], n = 3

Merge from end:
pos 5: 6 > 3 → nums1[5] = 6
pos 4: 5 > 3 → nums1[4] = 5
pos 3: 3 > 2 → nums1[3] = 3
pos 2: 2 >= 2 → nums1[2] = 2 (from nums2)
pos 1: 2 > (empty) → nums1[1] = 2 (from nums1)
...

Result: [1,2,2,3,5,6]
```

## 35. Template Mapping

```python
from typing import List

class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Modify nums1 in-place to contain merged result.

        Key insight: Fill from the end to avoid overwriting.
        """
        # Pointers to last elements of each array
        p1 = m - 1      # Last element in nums1's original data
        p2 = n - 1      # Last element in nums2
        write = m + n - 1  # Write position (end of nums1)

        # Merge from end: place larger element at write position
        while p1 >= 0 and p2 >= 0:
            if nums1[p1] > nums2[p2]:
                nums1[write] = nums1[p1]
                p1 -= 1
            else:
                nums1[write] = nums2[p2]
                p2 -= 1
            write -= 1

        # If nums2 has remaining elements, copy them
        # (If nums1 has remaining, they're already in place)
        while p2 >= 0:
            nums1[write] = nums2[p2]
            p2 -= 1
            write -= 1
```

## 36. Complexity
- Time: O(m + n)
- Space: O(1) - in-place

## 37. Why This Problem Third?

Merge Sorted Array teaches the **backward merge technique**:

1. **In-place constraint**: Can't use extra space for output
2. **Backward fill insight**: Prevents overwriting unprocessed elements
3. **One remaining copy**: Only nums2 leftovers need copying
4. **Array variant**: Same pattern as linked list, different data structure

## 38. Delta from Linked List Merge

| Aspect | Linked List | Array |
|--------|-------------|-------|
| Direction | Forward | Backward (in-place) |
| New space | Reuse nodes | Already allocated |
| Leftover handling | Attach remaining | Copy remaining |

## 39. Common Mistakes

1. **Merging forward** - Overwrites elements before processing
2. **Forgetting nums2 leftovers** - Must copy remaining nums2 elements
3. **Wrong pointer initialization** - p1 = m-1, p2 = n-1, write = m+n-1
4. **Off-by-one errors** - Use `>= 0` not `> 0` in while conditions

## 40. Related Problems
- LC 21: Merge Two Sorted Lists (linked list version)
- LC 23: Merge K Sorted Lists (generalization)
- LC 977: Squares of a Sorted Array (merge sorted subarrays)

---

## 41. Problem Comparison

| Problem | K Value | Data Structure | Direction | Space |
|---------|---------|----------------|-----------|-------|
| **Merge K Sorted Lists** | K (variable) | Linked List | Forward | O(K) heap |
| **Merge Two Sorted Lists** | 2 (fixed) | Linked List | Forward | O(1) |
| **Merge Sorted Array** | 2 (fixed) | Array | Backward | O(1) in-place |

## 42. Approach Comparison

| Problem | Heap | Divide-Conquer | Two-Pointer |
|---------|------|----------------|-------------|
| **Merge K Lists** | ✅ O(N log K) | ✅ O(N log K) | ❌ (K=2 only) |
| **Merge Two Lists** | ❌ Overkill | ❌ Overkill | ✅ O(N) |
| **Merge Array** | ❌ Overkill | ❌ Overkill | ✅ O(N) backward |

## 43. Pattern Evolution

```
┌──────────────────────────────────────────────────────────────────┐
│                    K-Way Merge Evolution                         │
└──────────────────────────────────────────────────────────────────┘

       Merge Two Lists (Base: K=2)
              │
              │ Core pattern:
              │ - Two pointers compare heads
              │ - Advance smaller pointer
              │ - Attach remaining list
              │
              ▼
    ┌─────────────────────┐
    │ What changes for    │
    │ Merge K Lists?      │
    ├─────────────────────┤
    │ + K pointers → heap │
    │ + Tie-breaker index │
    │ + Extract min loop  │
    └─────────────────────┘
              │
              ▼
       Merge K Lists (Heap)
              │
              │ Alternative approach:
              │ - Divide-and-conquer
              │ - Pairwise merge using K=2
              │
              ▼
    ┌─────────────────────┐
    │ What changes for    │
    │ Merge Sorted Array? │
    ├─────────────────────┤
    │ + In-place merge    │
    │ + Backward direction│
    │ + Pre-allocated     │
    └─────────────────────┘
              │
              ▼
        Merge Sorted Array
```

## 44. Code Structure Comparison

```python
# ===== Merge Two Lists (K=2, forward) =====
while list1 and list2:
    if list1.val <= list2.val:
        tail.next = list1
        list1 = list1.next
    else:
        tail.next = list2
        list2 = list2.next
    tail = tail.next
tail.next = list1 or list2

# ===== Merge K Lists (heap) =====
while heap:
    val, idx, node = heapq.heappop(heap)
    tail.next = node
    tail = tail.next
    if node.next:
        heapq.heappush(heap, (node.next.val, idx, node.next))

# ===== Merge Sorted Array (backward) =====
while p1 >= 0 and p2 >= 0:
    if nums1[p1] > nums2[p2]:
        nums1[write] = nums1[p1]
        p1 -= 1
    else:
        nums1[write] = nums2[p2]
        p2 -= 1
    write -= 1
```

---

## 45. Decision Tree

```
Start: Merging sorted sequences?
                    │
                    ▼
        ┌───────────────────────┐
        │ How many sequences    │
        │ to merge?             │
        └───────────────────────┘
                    │
            ┌───────┴───────┐
            ▼               ▼
          K = 2            K > 2
            │               │
            ▼               ▼
    ┌───────────────┐   ┌───────────────┐
    │ In-place      │   │ Use Heap      │
    │ constraint?   │   │ O(N log K)    │
    └───────────────┘   └───────────────┘
            │                   │
      ┌─────┴─────┐            │
      ▼           ▼            │
     YES          NO           ▼
      │           │        ┌────────────────┐
      ▼           ▼        │ Alternative:   │
  Backward    Forward      │ Divide-Conquer │
   Merge       Merge       │ (log K rounds) │
(LC 88)      (LC 21)       └────────────────┘
```

## 46. Pattern Selection Guide

### 46.1 Use Heap-based K-Way Merge when:

- ✅ K is large (heap maintains only K elements)
- ✅ Input is streams/iterators (don't need all data at once)
- ✅ Elements arrive incrementally
- ✅ K varies at runtime

### 46.2 Use Divide-and-Conquer when:

- ✅ All data is available upfront
- ✅ Want to avoid heap allocation
- ✅ Implementing merge sort
- ✅ K is moderate and recursion depth is acceptable

### 46.3 Use Two-Pointer Merge when:

- ✅ K = 2 (exactly two sequences)
- ✅ In-place merge required (backward direction)
- ✅ Simple case where heap overhead isn't worth it

## 47. Quick Pattern Recognition

| Problem Characteristics | Approach |
|------------------------|----------|
| "Merge K sorted X" | Heap-based K-way |
| "Merge two sorted X" | Two-pointer |
| "Merge in-place with extra space" | Backward merge |
| "External sort / streaming" | Heap-based |
| "Merge k sorted iterators" | Heap-based |

## 48. Complexity Trade-offs

| Approach | Time | Space | Best For |
|----------|------|-------|----------|
| Heap | O(N log K) | O(K) | Large K, streaming |
| Divide-Conquer | O(N log K) | O(log K) stack | All data available |
| Two-Pointer | O(N) | O(1) | K = 2 |
| Naive Sort | O(N log N) | O(N) | Never optimal |

---

## 49. Universal Templates

### 49.1 Template 1: Heap-based K-Way Merge (Arrays)

```python
import heapq
from typing import List, Iterator

def k_way_merge_arrays(arrays: List[List[int]]) -> List[int]:
    """
    Merge K sorted arrays using a min-heap.

    Time: O(N log K), Space: O(K) for heap
    Use for: General K-way merge on arrays
    """
    # Heap: (value, array_index, element_index)
    heap = []
    for i, arr in enumerate(arrays):
        if arr:
            heapq.heappush(heap, (arr[0], i, 0))

    result = []
    while heap:
        val, arr_idx, elem_idx = heapq.heappop(heap)
        result.append(val)

        # Push next element from same array
        next_idx = elem_idx + 1
        if next_idx < len(arrays[arr_idx]):
            heapq.heappush(heap, (arrays[arr_idx][next_idx], arr_idx, next_idx))

    return result
```

---

### 49.2 Template 2: Heap-based K-Way Merge (Linked Lists)

```python
import heapq
from typing import List, Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_k_lists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    """
    Merge K sorted linked lists using a min-heap.

    Time: O(N log K), Space: O(K) for heap
    Use for: LC 23 (Merge K Sorted Lists)
    """
    # Heap: (value, list_index, node)
    # list_index prevents comparing ListNode objects
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

---

### 49.3 Template 3: Two-Pointer Merge (K=2, Forward)

```python
from typing import Optional

def merge_two_lists(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    """
    Merge two sorted linked lists using two pointers.

    Time: O(n + m), Space: O(1)
    Use for: LC 21 (Merge Two Sorted Lists)
    """
    dummy = ListNode()
    tail = dummy

    while l1 and l2:
        if l1.val <= l2.val:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next

    tail.next = l1 or l2
    return dummy.next
```

---

### 49.4 Template 4: In-Place Backward Merge (Arrays)

```python
from typing import List

def merge_sorted_array(nums1: List[int], m: int, nums2: List[int], n: int) -> None:
    """
    Merge nums2 into nums1 in-place using backward merge.

    Time: O(m + n), Space: O(1)
    Use for: LC 88 (Merge Sorted Array)
    """
    p1 = m - 1
    p2 = n - 1
    write = m + n - 1

    while p1 >= 0 and p2 >= 0:
        if nums1[p1] > nums2[p2]:
            nums1[write] = nums1[p1]
            p1 -= 1
        else:
            nums1[write] = nums2[p2]
            p2 -= 1
        write -= 1

    # Copy remaining nums2 elements
    while p2 >= 0:
        nums1[write] = nums2[p2]
        p2 -= 1
        write -= 1
```

---

### 49.5 Template 5: Divide-and-Conquer K-Way Merge

```python
from typing import List, Optional

def merge_k_lists_dc(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    """
    Merge K sorted lists using divide-and-conquer.

    Time: O(N log K), Space: O(log K) recursion stack
    Use for: Alternative to heap when K is moderate
    """
    if not lists:
        return None

    while len(lists) > 1:
        merged = []
        for i in range(0, len(lists), 2):
            l1 = lists[i]
            l2 = lists[i + 1] if i + 1 < len(lists) else None
            merged.append(merge_two_lists(l1, l2))
        lists = merged

    return lists[0]
```



---



*Document generated for NeetCode Practice Framework — API Kernel: KWayMerge*
