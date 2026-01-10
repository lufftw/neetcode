# solutions/0105_construct_binary_tree_from_preorder_and_inorder_traversal.py
"""
Problem 0105 - Construct Binary Tree from Preorder and Inorder Traversal

Given two integer arrays preorder and inorder where:
- preorder is the preorder traversal of a binary tree
- inorder is the inorder traversal of the same tree

Construct and return the binary tree.

LeetCode Constraints:
- 1 <= preorder.length <= 3000
- inorder.length == preorder.length
- -3000 <= preorder[i], inorder[i] <= 3000
- preorder and inorder consist of unique values
- Each value of inorder also appears in preorder
- preorder is guaranteed to be the preorder traversal
- inorder is guaranteed to be the inorder traversal

Key Insight:
- Preorder: [root, ...left subtree..., ...right subtree...]
- Inorder: [...left subtree..., root, ...right subtree...]

The first element of preorder is always the root.
Finding that root in inorder tells us the boundary between left and right subtrees.
The number of elements before root in inorder = size of left subtree.

Solution Approaches:
1. Recursive with hash map: O(n) time, O(n) space - precompute inorder indices
2. Recursive without hash map: O(n^2) time worst case due to linear search
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
        "class": "SolutionHashMap",
        "method": "buildTree",
        "complexity": "O(n) time, O(n) space",
        "description": "Recursive with hash map for O(1) root lookup in inorder",
    },
    "linear_search": {
        "class": "SolutionLinearSearch",
        "method": "buildTree",
        "complexity": "O(n^2) time, O(n) space",
        "description": "Recursive with linear search for root in inorder",
    },
}


class SolutionHashMap:
    """
    Optimized recursive approach using hash map.

    Precompute a map from value -> index in inorder array.
    This allows O(1) lookup of root position instead of O(n) search.

    Algorithm:
    1. Root = preorder[preorder_start]
    2. Find root's index in inorder using hash map
    3. Left subtree size = root_idx - inorder_start
    4. Recursively build left subtree, then right subtree

    The preorder range for left subtree: [preorder_start+1, preorder_start+1+left_size)
    The preorder range for right subtree: [preorder_start+1+left_size, preorder_end)
    """

    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        # Map value to index in inorder for O(1) lookup
        inorder_map = {val: idx for idx, val in enumerate(inorder)}

        def build(pre_start: int, pre_end: int, in_start: int, in_end: int) -> Optional[TreeNode]:
            if pre_start >= pre_end:
                return None

            # Root is first element in preorder range
            root_val = preorder[pre_start]
            root = TreeNode(root_val)

            # Find root in inorder to determine subtree sizes
            root_idx = inorder_map[root_val]
            left_size = root_idx - in_start

            # Build subtrees
            root.left = build(
                pre_start + 1,
                pre_start + 1 + left_size,
                in_start,
                root_idx
            )
            root.right = build(
                pre_start + 1 + left_size,
                pre_end,
                root_idx + 1,
                in_end
            )

            return root

        return build(0, len(preorder), 0, len(inorder))


class SolutionLinearSearch:
    """
    Simple recursive approach with linear search.

    Same algorithm, but uses list slicing and index() for simplicity.
    Less efficient due to O(n) search for root in each recursion.

    This is cleaner to understand but O(n^2) in worst case
    (e.g., skewed tree where root is always at boundary).
    """

    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        if not preorder or not inorder:
            return None

        # Root is first element in preorder
        root_val = preorder[0]
        root = TreeNode(root_val)

        # Find root position in inorder
        root_idx = inorder.index(root_val)

        # Elements before root_idx in inorder are left subtree
        # They correspond to preorder[1:1+root_idx]
        root.left = self.buildTree(
            preorder[1:1 + root_idx],
            inorder[:root_idx]
        )

        # Elements after root_idx in inorder are right subtree
        # They correspond to preorder[1+root_idx:]
        root.right = self.buildTree(
            preorder[1 + root_idx:],
            inorder[root_idx + 1:]
        )

        return root


def _tree_to_list(root: Optional[TreeNode]) -> List[Optional[int]]:
    """Convert tree to level-order list."""
    if not root:
        return []

    result: List[Optional[int]] = []
    queue = deque([root])

    while queue:
        node = queue.popleft()
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)

    # Trim trailing nulls
    while result and result[-1] is None:
        result.pop()

    return result


def solve():
    import sys
    import json

    lines = sys.stdin.read().strip().split("\n")

    preorder = json.loads(lines[0])
    inorder = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    root = solver.buildTree(preorder, inorder)

    result = _tree_to_list(root)
    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
