# generators/0124_binary_tree_maximum_path_sum.py
"""
Test Case Generator for Problem 0124 - Binary Tree Maximum Path Sum

LeetCode Constraints:
- The number of nodes in the tree is in the range [1, 3 * 10^4]
- -1000 <= Node.val <= 1000
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Binary Tree Maximum Path Sum.

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
        [1],  # Single node
        [1, 2, 3],  # Example 1 (sum = 6)
        [-10, 9, 20, None, None, 15, 7],  # Example 2 (sum = 42)
        [-3],  # Single negative node
        [-1, -2, -3],  # All negative
        [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1],  # Complex
        [1, -2, 3],  # Mix of positive and negative
        [2, -1],  # Skip negative subtree
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
    return _build_random_tree(n)


def _build_random_tree(n: int) -> str:
    """Build a random binary tree with n nodes in level-order format."""
    if n == 0:
        return json.dumps([0], separators=(',', ':'))  # At least 1 node required

    result: List[Optional[int]] = [random.randint(-1000, 1000)]
    nodes_added = 1
    i = 0

    while nodes_added < n and i < len(result):
        if result[i] is not None:
            # Add left child
            if nodes_added < n and random.random() > 0.3:
                result.append(random.randint(-1000, 1000))
                nodes_added += 1
            else:
                result.append(None)

            # Add right child
            if nodes_added < n and random.random() > 0.3:
                result.append(random.randint(-1000, 1000))
                nodes_added += 1
            else:
                result.append(None)
        i += 1

    # Fill remaining if needed
    while nodes_added < n:
        for j in range(len(result)):
            if result[j] is None and nodes_added < n:
                result[j] = random.randint(-1000, 1000)
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
    n = max(1, min(30000, n))  # At least 1 node required
    return _build_random_tree(n)
