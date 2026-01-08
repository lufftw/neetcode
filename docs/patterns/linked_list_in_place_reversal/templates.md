# Linked List In-Place Reversal: Complete Reference

> **API Kernel**: `LinkedListInPlaceReversal`
> **Core Mechanism**: Reverse linked list nodes in-place by manipulating next pointers, using O(1) extra space.

This document presents the **canonical in-place linked list reversal templates** covering full list reversal, segment reversal, and k-group reversal. Each implementation follows consistent naming conventions and includes detailed pointer manipulation logic.

---

## Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [LeetCode 206: Reverse Linked List (Base Template)](#2-leetcode-206-reverse-linked-list-base-template)
3. [LeetCode 92: Reverse Linked List II (Segment Reversal)](#3-leetcode-92-reverse-linked-list-ii-segment-reversal)
4. [LeetCode 25: Reverse Nodes in k-Group (K-Group Reversal)](#4-leetcode-25-reverse-nodes-in-k-group-k-group-reversal)
5. [Comparison Table](#5-comparison-table)
6. [When to Use In-Place Reversal](#6-when-to-use-in-place-reversal)
7. [Quick Reference Templates](#7-quick-reference-templates)

---

## 1. Core Concepts

### 1.1 The In-Place Reversal Problem

Given a linked list, reverse some or all of its nodes without allocating new nodes.

**Key constraint**: O(1) space - we cannot copy values to an array and reverse there.

### 1.2 The Pointer Reversal Technique

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

### 1.3 Universal Reversal Template

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

### 1.4 Recursive Alternative

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

### 1.5 The Dummy Node Pattern

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

### 1.6 Segment Reversal Template

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

### 1.7 K-Group Reversal Template

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

### 1.8 Pattern Variants

| Variant | Target | Nodes Reversed | Complexity |
|---------|--------|----------------|------------|
| **Full reversal** | Entire list | All N | O(N) time, O(1) space |
| **Segment reversal** | [left, right] | right-left+1 | O(N) time, O(1) space |
| **K-group reversal** | Every k nodes | Floor(N/k) groups | O(N) time, O(1) space |
| **Recursive reversal** | Entire list | All N | O(N) time, O(N) space |

### 1.9 Complexity Analysis

All iterative reversal variants achieve:
- **Time**: O(N) - each node visited constant number of times
- **Space**: O(1) - only pointer variables, no auxiliary data structures

Recursive variants:
- **Time**: O(N)
- **Space**: O(N) or O(N/k) - recursion stack depth

### 1.10 Common Pitfalls

1. **Losing references**: Always save `curr.next` before modifying `curr.next`
2. **Off-by-one in segment**: Use 1-indexed positions, navigate carefully
3. **Forgetting to reconnect**: After reversing segment, connect both ends
4. **Returning wrong head**: After full reversal, return `prev`, not `head`

---

## 2. LeetCode 206: Reverse Linked List (Base Template)

> **Role**: Base Template
> **Difficulty**: Easy
> **Pattern**: `reverse_entire_list`

### 2.1 Problem Statement

Given the head of a singly linked list, reverse the list and return the reversed list.

**Constraints**:
- 0 <= n <= 5000 (number of nodes)
- -5000 <= Node.val <= 5000

### 2.2 Solution: Iterative Three-Pointer Reversal

```python
"""
Problem: Reverse Linked List
Link: https://leetcode.com/problems/reverse-linked-list/

Algorithm: Iterative In-Place Reversal
- Use three pointers: prev, curr, next_node
- At each step, reverse one edge: curr.next = prev
- Advance all pointers by one position
- When curr becomes None, prev is the new head

Visual trace for [1 -> 2 -> 3 -> 4 -> 5]:

Step 0: prev=None, curr=1
        None <- 1    2 -> 3 -> 4 -> 5 -> None

Step 1: prev=1, curr=2
        None <- 1 <- 2    3 -> 4 -> 5 -> None

Step 2: prev=2, curr=3
        None <- 1 <- 2 <- 3    4 -> 5 -> None

Step 3: prev=3, curr=4
        None <- 1 <- 2 <- 3 <- 4    5 -> None

Step 4: prev=4, curr=5
        None <- 1 <- 2 <- 3 <- 4 <- 5    None

Step 5: prev=5, curr=None -> Return prev (5)

Time: O(N) - single pass through list
Space: O(1) - only three pointer variables
"""
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: 'ListNode' = None):
        self.val = val
        self.next = next


class SolutionIterative:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Reverse linked list iteratively using three-pointer technique.

        Core invariant maintained at each iteration:
        - All nodes before curr have been reversed
        - prev points to the head of the reversed portion
        - curr points to the next node to reverse

        The three pointers work together:
        - prev: tracks the new head (last reversed node)
        - curr: the node currently being processed
        - next_node: saves curr's original next before we overwrite it
        """
        prev = None  # Will become the new head
        curr = head  # Start from original head

        while curr:
            # STEP 1: Save next pointer before we lose it
            # After curr.next = prev, we'd lose access to the rest of the list
            next_node = curr.next

            # STEP 2: Reverse the pointer direction
            # This is the core operation - make curr point backward
            curr.next = prev

            # STEP 3: Advance prev to curr
            # prev is now one step further into the reversed portion
            prev = curr

            # STEP 4: Advance curr to saved next
            # Move to the next unprocessed node
            curr = next_node

        # When curr is None, prev points to the last node (new head)
        return prev
```

### 2.3 Solution: Recursive Reversal

```python
class SolutionRecursive:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Reverse linked list recursively.

        Strategy: Reverse the tail first, then fix current node.

        For list [1 -> 2 -> 3 -> 4 -> 5]:
        1. Recurse until we reach node 5 (base case)
        2. On the way back:
           - At node 4: make 5 point to 4, disconnect 4 -> 5
           - At node 3: make 4 point to 3, disconnect 3 -> 4
           - ...and so on

        The key insight: after recursing, head.next is the TAIL of
        the reversed sublist. We make it point back to head.

        Time: O(N) - visit each node once
        Space: O(N) - recursion stack depth
        """
        # Base case: empty list or single node
        # A single node or empty list is already reversed
        if not head or not head.next:
            return head

        # Recursively reverse the rest of the list
        # new_head will be the last node (new head of reversed list)
        new_head = self.reverseList(head.next)

        # At this point:
        # - new_head points to the tail of original list (head of reversed)
        # - head.next points to head.next (unchanged yet)
        # - head.next is now the TAIL of the reversed sublist

        # Make head.next point back to head
        # Before: head -> head.next -> (reversed sublist with new_head)
        # After:  head <- head.next    (reversed sublist with new_head)
        head.next.next = head

        # Disconnect head from pointing forward
        # head is now the new tail, should point to None
        head.next = None

        # Return the head of the fully reversed list
        return new_head
```

### 2.4 Key Insights

1. **Iterative is preferred**: O(1) space vs O(N) recursion stack
2. **Save before modifying**: Always save `curr.next` before overwriting
3. **Return prev, not head**: After loop, `prev` is the new head
4. **Recursive builds from tail**: Recursion reverses tail first, fixes on return

---

## 3. LeetCode 92: Reverse Linked List II (Segment Reversal)

> **Role**: Variant
> **Difficulty**: Medium
> **Pattern**: `reverse_segment`
> **Delta from base**: Reverse only positions [left, right] instead of entire list. Requires finding segment boundaries and reconnecting after reversal.

### 3.1 Problem Statement

Given the head of a singly linked list and two integers `left` and `right` where `left <= right`, reverse the nodes of the list from position `left` to position `right`, and return the reversed list.

**Constraints**:
- 1 <= n <= 500 (number of nodes)
- -500 <= Node.val <= 500
- 1 <= left <= right <= n

### 3.2 Solution: Segment Reversal with Boundary Tracking

```python
"""
Problem: Reverse Linked List II
Link: https://leetcode.com/problems/reverse-linked-list-ii/

Algorithm: Segment Reversal with Dummy Node
- Use dummy node to handle edge case where left=1 (head changes)
- Navigate to the node BEFORE the segment to reverse
- Reverse exactly (right - left + 1) nodes
- Reconnect the reversed segment to the rest of the list

Visual for [1 -> 2 -> 3 -> 4 -> 5], left=2, right=4:

Original:
    dummy -> 1 -> 2 -> 3 -> 4 -> 5 -> None
              ^    ^---------^    ^
         before   segment to    after
                   reverse

Step 1: Navigate to before_segment (node 1)
Step 2: Reverse nodes 2->3->4 to get 4->3->2
Step 3: Reconnect:
    - Node 2 (segment_tail) points to node 5 (after)
    - Node 1 (before_segment) points to node 4 (reversed_head)

Result:
    dummy -> 1 -> 4 -> 3 -> 2 -> 5 -> None

Time: O(N) - single pass to find segment, single pass to reverse
Space: O(1) - only pointer variables
"""
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: 'ListNode' = None):
        self.val = val
        self.next = next


class SolutionIterative:
    def reverseBetween(
        self, head: Optional[ListNode], left: int, right: int
    ) -> Optional[ListNode]:
        """
        Reverse nodes from position left to right (1-indexed).

        Key insight: We need to track four critical positions:
        1. before_segment: node immediately before left position
        2. segment_start: first node to reverse (becomes tail after)
        3. segment_end: last node to reverse (becomes head after)
        4. after_segment: node immediately after right position

        The dummy node handles the edge case where left=1 (reversing from head).
        """
        # Edge case: no reversal needed
        if left == right:
            return head

        # Dummy node simplifies handling when left=1
        # Without dummy, we'd need special logic for head modification
        dummy = ListNode(0, head)

        # PHASE 1: Navigate to the node BEFORE the segment
        # After this loop, before_segment is at position (left-1)
        # Its .next is the first node to reverse
        before_segment = dummy
        for _ in range(left - 1):
            before_segment = before_segment.next

        # PHASE 2: Reverse the segment [left, right]
        # segment_start will become segment_tail after reversal
        segment_start = before_segment.next

        # Standard three-pointer reversal for exactly (right - left + 1) nodes
        prev = None
        curr = segment_start
        for _ in range(right - left + 1):
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node

        # After reversal:
        # - prev points to segment_end (new head of reversed segment)
        # - curr points to after_segment (first node after reversed portion)
        # - segment_start is now segment_tail

        # PHASE 3: Reconnect the reversed segment
        # Connect segment_tail to the rest of the list
        segment_start.next = curr  # segment_tail -> after_segment

        # Connect before_segment to the new head of reversed portion
        before_segment.next = prev  # before_segment -> segment_head

        return dummy.next
```

### 3.3 Alternative: One-Pass Insert-at-Front

```python
class SolutionOnePass:
    def reverseBetween(
        self, head: Optional[ListNode], left: int, right: int
    ) -> Optional[ListNode]:
        """
        One-pass reversal by repeatedly moving nodes to front of segment.

        Instead of reversing then reconnecting, we:
        1. Find before_segment
        2. Repeatedly take the next node after segment_start
           and insert it right after before_segment

        Visual for [1 -> 2 -> 3 -> 4 -> 5], left=2, right=4:

        Start:    1 -> 2 -> 3 -> 4 -> 5
                  ^    ^
              before  start

        Move 3:   1 -> 3 -> 2 -> 4 -> 5
                  ^         ^
              before      start (unchanged!)

        Move 4:   1 -> 4 -> 3 -> 2 -> 5
                  ^              ^
              before           start

        This approach maintains the invariant that segment_start
        always points to the original left-th node (which moves right).

        Time: O(N), Space: O(1)
        """
        dummy = ListNode(0, head)
        before_segment = dummy

        # Navigate to before left position
        for _ in range(left - 1):
            before_segment = before_segment.next

        # segment_start stays fixed as we move nodes in front of it
        segment_start = before_segment.next

        # Perform (right - left) moves
        # Each move takes segment_start.next and inserts after before_segment
        for _ in range(right - left):
            # Node to move: the one right after segment_start
            node_to_move = segment_start.next

            # Remove node_to_move from its position
            # segment_start.next now skips over node_to_move
            segment_start.next = node_to_move.next

            # Insert node_to_move right after before_segment
            node_to_move.next = before_segment.next
            before_segment.next = node_to_move

        return dummy.next
```

### 3.4 Key Insights

1. **Dummy node is essential**: When left=1, the head changes. Dummy node provides a stable anchor.
2. **Track four positions**: before_segment, segment_start, segment_end (implicit), after_segment
3. **Two-pass vs one-pass**: First approach is clearer; second is slightly trickier but same complexity
4. **The reconnection step**: Easy to forget - segment_tail must point to after_segment

---

## 4. LeetCode 25: Reverse Nodes in k-Group (K-Group Reversal)

> **Role**: Advanced Variant
> **Difficulty**: Hard
> **Pattern**: `reverse_k_group`
> **Delta from base**: Reverse every consecutive k nodes. Must check if k nodes available before reversing. Remaining nodes (< k) stay unchanged.

### 4.1 Problem Statement

Given the head of a linked list, reverse the nodes of the list k at a time, and return the modified list.

k is a positive integer and is less than or equal to the length of the linked list. If the number of nodes is not a multiple of k, then left-out nodes at the end should remain as-is.

You may not alter the values in the list's nodes, only nodes themselves may be changed.

**Constraints**:
- 1 <= n <= 5000 (number of nodes)
- 0 <= Node.val <= 1000
- 1 <= k <= n

### 4.2 Solution: Iterative K-Group Reversal

```python
"""
Problem: Reverse Nodes in k-Group
Link: https://leetcode.com/problems/reverse-nodes-in-k-group/

Algorithm: Iterative Group-by-Group Reversal
- Use dummy node for clean head handling
- For each group:
  1. Check if k nodes are available
  2. If yes, reverse exactly k nodes
  3. Reconnect the reversed group
  4. Move to next group
- If fewer than k nodes remain, leave them unchanged

Visual for [1 -> 2 -> 3 -> 4 -> 5], k=2:

Initial:
    dummy -> 1 -> 2 -> 3 -> 4 -> 5 -> None
    ^
group_prev

Group 1: Reverse [1,2]
    dummy -> 2 -> 1 -> 3 -> 4 -> 5 -> None
                  ^
             group_prev (now at node 1)

Group 2: Reverse [3,4]
    dummy -> 2 -> 1 -> 4 -> 3 -> 5 -> None
                            ^
                       group_prev (now at node 3)

Group 3: Only [5] remains (< k), stop

Result: [2 -> 1 -> 4 -> 3 -> 5]

Time: O(N) - each node visited twice (once for counting, once for reversal)
Space: O(1) - only pointer variables
"""
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: 'ListNode' = None):
        self.val = val
        self.next = next


class SolutionIterative:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        """
        Reverse every k consecutive nodes in the linked list.

        Key positions tracked:
        - group_prev: node before the current group (anchor for reconnection)
        - group_start: first node of current group (becomes tail after reversal)
        - kth_node: k-th node from group_prev (becomes head after reversal)
        - group_next: first node after current group

        The dummy node provides a stable anchor when the first group
        is reversed (changing the actual head of the list).
        """
        if k == 1 or not head:
            return head

        dummy = ListNode(0, head)
        group_prev = dummy

        while True:
            # PHASE 1: Find the k-th node from group_prev
            # If fewer than k nodes remain, we're done
            kth_node = self._get_kth_node(group_prev, k)
            if not kth_node:
                break

            # Save the node after this group (for reconnection)
            group_next = kth_node.next

            # PHASE 2: Reverse the k nodes [group_prev.next ... kth_node]
            # Standard reversal with prev initialized to group_next
            # This makes the last reversed node point to group_next automatically
            prev = group_next
            curr = group_prev.next

            # Reverse exactly k nodes
            for _ in range(k):
                next_node = curr.next
                curr.next = prev
                prev = curr
                curr = next_node

            # PHASE 3: Reconnect
            # After reversal:
            # - prev points to kth_node (new head of reversed group)
            # - group_prev.next is old group_start (new tail of reversed group)
            # - new tail already points to group_next (set up in phase 2)

            # Save old group_start (now group_tail) for next iteration
            group_tail = group_prev.next

            # Connect group_prev to new group head (kth_node)
            group_prev.next = prev

            # Move group_prev to the tail of this group for next iteration
            group_prev = group_tail

        return dummy.next

    def _get_kth_node(self, start: ListNode, k: int) -> Optional[ListNode]:
        """
        Return the k-th node from start.next.

        Starting from start, advance k times. If we hit None before
        k steps, return None (not enough nodes).

        Example: _get_kth_node(dummy, 3) for dummy->1->2->3->4
                 Returns node 3
        """
        curr = start
        while curr and k > 0:
            curr = curr.next
            k -= 1
        return curr
```

### 4.3 Solution: Recursive K-Group Reversal

```python
class SolutionRecursive:
    def __init__(self):
        # Stores the node after the reversed k nodes
        self.successor: Optional[ListNode] = None

    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        """
        Recursive k-group reversal.

        Strategy:
        1. Check if k nodes are available from head
        2. If yes, reverse exactly k nodes starting from head
        3. Recursively process the remaining list
        4. Connect the tail of reversed group to the result of recursion

        The recursion handles connecting groups naturally:
        Each call returns the head of its fully processed portion.

        Time: O(N) - each node visited twice
        Space: O(N/k) - recursion depth is number of groups
        """
        # STEP 1: Check if k nodes are available
        curr = head
        count = 0
        while curr and count < k:
            curr = curr.next
            count += 1

        # If fewer than k nodes, don't reverse - return as-is
        if count < k:
            return head

        # STEP 2: Reverse exactly k nodes
        # After this, head becomes tail and new_head is the k-th node
        new_head = self._reverse_k(head, k)

        # STEP 3: Recursively reverse remaining groups
        # self.successor was set by _reverse_k to point to (k+1)-th node
        # head is now the tail of the reversed group
        head.next = self.reverseKGroup(self.successor, k)

        return new_head

    def _reverse_k(self, head: ListNode, k: int) -> ListNode:
        """
        Reverse exactly k nodes starting from head.
        Sets self.successor to the (k+1)-th node.
        Returns the new head (originally the k-th node).

        Uses recursion to reverse:
        - Base case (k=1): we're at the k-th node, save successor
        - Recursive case: reverse rest first, then fix current pointer
        """
        if k == 1:
            # Base case: head is the k-th node
            # Save the node after it for later reconnection
            self.successor = head.next
            return head

        # Recursively reverse remaining k-1 nodes
        new_head = self._reverse_k(head.next, k - 1)

        # Reverse the pointer: make next node point back to current
        head.next.next = head
        head.next = None  # Will be set correctly in reverseKGroup

        return new_head
```

### 4.4 Key Insights

1. **Two-phase per group**: First check availability, then reverse. Don't mix these.
2. **Initialize prev to group_next**: Clever trick - reversed tail automatically connects to next group.
3. **Track group_prev carefully**: It's the node BEFORE the group, used for reconnection.
4. **Recursive space trade-off**: O(N/k) stack depth vs O(1) iterative. For small k, recursion has significant overhead.
5. **Edge cases**: k=1 means no reversal; single node means return immediately.

---

## 5. Comparison Table

| Problem | Scope | Key Challenge | Critical Step | Complexity |
|---------|-------|---------------|---------------|------------|
| **206. Reverse Linked List** | Entire list | Basic three-pointer reversal | Save `curr.next` before overwriting | O(N), O(1) |
| **92. Reverse Linked List II** | Segment [left, right] | Find boundaries, reconnect after | Track `before_segment` and reconnect both ends | O(N), O(1) |
| **25. Reverse Nodes in k-Group** | Every k nodes | Check availability, group management | Initialize `prev` to `group_next` for auto-connection | O(N), O(1) |

### 5.1 What Changes Between Variants

| Aspect | 206 (Full) | 92 (Segment) | 25 (K-Group) |
|--------|------------|--------------|--------------|
| **Pre-processing** | None | Navigate to before_segment | Find kth_node, check availability |
| **Nodes reversed** | All N | right - left + 1 | k per group |
| **Prev initialization** | None | None | group_next (trick) |
| **Post-processing** | None | Reconnect both ends | Move group_prev to new tail |
| **Dummy node needed** | Optional | Required (left=1) | Required (first group) |
| **Loop condition** | `while curr` | Fixed count | `while kth_node exists` |

### 5.2 Memory Model

```
Full Reversal (206):
Before: None  1 -> 2 -> 3 -> 4 -> 5 -> None
After:  None <- 1 <- 2 <- 3 <- 4 <- 5

Segment Reversal (92) [left=2, right=4]:
Before: 1 -> 2 -> 3 -> 4 -> 5
After:  1 -> 4 -> 3 -> 2 -> 5
        ^    ^---------^    ^
     anchor  reversed    reconnect

K-Group Reversal (25) [k=2]:
Before: 1 -> 2 -> 3 -> 4 -> 5
After:  2 -> 1 -> 4 -> 3 -> 5
        ^----^    ^----^    ^
        group1    group2   leftover
```

---

## 6. When to Use In-Place Reversal

### 6.1 Decision Flowchart

```
Is this a linked list problem?
├── No → Different pattern
└── Yes → Does it involve reversing node order?
    ├── No → Consider: two-pointers, fast/slow, merge
    └── Yes → IN-PLACE REVERSAL PATTERN
        │
        ├── Reverse entire list?
        │   └── Use 206 template (three-pointer)
        │
        ├── Reverse a specific segment [left, right]?
        │   └── Use 92 template (dummy + boundary tracking)
        │
        ├── Reverse in groups of k?
        │   └── Use 25 template (group management + kth-node check)
        │
        ├── Reverse pairs (k=2)?
        │   └── Use 25 template with k=2
        │
        └── Reverse with some condition?
            └── Combine with appropriate variant + condition check
```

### 6.2 Pattern Recognition Signals

**Use In-Place Reversal when you see**:
- "Reverse" + "linked list" in problem statement
- Need to reorder nodes without extra space
- Swap adjacent pairs or groups
- Follow-up asks for O(1) space

**Key constraint indicators**:
- "You may not modify the values" → Must manipulate pointers
- "O(1) extra memory" → Must be in-place
- "In one pass" → Iterative approach preferred

### 6.3 Variant Selection Guide

| Scenario | Variant | Template |
|----------|---------|----------|
| Reverse everything | Full | 206 |
| Reverse middle portion | Segment | 92 |
| Reverse from head to position | Segment (left=1) | 92 |
| Reverse every 2 nodes | K-Group (k=2) | 25 |
| Reverse every k nodes | K-Group | 25 |
| Reverse if condition met | Custom + base | 206 + condition |

### 6.4 Space-Time Trade-offs

| Approach | Time | Space | Use When |
|----------|------|-------|----------|
| Iterative | O(N) | O(1) | Default choice |
| Recursive | O(N) | O(N) | Cleaner for some k-group cases |
| Array copy | O(N) | O(N) | Only if space not constrained |

### 6.5 Common Mistakes to Avoid

1. **Not using dummy node** when head might change
2. **Forgetting to save `next`** before reversing pointer
3. **Wrong reconnection** after segment reversal
4. **Off-by-one** in position counting (1-indexed vs 0-indexed)
5. **Reversing too many nodes** in k-group when remainder < k

---

## 7. Quick Reference Templates

### 7.1 Template 1: Full Reversal (LC 206)

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

### 7.2 Template 2: Segment Reversal (LC 92)

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

### 7.3 Template 3: K-Group Reversal (LC 25)

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

### 7.4 Helper: Recursive Full Reversal

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

### 7.5 Common Utilities

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



---



*Document generated for NeetCode Practice Framework — API Kernel: LinkedListInPlaceReversal*
