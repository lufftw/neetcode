# solutions/0297_serialize_and_deserialize_binary_tree.py
"""
Problem 0297 - Serialize and Deserialize Binary Tree

Design an algorithm to serialize and deserialize a binary tree.
Serialization is converting a tree to a string.
Deserialization is recovering the tree from the string.

LeetCode Constraints:
- The number of nodes in the tree is in the range [0, 10^4]
- -1000 <= Node.val <= 1000

Key Insight:
A binary tree can be uniquely reconstructed from its pre-order traversal
if we include markers for null children. This is because pre-order visits
the root first, then left subtree, then right subtree.

Using "null" or "N" to mark missing children allows us to know exactly
where one subtree ends and another begins.

Solution Approaches:
1. Pre-order DFS: serialize recursively, deserialize with iterator
2. Level-order BFS: serialize level by level, deserialize using queue
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
        "class": "CodecDFS",
        "method": "_run_operations",
        "complexity": "O(n) time, O(n) space",
        "description": "Pre-order DFS serialization with null markers",
    },
    "bfs": {
        "class": "CodecBFS",
        "method": "_run_operations",
        "complexity": "O(n) time, O(n) space",
        "description": "Level-order BFS serialization",
    },
}


class CodecDFS:
    """
    Pre-order DFS approach.

    Serialize: Visit root, then left, then right.
    Use "N" for null nodes to mark boundaries.

    Deserialize: Process tokens in same pre-order.
    Each call consumes one token, builds node, recurses for children.

    Example: Tree [1,2,3,null,null,4,5]
    Serialize: "1,2,N,N,3,4,N,N,5,N,N"

    The key insight is that pre-order traversal with null markers
    uniquely identifies the tree structure.
    """

    def serialize(self, root: Optional[TreeNode]) -> str:
        """Serialize tree to comma-separated string."""
        tokens: List[str] = []

        def dfs(node: Optional[TreeNode]) -> None:
            if not node:
                tokens.append("N")
                return
            tokens.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(tokens)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        """Deserialize string back to tree."""
        if not data:
            return None

        tokens = iter(data.split(","))

        def dfs() -> Optional[TreeNode]:
            val = next(tokens)
            if val == "N":
                return None
            node = TreeNode(int(val))
            node.left = dfs()
            node.right = dfs()
            return node

        return dfs()

    def _run_operations(
        self, operations: List[str], arguments: List[List]
    ) -> List[Optional[str]]:
        """Test harness: execute operation sequence."""
        results: List[Optional[str]] = [None]  # Constructor returns null

        tree: Optional[TreeNode] = None
        serialized: str = ""

        for op, args in zip(operations[1:], arguments[1:]):
            if op == "serialize":
                # Build tree from input list
                tree = self._build_tree(args[0])
                serialized = self.serialize(tree)
                results.append(serialized)
            elif op == "deserialize":
                # Deserialize and return level-order representation
                restored_tree = self.deserialize(args[0])
                level_order = self._tree_to_list(restored_tree)
                results.append(level_order)
            else:
                results.append(None)

        return results

    def _build_tree(self, values: List[Optional[int]]) -> Optional[TreeNode]:
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

    def _tree_to_list(self, root: Optional[TreeNode]) -> List[Optional[int]]:
        """Convert tree to level-order list."""
        if not root:
            return []

        result: List[Optional[int]] = []
        queue = deque([root])

        while queue:
            node = queue.popleft()
            if node:
                result.append(node.val)
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append(None)

        # Trim trailing nulls
        while result and result[-1] is None:
            result.pop()

        return result


class CodecBFS:
    """
    Level-order BFS approach.

    Serialize: Use BFS queue, output values level by level.
    Use "N" for null nodes.

    Deserialize: Process tokens level by level using queue.
    Each dequeued node gets next two tokens as children.

    Same asymptotic complexity as DFS, but processes nodes
    in breadth-first order rather than depth-first.
    """

    def serialize(self, root: Optional[TreeNode]) -> str:
        """Serialize tree using BFS level-order."""
        if not root:
            return "N"

        tokens: List[str] = []
        queue = deque([root])

        while queue:
            node = queue.popleft()
            if node:
                tokens.append(str(node.val))
                queue.append(node.left)
                queue.append(node.right)
            else:
                tokens.append("N")

        # Trim trailing nulls for cleaner output
        while tokens and tokens[-1] == "N":
            tokens.pop()

        return ",".join(tokens)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        """Deserialize using BFS."""
        if not data or data == "N":
            return None

        tokens = data.split(",")
        root = TreeNode(int(tokens[0]))
        queue = deque([root])
        i = 1

        while queue and i < len(tokens):
            node = queue.popleft()

            # Left child
            if i < len(tokens):
                if tokens[i] != "N":
                    node.left = TreeNode(int(tokens[i]))
                    queue.append(node.left)
                i += 1

            # Right child
            if i < len(tokens):
                if tokens[i] != "N":
                    node.right = TreeNode(int(tokens[i]))
                    queue.append(node.right)
                i += 1

        return root

    def _run_operations(
        self, operations: List[str], arguments: List[List]
    ) -> List[Optional[str]]:
        """Test harness: execute operation sequence."""
        results: List[Optional[str]] = [None]  # Constructor returns null

        for op, args in zip(operations[1:], arguments[1:]):
            if op == "serialize":
                tree = self._build_tree(args[0])
                serialized = self.serialize(tree)
                results.append(serialized)
            elif op == "deserialize":
                restored_tree = self.deserialize(args[0])
                level_order = self._tree_to_list(restored_tree)
                results.append(level_order)
            else:
                results.append(None)

        return results

    def _build_tree(self, values: List[Optional[int]]) -> Optional[TreeNode]:
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

    def _tree_to_list(self, root: Optional[TreeNode]) -> List[Optional[int]]:
        """Convert tree to level-order list."""
        if not root:
            return []

        result: List[Optional[int]] = []
        queue = deque([root])

        while queue:
            node = queue.popleft()
            if node:
                result.append(node.val)
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append(None)

        while result and result[-1] is None:
            result.pop()

        return result


def solve():
    import sys
    import json
    import os

    lines = sys.stdin.read().strip().split("\n")

    operations = json.loads(lines[0])
    arguments = json.loads(lines[1])

    # Determine which solution class to use
    method_key = os.environ.get("_METHOD", "default")
    solution_info = SOLUTIONS.get(method_key, SOLUTIONS["default"])
    class_name = solution_info["class"]
    solver_class = globals()[class_name]

    obj = solver_class()
    result = obj._run_operations(operations, arguments)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
