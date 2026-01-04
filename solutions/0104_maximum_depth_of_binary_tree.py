"""
Problem: Maximum Depth of Binary Tree
Link: https://leetcode.com/problems/maximum-depth-of-binary-tree/

Given the root of a binary tree, return its maximum depth.

A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

Example 1:

    Input: root = [3,9,20,null,null,15,7]
    Output: 3

Example 2:

    Input: root = [1,null,2]
    Output: 2


Constraints:

- The number of nodes in the tree is in the range [0, 10^4].

- -100 <= Node.val <= 100

Topics: Tree, Depth First Search, Breadth First Search, Binary Tree
"""


from typing import Optional
from _runner import get_solver
from runner.utils.codec import TreeNode, list_to_tree


# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# Polymorphic pattern: each entry specifies class + method
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "maxDepth",
        "complexity": "TODO: O(?)",
        "description": "TODO: describe your approach",
    },
}


# ============================================
# Solution
# ============================================
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        # TODO: Implement your solution
        pass


def solve():
    """
    Auto-generated solve() for Tier-1 problem.
    Codec mode: import
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')

    root_list = json.loads(lines[0])
    root = list_to_tree(root_list)

    solver = get_solver(SOLUTIONS)
    result = solver.maxDepth(root)

    print(result)


if __name__ == "__main__":
    solve()
