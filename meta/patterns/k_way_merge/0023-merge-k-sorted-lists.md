# 23. Merge k Sorted Lists

## Problem Link
https://leetcode.com/problems/merge-k-sorted-lists/

## Difficulty
Hard

## Tags
- Linked List
- Divide and Conquer
- Heap (Priority Queue)
- Merge Sort

## Pattern
KWayMerge - Heap-based

## API Kernel
`KWayMerge`

## Problem Summary

Given an array of K linked lists, each sorted in ascending order, merge all lists into one sorted linked list.

## Key Insight

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

## Template Mapping

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

## Alternative: Divide and Conquer

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

## Complexity
- Heap: O(N log K) time, O(K) space
- Divide-and-conquer: O(N log K) time, O(1) extra space (excluding recursion)

## Why This Problem First?

Merge K Sorted Lists is the **canonical K-way merge** because:

1. **Direct pattern application**: Multiple sorted sequences → one sorted output
2. **Requires heap for efficiency**: O(N log K) vs O(NK) naive
3. **Tie-breaker pattern**: Using index to avoid comparing ListNode objects
4. **Foundation for streaming**: Same technique works for iterators/streams

## Common Mistakes

1. **Comparing ListNode objects directly** - Python can't compare custom objects; use index as tie-breaker
2. **Not handling empty lists** - Check `if node:` before adding to heap
3. **Using O(NK) greedy approach** - Comparing all K heads each time is too slow

## Related Problems
- LC 21: Merge Two Sorted Lists (K=2 base case)
- LC 88: Merge Sorted Array (array version)
- LC 378: Kth Smallest Element in a Sorted Matrix
- LC 373: Find K Pairs with Smallest Sums


