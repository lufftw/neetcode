"""Build linked list with optional cycle."""

from typing import List, Tuple, Optional

# Import for runtime use
try:
    from ...classes.ListNode import ListNode
except ImportError:
    pass


def build_list_with_cycle(values: List[int], pos: int) -> Tuple[Optional['ListNode'], List['ListNode']]:
    """
    Build linked list with optional cycle.
    
    Args:
        values: Node values
        pos: Cycle position (0-based), -1 if no cycle
        
    Returns:
        Tuple of (head, nodes_array)
        
    Canonical semantics:
        - pos is 0-based
        - pos = -1 means no cycle
    """
    if not values:
        return None, []
    nodes = [ListNode(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if 0 <= pos < len(nodes):
        nodes[-1].next = nodes[pos]
    return nodes[0], nodes

