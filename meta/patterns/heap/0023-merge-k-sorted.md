## Merge K Sorted Lists (LeetCode 23)

> **Problem**: Merge k sorted linked lists into one sorted list.
> **Pattern**: K-way merge using min-heap
> **Role**: BASE TEMPLATE for `KWayMerge` API Kernel.

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "merge k sorted" | → K-way merge with heap |
| "k sorted arrays/lists" | → Min-heap of k heads |
| "external merge sort" | → Same pattern at scale |

### The K-Way Merge Insight

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

### Implementation

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

### Trace Example

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

### Alternative: Divide and Conquer

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

### Complexity Comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Min-heap | O(N log k) | O(k) | N = total nodes, k = lists |
| Divide & Conquer | O(N log k) | O(1) | In-place merge |
| Sequential merge | O(Nk) | O(1) | Merge one at a time |
| Greedy (compare k) | O(Nk) | O(1) | Compare all k heads each step |

### Related Problems

| Problem | Variation |
|---------|-----------|
| LC 88: Merge Sorted Array | k=2, in-place |
| LC 21: Merge Two Lists | k=2, linked list |
| LC 378: Kth in Sorted Matrix | K-way merge on rows |
| LC 373: K Pairs with Smallest Sums | Virtual K-way merge |


