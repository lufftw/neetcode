def build_random_pointer_list(pairs: list) -> 'Node':
    """
    Build linked list with random pointers.
    
    Args:
        pairs: List of [val, random_index] pairs
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
