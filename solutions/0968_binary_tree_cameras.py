"""
Problem: Binary Tree Cameras
Link: https://leetcode.com/problems/binary-tree-cameras/

You are given the root of a binary tree. We install cameras on the tree nodes
where each camera at a node can monitor its parent, itself, and its immediate
children.

Return the minimum number of cameras needed to monitor all nodes of the tree.

Constraints:
- The number of nodes in the tree is in the range [1, 1000].
- Node.val == 0

Topics: Dynamic Programming, Tree, Depth-First Search, Binary Tree
Pattern: Tree DP - Multi-State (Coverage States)
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


# ============================================================================
# Solution 1: Greedy State Machine
# Time: O(n), Space: O(h) where h = tree height
#   - States: 0=not_covered, 1=covered, 2=has_camera
#   - Place cameras at parents of leaves (not leaves) for efficiency
#   - Any child==0 → place camera; Any child==2 → covered; Else → need parent
# ============================================================================
class SolutionGreedy:
    def minCameraCover(self, root: Optional[TreeNode]) -> int:
        self.camera_count = 0

        # State constants: 0=not_covered, 1=covered, 2=has_camera
        NOT_COVERED, COVERED, HAS_CAMERA = 0, 1, 2

        def coverage_state(node) -> int:
            """
            Returns the coverage state of this node after processing its subtree.
            Side effect: increments camera_count when placing a camera.
            """
            if not node:
                return COVERED  # Null nodes don't need monitoring

            left_state = coverage_state(node.left)
            right_state = coverage_state(node.right)

            # Priority 1: Child needs coverage → must install camera here
            if left_state == NOT_COVERED or right_state == NOT_COVERED:
                self.camera_count += 1
                return HAS_CAMERA

            # Priority 2: Child has camera → this node is already covered
            if left_state == HAS_CAMERA or right_state == HAS_CAMERA:
                return COVERED

            # Both children covered but no camera nearby → need parent's help
            return NOT_COVERED

        # Root has no parent, so if uncovered, must install camera
        if coverage_state(root) == NOT_COVERED:
            self.camera_count += 1

        return self.camera_count


# ============================================================================
# Solution 2: Explicit DP with Three States
# Time: O(n), Space: O(h) where h = tree height
#   - Returns (uncovered_cost, covered_cost, has_camera_cost) per node
#   - More explicit than greedy but same complexity
#   - Root must be covered: answer = min(result[1], result[2])
# ============================================================================
class SolutionDP:
    def minCameraCover(self, root: Optional[TreeNode]) -> int:
        INF = float("inf")

        def min_cameras(node) -> tuple[int, int, int]:
            """
            Returns (uncovered_cost, covered_cost, has_camera_cost)
            for the subtree rooted at node.
            """
            if not node:
                # Null node: "covered" with 0 cameras, can't have camera
                return (0, 0, INF)

            left = min_cameras(node.left)
            right = min_cameras(node.right)

            # State 0: This node not covered, children must be covered
            uncovered = left[1] + right[1]

            # State 1: This node covered by child's camera (no camera here)
            # At least one child must have camera to cover this node
            covered = min(
                left[2] + min(right[1], right[2]),  # left child has camera
                right[2] + min(left[1], left[2]),   # right child has camera
            )

            # State 2: This node has camera (children can be any state)
            has_camera = 1 + min(left) + min(right)

            return (uncovered, covered, has_camera)

        result = min_cameras(root)
        # Root must be covered: either by own camera or child's
        return min(result[1], result[2])


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
