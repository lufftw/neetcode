"""
Codec utilities for LeetCode data structure I/O.

This module provides functions for converting between simple formats (.in/.out)
and LeetCode data structures (ListNode, TreeNode, etc.).

Usage:
    from runner.utils.codec import list_to_tree, TreeNode
    
    root = list_to_tree([1, 2, 3])

Structure:
    codec/
    ├── classes/               - Data structure definitions
    │   ├── list_node.py       - ListNode (singly linked list)
    │   ├── tree_node.py       - TreeNode (binary tree)
    │   ├── node.py            - Node (random pointer list)
    │   ├── node_graph.py      - NodeGraph (graph clone)
    │   ├── node_nary.py       - NodeNary (N-ary tree)
    │   └── doubly_list_node.py- DoublyListNode
    └── functions/             - Conversion functions
        ├── list_node/         - Depends on ListNode
        │   ├── struct.py      - Tier-1: list_to_linkedlist, etc.
        │   └── semantic.py    - Tier-1.5: build_list_with_cycle, etc.
        ├── tree_node/         - Depends on TreeNode
        ├── node/              - Depends on Node
        ├── node_graph/        - Depends on NodeGraph
        ├── node_nary/         - Depends on NodeNary
        └── doubly_list_node/  - Depends on DoublyListNode

Reference: docs/contracts/problem-support-boundary.md
"""

# Classes
from .classes import (
    ListNode,
    TreeNode,
    Node,
    NodeGraph,
    NodeNary,
    DoublyListNode,
)

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
    # NodeGraph - Tier 1
    adjacency_to_graph,
    graph_to_adjacency,
    # NodeNary - Tier 1
    list_to_nary_tree,
    nary_tree_to_list,
    # DoublyListNode - Tier 1
    list_to_doubly_linked,
    doubly_linked_to_list,
)

__all__ = [
    # Classes
    "ListNode",
    "TreeNode",
    "Node",
    "NodeGraph",
    "NodeNary",
    "DoublyListNode",
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
    # NodeGraph functions
    "adjacency_to_graph",
    "graph_to_adjacency",
    # NodeNary functions
    "list_to_nary_tree",
    "nary_tree_to_list",
    # DoublyListNode functions
    "list_to_doubly_linked",
    "doubly_linked_to_list",
]
