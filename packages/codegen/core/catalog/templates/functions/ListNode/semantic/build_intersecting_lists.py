def build_intersecting_lists(listA: list, listB: list, skipA: int, skipB: int) -> tuple:
    """
    Build two linked lists that intersect at a shared node.
    
    Args:
        listA: Values for list A (including intersection)
        listB: Values for list B (prefix before intersection)
        skipA: Nodes in A before intersection
        skipB: Nodes in B before intersection
        
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
