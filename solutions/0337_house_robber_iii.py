"""
LeetCode 337: House Robber III
https://leetcode.com/problems/house-robber-iii/

The thief has found himself a new place for his thievery again. There is only
one entrance to this area, called root.

Besides the root, each house has one and only one parent house. After a tour,
the smart thief realized that all houses in this place form a binary tree.
It will automatically contact the police if two directly-linked houses were
broken into on the same night.

Given the root of the binary tree, return the maximum amount of money the
thief can rob without alerting the police.

Pattern: Tree DP - Include/Exclude
API Kernel: TreeDP
"""

import json
import sys
from typing import Optional

SOLUTIONS = {
    "default": {
        "class": "SolutionDP",
        "method": "rob",
        "complexity": "O(n) time, O(h) space",
        "description": "Tree DP with include/exclude states",
    },
    "memo": {
        "class": "SolutionMemo",
        "method": "rob",
        "complexity": "O(n) time, O(n) space",
        "description": "Memoization approach",
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
    correct = _reference_rob(root)

    try:
        actual_val = int(actual) if not isinstance(actual, int) else actual
        return actual_val == correct
    except (ValueError, TypeError):
        return False


def _reference_rob(root) -> int:
    """Reference implementation using tree DP."""

    def dfs(node):
        if not node:
            return (0, 0)  # (include, exclude)

        left = dfs(node.left)
        right = dfs(node.right)

        include = node.val + left[1] + right[1]
        exclude = max(left) + max(right)

        return (include, exclude)

    return max(dfs(root))


JUDGE_FUNC = judge


class SolutionDP:
    """
    Tree DP Approach:
    - For each node, compute two values:
      1. Max if we include (rob) this node
      2. Max if we exclude (skip) this node
    - Include: can't include children → add children's exclude values
    - Exclude: children are free → add max of each child's states

    Time: O(n) - visit each node once
    Space: O(h) - recursion stack (h = tree height)
    """

    def rob(self, root: Optional[TreeNode]) -> int:
        def dfs(node):
            if not node:
                return (0, 0)  # (with_node, without_node)

            left = dfs(node.left)
            right = dfs(node.right)

            # If we rob this house, can't rob children
            with_current = node.val + left[1] + right[1]

            # If we skip this house, each child is independent
            without_current = max(left) + max(right)

            return (with_current, without_current)

        return max(dfs(root))


class SolutionMemo:
    """
    Memoization Approach:
    - Recursive with caching
    - For each node, compute max robbery with/without including it

    Time: O(n)
    Space: O(n) for memo dict
    """

    def rob(self, root: Optional[TreeNode]) -> int:
        memo = {}

        def dfs(node, can_rob):
            if not node:
                return 0

            key = (id(node), can_rob)
            if key in memo:
                return memo[key]

            # Skip this node
            skip = dfs(node.left, True) + dfs(node.right, True)

            if can_rob:
                # Rob this node (children can't be robbed)
                rob_it = node.val + dfs(node.left, False) + dfs(node.right, False)
                result = max(skip, rob_it)
            else:
                result = skip

            memo[key] = result
            return result

        return dfs(root, True)


def solve():
    """
    Input format (JSON per line):
        Line 1: tree as level-order JSON array

    Output format:
        Integer - maximum amount that can be robbed
    """
    lines = sys.stdin.read().strip().split("\n")
    values = json.loads(lines[0])

    root = build_tree(values)

    from _runner import get_solver

    solver = get_solver(SOLUTIONS)
    result = solver.rob(root)

    print(result)


if __name__ == "__main__":
    solve()
