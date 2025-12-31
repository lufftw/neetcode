"""
Helper class catalog.

Canonical definitions of helper classes used in LeetCode problems.
These are the authoritative implementations for code generation.
"""

from typing import Dict, Optional


# ============================================
# Canonical Helper Class Definitions
# ============================================

HELPER_CATALOG: Dict[str, str] = {
    "ListNode": '''class ListNode:
    """Singly linked list node."""
    def __init__(self, val: int = 0, next: 'ListNode' = None):
        self.val = val
        self.next = next''',

    "TreeNode": '''class TreeNode:
    """Binary tree node."""
    def __init__(self, val: int = 0, left: 'TreeNode' = None, right: 'TreeNode' = None):
        self.val = val
        self.left = left
        self.right = right''',

    "Node": '''class Node:
    """Linked list node with random pointer (e.g., Copy List with Random Pointer)."""
    def __init__(self, val: int = 0, next: 'Node' = None, random: 'Node' = None):
        self.val = val
        self.next = next
        self.random = random''',

    "NodeGraph": '''class Node:
    """Graph node with neighbors list (e.g., Clone Graph)."""
    def __init__(self, val: int = 0, neighbors: list = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []''',

    "NodeNary": '''class Node:
    """N-ary tree node (e.g., N-ary Tree Traversal)."""
    def __init__(self, val: int = None, children: list = None):
        self.val = val
        self.children = children if children is not None else []''',

    "NestedInteger": '''class NestedInteger:
    """
    Interface for Nested List problems.
    
    This is a simplified version - actual implementation depends on problem.
    """
    def __init__(self, value=None):
        self._integer = None
        self._list = []
        if value is not None:
            if isinstance(value, int):
                self._integer = value
            elif isinstance(value, list):
                self._list = value
    
    def isInteger(self) -> bool:
        """Return True if this NestedInteger holds a single integer."""
        return self._integer is not None
    
    def getInteger(self) -> int:
        """Return the single integer this NestedInteger holds (if it holds one)."""
        return self._integer
    
    def getList(self) -> list:
        """Return the nested list this NestedInteger holds (if it holds a list)."""
        return self._list
    
    def setInteger(self, value: int) -> None:
        """Set this NestedInteger to hold a single integer."""
        self._integer = value
        self._list = []
    
    def add(self, elem: 'NestedInteger') -> None:
        """Add a NestedInteger to this list."""
        self._integer = None
        self._list.append(elem)''',

    "DoublyListNode": '''class DoublyListNode:
    """Doubly linked list node."""
    def __init__(self, val: int = 0, prev: 'DoublyListNode' = None, next: 'DoublyListNode' = None):
        self.val = val
        self.prev = prev
        self.next = next''',
}


# ============================================
# Helper Function Templates
# ============================================

HELPER_FUNCTIONS: Dict[str, str] = {
    "list_to_linkedlist": '''def list_to_linkedlist(lst: list) -> 'ListNode':
    """Convert Python list to LinkedList."""
    if not lst:
        return None
    dummy = ListNode(0)
    current = dummy
    for val in lst:
        current.next = ListNode(val)
        current = current.next
    return dummy.next''',

    "linkedlist_to_list": '''def linkedlist_to_list(node: 'ListNode') -> list:
    """Convert LinkedList to Python list."""
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result''',

    "list_to_tree": '''def list_to_tree(lst: list) -> 'TreeNode':
    """Convert level-order list to Binary Tree (None for missing nodes)."""
    if not lst:
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
    
    return root''',

    "tree_to_list": '''def tree_to_list(root: 'TreeNode') -> list:
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
    
    return result''',
}


# ============================================
# API Functions
# ============================================

def get_helper_code(name: str) -> Optional[str]:
    """
    Get canonical helper class code by name.
    
    Args:
        name: Helper class name (e.g., "ListNode", "TreeNode")
        
    Returns:
        str: Helper class code, or None if not found
    """
    return HELPER_CATALOG.get(name)


def get_helper_function(name: str) -> Optional[str]:
    """
    Get helper function code by name.
    
    Args:
        name: Function name (e.g., "list_to_linkedlist")
        
    Returns:
        str: Function code, or None if not found
    """
    return HELPER_FUNCTIONS.get(name)


def get_helpers_for_class(class_name: str) -> list:
    """
    Get related helper functions for a helper class.
    
    Args:
        class_name: Helper class name
        
    Returns:
        List of function names
    """
    mapping = {
        "ListNode": ["list_to_linkedlist", "linkedlist_to_list"],
        "TreeNode": ["list_to_tree", "tree_to_list"],
    }
    return mapping.get(class_name, [])


def list_all_helpers() -> list:
    """List all available helper class names."""
    return list(HELPER_CATALOG.keys())


def list_all_helper_functions() -> list:
    """List all available helper function names."""
    return list(HELPER_FUNCTIONS.keys())

