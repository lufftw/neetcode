# solutions/0094_binary_tree_inorder_traversal.py
"""
Problem: Binary Tree Inorder Traversal
Link: https://leetcode.com/problems/binary-tree-inorder-traversal/

Given the root of a binary tree, return the inorder traversal of its nodes' values.

Example 1:
    Input: root = [1,null,2,3]
    Output: [1,3,2]

Example 2:
    Input: root = []
    Output: []

Constraints:
- The number of nodes in the tree is in the range [0, 100].
- -100 <= Node.val <= 100

Topics: Stack, Tree, Depth-First Search, Binary Tree
"""
from typing import List, Optional
from _runner import get_solver


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Inorder Traversal solution."""
    if expected is not None:
        return actual == expected
    return True  # Trust actual for tree problems


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionRecursive",
        "method": "inorderTraversal",
        "complexity": "O(n) time, O(h) space",
        "description": "Recursive DFS inorder traversal",
        "api_kernels": ["TreeTraversalDFS"],
        "patterns": ["tree_dfs_inorder"],
    },
    "iterative": {
        "class": "SolutionIterative",
        "method": "inorderTraversal",
        "complexity": "O(n) time, O(h) space",
        "description": "Iterative with explicit stack",
        "api_kernels": ["TreeTraversalDFS"],
        "patterns": ["tree_dfs_iterative"],
    },
}


# ============================================
# Solution 1: Recursive DFS
# ============================================
class SolutionRecursive:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        """Inorder: Left → Node → Right."""
        result: list[int] = []

        def dfs(node: Optional[TreeNode]) -> None:
            if not node:
                return
            dfs(node.left)
            result.append(node.val)
            dfs(node.right)

        dfs(root)
        return result


# ============================================
# Solution 2: Iterative with Stack
# ============================================
class SolutionIterative:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        """Iterative inorder using explicit stack."""
        result: list[int] = []
        stack: list[TreeNode] = []
        curr = root

        while curr or stack:
            while curr:
                stack.append(curr)
                curr = curr.left

            curr = stack.pop()
            result.append(curr.val)
            curr = curr.right

        return result


def _build_tree(values: list) -> Optional[TreeNode]:
    """Build tree from level-order list."""
    if not values or values[0] is None:
        return None

    root = TreeNode(values[0])
    queue = [root]
    i = 1

    while queue and i < len(values):
        node = queue.pop(0)
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
    lines = sys.stdin.read().strip().split('\n')

    values = json.loads(lines[0])
    root = _build_tree(values)

    solver = get_solver(SOLUTIONS)
    result = solver.inorderTraversal(root)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
