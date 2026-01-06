"""
Test Generator for LeetCode 968: Binary Tree Cameras
https://leetcode.com/problems/binary-tree-cameras/

Generates random binary trees for testing camera coverage.

Constraints:
- 1 <= n <= 1000
- Node.val == 0 (values don't matter for this problem)
"""

import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test cases for Binary Tree Cameras.

    Each test case is a JSON array representing tree in level-order.
    """
    if seed is not None:
        random.seed(seed)

    for i in range(count):
        if i == 0:
            # Edge case: single node (needs 1 camera)
            tree = [0]
        elif i == 1:
            # Edge case: two nodes (needs 1 camera)
            tree = [0, 0, None]
        elif i == 2:
            # Example from problem: 3 nodes linear
            tree = [0, 0, None, 0, None]
        elif i == 3:
            # Perfect binary tree of depth 2 (needs 1 camera at root)
            tree = [0, 0, 0]
        elif i == 4:
            # Perfect binary tree of depth 3
            tree = [0, 0, 0, 0, 0, 0, 0]
        else:
            # Random tree
            n = random.randint(3, 30)
            tree = _generate_random_tree(n)

        yield json.dumps(tree)


def _generate_random_tree(n: int) -> list:
    """Generate a random binary tree with approximately n nodes."""
    if n <= 0:
        return []

    # All values are 0 for this problem
    tree = [0]
    nodes_added = 1
    level_start = 0
    level_size = 1

    while nodes_added < n:
        next_level = []
        for i in range(level_start, level_start + level_size):
            if i >= len(tree) or tree[i] is None:
                next_level.extend([None, None])
                continue

            # Randomly decide children
            for _ in range(2):
                if nodes_added < n and random.random() < 0.7:
                    next_level.append(0)
                    nodes_added += 1
                else:
                    next_level.append(None)

        tree.extend(next_level)
        level_start += level_size
        level_size = len(next_level)

        if all(x is None for x in next_level):
            break

    # Trim trailing Nones
    while tree and tree[-1] is None:
        tree.pop()

    return tree


def generate_for_complexity(n: int) -> str:
    """Generate test case with n nodes for complexity estimation."""
    random.seed(42)
    tree = _generate_random_tree(n)
    return json.dumps(tree)


if __name__ == "__main__":
    for i, test_input in enumerate(generate(5, seed=42)):
        print(f"Test case {i + 1}:")
        print(test_input)
        print()
