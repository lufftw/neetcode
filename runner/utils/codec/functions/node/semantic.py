"""Tier-1.5: Node (random pointer) semantic conversion functions."""

from typing import List, Optional, Any
from ...classes.node import Node


def build_random_pointer_list(pairs: List[List[Any]]) -> Optional[Node]:
    """
    Build linked list with random pointers.
    
    Args:
        pairs: List of [val, random_index] pairs
               random_index is 0-based, or None for no random pointer
               
    Returns:
        Head of the list
    """
    if not pairs:
        return None
    
    nodes = [Node(val=p[0]) for p in pairs]
    
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    
    for i, p in enumerate(pairs):
        random_idx = p[1]
        if random_idx is not None and 0 <= random_idx < len(nodes):
            nodes[i].random = nodes[random_idx]
    
    return nodes[0]


def encode_random_pointer_list(head: Optional[Node]) -> List[List[Any]]:
    """
    Encode linked list with random pointers to pairs format.
    
    Args:
        head: Head of the list
        
    Returns:
        List of [val, random_index] pairs
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


def verify_deep_copy(original: Optional[Node], copy: Optional[Node]) -> bool:
    """
    Verify that a list is a proper deep copy (no shared nodes).
    
    Args:
        original: Head of original list
        copy: Head of copied list
        
    Returns:
        True if copy is valid deep copy, False otherwise
    """
    orig_nodes = set()
    current = original
    while current:
        orig_nodes.add(id(current))
        current = current.next
    
    current = copy
    while current:
        if id(current) in orig_nodes:
            return False
        current = current.next
    
    orig_encoded = encode_random_pointer_list(original)
    copy_encoded = encode_random_pointer_list(copy)
    
    return orig_encoded == copy_encoded

