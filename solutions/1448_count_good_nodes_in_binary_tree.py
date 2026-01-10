"""
Problem: Count Good Nodes in Binary Tree
Link: https://leetcode.com/problems/count-good-nodes-in-binary-tree/

Given a binary tree root, a node X in the tree is named good if in the path from
root to X there are no nodes with a value greater than X.

Return the number of good nodes in the binary tree.

Example 1:
    Input: root = [3,1,4,3,null,1,5]
    Output: 4
    Explanation: Root 3 is always good.
                 Node 4 -> (3,4): no node > 4, good.
                 Node 5 -> (3,4,5): no node > 5, good.
                 Node 3 -> (3,1,3): no node > 3, good.

Example 2:
    Input: root = [3,3,null,4,2]
    Output: 3
    Explanation: Node 2 -> (3,3,2) has 3 > 2, not good.

Example 3:
    Input: root = [1]
    Output: 1
    Explanation: Root is always a good node.

Constraints:
- The number of nodes in the binary tree is in the range [1, 10^5].
- Each node's value is between [-10^4, 10^4].

Topics: Tree, Depth-First Search, Breadth-First Search, Binary Tree
"""

import json
from typing import Optional
from collections import deque
from _runner import get_solver


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ============================================================================
# JUDGE_FUNC - exact match for integer count
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    if expected is not None:
        return actual == expected
    return True


JUDGE_FUNC = judge


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionDFS",
        "method": "goodNodes",
        "complexity": "O(n) time, O(h) space",
        "description": "DFS tracking max value from root to current node",
    },
    "bfs": {
        "class": "SolutionBFS",
        "method": "goodNodes",
        "complexity": "O(n) time, O(w) space",
        "description": "BFS level-order traversal with max value tracking",
    },
}


# ============================================================================
# Solution 1: DFS with Max Value Tracking
# Time: O(n), Space: O(h) where h = tree height
#
# Key Insight:
#   A node is "good" if its value >= all values on the path from root to it.
#   Equivalently, node.val >= max value seen so far on the path.
#
# Algorithm:
#   - DFS from root, passing down the maximum value seen on the path
#   - At each node, check if node.val >= max_so_far
#   - If yes, increment count; update max for children
#   - Recurse on left and right subtrees
#
# Why DFS Works:
#   DFS naturally follows root-to-leaf paths. By passing max_so_far as a
#   parameter, each node has O(1) access to path information needed for
#   the "good" check.
# ============================================================================
class SolutionDFS:
    """
    DFS tracking maximum value along path from root.

    The key observation is that we only need to track the maximum value
    seen from root to current node - we don't need the entire path.
    This reduces path tracking to a single integer parameter.
    """

    def goodNodes(self, root: TreeNode) -> int:
        def dfs(node: Optional[TreeNode], max_so_far: int) -> int:
            if not node:
                return 0

            # Check if current node is good
            count = 1 if node.val >= max_so_far else 0

            # Update max for children
            new_max = max(max_so_far, node.val)

            # Recurse on children
            count += dfs(node.left, new_max)
            count += dfs(node.right, new_max)

            return count

        # Root is always good (no ancestors to compare)
        return dfs(root, root.val)


# ============================================================================
# Solution 2: BFS with Max Value Tracking
# Time: O(n), Space: O(w) where w = max width of tree
#
# Key Insight:
#   Same logic as DFS, but using level-order traversal. We need to track
#   the max value from root to each node separately, stored alongside
#   each node in the queue.
#
# Algorithm:
#   - BFS queue stores (node, max_value_on_path_to_node)
#   - For each node, check if it's good, then enqueue children with updated max
#
# Trade-off vs DFS:
#   BFS uses O(width) space vs O(height) for DFS. For balanced trees, width
#   can be O(n/2) vs O(log n) height. DFS is usually more space-efficient.
# ============================================================================
class SolutionBFS:
    """
    BFS level-order traversal with path max tracking.

    Each queue entry carries the maximum value seen on the path from root
    to that node. This allows O(1) checking at each node.
    """

    def goodNodes(self, root: TreeNode) -> int:
        if not root:
            return 0

        count = 0
        # Queue entries: (node, max value on path to this node)
        queue = deque([(root, root.val)])

        while queue:
            node, max_so_far = queue.popleft()

            # Check if current node is good
            if node.val >= max_so_far:
                count += 1

            # Update max for children
            new_max = max(max_so_far, node.val)

            # Enqueue children with updated max
            if node.left:
                queue.append((node.left, new_max))
            if node.right:
                queue.append((node.right, new_max))

        return count


# ============================================================================
# Tree building helper
# ============================================================================
def _build_tree(values: list) -> Optional[TreeNode]:
    """Build binary tree from level-order array representation."""
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


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: root as JSON array (level-order with null for missing nodes)

    Example:
        [3,1,4,3,null,1,5]
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")

    values = json.loads(lines[0])
    root = _build_tree(values)

    solver = get_solver(SOLUTIONS)
    result = solver.goodNodes(root)

    print(result)


if __name__ == "__main__":
    solve()
