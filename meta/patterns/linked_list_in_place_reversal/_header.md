# Linked List In-Place Reversal: Complete Reference

> **API Kernel**: `LinkedListInPlaceReversal`
> **Core Mechanism**: Reverse linked list nodes in-place by manipulating next pointers, using O(1) extra space.

This document presents the **canonical in-place linked list reversal templates** covering full list reversal, segment reversal, and k-group reversal. Each implementation follows consistent naming conventions and includes detailed pointer manipulation logic.

---

## Core Concepts

### The In-Place Reversal Problem

Given a linked list, reverse some or all of its nodes without allocating new nodes.

**Key constraint**: O(1) space - we cannot copy values to an array and reverse there.

### The Pointer Reversal Technique

> **At each step, we reverse the direction of one edge: make `curr.next` point to `prev` instead of the original next node.**

The fundamental operation is a three-pointer dance:

```
Before:  prev -> curr -> next_node -> ...
After:   prev <- curr    next_node -> ...
```

```python
# The atomic reversal step (memorize this!)
next_node = curr.next    # 1. Save next (will lose reference otherwise)
curr.next = prev         # 2. Reverse the pointer
prev = curr              # 3. Advance prev
curr = next_node         # 4. Advance curr
```

### Universal Reversal Template

```python
from typing import Optional

class ListNode:
    def __init__(self, val: int = 0, next: 'ListNode' = None):
        self.val = val
        self.next = next


def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Reverse an entire linked list in-place.

    Core invariant:
    - All nodes before `curr` have been reversed
    - `prev` points to the new head of the reversed portion
    - `curr` points to the next node to process

    Three-pointer technique:
    - prev: last node of reversed portion (starts as None)
    - curr: current node being processed (starts as head)
    - next_node: saved reference to curr's original next

    Time: O(n) - single pass through list
    Space: O(1) - only three pointers
    """
    prev = None
    curr = head

    while curr:
        next_node = curr.next  # Save next before breaking link
        curr.next = prev       # Reverse pointer direction
        prev = curr            # Advance prev
        curr = next_node       # Advance curr

    return prev  # prev is now the new head
```

### Recursive Alternative

```python
def reverse_list_recursive(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Reverse list recursively.

    Base case: empty list or single node
    Recursive case: reverse rest, then fix current node's position

    Time: O(n)
    Space: O(n) - recursion stack
    """
    # Base case: empty or single node
    if not head or not head.next:
        return head

    # Recursively reverse the rest
    new_head = reverse_list_recursive(head.next)

    # head.next is now the tail of reversed portion
    # Make it point back to head
    head.next.next = head
    head.next = None  # head becomes new tail

    return new_head
```

### The Dummy Node Pattern

For problems that modify list structure near the head, use a dummy node:

```python
def some_reversal_operation(head: ListNode) -> ListNode:
    """
    Dummy node simplifies edge cases:
    - When head might change
    - When we need to track "the node before" a segment
    """
    dummy = ListNode(0, head)

    # ... reversal logic using dummy as anchor ...

    return dummy.next
```

### Segment Reversal Template

To reverse a segment [left, right] within a list:

```python
def reverse_segment(head: ListNode, left: int, right: int) -> ListNode:
    """
    Reverse nodes from position left to right (1-indexed).

    Key insight: Find the node before the segment, then reverse exactly
    (right - left + 1) nodes, then reconnect.

    Visual:
    Before: ... -> before -> [L -> ... -> R] -> after -> ...
    After:  ... -> before -> [R -> ... -> L] -> after -> ...
    """
    dummy = ListNode(0, head)
    before_segment = dummy

    # Navigate to node before left position
    for _ in range(left - 1):
        before_segment = before_segment.next

    # Reverse the segment
    prev = None
    curr = before_segment.next
    for _ in range(right - left + 1):
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node

    # Reconnect:
    # - before_segment.next (old left) becomes new tail, points to curr
    # - before_segment points to prev (new head of reversed segment)
    before_segment.next.next = curr  # Connect old left (now tail) to after
    before_segment.next = prev       # Connect before to new head

    return dummy.next
```

### K-Group Reversal Template

Reverse every k consecutive nodes:

```python
def reverse_k_group(head: ListNode, k: int) -> ListNode:
    """
    Reverse nodes in k-groups. Remaining nodes (< k) stay as-is.

    Strategy:
    1. Check if k nodes available
    2. Reverse exactly k nodes
    3. Recursively process remaining
    4. Connect reversed group to result of recursion
    """
    # Check if k nodes are available
    curr = head
    count = 0
    while curr and count < k:
        curr = curr.next
        count += 1

    if count < k:
        return head  # Not enough nodes, don't reverse

    # Reverse k nodes
    prev = None
    curr = head
    for _ in range(k):
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node

    # head is now tail of reversed group
    # prev is now head of reversed group
    # curr is head of remaining list

    # Recursively reverse remaining groups
    head.next = reverse_k_group(curr, k)

    return prev  # New head of this group
```

### Pattern Variants

| Variant | Target | Nodes Reversed | Complexity |
|---------|--------|----------------|------------|
| **Full reversal** | Entire list | All N | O(N) time, O(1) space |
| **Segment reversal** | [left, right] | right-left+1 | O(N) time, O(1) space |
| **K-group reversal** | Every k nodes | Floor(N/k) groups | O(N) time, O(1) space |
| **Recursive reversal** | Entire list | All N | O(N) time, O(N) space |

### Complexity Analysis

All iterative reversal variants achieve:
- **Time**: O(N) - each node visited constant number of times
- **Space**: O(1) - only pointer variables, no auxiliary data structures

Recursive variants:
- **Time**: O(N)
- **Space**: O(N) or O(N/k) - recursion stack depth

### Common Pitfalls

1. **Losing references**: Always save `curr.next` before modifying `curr.next`
2. **Off-by-one in segment**: Use 1-indexed positions, navigate carefully
3. **Forgetting to reconnect**: After reversing segment, connect both ends
4. **Returning wrong head**: After full reversal, return `prev`, not `head`


