# solutions/0110_balanced_binary_tree.py
"""
Problem: Balanced Binary Tree
Link: https://leetcode.com/problems/balanced-binary-tree/

Given a binary tree, determine if it is height-balanced.

A height-balanced binary tree is a binary tree in which the depth of the two subtrees of
every node never differs by more than one.

Example 1:
    Input: root = [3,9,20,null,null,15,7]
    Output: true

Example 2:
    Input: root = [1,2,2,3,3,null,null,4,4]
    Output: false

Constraints:
- The number of nodes in the tree is in the range [0, 5000].
- -10^4 <= Node.val <= 10^4

Topics: Tree, Depth-First Search, Binary Tree
"""
from typing import Optional
from _runner import get_solver


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ============================================
# JUDGE_FUNC
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    if expected is not None:
        return actual == expected
    return True


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "isBalanced",
        "complexity": "O(n) time, O(h) space",
        "description": "DFS with early termination using sentinel -1",
        "api_kernels": ["TreeTraversalDFS"],
        "patterns": ["tree_property_validation"],
    },
}


# ============================================
# Solution 1: DFS with Early Termination
# ============================================
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        """
        Check if tree is height-balanced.

        Returns height if balanced, -1 if not (early termination).
        """
        def check(node: Optional[TreeNode]) -> int:
            if not node:
                return 0

            left = check(node.left)
            if left == -1:
                return -1

            right = check(node.right)
            if right == -1:
                return -1

            if abs(left - right) > 1:
                return -1

            return 1 + max(left, right)

        return check(root) != -1


def _build_tree(values: list) -> Optional[TreeNode]:
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
    result = solver.isBalanced(root)

    print(str(result).lower())


if __name__ == "__main__":
    solve()
