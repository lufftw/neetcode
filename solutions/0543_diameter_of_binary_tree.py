# solutions/0543_diameter_of_binary_tree.py
"""
Problem: Diameter of Binary Tree
Link: https://leetcode.com/problems/diameter-of-binary-tree/

Given the root of a binary tree, return the length of the diameter of the tree.

The diameter of a binary tree is the length of the longest path between any two nodes
in a tree. This path may or may not pass through the root.

The length of a path between two nodes is represented by the number of edges between them.

Example 1:
    Input: root = [1,2,3,4,5]
    Output: 3
    Explanation: 3 is the length of the path [4,2,1,3] or [5,2,1,3].

Example 2:
    Input: root = [1,2]
    Output: 1

Constraints:
- The number of nodes in the tree is in the range [1, 10^4].
- -100 <= Node.val <= 100

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
        "method": "diameterOfBinaryTree",
        "complexity": "O(n) time, O(h) space",
        "description": "DFS tracking max path through each node",
        "api_kernels": ["TreeTraversalDFS"],
        "patterns": ["tree_path_computation"],
    },
}


# ============================================
# Solution 1: DFS Path Tracking
# ============================================
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        """
        Longest path between any two nodes (in edges).

        Track maximum left_height + right_height during height computation.
        """
        self.diameter = 0

        def height(node: Optional[TreeNode]) -> int:
            if not node:
                return 0

            left_h = height(node.left)
            right_h = height(node.right)

            # Update diameter (path through this node)
            self.diameter = max(self.diameter, left_h + right_h)

            # Return height for parent
            return 1 + max(left_h, right_h)

        height(root)
        return self.diameter


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
    result = solver.diameterOfBinaryTree(root)

    print(result)


if __name__ == "__main__":
    solve()
