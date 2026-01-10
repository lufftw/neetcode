# solutions/0199_binary_tree_right_side_view.py
"""
Problem 0199 - Binary Tree Right Side View

Given the root of a binary tree, imagine yourself standing on the right side
of it, return the values of the nodes you can see ordered from top to bottom.

LeetCode Constraints:
- The number of nodes in the tree is in the range [0, 100]
- -100 <= Node.val <= 100

Key Insight:
We need the rightmost node at each level of the tree.

BFS approach: Process level by level, track the last node in each level.
DFS approach: Visit right subtree first; first node seen at each depth is rightmost.

Solution Approaches:
1. BFS level-order: O(n) time, O(w) space where w = max width
2. DFS right-first: O(n) time, O(h) space where h = height
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
        "class": "SolutionBFS",
        "method": "rightSideView",
        "complexity": "O(n) time, O(w) space",
        "description": "BFS level-order, collect rightmost node per level",
    },
    "dfs": {
        "class": "SolutionDFS",
        "method": "rightSideView",
        "complexity": "O(n) time, O(h) space",
        "description": "DFS right-first traversal, track first at each depth",
    },
}


class SolutionBFS:
    """
    BFS level-order traversal.

    Process the tree level by level. For each level, the last node
    processed is the rightmost node visible from the right side.

    Use a queue and process all nodes at current level before moving
    to the next level. Track level size to know when level ends.

    Time: O(n) - visit each node once
    Space: O(w) - queue holds at most one level, max width w
    """

    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []

        result: List[int] = []
        queue: deque = deque([root])

        while queue:
            level_size = len(queue)
            rightmost = None

            for _ in range(level_size):
                node = queue.popleft()
                rightmost = node.val  # Keep updating; last one is rightmost

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.append(rightmost)

        return result


class SolutionDFS:
    """
    DFS with right-first traversal.

    Visit right subtree before left. Track the current depth.
    The first node we see at each depth is the rightmost node
    for that level (since we visit right first).

    Compare depth with result length: if depth == len(result),
    this is the first node at this depth, so add it.

    Time: O(n) - visit each node once
    Space: O(h) - recursion stack depth equals tree height
    """

    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        result: List[int] = []

        def dfs(node: Optional[TreeNode], depth: int) -> None:
            if not node:
                return

            # First node at this depth = rightmost (we visit right first)
            if depth == len(result):
                result.append(node.val)

            # Visit right subtree first, then left
            dfs(node.right, depth + 1)
            dfs(node.left, depth + 1)

        dfs(root, 0)
        return result


def _build_tree(values: List[Optional[int]]) -> Optional[TreeNode]:
    """Build tree from level-order list."""
    if not values or values[0] is None:
        return None

    root = TreeNode(values[0])
    queue = deque([root])
    i = 1

    while queue and i < len(values):
        node = queue.popleft()

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

    data = sys.stdin.read().strip()
    values = json.loads(data)

    root = _build_tree(values)

    solver = get_solver(SOLUTIONS)
    result = solver.rightSideView(root)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
