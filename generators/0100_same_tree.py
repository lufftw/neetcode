# generators/0100_same_tree.py
"""
Test Case Generator for Problem 0100 - Same Tree

LeetCode Constraints:
- The number of nodes in both trees is in the range [0, 100]
- -10^4 <= Node.val <= 10^4
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Same Tree."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        ([], []),  # Both empty
        ([1], [1]),  # Single node, same
        ([1], [2]),  # Single node, different
        ([1, 2, 3], [1, 2, 3]),  # Same trees
        ([1, 2], [1, None, 2]),  # Different structure
    ]

    for p, q in edge_cases:
        yield f"{json.dumps(p)}\n{json.dumps(q)}"
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate random pair of trees."""
    n = random.randint(3, 20)
    tree1 = _generate_random_tree(n)

    # 50% chance same tree, 50% chance different
    if random.random() < 0.5:
        tree2 = tree1.copy()
    else:
        # Generate different tree or modify tree1
        if random.random() < 0.5:
            tree2 = _generate_random_tree(random.randint(3, 20))
        else:
            # Modify one value
            tree2 = tree1.copy()
            if tree2:
                idx = random.randint(0, len(tree2) - 1)
                while tree2[idx] is None:
                    idx = random.randint(0, len(tree2) - 1)
                tree2[idx] = tree2[idx] + random.choice([-1, 1])

    return f"{json.dumps(tree1)}\n{json.dumps(tree2)}"


def _generate_random_tree(n: int) -> List[Optional[int]]:
    """Generate a random tree as level-order list."""
    if n == 0:
        return []

    tree = [random.randint(-10000, 10000)]
    remaining = n - 1

    i = 0
    while remaining > 0 and i < len(tree):
        if tree[i] is not None:
            # Left child
            if remaining > 0 and random.random() < 0.7:
                tree.append(random.randint(-10000, 10000))
                remaining -= 1
            else:
                tree.append(None)

            # Right child
            if remaining > 0 and random.random() < 0.7:
                tree.append(random.randint(-10000, 10000))
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
        return "[]\n[]"
    tree = _generate_random_tree(n)
    return f"{json.dumps(tree)}\n{json.dumps(tree)}"


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        lines = test.split("\n")
        print(f"Test {i}: p={lines[0][:30]}... q={lines[1][:30]}...")
