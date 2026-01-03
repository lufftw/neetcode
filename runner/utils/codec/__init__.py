"""
Codec utilities for LeetCode data structure I/O.

This module provides functions for converting between simple formats (.in/.out)
and LeetCode data structures (ListNode, TreeNode, etc.).

Usage:
    from runner.utils.codec import list_to_tree, TreeNode
    
    root = list_to_tree([1, 2, 3])

Structure:
    codec/
    ├── classes/           - Data structure definitions
    │   ├── list_node.py   - ListNode
    │   ├── tree_node.py   - TreeNode
    │   └── node.py        - Node (random pointer)
    └── functions/         - Conversion functions
        ├── list_node/     - ListNode functions (depends on ListNode)
        │   ├── struct.py  - Tier-1: list_to_linkedlist, etc.
        │   └── semantic.py- Tier-1.5: build_list_with_cycle, etc.
        ├── tree_node/     - TreeNode functions
        └── node/          - Node functions

Reference: docs/contracts/problem-support-boundary.md
"""

# Classes
from .classes import ListNode, TreeNode, Node

# Functions
from .functions import (
    # ListNode - Tier 1
    list_to_linkedlist,
    linkedlist_to_list,
    # ListNode - Tier 1.5
    build_list_with_cycle,
    node_to_index,
    build_intersecting_lists,
    # TreeNode - Tier 1
    list_to_tree,
    tree_to_list,
    # Node - Tier 1.5
    build_random_pointer_list,
    encode_random_pointer_list,
    verify_deep_copy,
)

__all__ = [
    # Classes
    "ListNode",
    "TreeNode",
    "Node",
    # ListNode functions
    "list_to_linkedlist",
    "linkedlist_to_list",
    "build_list_with_cycle",
    "node_to_index",
    "build_intersecting_lists",
    # TreeNode functions
    "list_to_tree",
    "tree_to_list",
    # Node functions
    "build_random_pointer_list",
    "encode_random_pointer_list",
    "verify_deep_copy",
]

