# solutions/0025_reverse_nodes_in_k_group.py
"""
Problem: Reverse Nodes in k-Group
Link: https://leetcode.com/problems/reverse-nodes-in-k-group/

Given the head of a linked list, reverse the nodes of the list k at a time,
and return the modified list.

k is a positive integer and is less than or equal to the length of the linked list.
If the number of nodes is not a multiple of k then left-out nodes, in the end,
should remain as it is.
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
        "method": "reverseKGroup",
        "complexity": "O(N) time, O(1) space",
        "description": "Iterative in-place k-group reversal using pointer manipulation",
    },
    "iterative": {
        "class": "SolutionIterative",
        "method": "reverseKGroup",
        "complexity": "O(N) time, O(1) space",
        "description": "Iterative in-place k-group reversal using pointer manipulation",
    },
    "recursive": {
        "class": "SolutionRecursive",
        "method": "reverseKGroup",
        "complexity": "O(N) time, O(N) space",
        "description": "Recursive k-group reversal using a helper to reverse exactly k nodes",
    },
}


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result by computing the expected k-group reversal.
    
    Args:
        actual: Program output (may be list or string)
        expected: Expected output (None if from generator)
        input_data: Raw input string
    
    Returns:
        bool: True if correct
    """
    import ast
    
    # Parse input
    lines = input_data.strip().split('\n')
    values = list(map(int, lines[0].split(',')))
    k = int(lines[1])
    
    # Compute expected result using simple simulation
    correct = _compute_k_group_reversal(values, k)
    
    # Parse actual output
    try:
        if isinstance(actual, list):
            actual_list = actual
        else:
            actual_list = ast.literal_eval(str(actual).strip())
        return actual_list == correct
    except (ValueError, SyntaxError):
        return False


def _compute_k_group_reversal(values: List[int], k: int) -> List[int]:
    """Compute expected k-group reversal result."""
    n = len(values)
    result = values.copy()
    
    # Process each complete group of k elements
    i = 0
    while i + k <= n:
        # Reverse the group [i, i+k)
        result[i:i+k] = result[i:i+k][::-1]
        i += k
    
    return result


JUDGE_FUNC = judge


# ============================================
# Solution 1: Recursive k-group reversal
# Time: O(N), Space: O(N) recursion stack in worst case
#   - We scan at most k nodes per group to check availability
#   - Each node is reversed exactly once
# Space details:
#   - O(k) recursion depth in reverseK
#   - O(N / k) recursion depth in reverseKGroup
#   => Overall stack usage is O(N) in the worst case
# ============================================
class SolutionRecursive:
    def __init__(self) -> None:
        # Will point to the (k+1)-th node after reversing k nodes
        self.successor: Optional[ListNode] = None

    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        # Check if there are at least k nodes remaining
        curr = head
        count = 0

        while curr and count < k:
            curr = curr.next
            count += 1

        # If fewer than k nodes remain, return head as-is
        if count < k:
            return head

        # Reverse the first k nodes
        new_head = self._reverse_k(head, k)

        # After _reverse_k, 'head' becomes the tail of the reversed segment
        # self.successor points to the (k+1)-th node
        head.next = self.reverseKGroup(self.successor, k)

        return new_head

    def _reverse_k(self, head: ListNode, k: int) -> ListNode:
        """
        Recursively reverse k nodes starting from head.
        Sets self.successor to the node after the k-th node.
        Returns the new head (originally the k-th node).
        """
        # Base case: when k == 1, we've reached the k-th node
        if k == 1:
            self.successor = head.next
            return head

        # Recursively reverse the remaining k-1 nodes
        new_head = self._reverse_k(head.next, k - 1)

        # Reverse the pointer: make the next node point back to current
        head.next.next = head
        head.next = None  # Temporarily disconnect; will be reconnected in reverseKGroup

        return new_head


# ============================================
# Solution 2: Iterative k-group reversal
# Time: O(N), Space: O(1)
#   - We scan each node a constant number of times
#   - Reversal is done in-place with pointer manipulation
# ============================================
class SolutionIterative:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if k == 1 or not head:
            # No need to reverse when k == 1 or list is empty
            return head

        # Dummy node simplifies handling of head changes
        dummy = ListNode(0, head)
        group_prev = dummy

        while True:
            # 1) Find the k-th node from group_prev
            kth = self._get_kth_node(group_prev, k)
            if not kth:
                # Fewer than k nodes remain; do not reverse
                break

            group_next = kth.next  # Node after the k-th node

            # 2) Reverse the group [group_prev.next ... kth]
            prev = group_next
            curr = group_prev.next

            # Reverse exactly k nodes
            while curr != group_next:
                tmp = curr.next
                curr.next = prev
                prev = curr
                curr = tmp

            # 3) Connect the reversed group back to the list
            # group_prev.next was the old head of the group, now becomes the tail
            old_group_head = group_prev.next
            group_prev.next = kth
            group_prev = old_group_head  # Move group_prev to the tail of this group

        return dummy.next

    def _get_kth_node(self, start: ListNode, k: int) -> Optional[ListNode]:
        """
        Return the k-th node starting from `start.next`.
        If fewer than k nodes remain, return None.
        """
        curr = start
        while curr and k > 0:
            curr = curr.next
            k -= 1
        return curr


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
    Line 1: values of the linked list (comma-separated)
    Line 2: k (group size)

    Example:
    1,2,3,4,5
    2
    """
    import sys

    # Parse input
    lines = sys.stdin.read().strip().split('\n')
    values = list(map(int, lines[0].split(',')))
    head = list_to_linkedlist(values)
    k = int(lines[1])

    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.reverseKGroup(head, k)

    # Output result as list
    print(linkedlist_to_list(result))


if __name__ == "__main__":
    solve()
