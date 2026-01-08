# solutions/0206_reverse_linked_list.py
"""
Problem: Reverse Linked List
Link: https://leetcode.com/problems/reverse-linked-list/

Given the head of a singly linked list, reverse the list, and return the
reversed list.

Example 1:
    Input: head = [1,2,3,4,5]
    Output: [5,4,3,2,1]

Example 2:
    Input: head = [1,2]
    Output: [2,1]

Example 3:
    Input: head = []
    Output: []

Constraints:
- The number of nodes in the list is in the range [0, 5000]
- -5000 <= Node.val <= 5000

Topics: Linked List, Recursion

Follow-up: A linked list can be reversed either iteratively or recursively.
Could you implement both?
"""
from typing import List, Optional
from _runner import get_solver


class ListNode:
    def __init__(self, val: int = 0, next: 'ListNode' = None):
        self.val = val
        self.next = next


# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# Polymorphic pattern: each entry specifies class + method
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionIterative",
        "method": "reverseList",
        "complexity": "O(N) time, O(1) space",
        "description": "Iterative three-pointer reversal",
        "api_kernels": ["LinkedListInPlaceReversal"],
        "patterns": ["reverse_entire_list"],
    },
    "iterative": {
        "class": "SolutionIterative",
        "method": "reverseList",
        "complexity": "O(N) time, O(1) space",
        "description": "Iterative three-pointer reversal",
        "api_kernels": ["LinkedListInPlaceReversal"],
        "patterns": ["reverse_entire_list"],
    },
    "recursive": {
        "class": "SolutionRecursive",
        "method": "reverseList",
        "complexity": "O(N) time, O(N) space",
        "description": "Recursive reversal - reverse tail first, fix on return",
        "api_kernels": ["LinkedListInPlaceReversal"],
        "patterns": ["reverse_entire_list"],
    },
}


# ============================================
# Solution 1: Iterative Three-Pointer Reversal
#
# Algorithm:
#   At each step, reverse one edge: make curr.next point to prev.
#   Use three pointers to track positions:
#   - prev: last node of reversed portion (starts as None)
#   - curr: current node being processed (starts as head)
#   - next_node: saved reference to curr's original next
#
# Time: O(N) - single pass through list
# Space: O(1) - only three pointer variables
# ============================================
class SolutionIterative:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Reverse linked list iteratively using three-pointer technique.

        Core invariant maintained at each iteration:
        - All nodes before curr have been reversed
        - prev points to the head of the reversed portion
        - curr points to the next node to reverse

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


# ============================================
# Solution 2: Recursive Reversal
#
# Algorithm:
#   Base case: empty list or single node - already reversed
#   Recursive case: reverse the tail first, then fix current node
#
#   Key insight: after recursing, head.next is the TAIL of
#   the reversed sublist. Make it point back to head.
#
# Time: O(N) - visit each node once
# Space: O(N) - recursion stack depth
# ============================================
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


# ============================================
# Helper functions for LinkedList conversion
# ============================================
def list_to_linkedlist(lst: List[int]) -> Optional[ListNode]:
    """Convert Python list to LinkedList."""
    if not lst:
        return None
    dummy = ListNode(0)
    current = dummy
    for val in lst:
        current.next = ListNode(val)
        current = current.next
    return dummy.next


def linkedlist_to_list(node: Optional[ListNode]) -> List[int]:
    """Convert LinkedList to Python list."""
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result


def solve():
    """
    Input format:
    Line 1: JSON array of integers representing the linked list

    Example:
    [1,2,3,4,5]
    """
    import sys
    import json

    # Parse input
    lines = sys.stdin.read().strip().split('\n')
    values = json.loads(lines[0])
    head = list_to_linkedlist(values)

    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.reverseList(head)

    # Output result as JSON array
    print(json.dumps(linkedlist_to_list(result), separators=(',', ':')))


if __name__ == "__main__":
    solve()
