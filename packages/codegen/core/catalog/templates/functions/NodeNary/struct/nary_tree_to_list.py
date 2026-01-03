def nary_tree_to_list(root: 'Node') -> list:
    """
    Convert N-ary Tree to level-order list.
    
    Returns list with null separators between siblings groups.
    """
    if not root:
        return []
    
    result = [root.val, None]
    queue = [root]
    
    while queue:
        node = queue.pop(0)
        for child in node.children:
            result.append(child.val)
            queue.append(child)
        result.append(None)
    
    # Remove trailing nulls
    while result and result[-1] is None:
        result.pop()
    
    return result

