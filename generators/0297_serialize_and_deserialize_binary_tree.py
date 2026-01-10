# generators/0297_serialize_and_deserialize_binary_tree.py
"""
Test Case Generator for Problem 0297 - Serialize and Deserialize Binary Tree

LeetCode Constraints:
- The number of nodes in the tree is in the range [0, 10^4]
- -1000 <= Node.val <= 1000
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Serialize and Deserialize Binary Tree."""
    if seed is not None:
        random.seed(seed)

    # Edge cases - using pre-order DFS serialization format
    edge_cases = [
        [],                           # Empty tree
        [1],                          # Single node
        [1, 2, 3],                    # Simple tree
        [1, None, 2],                 # Skewed right
        [1, 2, None],                 # Skewed left
    ]

    for tree in edge_cases:
        # Create test with serialize and deserialize operations
        serialized = _serialize_dfs(tree)
        ops = ["Codec", "serialize", "deserialize"]
        args = [[], [tree], [serialized]]
        yield f"{json.dumps(ops)}\n{json.dumps(args)}"
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _serialize_dfs(tree_list: List[Optional[int]]) -> str:
    """Serialize tree list to DFS format."""
    if not tree_list or tree_list[0] is None:
        return "N"

    # Build tree from list first
    from collections import deque

    class Node:
        def __init__(self, val):
            self.val = val
            self.left = None
            self.right = None

    root = Node(tree_list[0])
    queue = deque([root])
    i = 1

    while queue and i < len(tree_list):
        node = queue.popleft()

        if i < len(tree_list) and tree_list[i] is not None:
            node.left = Node(tree_list[i])
            queue.append(node.left)
        i += 1

        if i < len(tree_list) and tree_list[i] is not None:
            node.right = Node(tree_list[i])
            queue.append(node.right)
        i += 1

    # Serialize using pre-order DFS
    tokens = []

    def dfs(node):
        if not node:
            tokens.append("N")
            return
        tokens.append(str(node.val))
        dfs(node.left)
        dfs(node.right)

    dfs(root)
    return ",".join(tokens)


def _generate_random_case() -> str:
    """Generate a random test case."""
    # Generate random tree as level-order list
    num_nodes = random.randint(1, 20)
    tree_list = []

    # Start with root
    tree_list.append(random.randint(-1000, 1000))
    nodes_to_add = num_nodes - 1

    i = 0
    while nodes_to_add > 0 and i < len(tree_list):
        # For each existing node, potentially add left and right children
        if tree_list[i] is not None:
            # Left child
            if nodes_to_add > 0 and random.random() < 0.7:
                tree_list.append(random.randint(-1000, 1000))
                nodes_to_add -= 1
            else:
                tree_list.append(None)

            # Right child
            if nodes_to_add > 0 and random.random() < 0.7:
                tree_list.append(random.randint(-1000, 1000))
                nodes_to_add -= 1
            else:
                tree_list.append(None)
        i += 1

    # Trim trailing Nones
    while tree_list and tree_list[-1] is None:
        tree_list.pop()

    serialized = _serialize_dfs(tree_list)
    ops = ["Codec", "serialize", "deserialize"]
    args = [[], [tree_list], [serialized]]
    return f"{json.dumps(ops)}\n{json.dumps(args)}"


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with n nodes for complexity estimation.
    """
    n = max(1, min(n, 10000))

    # Generate a balanced-ish tree
    tree_list = []
    for i in range(n):
        tree_list.append(random.randint(-1000, 1000))

    serialized = _serialize_dfs(tree_list)
    ops = ["Codec", "serialize", "deserialize"]
    args = [[], [tree_list], [serialized]]
    return f"{json.dumps(ops)}\n{json.dumps(args)}"


if __name__ == "__main__":
    for i, test in enumerate(generate(3, seed=42), 1):
        print(f"Test {i}:")
        print(test)
        print()
