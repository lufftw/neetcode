"""Codec functions organized by data structure."""

from .list_node import (
    list_to_linkedlist,
    linkedlist_to_list,
    build_list_with_cycle,
    node_to_index,
    build_intersecting_lists,
)
from .tree_node import list_to_tree, tree_to_list
from .node import build_random_pointer_list, encode_random_pointer_list, verify_deep_copy

__all__ = [
    # ListNode
    "list_to_linkedlist",
    "linkedlist_to_list",
    "build_list_with_cycle",
    "node_to_index",
    "build_intersecting_lists",
    # TreeNode
    "list_to_tree",
    "tree_to_list",
    # Node
    "build_random_pointer_list",
    "encode_random_pointer_list",
    "verify_deep_copy",
]

