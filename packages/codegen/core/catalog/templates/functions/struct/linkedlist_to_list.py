"""Convert LinkedList to Python list."""

from typing import List, Optional


def linkedlist_to_list(node: Optional['ListNode']) -> List[int]:
    """Convert LinkedList to Python list."""
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result

