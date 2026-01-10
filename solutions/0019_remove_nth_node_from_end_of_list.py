"""
Problem: Remove Nth Node From End of List
Link: https://leetcode.com/problems/remove-nth-node-from-end-of-list/

Given the head of a linked list, remove the n-th node from the end of the list
and return its head.

Example 1:
    Input: head = [1,2,3,4,5], n = 2
    Output: [1,2,3,5]

Example 2:
    Input: head = [1], n = 1
    Output: []

Example 3:
    Input: head = [1,2], n = 1
    Output: [1]

Constraints:
- The number of nodes in the list is sz.
- 1 <= sz <= 30
- 0 <= Node.val <= 100
- 1 <= n <= sz

Follow-up: Could you do this in one pass?

Topics: Linked List, Two Pointers
"""
import json
from typing import Optional
from _runner import get_solver
from runner.utils.codec import ListNode, linkedlist_to_list, list_to_linkedlist


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionTwoPointer",
        "method": "removeNthFromEnd",
        "complexity": "O(n) time, O(1) space",
        "description": "Two pointers with n-gap - single pass solution",
    },
    "two_pointer": {
        "class": "SolutionTwoPointer",
        "method": "removeNthFromEnd",
        "complexity": "O(n) time, O(1) space",
        "description": "Two pointers with n-gap - single pass solution",
    },
    "two_pass": {
        "class": "SolutionTwoPass",
        "method": "removeNthFromEnd",
        "complexity": "O(n) time, O(1) space",
        "description": "Two pass - count length first, then remove",
    },
}


# ============================================================================
# Solution 1: Two Pointers (Single Pass)
# Time: O(n), Space: O(1)
#   - Use two pointers separated by n nodes
#   - When fast reaches end, slow is at the node before target
#   - Dummy node handles edge case of removing head
# ============================================================================
class SolutionTwoPointer:
    """
    Two-pointer approach for single-pass removal.

    Key insight: If we maintain a gap of n nodes between two pointers,
    when the fast pointer reaches the end, the slow pointer will be
    exactly at the node BEFORE the one we need to remove.

    Using a dummy node simplifies edge cases (e.g., removing the head).
    """

    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # Dummy node handles edge case where we remove the head
        dummy = ListNode(0, head)

        # Initialize both pointers at dummy
        slow = dummy
        fast = dummy

        # Move fast pointer n+1 steps ahead
        # This creates a gap of n nodes between slow and fast
        # We use n+1 so that slow ends up at the node BEFORE the target
        for _ in range(n + 1):
            fast = fast.next

        # Move both pointers until fast reaches the end
        while fast is not None:
            slow = slow.next
            fast = fast.next

        # Now slow.next is the node to remove
        # Skip over it by adjusting the next pointer
        slow.next = slow.next.next

        return dummy.next


# ============================================================================
# Solution 2: Two Pass
# Time: O(n), Space: O(1)
#   - First pass: count total nodes
#   - Second pass: navigate to (length - n)th node and remove next
# ============================================================================
class SolutionTwoPass:
    """
    Two-pass approach - simpler but requires traversing the list twice.

    First pass counts the total length, then we calculate which node
    to remove from the start: position = length - n.
    """

    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # First pass: count total nodes
        length = 0
        current = head
        while current:
            length += 1
            current = current.next

        # Calculate position from start (0-indexed)
        # Node to remove is at position (length - n)
        # We need to stop at position (length - n - 1) to remove it
        remove_pos = length - n

        # Edge case: removing the head
        if remove_pos == 0:
            return head.next

        # Second pass: navigate to node before target
        current = head
        for _ in range(remove_pos - 1):
            current = current.next

        # Remove the target node
        current.next = current.next.next

        return head


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: head as JSON array
        Line 2: n (integer)

    Example:
        [1,2,3,4,5]
        2
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')

    head_list = json.loads(lines[0])
    head = list_to_linkedlist(head_list)
    n = int(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.removeNthFromEnd(head, n)

    out = linkedlist_to_list(result)
    print(json.dumps(out, separators=(',', ':')))


if __name__ == "__main__":
    solve()
