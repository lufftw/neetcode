"""
Problem: House Robber III
Link: https://leetcode.com/problems/house-robber-iii/

The thief has found himself a new place for his thievery again. There is only
one entrance to this area, called root.

Besides the root, each house has one and only one parent house. After a tour,
the smart thief realized that all houses in this place form a binary tree.
It will automatically contact the police if two directly-linked houses were
broken into on the same night.

Given the root of the binary tree, return the maximum amount of money the
thief can rob without alerting the police.

Constraints:
- The number of nodes in the tree is in the range [1, 10^4].
- 0 <= Node.val <= 10^4

Topics: Dynamic Programming, Tree, Depth-First Search, Binary Tree
Pattern: Tree DP - Include/Exclude (Base Template)
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


# ============================================================================
# Solution 1: Include/Exclude Tree DP
# Time: O(n), Space: O(h) where h = tree height
#   - Each node returns (rob_profit, skip_profit) tuple
#   - Rob this node → must skip children; Skip → children free choice
#   - Post-order traversal ensures children resolved before parent
# ============================================================================
class SolutionDP:
    def rob(self, root: Optional[TreeNode]) -> int:
        def postorder(node) -> tuple[int, int]:
            if not node:
                return (0, 0)

            left_rob, left_skip = postorder(node.left)
            right_rob, right_skip = postorder(node.right)

            rob_profit = node.val + left_skip + right_skip
            skip_profit = max(left_rob, left_skip) + max(right_rob, right_skip)

            return (rob_profit, skip_profit)

        rob_root, skip_root = postorder(root)
        return max(rob_root, skip_root)


# ============================================================================
# Solution 2: Top-Down Memoization
# Time: O(n), Space: O(n) for memo dictionary
#   - Pass "can_rob" flag downward based on parent's choice
#   - Memoize by (node_id, can_rob) to avoid recomputation
#   - Higher memory than Solution 1 but more intuitive flow
# ============================================================================
class SolutionMemo:
    def rob(self, root: Optional[TreeNode]) -> int:
        memo = {}

        def max_profit(node, can_rob: bool) -> int:
            if not node:
                return 0

            cache_key = (id(node), can_rob)
            if cache_key in memo:
                return memo[cache_key]

            profit_skip = max_profit(node.left, True) + max_profit(node.right, True)

            if can_rob:
                profit_rob = node.val + max_profit(node.left, False) + max_profit(node.right, False)
                best = max(profit_skip, profit_rob)
            else:
                best = profit_skip

            memo[cache_key] = best
            return best

        return max_profit(root, can_rob=True)


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
