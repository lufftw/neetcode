"""Convert Binary Tree to level-order list."""

from typing import List, Optional


def tree_to_list(root: Optional['TreeNode']) -> List[Optional[int]]:
    """Convert Binary Tree to level-order list (None for missing nodes)."""
    if not root:
        return []
    
    result = []
    queue = [root]
    
    while queue:
        node = queue.pop(0)
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)
    
    # Remove trailing Nones
    while result and result[-1] is None:
        result.pop()
    
    return result

