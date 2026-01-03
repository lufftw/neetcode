"""Build two linked lists that intersect at a shared node."""

from typing import List, Tuple, Optional

# Import for runtime use
try:
    from ...classes.ListNode import ListNode
except ImportError:
    pass


def build_intersecting_lists(
    listA: List[int],
    listB: List[int],
    skipA: int,
    skipB: int
) -> Tuple[Optional['ListNode'], Optional['ListNode'], Optional['ListNode']]:
    """
    Build two linked lists that intersect at a shared node.
    
    Args:
        listA: Values for list A (including intersection)
        listB: Values for list B (prefix only, before intersection)
        skipA: Number of nodes in A before intersection
        skipB: Number of nodes in B before intersection
        
    Returns:
        Tuple of (headA, headB, intersectionNode)
        
    Canonical semantics:
        - skipA/skipB are 0-based counts
        - If no intersection, returns (headA, headB, None)
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

