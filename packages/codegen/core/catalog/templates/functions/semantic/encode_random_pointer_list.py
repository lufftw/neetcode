"""Encode linked list with random pointers to pairs format."""

from typing import List, Any, Optional


def encode_random_pointer_list(head: Optional['Node']) -> List[List[Any]]:
    """
    Encode linked list with random pointers to pairs format.
    
    Args:
        head: Head of the list
        
    Returns:
        List of [val, random_index] pairs
        
    Canonical semantics:
        - random_index is 0-based
        - None for no random pointer
    """
    if not head:
        return []
    nodes = []
    node_to_idx = {}
    current = head
    idx = 0
    while current:
        nodes.append(current)
        node_to_idx[id(current)] = idx
        current = current.next
        idx += 1
    result = []
    for node in nodes:
        random_idx = node_to_idx.get(id(node.random)) if node.random else None
        result.append([node.val, random_idx])
    return result

