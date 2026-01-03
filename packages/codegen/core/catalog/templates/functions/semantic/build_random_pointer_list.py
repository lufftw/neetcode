"""Build linked list with random pointers."""

from typing import List, Any, Optional

# Import for runtime use
try:
    from ...classes.Node import Node
except ImportError:
    pass


def build_random_pointer_list(pairs: List[List[Any]]) -> Optional['Node']:
    """
    Build linked list with random pointers.
    
    Args:
        pairs: List of [val, random_index] pairs
               random_index is 0-based, or None for no random pointer
               
    Returns:
        Head of the list
        
    Canonical semantics:
        - random_index is 0-based
        - None means no random pointer
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

