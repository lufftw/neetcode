# solutions/0572_subtree_of_another_tree.py
"""
Problem 0572 - Subtree of Another Tree

Given the roots of two binary trees root and subRoot, return true if there
is a subtree of root with the same structure and node values as subRoot.

A subtree of a binary tree is a tree that consists of a node in tree and
all of this node's descendants.

LeetCode Constraints:
- The number of nodes in root is in the range [1, 2000]
- The number of nodes in subRoot is in the range [1, 1000]
- -10^4 <= root.val <= 10^4
- -10^4 <= subRoot.val <= 10^4

Key Insight:
At each node in root, check if the subtree rooted there matches subRoot.
Two trees match if they have the same structure and values.

The naive approach checks for a match at each node in root, leading to
O(m * n) time. We can optimize with serialization + string matching.

Solution Approaches:
1. DFS with tree matching: O(m * n) time, O(h) space
2. Serialization with string matching: O(m + n) time, O(m + n) space
"""
from typing import List, Optional
from collections import deque
from _runner import get_solver


class TreeNode:
    """Definition for a binary tree node."""

    def __init__(self, val: int = 0, left: "TreeNode" = None, right: "TreeNode" = None):
        self.val = val
        self.left = left
        self.right = right


SOLUTIONS = {
    "default": {
        "class": "SolutionDFS",
        "method": "isSubtree",
        "complexity": "O(m * n) time, O(h) space",
        "description": "DFS traversal checking tree equality at each node",
    },
    "serialization": {
        "class": "SolutionSerialization",
        "method": "isSubtree",
        "complexity": "O(m + n) time, O(m + n) space",
        "description": "Serialize both trees, use string containment",
    },
}


class SolutionDFS:
    """
    DFS approach with tree matching.

    For each node in root, check if the subtree starting there
    is identical to subRoot using a separate isSameTree helper.

    Time: O(m * n) where m = nodes in root, n = nodes in subRoot
    - We potentially call isSameTree (O(n)) for each node in root (m nodes)

    Space: O(h) for recursion stack, where h = max height
    """

    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        if not subRoot:
            return True  # Empty tree is subtree of any tree
        if not root:
            return False  # Non-empty subRoot can't be subtree of empty root

        # Check if trees rooted here are identical
        if self._isSameTree(root, subRoot):
            return True

        # Otherwise, check left and right subtrees
        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)

    def _isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """Check if two trees are structurally identical with same values."""
        if not p and not q:
            return True
        if not p or not q:
            return False
        if p.val != q.val:
            return False
        return self._isSameTree(p.left, q.left) and self._isSameTree(p.right, q.right)


class SolutionSerialization:
    """
    Serialization approach using string matching.

    Serialize both trees using pre-order traversal with null markers.
    Then check if serialization of subRoot is contained in serialization
    of root.

    Important: Use delimiters (like commas) to avoid false matches.
    "12" should not match "123", but ",1,2," won't match ",1,23,".

    Time: O(m + n) for serialization + O(m + n) for string matching
    Space: O(m + n) for storing serialized strings
    """

    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        def serialize(node: Optional[TreeNode]) -> str:
            """Serialize tree to string with null markers."""
            if not node:
                return "#"
            # Use ^ as prefix to avoid substring issues (e.g., 2 vs 12)
            return f"^{node.val},{serialize(node.left)},{serialize(node.right)}"

        root_serial = serialize(root)
        sub_serial = serialize(subRoot)

        return sub_serial in root_serial


def _build_tree(values: List[Optional[int]]) -> Optional[TreeNode]:
    """Build tree from level-order list."""
    if not values or values[0] is None:
        return None

    root = TreeNode(values[0])
    queue = deque([root])
    i = 1

    while queue and i < len(values):
        node = queue.popleft()

        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1

        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1

    return root


def solve():
    import sys
    import json

    lines = sys.stdin.read().strip().split("\n")

    root_vals = json.loads(lines[0])
    sub_vals = json.loads(lines[1])

    root = _build_tree(root_vals)
    subRoot = _build_tree(sub_vals)

    solver = get_solver(SOLUTIONS)
    result = solver.isSubtree(root, subRoot)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
