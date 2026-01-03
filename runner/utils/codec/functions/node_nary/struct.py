"""Tier-1: NodeNary structure conversion functions."""

from typing import List, Optional, Any
from ...classes.node_nary import NodeNary


def list_to_nary_tree(lst: List[Any]) -> Optional[NodeNary]:
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
    
    root = NodeNary(lst[0])
    queue = [root]
    i = 2  # Skip first value and first null
    
    while queue and i < len(lst):
        parent = queue.pop(0)
        children = []
        
        while i < len(lst) and lst[i] is not None:
            child = NodeNary(lst[i])
            children.append(child)
            queue.append(child)
            i += 1
        
        parent.children = children
        i += 1  # Skip null separator
    
    return root


def nary_tree_to_list(root: Optional[NodeNary]) -> List[Any]:
    """
    Convert N-ary Tree to level-order list.
    
    Returns list with null separators between siblings groups.
    """
    if not root:
        return []
    
    result: List[Any] = [root.val, None]
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

