def list_to_nary_tree(lst: list) -> 'Node':
    """
    Convert level-order list to N-ary Tree.
    
    Format: [val, null, child1, child2, ..., null, ...]
    null separates children of different nodes.
    
    Example:
        [1, null, 3, 2, 4, null, 5, 6]
        represents:
              1
            / | \\
           3  2  4
          / \\
         5   6
    """
    if not lst or lst[0] is None:
        return None
    
    root = Node(lst[0])
    queue = [root]
    i = 2  # Skip first value and first null
    
    while queue and i < len(lst):
        parent = queue.pop(0)
        children = []
        
        while i < len(lst) and lst[i] is not None:
            child = Node(lst[i])
            children.append(child)
            queue.append(child)
            i += 1
        
        parent.children = children
        i += 1  # Skip null separator
    
    return root

