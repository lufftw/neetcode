# solutions/0124_binary_tree_maximum_path_sum.py
"""
Problem: Binary Tree Maximum Path Sum
Link: https://leetcode.com/problems/binary-tree-maximum-path-sum/

A path in a binary tree is a sequence of nodes where each pair of adjacent nodes in the
sequence has an edge connecting them. A node can only appear in the sequence at most once.
Note that the path does not need to pass through the root.

The path sum of a path is the sum of the node's values in the path.

Given the root of a binary tree, return the maximum path sum of any non-empty path.

Example 1:
    Input: root = [1,2,3]
    Output: 6
    Explanation: The optimal path is 2 -> 1 -> 3 with a path sum of 2 + 1 + 3 = 6.

Example 2:
    Input: root = [-10,9,20,null,null,15,7]
    Output: 42
    Explanation: The optimal path is 15 -> 20 -> 7 with a path sum of 15 + 20 + 7 = 42.

Constraints:
- The number of nodes in the tree is in the range [1, 3 * 10^4].
- -1000 <= Node.val <= 1000

Topics: Dynamic Programming, Tree, Depth-First Search, Binary Tree
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
        "method": "maxPathSum",
        "complexity": "O(n) time, O(h) space",
        "description": "DFS tracking max path sum through each node",
        "api_kernels": ["TreeTraversalDFS"],
        "patterns": ["tree_path_sum"],
    },
}


# ============================================
# Solution 1: DFS Path Sum Tracking
# ============================================
class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        """
        Maximum path sum in binary tree.

        At each node:
        - Consider it as path apex: node.val + left_gain + right_gain
        - Return single branch max for parent: node.val + max(left, right)
        - Use max(0, child) to skip negative paths
        """
        self.max_sum = float('-inf')

        def max_gain(node: Optional[TreeNode]) -> int:
            if not node:
                return 0

            # Max gain from left/right (can skip negative paths)
            left_gain = max(0, max_gain(node.left))
            right_gain = max(0, max_gain(node.right))

            # Path sum if this node is apex
            path_sum = node.val + left_gain + right_gain
            self.max_sum = max(self.max_sum, path_sum)

            # Return max single-branch gain for parent
            return node.val + max(left_gain, right_gain)

        max_gain(root)
        return self.max_sum


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
    result = solver.maxPathSum(root)

    print(result)


if __name__ == "__main__":
    solve()
