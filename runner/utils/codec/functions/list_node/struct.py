"""Tier-1: ListNode structure conversion functions."""

from typing import List, Optional
from ...classes.list_node import ListNode


def list_to_linkedlist(lst: List[int]) -> Optional[ListNode]:
    """
    Convert Python list to LinkedList.
    
    Args:
        lst: List of integer values
        
    Returns:
        Head of the linked list, or None if empty
    """
    if not lst:
        return None
    dummy = ListNode(0)
    current = dummy
    for val in lst:
        current.next = ListNode(val)
        current = current.next
    return dummy.next


def linkedlist_to_list(node: Optional[ListNode]) -> List[int]:
    """
    Convert LinkedList to Python list.
    
    Args:
        node: Head of the linked list
        
    Returns:
        List of integer values
    """
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result

