# generators/0102_binary_tree_level_order_traversal.py
"""
Test Case Generator for Problem 0102 - Binary Tree Level Order Traversal

LeetCode Constraints:
- The number of nodes in the tree is in the range [0, 2000]
- -1000 <= Node.val <= 1000
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Binary Tree Level Order Traversal.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Level-order tree representation in JSON format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [],  # Empty tree
        [1],  # Single node
        [3, 9, 20, None, None, 15, 7],  # Example 1
        [1, 2, 3, 4, 5, 6, 7],  # Perfect binary tree
        [1, 2, None, 3, None, None, None, 4],  # Left-skewed
        [1, None, 2, None, 3],  # Right-skewed
    ]

    for tree in edge_cases:
        yield json.dumps(tree, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random binary tree."""
    n = random.randint(1, 100)
    return _build_random_tree(n, -1000, 1000)


def _build_random_tree(n: int, min_val: int = -1000, max_val: int = 1000) -> str:
    """Build a random binary tree with n nodes in level-order format."""
    if n == 0:
        return json.dumps([], separators=(',', ':'))

    result: List[Optional[int]] = [random.randint(min_val, max_val)]
    nodes_added = 1
    i = 0

    while nodes_added < n and i < len(result):
        if result[i] is not None:
            # Add left child
            if nodes_added < n and random.random() > 0.3:
                result.append(random.randint(min_val, max_val))
                nodes_added += 1
            else:
                result.append(None)

            # Add right child
            if nodes_added < n and random.random() > 0.3:
                result.append(random.randint(min_val, max_val))
                nodes_added += 1
            else:
                result.append(None)
        i += 1

    # Fill remaining if needed
    while nodes_added < n:
        for j in range(len(result)):
            if result[j] is None and nodes_added < n:
                result[j] = random.randint(min_val, max_val)
                nodes_added += 1

    # Trim trailing nulls
    while result and result[-1] is None:
        result.pop()

    return json.dumps(result, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size.

    Args:
        n: Number of nodes

    Returns:
        str: Level-order tree with n nodes
    """
    n = max(0, min(2000, n))
    return _build_random_tree(n)
