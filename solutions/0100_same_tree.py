# solutions/0100_same_tree.py
"""
Problem: Same Tree
https://leetcode.com/problems/same-tree/

Given the roots of two binary trees p and q, check if they are the same
or not. Two binary trees are considered the same if they are structurally
identical, and the nodes have the same value.

Constraints:
- The number of nodes in both trees is in the range [0, 100]
- -10^4 <= Node.val <= 10^4
"""
from typing import Optional, List
from collections import deque
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionRecursive",
        "method": "isSameTree",
        "complexity": "O(n) time, O(h) space",
        "description": "Recursive DFS comparing nodes simultaneously",
    },
    "iterative": {
        "class": "SolutionIterative",
        "method": "isSameTree",
        "complexity": "O(n) time, O(w) space",
        "description": "Iterative BFS using queue for parallel traversal",
    },
}


class TreeNode:
    def __init__(self, val: int = 0, left: "TreeNode" = None, right: "TreeNode" = None):
        self.val = val
        self.left = left
        self.right = right


class SolutionRecursive:
    """
    Recursive comparison with structural and value checks.

    Trees are identical if and only if their roots match and their
    corresponding subtrees are identical. This naturally maps to a
    recursive definition: same(p, q) = match(p, q) AND same(p.left, q.left)
    AND same(p.right, q.right).

    Base case: two null nodes are identical; null and non-null differ.
    """

    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        # Base case: both empty
        if not p and not q:
            return True

        # Structure mismatch: one is null, other isn't
        if not p or not q:
            return False

        # Value mismatch at current nodes
        if p.val != q.val:
            return False

        # Recursively check both subtrees
        # Short-circuit: if left differs, skip right check
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)


class SolutionIterative:
    """
    Iterative comparison using dual-queue BFS traversal.

    Process nodes level-by-level from both trees simultaneously.
    At each step, dequeue one node from each tree and compare.
    If any mismatch occurs, return false immediately.

    This approach uses O(w) space where w is the maximum width,
    better than recursion for wide trees with shallow height.
    """

    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        # Queue holds pairs of corresponding nodes
        queue = deque([(p, q)])

        while queue:
            node1, node2 = queue.popleft()

            # Both null: matching empty subtrees
            if not node1 and not node2:
                continue

            # Structural mismatch
            if not node1 or not node2:
                return False

            # Value mismatch
            if node1.val != node2.val:
                return False

            # Enqueue children for comparison
            queue.append((node1.left, node2.left))
            queue.append((node1.right, node2.right))

        return True


def _build_tree(nodes: List[Optional[int]]) -> Optional[TreeNode]:
    """Build binary tree from level-order list representation."""
    if not nodes or nodes[0] is None:
        return None

    root = TreeNode(nodes[0])
    queue = [root]
    i = 1

    while queue and i < len(nodes):
        node = queue.pop(0)

        # Left child
        if i < len(nodes):
            if nodes[i] is not None:
                node.left = TreeNode(nodes[i])
                queue.append(node.left)
            i += 1

        # Right child
        if i < len(nodes):
            if nodes[i] is not None:
                node.right = TreeNode(nodes[i])
                queue.append(node.right)
            i += 1

    return root


def _is_same_tree_ref(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
    """Reference implementation for validation."""
    if not p and not q:
        return True
    if not p or not q:
        return False
    if p.val != q.val:
        return False
    return _is_same_tree_ref(p.left, q.left) and _is_same_tree_ref(p.right, q.right)


def judge(actual, expected, input_data: str) -> bool:
    """
    Validate same tree result using reference implementation.
    """
    import json

    # Parse actual if string (ast.literal_eval fails on JSON true/false)
    if isinstance(actual, str):
        actual = json.loads(actual)

    lines = input_data.strip().split("\n")
    tree_p = json.loads(lines[0])
    tree_q = json.loads(lines[1])

    p = _build_tree(tree_p)
    q = _build_tree(tree_q)
    expected_result = _is_same_tree_ref(p, q)

    return actual == expected_result


JUDGE_FUNC = judge


def solve():
    import sys
    import json

    lines = sys.stdin.read().strip().split("\n")

    # Parse input: two trees as level-order lists
    tree_p = json.loads(lines[0])
    tree_q = json.loads(lines[1])

    # Build trees
    p = _build_tree(tree_p)
    q = _build_tree(tree_q)

    # Get solver and check if same
    solver = get_solver(SOLUTIONS)
    result = solver.isSameTree(p, q)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
