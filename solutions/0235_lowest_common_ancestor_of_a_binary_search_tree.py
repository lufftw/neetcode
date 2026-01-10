# solutions/0235_lowest_common_ancestor_of_a_binary_search_tree.py
"""
Problem: Lowest Common Ancestor of a Binary Search Tree
https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/

Given a binary search tree (BST) and two nodes p and q, find their lowest
common ancestor (LCA). The LCA is the lowest node that has both p and q as
descendants (a node can be a descendant of itself).

Constraints:
- The number of nodes in the tree is in the range [2, 10^5]
- -10^9 <= Node.val <= 10^9
- All node values are unique
- p != q
- p and q exist in the BST
"""
from typing import Optional, List
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionIterative",
        "method": "lowestCommonAncestor",
        "complexity": "O(h) time, O(1) space",
        "description": "Iterative BST traversal to split point",
    },
    "recursive": {
        "class": "SolutionRecursive",
        "method": "lowestCommonAncestor",
        "complexity": "O(h) time, O(h) space",
        "description": "Recursive approach using BST property",
    },
}


class TreeNode:
    def __init__(self, val: int = 0, left: "TreeNode" = None, right: "TreeNode" = None):
        self.val = val
        self.left = left
        self.right = right


class SolutionIterative:
    """
    Iterative traversal exploiting BST ordering invariant.

    The BST property guarantees that the LCA is the first node where p and q
    "split" - one goes left, one goes right. Starting from root, we descend
    until values diverge across the current node.

    This approach eliminates recursion overhead, achieving constant space.
    The loop terminates when neither child direction is unanimously chosen.
    """

    def lowestCommonAncestor(
        self, root: TreeNode, p: TreeNode, q: TreeNode
    ) -> TreeNode:
        # Traverse from root toward the split point
        # BST invariant: left < node < right enables directed search
        current = root

        while current:
            # Both targets smaller than current node - LCA must be in left subtree
            # This follows from BST property: larger values cannot be ancestors
            if p.val < current.val and q.val < current.val:
                current = current.left
            # Both targets larger than current node - LCA must be in right subtree
            # Symmetric reasoning: smaller values cannot contain both nodes
            elif p.val > current.val and q.val > current.val:
                current = current.right
            else:
                # Values straddle current node or one equals it
                # This is the split point - current node is the LCA
                return current

        return None


class SolutionRecursive:
    """
    Recursive approach mirroring iterative logic with implicit stack.

    Each recursive call narrows the search space by half (on average in
    balanced BST). The base case occurs when p and q straddle the current
    node or one of them equals the current node.

    While conceptually cleaner, this uses O(h) stack space. For skewed trees,
    h approaches n, making space complexity O(n) in worst case.
    """

    def lowestCommonAncestor(
        self, root: TreeNode, p: TreeNode, q: TreeNode
    ) -> TreeNode:
        # Base condition: null root means empty subtree (shouldn't happen per constraints)
        if not root:
            return None

        # Both values smaller - recurse left following BST ordering
        if p.val < root.val and q.val < root.val:
            return self.lowestCommonAncestor(root.left, p, q)

        # Both values larger - recurse right following BST ordering
        if p.val > root.val and q.val > root.val:
            return self.lowestCommonAncestor(root.right, p, q)

        # Split point found: one value on each side, or one equals root
        # Current node is guaranteed to be the lowest common ancestor
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


def _find_node(root: TreeNode, val: int) -> Optional[TreeNode]:
    """Find node with given value in tree."""
    if not root:
        return None
    if root.val == val:
        return root
    left = _find_node(root.left, val)
    if left:
        return left
    return _find_node(root.right, val)


def judge(actual, expected, input_data: str) -> bool:
    """
    Validate LCA result using BST property.
    For BST, LCA is unique and deterministic based on split point.
    """
    import json

    lines = input_data.strip().split("\n")
    tree_data = json.loads(lines[0])
    p_val = json.loads(lines[1])
    q_val = json.loads(lines[2])

    # Compute expected LCA using BST property
    root = _build_tree(tree_data)
    if not root:
        return actual is None

    # Find LCA by traversing to split point
    current = root
    while current:
        if p_val < current.val and q_val < current.val:
            current = current.left
        elif p_val > current.val and q_val > current.val:
            current = current.right
        else:
            break

    expected_val = current.val if current else None
    return actual == expected_val


JUDGE_FUNC = judge


def solve():
    import sys
    import json

    lines = sys.stdin.read().strip().split("\n")

    # Parse input: tree, p value, q value
    tree_data = json.loads(lines[0])
    p_val = json.loads(lines[1])
    q_val = json.loads(lines[2])

    # Build tree and find nodes
    root = _build_tree(tree_data)
    p = _find_node(root, p_val)
    q = _find_node(root, q_val)

    # Get solver and find LCA
    solver = get_solver(SOLUTIONS)
    result = solver.lowestCommonAncestor(root, p, q)

    # Output the LCA node value
    print(json.dumps(result.val if result else None, separators=(",", ":")))


if __name__ == "__main__":
    solve()
