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
from .node_graph import adjacency_to_graph, graph_to_adjacency
from .node_nary import list_to_nary_tree, nary_tree_to_list
from .doubly_list_node import list_to_doubly_linked, doubly_linked_to_list

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
    # Node (random pointer)
    "build_random_pointer_list",
    "encode_random_pointer_list",
    "verify_deep_copy",
    # NodeGraph
    "adjacency_to_graph",
    "graph_to_adjacency",
    # NodeNary
    "list_to_nary_tree",
    "nary_tree_to_list",
    # DoublyListNode
    "list_to_doubly_linked",
    "doubly_linked_to_list",
]

