"""Tier-1: TreeNode structure conversion functions."""

from typing import List, Optional
from ...classes.tree_node import TreeNode


def list_to_tree(lst: List[Optional[int]]) -> Optional[TreeNode]:
    """
    Convert level-order list to Binary Tree.
    
    Args:
        lst: Level-order list with None for missing nodes
        
    Returns:
        Root of the tree, or None if empty
    """
    if not lst or lst[0] is None:
        return None
    
    root = TreeNode(lst[0])
    queue = [root]
    i = 1
    
    while queue and i < len(lst):
        node = queue.pop(0)
        
        if i < len(lst) and lst[i] is not None:
            node.left = TreeNode(lst[i])
            queue.append(node.left)
        i += 1
        
        if i < len(lst) and lst[i] is not None:
            node.right = TreeNode(lst[i])
            queue.append(node.right)
        i += 1
    
    return root


def tree_to_list(root: Optional[TreeNode]) -> List[Optional[int]]:
    """
    Convert Binary Tree to level-order list.
    
    Args:
        root: Root of the tree
        
    Returns:
        Level-order list with None for missing nodes (trailing Nones removed)
    """
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
    
    while result and result[-1] is None:
        result.pop()
    
    return result

