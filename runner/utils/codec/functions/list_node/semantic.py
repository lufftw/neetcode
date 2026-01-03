"""Tier-1.5: ListNode semantic conversion functions."""

from typing import List, Optional, Tuple
from ...classes.list_node import ListNode


def build_list_with_cycle(values: List[int], pos: int) -> Tuple[Optional[ListNode], List[ListNode]]:
    """
    Build linked list with optional cycle.
    
    Args:
        values: Node values
        pos: Cycle position (0-based), -1 if no cycle
        
    Returns:
        Tuple of (head, nodes_array)
    """
    if not values:
        return None, []
    
    nodes = [ListNode(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    
    if 0 <= pos < len(nodes):
        nodes[-1].next = nodes[pos]
    
    return nodes[0], nodes


def node_to_index(node: Optional[ListNode], nodes: List[ListNode]) -> int:
    """
    Find index of a node in the nodes array.
    
    Args:
        node: Target node
        nodes: Array of all nodes
        
    Returns:
        0-based index, or -1 if not found
    """
    if node is None:
        return -1
    for i, n in enumerate(nodes):
        if n is node:
            return i
    return -1


def build_intersecting_lists(
    listA: List[int],
    listB: List[int],
    skipA: int,
    skipB: int
) -> Tuple[Optional[ListNode], Optional[ListNode], Optional[ListNode]]:
    """
    Build two linked lists that intersect at a shared node.
    
    Args:
        listA: Values for list A (including intersection)
        listB: Values for list B (prefix only, before intersection)
        skipA: Number of nodes in A before intersection
        skipB: Number of nodes in B before intersection
        
    Returns:
        Tuple of (headA, headB, intersectionNode)
    """
    if not listA:
        return None, None, None
    
    nodesA = [ListNode(v) for v in listA]
    for i in range(len(nodesA) - 1):
        nodesA[i].next = nodesA[i + 1]
    
    if skipB > 0 and listB:
        nodesB = [ListNode(v) for v in listB[:skipB]]
        for i in range(len(nodesB) - 1):
            nodesB[i].next = nodesB[i + 1]
        headB = nodesB[0]
        
        if skipA < len(nodesA):
            nodesB[-1].next = nodesA[skipA]
            intersection = nodesA[skipA]
        else:
            intersection = None
    else:
        if skipA < len(nodesA):
            headB = nodesA[skipA]
            intersection = nodesA[skipA]
        else:
            headB = None
            intersection = None
    
    return nodesA[0], headB, intersection

