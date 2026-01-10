# generators/0226_invert_binary_tree.py
"""
Test Case Generator for Problem 0226 - Invert Binary Tree

LeetCode Constraints:
- The number of nodes in the tree is in the range [0, 100]
- -100 <= Node.val <= 100
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Invert Binary Tree."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        [],  # Empty tree
        [1],  # Single node
        [1, 2],  # Left child only
        [1, None, 2],  # Right child only
        [1, 2, 3],  # Complete 3 nodes
    ]

    for tree in edge_cases:
        yield json.dumps(tree)
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random binary tree."""
    n = random.randint(3, 30)
    tree = _generate_random_tree(n)
    return json.dumps(tree)


def _generate_random_tree(n: int) -> List[Optional[int]]:
    """Generate a random tree as level-order list."""
    if n == 0:
        return []

    tree = [random.randint(-100, 100)]
    remaining = n - 1

    i = 0
    while remaining > 0 and i < len(tree):
        if tree[i] is not None:
            # Left child
            if remaining > 0 and random.random() < 0.7:
                tree.append(random.randint(-100, 100))
                remaining -= 1
            else:
                tree.append(None)

            # Right child
            if remaining > 0 and random.random() < 0.7:
                tree.append(random.randint(-100, 100))
                remaining -= 1
            else:
                tree.append(None)
        i += 1

    # Trim trailing Nones
    while tree and tree[-1] is None:
        tree.pop()

    return tree


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with n nodes for complexity estimation.
    """
    n = max(0, min(n, 100))
    if n == 0:
        return "[]"
    tree = _generate_random_tree(n)
    return json.dumps(tree)


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}: {test}")
