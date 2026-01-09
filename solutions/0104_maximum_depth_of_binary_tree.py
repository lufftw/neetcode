# solutions/0104_maximum_depth_of_binary_tree.py
"""
Problem: Maximum Depth of Binary Tree
Link: https://leetcode.com/problems/maximum-depth-of-binary-tree/

Given the root of a binary tree, return its maximum depth.

A binary tree's maximum depth is the number of nodes along the longest path
from the root node down to the farthest leaf node.

Example 1:
    Input: root = [3,9,20,null,null,15,7]
    Output: 3

Example 2:
    Input: root = [1,null,2]
    Output: 2

Constraints:
- The number of nodes in the tree is in the range [0, 10^4].
- -100 <= Node.val <= 100

Topics: Tree, Depth-First Search, Breadth-First Search, Binary Tree
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
        "method": "maxDepth",
        "complexity": "O(n) time, O(h) space",
        "description": "Recursive DFS computing max depth",
        "api_kernels": ["TreeTraversalDFS"],
        "patterns": ["tree_property_computation"],
    },
    "recursive": {
        "class": "Solution",
        "method": "maxDepth",
        "complexity": "O(n) time, O(h) space",
        "description": "Recursive DFS, elegant one-liner",
    },
    "bfs": {
        "class": "SolutionBFS",
        "method": "maxDepth",
        "complexity": "O(n) time, O(w) space",
        "description": "BFS level-order traversal, count levels",
    },
    "iterative_dfs": {
        "class": "SolutionIterativeDFS",
        "method": "maxDepth",
        "complexity": "O(n) time, O(h) space",
        "description": "Iterative DFS with explicit stack",
    },
}


# ============================================
# Solution 1: Recursive DFS
# ============================================
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        """
        Find maximum depth (height) of binary tree.

        Core insight: Depth is computed bottom-up. Empty tree has depth 0, leaf
        has depth 1, internal node has depth = 1 + max(left_depth, right_depth).
        Recursion naturally handles the postorder computation.

        Invariant: Return value represents the height of the subtree rooted at
        the current node.

        Args:
            root: Root of binary tree

        Returns:
            Maximum depth (number of nodes on longest root-to-leaf path)
        """
        if not root:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))


# ============================================
# Solution 2: BFS Level-Order Traversal
# ============================================
class SolutionBFS:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        """
        Find maximum depth using BFS level-order traversal.

        Core insight: Process tree level by level. Each level increment
        corresponds to one depth unit. Count how many levels exist.

        Advantage: No recursion, avoids stack overflow on deep trees.

        Args:
            root: Root of binary tree

        Returns:
            Maximum depth (number of levels)
        """
        if not root:
            return 0

        from collections import deque

        queue = deque([root])
        depth = 0

        while queue:
            depth += 1
            # Process all nodes at current level
            for _ in range(len(queue)):
                node = queue.popleft()
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

        return depth


# ============================================
# Solution 3: Iterative DFS with Stack
# ============================================
class SolutionIterativeDFS:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        """
        Find maximum depth using iterative DFS with explicit stack.

        Core insight: Simulate recursion with a stack. Track depth at each
        node by storing (node, depth) pairs. Update max_depth as we go.

        Advantage: No recursion, explicit control over traversal.

        Args:
            root: Root of binary tree

        Returns:
            Maximum depth
        """
        if not root:
            return 0

        stack = [(root, 1)]
        max_depth = 0

        while stack:
            node, depth = stack.pop()
            max_depth = max(max_depth, depth)

            if node.left:
                stack.append((node.left, depth + 1))
            if node.right:
                stack.append((node.right, depth + 1))

        return max_depth


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
    result = solver.maxDepth(root)

    print(result)


if __name__ == "__main__":
    solve()
