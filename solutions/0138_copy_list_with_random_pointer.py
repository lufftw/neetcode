# solutions/0138_copy_list_with_random_pointer.py
"""
Problem 0138 - Copy List with Random Pointer

A linked list of length n is given such that each node contains an additional
random pointer which could point to any node in the list, or null.

Construct a deep copy of the list.

LeetCode Constraints:
- 0 <= n <= 1000
- -10^4 <= Node.val <= 10^4
- Node.random is null or points to some node in the linked list

Key Insight:
The challenge is that random pointers may reference nodes not yet created.
Two main approaches:

1. Hash Map: First pass creates all copy nodes and maps original -> copy.
   Second pass connects next and random pointers using the map.

2. Interweaving: Insert copy nodes right after originals (A -> A' -> B -> B').
   This allows finding copies in O(1) without extra space.
   Then extract the copy list.

Solution Approaches:
1. Hash map (two-pass): O(n) time, O(n) space
2. Interweaving (three-pass): O(n) time, O(1) space
"""
from typing import List, Optional, Dict
from _runner import get_solver


class Node:
    """Definition for a Node with random pointer."""

    def __init__(self, val: int = 0, next: "Node" = None, random: "Node" = None):
        self.val = val
        self.next = next
        self.random = random


SOLUTIONS = {
    "default": {
        "class": "SolutionHashMap",
        "method": "copyRandomList",
        "complexity": "O(n) time, O(n) space",
        "description": "Hash map to track original-to-copy mapping",
    },
    "interweave": {
        "class": "SolutionInterweave",
        "method": "copyRandomList",
        "complexity": "O(n) time, O(1) space",
        "description": "Interweave copies with originals, then extract",
    },
}


class SolutionHashMap:
    """
    Hash map approach.

    Pass 1: Create copy nodes, build map from original -> copy.
    Pass 2: Set next and random pointers using the map.

    The map allows O(1) lookup of the copy corresponding to any original.

    Time: O(n) - two passes through the list
    Space: O(n) - hash map storing n mappings
    """

    def copyRandomList(self, head: Optional[Node]) -> Optional[Node]:
        if not head:
            return None

        # Map from original node to its copy
        old_to_new: Dict[Node, Node] = {}

        # Pass 1: Create all copy nodes
        current = head
        while current:
            old_to_new[current] = Node(current.val)
            current = current.next

        # Pass 2: Connect next and random pointers
        current = head
        while current:
            copy = old_to_new[current]
            copy.next = old_to_new.get(current.next)
            copy.random = old_to_new.get(current.random)
            current = current.next

        return old_to_new[head]


class SolutionInterweave:
    """
    Interweaving approach for O(1) space.

    Pass 1: Insert copy nodes right after each original.
            A -> B -> C becomes A -> A' -> B -> B' -> C -> C'

    Pass 2: Set random pointers. If original.random = X,
            then copy.random = X.next (which is X').

    Pass 3: Separate the two lists by restoring original next pointers
            and extracting copy list.

    Time: O(n) - three passes
    Space: O(1) - no extra data structures (output doesn't count)
    """

    def copyRandomList(self, head: Optional[Node]) -> Optional[Node]:
        if not head:
            return None

        # Pass 1: Insert copy nodes after each original
        current = head
        while current:
            copy = Node(current.val)
            copy.next = current.next
            current.next = copy
            current = copy.next

        # Pass 2: Set random pointers for copy nodes
        current = head
        while current:
            copy = current.next
            if current.random:
                copy.random = current.random.next  # Random's copy
            current = copy.next

        # Pass 3: Separate the two lists
        current = head
        copy_head = head.next

        while current:
            copy = current.next
            current.next = copy.next
            current = current.next
            if current:
                copy.next = current.next

        return copy_head


def _build_list(nodes: List[List[Optional[int]]]) -> Optional[Node]:
    """Build linked list from [[val, random_idx], ...] format."""
    if not nodes:
        return None

    # Create all nodes
    node_list: List[Node] = []
    for val, _ in nodes:
        node_list.append(Node(val))

    # Connect next pointers
    for i in range(len(node_list) - 1):
        node_list[i].next = node_list[i + 1]

    # Connect random pointers
    for i, (_, random_idx) in enumerate(nodes):
        if random_idx is not None:
            node_list[i].random = node_list[random_idx]

    return node_list[0]


def _list_to_array(head: Optional[Node]) -> List[List[Optional[int]]]:
    """Convert linked list to [[val, random_idx], ...] format."""
    if not head:
        return []

    # Build index map
    node_to_idx: Dict[Node, int] = {}
    current = head
    idx = 0
    while current:
        node_to_idx[current] = idx
        current = current.next
        idx += 1

    # Build result
    result: List[List[Optional[int]]] = []
    current = head
    while current:
        random_idx = node_to_idx.get(current.random) if current.random else None
        result.append([current.val, random_idx])
        current = current.next

    return result


def solve():
    import sys
    import json

    data = sys.stdin.read().strip()
    nodes = json.loads(data)

    head = _build_list(nodes)

    solver = get_solver(SOLUTIONS)
    copy_head = solver.copyRandomList(head)

    result = _list_to_array(copy_head)
    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
