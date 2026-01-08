## LeetCode 206: Reverse Linked List (Base Template)

> **Role**: Base Template
> **Difficulty**: Easy
> **Pattern**: `reverse_entire_list`

### Problem Statement

Given the head of a singly linked list, reverse the list and return the reversed list.

**Constraints**:
- 0 <= n <= 5000 (number of nodes)
- -5000 <= Node.val <= 5000

### Solution: Iterative Three-Pointer Reversal

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

### Solution: Recursive Reversal

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

### Key Insights

1. **Iterative is preferred**: O(1) space vs O(N) recursion stack
2. **Save before modifying**: Always save `curr.next` before overwriting
3. **Return prev, not head**: After loop, `prev` is the new head
4. **Recursive builds from tail**: Recursion reverses tail first, fixes on return


