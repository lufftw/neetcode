"""
Codec utilities for LeetCode data structure I/O.

This module provides functions for converting between simple formats (.in/.out)
and LeetCode data structures (ListNode, TreeNode, etc.).

Usage:
    from runner.utils.codec import list_to_linkedlist, linkedlist_to_list

For inline mode (copy-paste to LeetCode), use templates from:
    packages/codegen/core/helpers/catalog.py

Reference: docs/contracts/problem-support-boundary.md
"""

from typing import List, Optional, Tuple, Any


# =============================================================================
# Data Structure Definitions
# =============================================================================

class ListNode:
    """Singly linked list node."""
    def __init__(self, val: int = 0, next: 'ListNode' = None):
        self.val = val
        self.next = next
    
    def __repr__(self) -> str:
        return f"ListNode({self.val})"


class TreeNode:
    """Binary tree node."""
    def __init__(self, val: int = 0, left: 'TreeNode' = None, right: 'TreeNode' = None):
        self.val = val
        self.left = left
        self.right = right
    
    def __repr__(self) -> str:
        return f"TreeNode({self.val})"


class Node:
    """Linked list node with random pointer (for Copy List with Random Pointer)."""
    def __init__(self, val: int = 0, next: 'Node' = None, random: 'Node' = None):
        self.val = val
        self.next = next
        self.random = random
    
    def __repr__(self) -> str:
        return f"Node({self.val})"


# =============================================================================
# Tier-1: Value-Based Codec (ListNode)
# =============================================================================

def list_to_linkedlist(lst: List[int]) -> Optional[ListNode]:
    """
    Convert Python list to LinkedList.
    
    Args:
        lst: List of integer values
        
    Returns:
        Head of the linked list, or None if empty
        
    Example:
        >>> list_to_linkedlist([1, 2, 3])
        ListNode(1) -> ListNode(2) -> ListNode(3)
    """
    if not lst:
        return None
    dummy = ListNode(0)
    current = dummy
    for val in lst:
        current.next = ListNode(val)
        current = current.next
    return dummy.next


def linkedlist_to_list(node: Optional[ListNode]) -> List[int]:
    """
    Convert LinkedList to Python list.
    
    Args:
        node: Head of the linked list
        
    Returns:
        List of integer values
        
    Example:
        >>> linkedlist_to_list(head)
        [1, 2, 3]
    """
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result


# =============================================================================
# Tier-1: Value-Based Codec (TreeNode)
# =============================================================================

def list_to_tree(lst: List[Optional[int]]) -> Optional[TreeNode]:
    """
    Convert level-order list to Binary Tree.
    
    Args:
        lst: Level-order list with None for missing nodes
        
    Returns:
        Root of the tree, or None if empty
        
    Example:
        >>> list_to_tree([1, 2, 3, None, 4])
        #       1
        #      / \\
        #     2   3
        #      \\
        #       4
    """
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


