def node_to_index(node, nodes: list) -> int:
    """
    Find index of a node in the nodes array.
        
    Returns:
        0-based index, or -1 if not found
    """
    if node is None:
        return -1
    for i, n in enumerate(nodes):
        if n is node:
            return i
    return -1
