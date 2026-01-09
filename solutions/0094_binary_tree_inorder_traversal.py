# solutions/0094_binary_tree_inorder_traversal.py
"""
Problem: Binary Tree Inorder Traversal
Link: https://leetcode.com/problems/binary-tree-inorder-traversal/

Given the root of a binary tree, return the inorder traversal of its nodes' values.

Example 1:
    Input: root = [1,null,2,3]
    Output: [1,3,2]

Example 2:
    Input: root = []
    Output: []

Constraints:
- The number of nodes in the tree is in the range [0, 100].
- -100 <= Node.val <= 100

Topics: Stack, Tree, Depth-First Search, Binary Tree
"""
from typing import List, Optional
from _runner import get_solver


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Inorder Traversal solution."""
    if expected is not None:
        return actual == expected
    return True  # Trust actual for tree problems


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionRecursive",
        "method": "inorderTraversal",
        "complexity": "O(n) time, O(h) space",
        "description": "Recursive DFS inorder traversal",
        "api_kernels": ["TreeTraversalDFS"],
        "patterns": ["tree_dfs_inorder"],
    },
    "recursive": {
        "class": "SolutionRecursive",
        "method": "inorderTraversal",
        "complexity": "O(n) time, O(h) space",
        "description": "Recursive DFS, natural Left-Node-Right order",
    },
    "iterative": {
        "class": "SolutionIterative",
        "method": "inorderTraversal",
        "complexity": "O(n) time, O(h) space",
        "description": "Iterative with explicit stack",
        "api_kernels": ["TreeTraversalDFS"],
        "patterns": ["tree_dfs_iterative"],
    },
    "morris": {
        "class": "SolutionMorris",
        "method": "inorderTraversal",
        "complexity": "O(n) time, O(1) space",
        "description": "Morris traversal using threaded binary tree",
    },
}


# ============================================
# Solution 1: Recursive DFS
# ============================================
class SolutionRecursive:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        """
        Return inorder traversal of binary tree nodes.

        Core insight: Inorder visits Left → Node → Right. For BST, this produces
        sorted order. Recursion naturally handles the ordering — fully process
        left subtree before visiting current node.

        Invariant: When visiting a node, its entire left subtree has been processed.

        Args:
            root: Root of binary tree

        Returns:
            List of node values in inorder sequence
        """
        result: list[int] = []

        def dfs(node: Optional[TreeNode]) -> None:
            if not node:
                return
            dfs(node.left)
            result.append(node.val)
            dfs(node.right)

        dfs(root)
        return result


# ============================================
# Solution 2: Iterative with Stack
# ============================================
class SolutionIterative:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        """Iterative inorder using explicit stack."""
        result: list[int] = []
        stack: list[TreeNode] = []
        curr = root

        while curr or stack:
            while curr:
                stack.append(curr)
                curr = curr.left

            curr = stack.pop()
            result.append(curr.val)
            curr = curr.right

        return result


# ============================================
# Solution 3: Morris Traversal (O(1) Space)
# ============================================
class SolutionMorris:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        """
        Inorder traversal using Morris algorithm (threaded binary tree).

        Core insight: Use the null right pointers of predecessors to create
        temporary links back to the current node. This eliminates the need
        for a stack, achieving O(1) space.

        Algorithm:
        1. If no left child: visit node, go right
        2. If left child exists: find inorder predecessor (rightmost in left subtree)
           - If predecessor.right is null: create thread, go left
           - If predecessor.right points to curr: remove thread, visit node, go right

        Trade-off: O(1) space but modifies tree temporarily (restored after).

        Args:
            root: Root of binary tree

        Returns:
            List of node values in inorder sequence
        """
        result: List[int] = []
        curr = root

        while curr:
            if not curr.left:
                # No left subtree: visit and go right
                result.append(curr.val)
                curr = curr.right
            else:
                # Find inorder predecessor (rightmost node in left subtree)
                predecessor = curr.left
                while predecessor.right and predecessor.right != curr:
                    predecessor = predecessor.right

                if not predecessor.right:
                    # Create thread: predecessor -> current
                    predecessor.right = curr
                    curr = curr.left
                else:
                    # Thread exists: we've returned via thread
                    # Remove thread, visit current, go right
                    predecessor.right = None
                    result.append(curr.val)
                    curr = curr.right

        return result


def _build_tree(values: list) -> Optional[TreeNode]:
    """Build tree from level-order list."""
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
    result = solver.inorderTraversal(root)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
