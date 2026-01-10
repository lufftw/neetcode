# generators/0230_kth_smallest_element_in_a_bst.py
"""
Test Case Generator for Problem 0230 - Kth Smallest Element in a BST

LeetCode Constraints:
- The number of nodes in the tree is n
- 1 <= k <= n <= 10^4
- 0 <= Node.val <= 10^4
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Kth Smallest Element in BST."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        ([1], 1),                    # Single node
        ([2, 1], 1),                 # Two nodes, find smallest
        ([1, None, 2], 2),           # Two nodes, find largest
        ([2, 1, 3], 2),              # Balanced 3 nodes, find middle
    ]

    for tree, k in edge_cases:
        yield f"{json.dumps(tree)}\n{k}"
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random BST test case."""
    n = random.randint(3, 20)
    values = random.sample(range(1, 1001), n)

    # Build BST and get level-order representation
    tree = _build_bst_level_order(values)
    k = random.randint(1, n)

    return f"{json.dumps(tree)}\n{k}"


def _build_bst_level_order(values: List[int]) -> List[Optional[int]]:
    """Build a BST from values and return level-order representation."""
    if not values:
        return []

    class Node:
        def __init__(self, val):
            self.val = val
            self.left = None
            self.right = None

    def insert(root, val):
        if not root:
            return Node(val)
        if val < root.val:
            root.left = insert(root.left, val)
        else:
            root.right = insert(root.right, val)
        return root

    root = None
    for val in values:
        root = insert(root, val)

    # Convert to level-order list
    from collections import deque
    result = []
    queue = deque([root])

    while queue:
        node = queue.popleft()
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)

    # Trim trailing Nones
    while result and result[-1] is None:
        result.pop()

    return result


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with n nodes for complexity estimation.
    """
    n = max(1, min(n, 10000))
    values = random.sample(range(1, 100001), n)
    tree = _build_bst_level_order(values)
    k = random.randint(1, n)

    return f"{json.dumps(tree)}\n{k}"


if __name__ == "__main__":
    for i, test in enumerate(generate(3, seed=42), 1):
        print(f"Test {i}:")
        print(test)
        print()
