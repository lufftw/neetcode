# generators/0572_subtree_of_another_tree.py
"""
Test Case Generator for Problem 0572 - Subtree of Another Tree

LeetCode Constraints:
- The number of nodes in root is in the range [1, 2000]
- The number of nodes in subRoot is in the range [1, 1000]
- -10^4 <= root.val <= 10^4
- -10^4 <= subRoot.val <= 10^4
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Subtree of Another Tree."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        ([1], [1]),                            # Both single node, equal
        ([1, 2], [2]),                         # subRoot is leaf
        ([1, 2, 3], [2]),                      # Simple match
        ([1, 2, 3], [4]),                      # No match
        ([1, 1], [1]),                         # Duplicate values
    ]

    for root, sub in edge_cases:
        yield f"{json.dumps(root)}\n{json.dumps(sub)}"
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random test case."""
    # Generate root tree
    root_size = random.randint(5, 30)
    root_tree = _generate_random_tree(root_size)

    # Generate subRoot - either a subtree of root or a random tree
    if random.random() < 0.5:
        # Generate random tree that may or may not be subtree
        sub_size = random.randint(1, min(10, root_size))
        sub_tree = _generate_random_tree(sub_size)
    else:
        # Take a subtree from root
        sub_tree = _extract_subtree(root_tree)

    return f"{json.dumps(root_tree)}\n{json.dumps(sub_tree)}"


def _generate_random_tree(size: int) -> List[Optional[int]]:
    """Generate a random tree as level-order list."""
    if size == 0:
        return []

    tree = [random.randint(-100, 100)]
    remaining = size - 1

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


def _extract_subtree(tree: List[Optional[int]]) -> List[Optional[int]]:
    """Extract a random subtree from given tree."""
    if not tree:
        return [random.randint(-100, 100)]

    # Pick a random non-null node as subtree root
    non_null = [i for i, v in enumerate(tree) if v is not None]
    if not non_null:
        return [random.randint(-100, 100)]

    # For simplicity, just return single node or small subtree
    idx = random.choice(non_null)
    return [tree[idx]]


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with approximately n total nodes.
    """
    n = max(2, min(n, 3000))
    root_size = n * 2 // 3
    sub_size = n // 3

    root_tree = _generate_random_tree(root_size)
    sub_tree = _generate_random_tree(sub_size)

    return f"{json.dumps(root_tree)}\n{json.dumps(sub_tree)}"


if __name__ == "__main__":
    for i, test in enumerate(generate(3, seed=42), 1):
        print(f"Test {i}:")
        print(test)
        print()
