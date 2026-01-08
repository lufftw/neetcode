## Problem Comparison

| Problem | K Value | Data Structure | Direction | Space |
|---------|---------|----------------|-----------|-------|
| **Merge K Sorted Lists** | K (variable) | Linked List | Forward | O(K) heap |
| **Merge Two Sorted Lists** | 2 (fixed) | Linked List | Forward | O(1) |
| **Merge Sorted Array** | 2 (fixed) | Array | Backward | O(1) in-place |

## Approach Comparison

| Problem | Heap | Divide-Conquer | Two-Pointer |
|---------|------|----------------|-------------|
| **Merge K Lists** | ✅ O(N log K) | ✅ O(N log K) | ❌ (K=2 only) |
| **Merge Two Lists** | ❌ Overkill | ❌ Overkill | ✅ O(N) |
| **Merge Array** | ❌ Overkill | ❌ Overkill | ✅ O(N) backward |

## Pattern Evolution

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

## Code Structure Comparison

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


