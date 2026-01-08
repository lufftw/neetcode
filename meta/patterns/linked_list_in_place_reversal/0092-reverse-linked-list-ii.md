## LeetCode 92: Reverse Linked List II (Segment Reversal)

> **Role**: Variant
> **Difficulty**: Medium
> **Pattern**: `reverse_segment`
> **Delta from base**: Reverse only positions [left, right] instead of entire list. Requires finding segment boundaries and reconnecting after reversal.

### Problem Statement

Given the head of a singly linked list and two integers `left` and `right` where `left <= right`, reverse the nodes of the list from position `left` to position `right`, and return the reversed list.

**Constraints**:
- 1 <= n <= 500 (number of nodes)
- -500 <= Node.val <= 500
- 1 <= left <= right <= n

### Solution: Segment Reversal with Boundary Tracking

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

### Alternative: One-Pass Insert-at-Front

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

### Key Insights

1. **Dummy node is essential**: When left=1, the head changes. Dummy node provides a stable anchor.
2. **Track four positions**: before_segment, segment_start, segment_end (implicit), after_segment
3. **Two-pass vs one-pass**: First approach is clearer; second is slightly trickier but same complexity
4. **The reconnection step**: Easy to forget - segment_tail must point to after_segment


