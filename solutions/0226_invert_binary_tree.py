# solutions/0226_invert_binary_tree.py
"""
Problem: Invert Binary Tree
https://leetcode.com/problems/invert-binary-tree/

Given the root of a binary tree, invert the tree, and return its root.
Inverting a binary tree means swapping the left and right children of all
nodes in the tree.

Constraints:
- The number of nodes in the tree is in the range [0, 100]
- -100 <= Node.val <= 100
"""
from typing import Optional, List
from collections import deque
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionRecursive",
        "method": "invertTree",
        "complexity": "O(n) time, O(h) space",
        "description": "Recursive DFS with postorder child swap",
    },
    "iterative": {
        "class": "SolutionIterative",
        "method": "invertTree",
        "complexity": "O(n) time, O(w) space",
        "description": "Iterative BFS level-order swap",
    },
}


class TreeNode:
    def __init__(self, val: int = 0, left: "TreeNode" = None, right: "TreeNode" = None):
        self.val = val
        self.left = left
        self.right = right


class SolutionRecursive:
    """
    Recursive DFS approach swapping children at each node.

    The inversion property is self-similar: inverting a tree equals
    swapping root's children, then recursively inverting each subtree.
    This maps naturally to a postorder traversal pattern.

    Stack depth equals tree height, giving O(h) space. For balanced trees
    h = O(log n), but worst case (skewed) is O(n).
    """

    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        # Base case: empty subtree needs no inversion
        if not root:
            return None

        # Swap left and right children
        # This is the core operation - mirror reflection at this node
        root.left, root.right = root.right, root.left

        # Recursively invert both subtrees
        # Order doesn't matter since subtrees are independent
        self.invertTree(root.left)
        self.invertTree(root.right)

        return root


class SolutionIterative:
    """
    Iterative BFS using queue for level-order traversal.

    Instead of implicit call stack, we use an explicit queue to visit
    nodes. At each node, we swap its children before enqueueing them.
    This processes nodes level by level, left to right.

    Space complexity is O(w) where w is maximum tree width. For complete
    binary trees, w = n/2 at the last level, giving O(n) worst case.
    """

    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None

        # BFS queue initialized with root
        queue = deque([root])

        while queue:
            node = queue.popleft()

            # Swap children - core inversion operation
            node.left, node.right = node.right, node.left

            # Enqueue children for processing
            # After swap, original left is now right and vice versa
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        return root


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


def _tree_to_list(root: Optional[TreeNode]) -> List[Optional[int]]:
    """Convert tree to level-order list representation."""
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

    # Trim trailing Nones
    while result and result[-1] is None:
        result.pop()

    return result


def _invert_tree_reference(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """Reference implementation for validation."""
    if not root:
        return None
    root.left, root.right = root.right, root.left
    _invert_tree_reference(root.left)
    _invert_tree_reference(root.right)
    return root


def judge(actual, expected, input_data: str) -> bool:
    """
    Validate inverted tree by computing expected result.
    """
    import json

    # Parse actual if it's a string (ast.literal_eval fails on JSON null)
    if isinstance(actual, str):
        actual = json.loads(actual)

    tree_data = json.loads(input_data.strip())

    # Build and invert tree using reference implementation
    root = _build_tree(tree_data)
    inverted = _invert_tree_reference(root)
    expected_list = _tree_to_list(inverted)

    return actual == expected_list


JUDGE_FUNC = judge


def solve():
    import sys
    import json

    lines = sys.stdin.read().strip().split("\n")

    # Parse input: tree as level-order list
    tree_data = json.loads(lines[0])

    # Build tree
    root = _build_tree(tree_data)

    # Get solver and invert tree
    solver = get_solver(SOLUTIONS)
    result = solver.invertTree(root)

    # Convert back to list and output
    output = _tree_to_list(result)
    print(json.dumps(output, separators=(",", ":")))


if __name__ == "__main__":
    solve()
