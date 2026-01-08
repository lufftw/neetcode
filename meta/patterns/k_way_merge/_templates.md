## Universal Templates

### Template 1: Heap-based K-Way Merge (Arrays)

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

### Template 2: Heap-based K-Way Merge (Linked Lists)

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

### Template 3: Two-Pointer Merge (K=2, Forward)

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

### Template 4: In-Place Backward Merge (Arrays)

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

### Template 5: Divide-and-Conquer K-Way Merge

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


