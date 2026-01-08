# solutions/0092_reverse_linked_list_ii.py
"""
Problem: Reverse Linked List II
Link: https://leetcode.com/problems/reverse-linked-list-ii/

Given the head of a singly linked list and two integers left and right where
left <= right, reverse the nodes of the list from position left to position
right, and return the reversed list.

Example 1:
    Input: head = [1,2,3,4,5], left = 2, right = 4
    Output: [1,4,3,2,5]

Example 2:
    Input: head = [5], left = 1, right = 1
    Output: [5]

Constraints:
- The number of nodes in the list is n
- 1 <= n <= 500
- -500 <= Node.val <= 500
- 1 <= left <= right <= n

Topics: Linked List

Follow-up: Could you do it in one pass?
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
        "class": "SolutionTwoPass",
        "method": "reverseBetween",
        "complexity": "O(N) time, O(1) space",
        "description": "Two-pass segment reversal with boundary tracking",
        "api_kernels": ["LinkedListInPlaceReversal"],
        "patterns": ["reverse_segment"],
    },
    "two_pass": {
        "class": "SolutionTwoPass",
        "method": "reverseBetween",
        "complexity": "O(N) time, O(1) space",
        "description": "Two-pass segment reversal with boundary tracking",
        "api_kernels": ["LinkedListInPlaceReversal"],
        "patterns": ["reverse_segment"],
    },
    "one_pass": {
        "class": "SolutionOnePass",
        "method": "reverseBetween",
        "complexity": "O(N) time, O(1) space",
        "description": "One-pass reversal by repeatedly inserting at front",
        "api_kernels": ["LinkedListInPlaceReversal"],
        "patterns": ["reverse_segment"],
    },
}


# ============================================
# Solution 1: Two-Pass Segment Reversal
#
# Algorithm:
#   Pass 1: Navigate to the node BEFORE the segment to reverse
#   Pass 2: Reverse exactly (right - left + 1) nodes
#   Finally: Reconnect the reversed segment to the list
#
# Visual for [1 -> 2 -> 3 -> 4 -> 5], left=2, right=4:
#
# Original:
#     dummy -> 1 -> 2 -> 3 -> 4 -> 5 -> None
#              ^    ^---------^    ^
#         before   segment to    after
#                   reverse
#
# After reversal:
#     dummy -> 1 -> 4 -> 3 -> 2 -> 5 -> None
#
# Time: O(N) - single pass to find segment, single pass to reverse
# Space: O(1) - only pointer variables
# ============================================
class SolutionTwoPass:
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


# ============================================
# Solution 2: One-Pass Insert-at-Front
#
# Algorithm:
#   Instead of reversing then reconnecting, we:
#   1. Find before_segment
#   2. Repeatedly take the next node after segment_start
#      and insert it right after before_segment
#
# Visual for [1 -> 2 -> 3 -> 4 -> 5], left=2, right=4:
#
# Start:    1 -> 2 -> 3 -> 4 -> 5
#           ^    ^
#       before  start
#
# Move 3:   1 -> 3 -> 2 -> 4 -> 5
#           ^         ^
#       before      start (unchanged!)
#
# Move 4:   1 -> 4 -> 3 -> 2 -> 5
#           ^              ^
#       before           start
#
# This approach maintains the invariant that segment_start
# always points to the original left-th node (which moves right).
#
# Time: O(N) - single pass
# Space: O(1) - only pointer variables
# ============================================
class SolutionOnePass:
    def reverseBetween(
        self, head: Optional[ListNode], left: int, right: int
    ) -> Optional[ListNode]:
        """
        One-pass reversal by repeatedly moving nodes to front of segment.

        The trick: segment_start stays fixed as we move nodes in front of it.
        Each iteration takes segment_start.next and inserts it after before_segment.
        """
        # Edge case: no reversal needed
        if left == right:
            return head

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


# ============================================
# JUDGE_FUNC - Custom validation
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result by computing the expected segment reversal.

    Args:
        actual: Program output (may be list or string)
        expected: Expected output (None if from generator)
        input_data: Raw input string

    Returns:
        bool: True if correct
    """
    import json
    import ast

    # Parse input
    lines = input_data.strip().split('\n')
    values = json.loads(lines[0])
    left = int(lines[1])
    right = int(lines[2])

    # Compute expected result using simple simulation
    correct = _compute_segment_reversal(values, left, right)

    # Parse actual output
    try:
        if isinstance(actual, list):
            actual_list = actual
        else:
            actual_list = ast.literal_eval(str(actual).strip())
        return actual_list == correct
    except (ValueError, SyntaxError):
        return False


def _compute_segment_reversal(values: List[int], left: int, right: int) -> List[int]:
    """Compute expected segment reversal result."""
    result = values.copy()
    # Convert to 0-indexed
    l, r = left - 1, right - 1
    # Reverse the segment [l, r]
    result[l:r+1] = result[l:r+1][::-1]
    return result


JUDGE_FUNC = judge


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
    Line 2: left position (1-indexed)
    Line 3: right position (1-indexed)

    Example:
    [1,2,3,4,5]
    2
    4
    """
    import sys
    import json

    # Parse input
    lines = sys.stdin.read().strip().split('\n')
    values = json.loads(lines[0])
    head = list_to_linkedlist(values)
    left = int(lines[1])
    right = int(lines[2])

    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.reverseBetween(head, left, right)

    # Output result as JSON array
    print(json.dumps(linkedlist_to_list(result), separators=(',', ':')))


if __name__ == "__main__":
    solve()
