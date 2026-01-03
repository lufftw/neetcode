"""Tier-1: DoublyListNode structure conversion functions."""

from typing import List, Optional
from ...classes.doubly_list_node import DoublyListNode


def list_to_doubly_linked(lst: List[int]) -> Optional[DoublyListNode]:
    """
    Convert Python list to Doubly Linked List.
    
    Args:
        lst: List of values
        
    Returns:
        Head of the doubly linked list
    """
    if not lst:
        return None
    
    head = DoublyListNode(lst[0])
    current = head
    
    for val in lst[1:]:
        new_node = DoublyListNode(val)
        current.next = new_node
        new_node.prev = current
        current = new_node
    
    return head


def doubly_linked_to_list(head: Optional[DoublyListNode]) -> List[int]:
    """
    Convert Doubly Linked List to Python list.
    
    Args:
        head: Head of the doubly linked list
        
    Returns:
        List of values
    """
    result = []
    current = head
    while current:
        result.append(current.val)
        current = current.next
    return result

