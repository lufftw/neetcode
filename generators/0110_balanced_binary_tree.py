# generators/0110_balanced_binary_tree.py
"""
Test Case Generator for Problem 0110 - Balanced Binary Tree

LeetCode Constraints:
- The number of nodes in the tree is in the range [0, 5000]
- -10^4 <= Node.val <= 10^4
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Balanced Binary Tree.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Level-order tree representation in JSON format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first - mix of balanced and unbalanced
    edge_cases = [
        [],  # Empty tree (balanced)
        [1],  # Single node (balanced)
        [3, 9, 20, None, None, 15, 7],  # Example 1 (balanced)
        [1, 2, 2, 3, 3, None, None, 4, 4],  # Example 2 (unbalanced)
        [1, 2, 3, 4, 5, 6, 7],  # Perfect tree (balanced)
        [1, 2, None, 3, None, None, None, 4],  # Left-skewed (unbalanced)
        [1, None, 2, None, 3],  # Right-skewed (unbalanced)
        [1, 2, 3],  # Complete tree (balanced)
    ]

    for tree in edge_cases:
        yield json.dumps(tree, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases - mix of balanced and unbalanced
    for _ in range(count):
        if random.random() > 0.5:
            yield _generate_balanced_tree()
        else:
            yield _generate_unbalanced_tree()


def _generate_balanced_tree() -> str:
    """Generate a balanced binary tree."""
    n = random.randint(1, 63)  # Up to 6 levels
    result: List[Optional[int]] = []

    # Build a nearly complete tree for balance
    for i in range(n):
        result.append(random.randint(-10000, 10000))

    # Randomly remove some leaf nodes while maintaining balance
    if len(result) > 7:
        # Only remove from the last level
        last_level_start = (len(result) + 1) // 2 - 1
        for i in range(last_level_start, len(result)):
            if random.random() > 0.7:
                result[i] = None

    # Trim trailing nulls
    while result and result[-1] is None:
        result.pop()

    return json.dumps(result, separators=(',', ':'))


def _generate_unbalanced_tree() -> str:
    """Generate an unbalanced binary tree."""
    depth = random.randint(4, 8)
    result: List[Optional[int]] = [random.randint(-10000, 10000)]

    # Create a long path on one side
    side = random.choice(['left', 'right'])
    current_level = [0]

    for _ in range(depth - 1):
        new_level = []
        for idx in current_level:
            # Extend result to accommodate children
            while len(result) <= 2 * idx + 2:
                result.append(None)

            if side == 'left':
                result[2 * idx + 1] = random.randint(-10000, 10000)
                new_level.append(2 * idx + 1)
            else:
                result[2 * idx + 2] = random.randint(-10000, 10000)
                new_level.append(2 * idx + 2)

        current_level = new_level

    # Trim trailing nulls
    while result and result[-1] is None:
        result.pop()

    return json.dumps(result, separators=(',', ':'))


def _generate_case() -> str:
    """Generate a single random binary tree."""
    if random.random() > 0.5:
        return _generate_balanced_tree()
    return _generate_unbalanced_tree()


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size.

    Args:
        n: Number of nodes

    Returns:
        str: Level-order tree with n nodes
    """
    n = max(0, min(5000, n))
    if n == 0:
        return json.dumps([], separators=(',', ':'))

    # Generate a balanced tree of appropriate size
    result: List[Optional[int]] = []
    for i in range(n):
        result.append(random.randint(-10000, 10000))

    # Trim trailing nulls
    while result and result[-1] is None:
        result.pop()

    return json.dumps(result, separators=(',', ':'))
