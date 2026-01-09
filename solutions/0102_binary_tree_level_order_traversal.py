# solutions/0102_binary_tree_level_order_traversal.py
"""
Problem: Binary Tree Level Order Traversal
Link: https://leetcode.com/problems/binary-tree-level-order-traversal/

Given the root of a binary tree, return the level order traversal of its nodes' values.
(i.e., from left to right, level by level).

Example 1:
    Input: root = [3,9,20,null,null,15,7]
    Output: [[3],[9,20],[15,7]]

Example 2:
    Input: root = [1]
    Output: [[1]]

Constraints:
- The number of nodes in the tree is in the range [0, 2000].
- -1000 <= Node.val <= 1000

Topics: Tree, Breadth-First Search, Binary Tree
"""
from typing import List, Optional
from collections import deque
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
        "method": "levelOrder",
        "complexity": "O(n) time, O(w) space",
        "description": "BFS with queue, process level by level",
        "api_kernels": ["TreeTraversalBFS"],
        "patterns": ["tree_bfs_level_order"],
    },
    "bfs": {
        "class": "Solution",
        "method": "levelOrder",
        "complexity": "O(n) time, O(w) space",
        "description": "BFS with queue - canonical level order traversal",
    },
    "dfs": {
        "class": "SolutionDFS",
        "method": "levelOrder",
        "complexity": "O(n) time, O(h) space",
        "description": "DFS with depth tracking - recursive alternative",
    },
}


# ============================================
# Solution 1: BFS Level Order
# ============================================
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        Return level-order traversal as list of lists.

        Core insight: BFS with queue naturally processes nodes level by level.
        By recording queue size at start of each iteration, we process exactly
        one level before moving to the next.

        Invariant: At start of each while iteration, queue contains exactly all
        nodes at the current depth level.

        Args:
            root: Root of binary tree

        Returns:
            List of lists, where each inner list contains values at that depth
        """
        if not root:
            return []

        result: list[list[int]] = []
        queue: deque[TreeNode] = deque([root])

        while queue:
            level: list[int] = []
            level_size = len(queue)

            for _ in range(level_size):
                node = queue.popleft()
                level.append(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.append(level)

        return result


# ============================================
# Solution 2: DFS with Depth Tracking
# ============================================
class SolutionDFS:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        Return level-order traversal using DFS with depth tracking.

        Core insight: DFS can achieve level-order by tracking depth. As we
        recurse, we pass the current depth and append to the corresponding
        level list. This demonstrates that level-order doesn't require BFS.

        Invariant: result[depth] contains all values at that depth visited so far.

        Args:
            root: Root of binary tree

        Returns:
            List of lists, where each inner list contains values at that depth
        """
        result: list[list[int]] = []

        def dfs(node: Optional[TreeNode], depth: int) -> None:
            if not node:
                return

            # Extend result if we've reached a new depth
            if depth >= len(result):
                result.append([])

            result[depth].append(node.val)

            # Pre-order: process left before right to maintain left-to-right order
            dfs(node.left, depth + 1)
            dfs(node.right, depth + 1)

        dfs(root, 0)
        return result


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
    result = solver.levelOrder(root)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
