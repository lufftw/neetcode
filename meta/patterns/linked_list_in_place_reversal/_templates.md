## Quick Reference Templates

### Template 1: Full Reversal (LC 206)

```python
def reverseList(head: ListNode) -> ListNode:
    """
    Reverse entire linked list in-place.
    Time: O(N), Space: O(1)
    """
    prev = None
    curr = head

    while curr:
        next_node = curr.next  # Save
        curr.next = prev       # Reverse
        prev = curr            # Advance prev
        curr = next_node       # Advance curr

    return prev  # New head
```

### Template 2: Segment Reversal (LC 92)

```python
def reverseBetween(head: ListNode, left: int, right: int) -> ListNode:
    """
    Reverse nodes from position left to right (1-indexed).
    Time: O(N), Space: O(1)
    """
    if left == right:
        return head

    dummy = ListNode(0, head)
    before_segment = dummy

    # Navigate to before left
    for _ in range(left - 1):
        before_segment = before_segment.next

    # Reverse segment
    segment_start = before_segment.next
    prev = None
    curr = segment_start

    for _ in range(right - left + 1):
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node

    # Reconnect
    segment_start.next = curr       # Tail -> after
    before_segment.next = prev      # Before -> new head

    return dummy.next
```

### Template 3: K-Group Reversal (LC 25)

```python
def reverseKGroup(head: ListNode, k: int) -> ListNode:
    """
    Reverse every k consecutive nodes.
    Time: O(N), Space: O(1)
    """
    if k == 1 or not head:
        return head

    dummy = ListNode(0, head)
    group_prev = dummy

    while True:
        # Find kth node
        kth = group_prev
        for _ in range(k):
            kth = kth.next
            if not kth:
                return dummy.next  # Not enough nodes

        group_next = kth.next

        # Reverse group
        prev = group_next  # Trick: auto-connect to next group
        curr = group_prev.next

        for _ in range(k):
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node

        # Reconnect
        group_tail = group_prev.next
        group_prev.next = prev
        group_prev = group_tail  # Move to next group

    return dummy.next
```

### Helper: Recursive Full Reversal

```python
def reverseListRecursive(head: ListNode) -> ListNode:
    """
    Recursive reversal. Time: O(N), Space: O(N) stack.
    """
    if not head or not head.next:
        return head

    new_head = reverseListRecursive(head.next)
    head.next.next = head
    head.next = None

    return new_head
```

### Common Utilities

```python
# List <-> LinkedList conversion
def list_to_linkedlist(lst):
    dummy = ListNode(0)
    curr = dummy
    for val in lst:
        curr.next = ListNode(val)
        curr = curr.next
    return dummy.next

def linkedlist_to_list(head):
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result
```


