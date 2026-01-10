# solutions/0143_reorder_list.py
"""
Problem 0143 - Reorder List

Given a singly linked list L0 → L1 → … → Ln-1 → Ln,
reorder it to: L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → …

You may not modify the values in the list's nodes.
Only nodes themselves may be changed.

LeetCode Constraints:
- The number of nodes in the list is in the range [1, 5 * 10^4]
- 1 <= Node.val <= 1000

Key Insight:
The reordering interleaves the first half with the reversed second half.

Algorithm:
1. Find middle using slow/fast pointers
2. Reverse the second half of the list
3. Merge two halves by alternating nodes

This achieves O(n) time and O(1) space by avoiding any array storage.

Solution Approaches:
1. Three-phase (find middle + reverse + merge): O(n) time, O(1) space
2. Using array for random access: O(n) time, O(n) space
"""
from typing import List, Optional
from _runner import get_solver


class ListNode:
    """Definition for singly-linked list."""

    def __init__(self, val: int = 0, next: "ListNode" = None):
        self.val = val
        self.next = next


SOLUTIONS = {
    "default": {
        "class": "SolutionThreePhase",
        "method": "reorderList",
        "complexity": "O(n) time, O(1) space",
        "description": "Find middle, reverse second half, merge alternating",
    },
    "array": {
        "class": "SolutionArray",
        "method": "reorderList",
        "complexity": "O(n) time, O(n) space",
        "description": "Store nodes in array for O(1) random access",
    },
}


class SolutionThreePhase:
    """
    Three-phase approach: find middle, reverse, merge.

    Phase 1 - Find Middle:
    Use slow/fast pointers. When fast reaches end, slow is at middle.
    For even length lists, this gives the first middle node.

    Phase 2 - Reverse Second Half:
    Standard iterative reversal starting from slow.next.
    Disconnect first half by setting slow.next = None.

    Phase 3 - Merge:
    Alternate between nodes from first half and reversed second half.
    Each step: take from first, take from second, repeat.

    Example: 1 → 2 → 3 → 4 → 5
    After split: [1,2,3] and [4,5]
    After reverse: [1,2,3] and [5,4]
    After merge: 1 → 5 → 2 → 4 → 3
    """

    def reorderList(self, head: Optional[ListNode]) -> None:
        if not head or not head.next:
            return

        # Phase 1: Find middle using slow/fast pointers
        slow = fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next

        # Phase 2: Reverse second half
        # slow is now at the last node of first half
        second = slow.next
        slow.next = None  # Cut the list
        prev = None

        while second:
            next_node = second.next
            second.next = prev
            prev = second
            second = next_node

        # Now prev is head of reversed second half

        # Phase 3: Merge alternating
        first = head
        second = prev

        while second:
            # Save next pointers
            first_next = first.next
            second_next = second.next

            # Interleave
            first.next = second
            second.next = first_next

            # Move forward
            first = first_next
            second = second_next


class SolutionArray:
    """
    Array-based approach using random access.

    Store all nodes in an array, then use two pointers from
    both ends to create the new ordering.

    Trade-off: Simpler logic but uses O(n) extra space.
    Useful when the constraint allows extra space.
    """

    def reorderList(self, head: Optional[ListNode]) -> None:
        if not head or not head.next:
            return

        # Collect all nodes in array
        nodes: List[ListNode] = []
        current = head
        while current:
            nodes.append(current)
            current = current.next

        # Two-pointer approach
        left, right = 0, len(nodes) - 1

        while left < right:
            nodes[left].next = nodes[right]
            left += 1

            if left == right:
                break

            nodes[right].next = nodes[left]
            right -= 1

        nodes[left].next = None  # Terminate the list


def _list_to_linked(values: List[int]) -> Optional[ListNode]:
    """Convert list to linked list."""
    if not values:
        return None
    head = ListNode(values[0])
    current = head
    for val in values[1:]:
        current.next = ListNode(val)
        current = current.next
    return head


def _linked_to_list(head: Optional[ListNode]) -> List[int]:
    """Convert linked list to list."""
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


def solve():
    import sys
    import json

    data = sys.stdin.read().strip()
    values = json.loads(data)

    head = _list_to_linked(values)

    solver = get_solver(SOLUTIONS)
    solver.reorderList(head)

    result = _linked_to_list(head)
    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
