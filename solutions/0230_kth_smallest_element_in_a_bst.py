# solutions/0230_kth_smallest_element_in_a_bst.py
"""
Problem 0230 - Kth Smallest Element in a BST

Given the root of a binary search tree and an integer k, return the
kth smallest value (1-indexed) of all the values of the nodes in the tree.

LeetCode Constraints:
- The number of nodes in the tree is n
- 1 <= k <= n <= 10^4
- 0 <= Node.val <= 10^4

Key Insight:
BST inorder traversal visits nodes in sorted order.
The k-th visited node during inorder traversal is the answer.

We can stop early once we've found the k-th element, achieving
O(H + k) time where H is tree height.

Solution Approaches:
1. Iterative inorder with stack: O(H + k) time, O(H) space
2. Recursive inorder: O(n) time worst case, O(H) space
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
        "class": "SolutionIterative",
        "method": "kthSmallest",
        "complexity": "O(H + k) time, O(H) space",
        "description": "Iterative inorder with stack, early termination",
    },
    "recursive": {
        "class": "SolutionRecursive",
        "method": "kthSmallest",
        "complexity": "O(n) time, O(H) space",
        "description": "Recursive inorder collecting all elements",
    },
}


class SolutionIterative:
    """
    Iterative inorder traversal with early termination.

    Use a stack to simulate recursion. Push nodes while going left,
    pop and visit, then go right. Count visited nodes until we hit k.

    This is optimal when k is small relative to n, as we only
    traverse the leftmost path (H nodes) plus k-1 more nodes.

    Time: O(H + k) where H is height
    Space: O(H) for the stack
    """

    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        stack: List[TreeNode] = []
        current = root

        while stack or current:
            # Go to leftmost node
            while current:
                stack.append(current)
                current = current.left

            # Visit node (inorder position)
            current = stack.pop()
            k -= 1

            if k == 0:
                return current.val

            # Move to right subtree
            current = current.right

        return -1  # Should never reach here if k is valid


class SolutionRecursive:
    """
    Recursive inorder traversal.

    Collect all values in sorted order, return the k-th one.
    Simple but traverses entire tree even if k is small.

    Could be optimized with early return, but that complicates
    the recursive structure.
    """

    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        def inorder(node: Optional[TreeNode]) -> List[int]:
            if not node:
                return []
            return inorder(node.left) + [node.val] + inorder(node.right)

        return inorder(root)[k - 1]


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

    lines = sys.stdin.read().strip().split("\n")

    values = json.loads(lines[0])
    k = int(lines[1])

    root = _build_tree(values)

    solver = get_solver(SOLUTIONS)
    result = solver.kthSmallest(root, k)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
