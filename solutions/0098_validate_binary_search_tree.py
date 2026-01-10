# solutions/0098_validate_binary_search_tree.py
"""
Problem: Validate Binary Search Tree
https://leetcode.com/problems/validate-binary-search-tree/

Given the root of a binary tree, determine if it is a valid BST.
A valid BST has left subtree values < node < right subtree values,
with this property holding recursively for all nodes.

Key insight: Each node must fall within a valid range determined by
its ancestors. Going left tightens upper bound; going right tightens lower.

Constraints:
- The number of nodes in the tree is in the range [1, 10^4]
- -2^31 <= Node.val <= 2^31 - 1
"""
import json
import sys
from typing import Optional, List

from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionRangeCheck",
        "method": "isValidBST",
        "complexity": "O(n) time, O(h) space",
        "description": "Recursive with valid range bounds propagation",
    },
    "inorder": {
        "class": "SolutionInorder",
        "method": "isValidBST",
        "complexity": "O(n) time, O(h) space",
        "description": "In-order traversal checking strictly increasing",
    },
}


class TreeNode:
    def __init__(self, val: int = 0, left: "TreeNode" = None, right: "TreeNode" = None):
        self.val = val
        self.left = left
        self.right = right


class SolutionRangeCheck:
    """
    Recursive range propagation approach.

    WHY: Simply checking node.left.val < node.val < node.right.val is wrong—
    ALL nodes in left subtree must be less than current node (not just
    immediate child). We track the valid range as we descend.

    HOW: Start with (-inf, +inf) as valid range. Going left, upper bound
    becomes current value. Going right, lower bound becomes current value.
    If any node violates its range, tree is invalid.
    """

    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def validate(node: Optional[TreeNode], lower: float, upper: float) -> bool:
            if not node:
                return True

            # Node must be strictly within bounds
            if node.val <= lower or node.val >= upper:
                return False

            # Left subtree: values must be < node.val (update upper bound)
            # Right subtree: values must be > node.val (update lower bound)
            return (
                validate(node.left, lower, node.val) and
                validate(node.right, node.val, upper)
            )

        return validate(root, float("-inf"), float("inf"))


class SolutionInorder:
    """
    In-order traversal approach.

    WHY: In-order traversal of a valid BST produces a strictly increasing
    sequence. If we ever see a value <= previous value, tree is invalid.

    HOW: Perform in-order traversal (left, node, right), tracking the
    previous value seen. Each new value must be strictly greater.
    """

    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        self.prev = float("-inf")

        def inorder(node: Optional[TreeNode]) -> bool:
            if not node:
                return True

            # Visit left subtree
            if not inorder(node.left):
                return False

            # Check current node against previous
            if node.val <= self.prev:
                return False
            self.prev = node.val

            # Visit right subtree
            return inorder(node.right)

        return inorder(root)


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


def _is_valid_bst_ref(root: Optional[TreeNode]) -> bool:
    """Reference implementation for validation."""
    def validate(node, lower, upper):
        if not node:
            return True
        if node.val <= lower or node.val >= upper:
            return False
        return validate(node.left, lower, node.val) and validate(node.right, node.val, upper)
    return validate(root, float("-inf"), float("inf"))


def judge(actual, expected, input_data: str) -> bool:
    """Validate BST result using reference implementation."""
    if isinstance(actual, str):
        actual = json.loads(actual)

    tree_list = json.loads(input_data.strip())
    root = _build_tree(tree_list)
    expected_result = _is_valid_bst_ref(root)

    return actual == expected_result


JUDGE_FUNC = judge


def solve():
    lines = sys.stdin.read().strip().split("\n")
    tree_list = json.loads(lines[0])
    root = _build_tree(tree_list)

    solver = get_solver(SOLUTIONS)
    result = solver.isValidBST(root)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
