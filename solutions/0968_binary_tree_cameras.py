"""
LeetCode 968: Binary Tree Cameras
https://leetcode.com/problems/binary-tree-cameras/

You are given the root of a binary tree. We install cameras on the tree nodes
where each camera at a node can monitor its parent, itself, and its immediate
children.

Return the minimum number of cameras needed to monitor all nodes of the tree.

Pattern: Tree DP - Multi-State
API Kernel: TreeDP
"""

import json
import sys
from typing import Optional

SOLUTIONS = {
    "default": {
        "class": "SolutionGreedy",
        "method": "minCameraCover",
        "complexity": "O(n) time, O(h) space",
        "description": "Greedy with state machine",
    },
    "dp": {
        "class": "SolutionDP",
        "method": "minCameraCover",
        "complexity": "O(n) time, O(h) space",
        "description": "Full DP with 3 states",
    },
}


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(values):
    """Build tree from level-order list representation."""
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


def judge(actual, expected, input_data: str) -> bool:
    """Validate result using reference implementation."""
    lines = input_data.strip().split("\n")
    values = json.loads(lines[0])

    root = build_tree(values)
    correct = _reference_cameras(root)

    try:
        actual_val = int(actual) if not isinstance(actual, int) else actual
        return actual_val == correct
    except (ValueError, TypeError):
        return False


def _reference_cameras(root) -> int:
    """Reference implementation using greedy."""
    cameras = 0

    def dfs(node):
        nonlocal cameras

        if not node:
            return 1  # null is "covered"

        left = dfs(node.left)
        right = dfs(node.right)

        if left == 0 or right == 0:
            cameras += 1
            return 2

        if left == 2 or right == 2:
            return 1

        return 0

    if dfs(root) == 0:
        cameras += 1

    return cameras


JUDGE_FUNC = judge


class SolutionGreedy:
    """
    Greedy Approach with State Machine:

    States:
    - 0: NOT COVERED (needs camera from parent)
    - 1: COVERED (by child's camera)
    - 2: HAS CAMERA

    Strategy: Place cameras at parents of leaves (not at leaves).
    This greedy is optimal because each camera covers at most 3 levels.

    Transitions:
    - If any child is not covered (0) → must place camera (return 2)
    - If any child has camera (2) → this node is covered (return 1)
    - Otherwise → not covered (return 0)

    Time: O(n)
    Space: O(h) for recursion stack
    """

    def minCameraCover(self, root: Optional[TreeNode]) -> int:
        self.cameras = 0

        def dfs(node):
            if not node:
                return 1  # Null nodes are considered "covered"

            left = dfs(node.left)
            right = dfs(node.right)

            # If any child is not covered, must place camera here
            if left == 0 or right == 0:
                self.cameras += 1
                return 2  # Has camera

            # If any child has camera, this node is covered
            if left == 2 or right == 2:
                return 1  # Covered

            # Both children covered, no camera nearby
            return 0  # Not covered, needs parent

        # Handle root specially
        if dfs(root) == 0:
            self.cameras += 1

        return self.cameras


class SolutionDP:
    """
    Full DP Approach with Explicit States:

    For each node, compute minimum cameras for 3 scenarios:
    - s0: node is not covered (but subtree is covered)
    - s1: node is covered (by child's camera), no camera here
    - s2: node has camera

    More explicit than greedy but same complexity.

    Time: O(n)
    Space: O(h)
    """

    def minCameraCover(self, root: Optional[TreeNode]) -> int:
        INF = float("inf")

        def dfs(node):
            # Returns (s0, s1, s2)
            # s0: not covered, s1: covered no camera, s2: has camera
            if not node:
                return (0, 0, INF)  # null: covered, no camera needed

            left = dfs(node.left)
            right = dfs(node.right)

            # s0: This node not covered
            # Children must be covered (s1 or s2)
            s0 = left[1] + right[1]

            # s1: This node covered by child's camera (no camera here)
            # At least one child has camera (s2)
            # Both children must be covered (s1 or s2)
            s1 = min(
                left[2] + min(right[1], right[2]),  # left has camera
                right[2] + min(left[1], left[2]),  # right has camera
            )

            # s2: This node has camera
            # Children can be anything (camera covers them)
            s2 = 1 + min(left) + min(right)

            return (s0, s1, s2)

        result = dfs(root)
        return min(result[1], result[2])  # Root must be covered


def solve():
    """
    Input format (JSON per line):
        Line 1: tree as level-order JSON array

    Output format:
        Integer - minimum number of cameras
    """
    lines = sys.stdin.read().strip().split("\n")
    values = json.loads(lines[0])

    root = build_tree(values)

    from _runner import get_solver

    solver = get_solver(SOLUTIONS)
    result = solver.minCameraCover(root)

    print(result)


if __name__ == "__main__":
    solve()
