"""
Test Generator for LeetCode 337: House Robber III
https://leetcode.com/problems/house-robber-iii/

Generates random binary trees for testing tree DP.

Constraints:
- 1 <= n <= 10^4
- 0 <= Node.val <= 10^4
"""

import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test cases for House Robber III.

    Each test case is a JSON array representing tree in level-order.
    """
    if seed is not None:
        random.seed(seed)

    for i in range(count):
        if i == 0:
            # Edge case: single node
            tree = [3]
        elif i == 1:
            # Edge case: two nodes
            tree = [3, 2, None]
        elif i == 2:
            # Example from problem
            tree = [3, 2, 3, None, 3, None, 1]
        elif i == 3:
            # Example 2 from problem
            tree = [3, 4, 5, 1, 3, None, 1]
        elif i == 4:
            # Linear tree (worst case for naive recursion)
            tree = [1, 2, None, 3, None, 4, None, 5]
        else:
            # Random tree
            n = random.randint(3, 30)
            tree = _generate_random_tree(n)

        yield json.dumps(tree)


def _generate_random_tree(n: int) -> list:
    """Generate a random binary tree with approximately n nodes."""
    if n <= 0:
        return []

    # Start with root
    tree = [random.randint(0, 100)]
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
                    next_level.append(random.randint(0, 100))
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
