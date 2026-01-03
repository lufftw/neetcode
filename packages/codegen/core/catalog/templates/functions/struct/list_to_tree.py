"""Convert level-order list to Binary Tree."""

from typing import List, Optional

# Import for runtime use
try:
    from ...classes.TreeNode import TreeNode
except ImportError:
    pass


def list_to_tree(lst: List[Optional[int]]) -> Optional['TreeNode']:
    """Convert level-order list to Binary Tree (None for missing nodes)."""
    if not lst or lst[0] is None:
        return None
    
    root = TreeNode(lst[0])
    queue = [root]
    i = 1
    
    while queue and i < len(lst):
        node = queue.pop(0)
        
        # Left child
        if i < len(lst) and lst[i] is not None:
            node.left = TreeNode(lst[i])
            queue.append(node.left)
        i += 1
        
        # Right child
        if i < len(lst) and lst[i] is not None:
            node.right = TreeNode(lst[i])
            queue.append(node.right)
        i += 1
    
    return root

