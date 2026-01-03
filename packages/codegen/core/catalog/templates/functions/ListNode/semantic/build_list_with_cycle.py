def build_list_with_cycle(values: list, pos: int) -> tuple:
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
