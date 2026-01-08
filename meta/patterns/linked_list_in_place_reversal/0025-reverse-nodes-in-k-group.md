## LeetCode 25: Reverse Nodes in k-Group (K-Group Reversal)

> **Role**: Advanced Variant
> **Difficulty**: Hard
> **Pattern**: `reverse_k_group`
> **Delta from base**: Reverse every consecutive k nodes. Must check if k nodes available before reversing. Remaining nodes (< k) stay unchanged.

### Problem Statement

Given the head of a linked list, reverse the nodes of the list k at a time, and return the modified list.

k is a positive integer and is less than or equal to the length of the linked list. If the number of nodes is not a multiple of k, then left-out nodes at the end should remain as-is.

You may not alter the values in the list's nodes, only nodes themselves may be changed.

**Constraints**:
- 1 <= n <= 5000 (number of nodes)
- 0 <= Node.val <= 1000
- 1 <= k <= n

### Solution: Iterative K-Group Reversal

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

### Solution: Recursive K-Group Reversal

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

### Key Insights

1. **Two-phase per group**: First check availability, then reverse. Don't mix these.
2. **Initialize prev to group_next**: Clever trick - reversed tail automatically connects to next group.
3. **Track group_prev carefully**: It's the node BEFORE the group, used for reconnection.
4. **Recursive space trade-off**: O(N/k) stack depth vs O(1) iterative. For small k, recursion has significant overhead.
5. **Edge cases**: k=1 means no reversal; single node means return immediately.


