"""Find index of a node in the nodes array."""

from typing import List, Optional


def node_to_index(node: Optional['ListNode'], nodes: List['ListNode']) -> int:
    """
    Find index of a node in the nodes array.
    
    Args:
        node: Target node
        nodes: Array of all nodes
        
    Returns:
        0-based index, or -1 if not found
        
    Canonical semantics:
        - Returns 0-based index
        - Returns -1 for None or not found
    """
    if node is None:
        return -1
    for i, n in enumerate(nodes):
        if n is node:
            return i
    return -1

