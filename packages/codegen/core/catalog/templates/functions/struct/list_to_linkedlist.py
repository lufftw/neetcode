"""Convert Python list to LinkedList."""

from typing import List, Optional

# Import for runtime use (when this file is imported)
try:
    from ...classes.ListNode import ListNode
except ImportError:
    # Fallback for template extraction
    pass


def list_to_linkedlist(lst: List[int]) -> Optional['ListNode']:
    """Convert Python list to LinkedList."""
    if not lst:
        return None
    dummy = ListNode(0)
    current = dummy
    for val in lst:
        current.next = ListNode(val)
        current = current.next
    return dummy.next