def tree_to_list(root: Optional[TreeNode]) -> List[Optional[int]]:
    """
    Convert Binary Tree to level-order list.
    
    Args:
        root: Root of the tree
        
    Returns:
        Level-order list with None for missing nodes (trailing Nones removed)
        
    Example:
        >>> tree_to_list(root)
        [1, 2, 3, None, 4]
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
    
    # Remove trailing Nones
    while result and result[-1] is None:
        result.pop()
    
    return result


# =============================================================================
# Tier-1.5: Semantic Codec (Cycle)
# =============================================================================

def build_list_with_cycle(values: List[int], pos: int) -> Tuple[Optional[ListNode], List[ListNode]]:
    """
    Build linked list with optional cycle.
    
    Args:
        values: Node values
        pos: Cycle position (0-based), -1 if no cycle
        
    Returns:
        Tuple of (head, nodes_array)
        - head: Head of the linked list
        - nodes_array: Array of all nodes (for index lookup)
        
    Example:
        >>> head, nodes = build_list_with_cycle([3, 2, 0, -4], 1)
        # Creates: 3 -> 2 -> 0 -> -4 -> (back to 2)
        
    Canonical semantics:
        - pos is 0-based
        - pos = -1 means no cycle
    """
    if not values:
        return None, []
    
    nodes = [ListNode(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    
    # Create cycle if pos >= 0
    if 0 <= pos < len(nodes):
        nodes[-1].next = nodes[pos]
    
    return nodes[0], nodes


def node_to_index(node: Optional[ListNode], nodes: List[ListNode]) -> int:
    """
    Find index of a node in the nodes array.
    
    Args:
        node: Target node
        nodes: Array of all nodes
        
    Returns:
        0-based index, or -1 if not found
        
    Canonical semantics:
        - Returns 0-based index
        - Returns -1 for None or not found
    """
    if node is None:
        return -1
    for i, n in enumerate(nodes):
        if n is node:
            return i
    return -1


# =============================================================================
# Tier-1.5: Semantic Codec (Intersection)
# =============================================================================

def build_intersecting_lists(
    listA: List[int],
    listB: List[int],
    skipA: int,
    skipB: int
) -> Tuple[Optional[ListNode], Optional[ListNode], Optional[ListNode]]:
    """
    Build two linked lists that intersect at a shared node.
    
    Args:
        listA: Values for list A (including intersection)
        listB: Values for list B (prefix only, before intersection)
        skipA: Number of nodes in A before intersection
        skipB: Number of nodes in B before intersection
        
    Returns:
        Tuple of (headA, headB, intersectionNode)
        
    Example:
        >>> headA, headB, inter = build_intersecting_lists(
        ...     [4, 1, 8, 4, 5],  # A: 4 -> 1 -> [8 -> 4 -> 5]
        ...     [5, 6, 1],        # B prefix: 5 -> 6 -> 1
        ...     2,                # skipA: intersection starts at index 2
        ...     3                 # skipB: B has 3 nodes before intersection
        ... )
        # Result: A: 4 -> 1 -> 8 -> 4 -> 5
        #         B: 5 -> 6 -> 1 -> 8 -> 4 -> 5 (shares 8,4,5 with A)
        
    Canonical semantics:
        - skipA/skipB are 0-based counts
        - If no intersection, returns (headA, headB, None)
    """
    if not listA:
        return None, None, None
    
    # Build list A
    nodesA = [ListNode(v) for v in listA]
    for i in range(len(nodesA) - 1):
        nodesA[i].next = nodesA[i + 1]
    
    # Build list B prefix (nodes before intersection)
    if skipB > 0 and listB:
        nodesB = [ListNode(v) for v in listB[:skipB]]
        for i in range(len(nodesB) - 1):
            nodesB[i].next = nodesB[i + 1]
        headB = nodesB[0]
        
        # Connect B to intersection point in A
        if skipA < len(nodesA):
            nodesB[-1].next = nodesA[skipA]
            intersection = nodesA[skipA]
        else:
            intersection = None
    else:
        # No B prefix, B starts at intersection
        if skipA < len(nodesA):
            headB = nodesA[skipA]
            intersection = nodesA[skipA]
        else:
            headB = None
            intersection = None
    
    return nodesA[0], headB, intersection


# =============================================================================
# Tier-1.5: Semantic Codec (Random Pointer)
# =============================================================================

def build_random_pointer_list(pairs: List[List[Any]]) -> Optional[Node]:
    """
    Build linked list with random pointers.
    
    Args:
        pairs: List of [val, random_index] pairs
               random_index is 0-based, or None for no random pointer
               
    Returns:
        Head of the list
        
    Example:
        >>> head = build_random_pointer_list([[7, None], [13, 0], [11, 4]])
        # Node(7).random = None
        # Node(13).random = Node(7)  (index 0)
        # Node(11).random = Node at index 4
        
    Canonical semantics:
        - random_index is 0-based
        - None means no random pointer
    """
    if not pairs:
        return None
    
    # Create all nodes first
    nodes = [Node(val=p[0]) for p in pairs]
    
    # Link next pointers
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    
    # Link random pointers
    for i, p in enumerate(pairs):
        random_idx = p[1]
        if random_idx is not None and 0 <= random_idx < len(nodes):
            nodes[i].random = nodes[random_idx]
    
    return nodes[0]


def encode_random_pointer_list(head: Optional[Node]) -> List[List[Any]]:
    """
    Encode linked list with random pointers to pairs format.
    
    Args:
        head: Head of the list
        
    Returns:
        List of [val, random_index] pairs
        
    Example:
        >>> encode_random_pointer_list(head)
        [[7, None], [13, 0], [11, 4]]
        
    Canonical semantics:
        - random_index is 0-based
        - None for no random pointer
    """
    if not head:
        return []
    
    # First pass: collect all nodes and create index map
    nodes = []
    node_to_idx = {}
    current = head
    idx = 0
    while current:
        nodes.append(current)
        node_to_idx[id(current)] = idx
        current = current.next
        idx += 1
    
    # Second pass: encode
    result = []
    for node in nodes:
        random_idx = node_to_idx.get(id(node.random)) if node.random else None
        result.append([node.val, random_idx])
    
    return result


# =============================================================================
# Utility Functions
# =============================================================================

def verify_deep_copy(original: Optional[Node], copy: Optional[Node]) -> bool:
    """
    Verify that a list is a proper deep copy (no shared nodes).
    
    Args:
        original: Head of original list
        copy: Head of copied list
        
    Returns:
        True if copy is valid deep copy, False otherwise
        
    Note:
        This checks both structure equality AND that no nodes are shared.
    """
    orig_nodes = set()
    current = original
    while current:
        orig_nodes.add(id(current))
        current = current.next
    
    # Check copy has no shared nodes
    current = copy
    while current:
        if id(current) in orig_nodes:
            return False
        current = current.next
    
    # Check structure matches
    orig_encoded = encode_random_pointer_list(original)
    copy_encoded = encode_random_pointer_list(copy)
    
    return orig_encoded == copy_encoded

