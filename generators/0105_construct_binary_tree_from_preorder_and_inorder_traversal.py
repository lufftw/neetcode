# generators/0105_construct_binary_tree_from_preorder_and_inorder_traversal.py
"""
Test Case Generator for Problem 0105 - Construct Binary Tree from Preorder and Inorder Traversal

LeetCode Constraints:
- 1 <= preorder.length <= 3000
- inorder.length == preorder.length
- -3000 <= preorder[i], inorder[i] <= 3000
- preorder and inorder consist of unique values
"""
import json
import random
from typing import Iterator, Optional, List, Tuple


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Construct Binary Tree."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        ([1], [1]),                          # Single node
        ([1, 2], [2, 1]),                    # Left child only
        ([1, 2], [1, 2]),                    # Right child only
        ([1, 2, 3], [2, 1, 3]),              # Balanced 3 nodes
    ]

    for preorder, inorder in edge_cases:
        yield f"{json.dumps(preorder)}\n{json.dumps(inorder)}"
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random test case by building a random tree."""
    n = random.randint(3, 20)
    preorder, inorder = _generate_traversals(n)
    return f"{json.dumps(preorder)}\n{json.dumps(inorder)}"


def _generate_traversals(n: int) -> Tuple[List[int], List[int]]:
    """Generate preorder and inorder traversals for a random tree."""
    # Generate unique values
    values = random.sample(range(-1000, 1001), n)

    # Build a random tree structure and get traversals
    preorder: List[int] = []
    inorder: List[int] = []

    def build_random_tree(vals: List[int]) -> None:
        if not vals:
            return

        # Pick a random root position
        root_idx = random.randint(0, len(vals) - 1)
        root = vals[root_idx]
        left_vals = vals[:root_idx]
        right_vals = vals[root_idx + 1:]

        preorder.append(root)
        build_random_tree(left_vals)
        build_random_tree(right_vals)

    def build_inorder(vals: List[int]) -> None:
        if not vals:
            return
        root_idx = random.randint(0, len(vals) - 1)
        left_vals = vals[:root_idx]
        right_vals = vals[root_idx + 1:]

        build_inorder(left_vals)
        inorder.append(vals[root_idx])
        build_inorder(right_vals)

    # For simplicity, use inorder = values in some order
    # and build preorder based on a random tree structure
    random.shuffle(values)
    inorder = values.copy()

    # Build preorder from a BST-like structure based on inorder
    def build_preorder_from_inorder(start: int, end: int) -> None:
        if start > end:
            return
        mid = random.randint(start, end)
        preorder.append(inorder[mid])
        build_preorder_from_inorder(start, mid - 1)
        build_preorder_from_inorder(mid + 1, end)

    preorder = []
    build_preorder_from_inorder(0, len(inorder) - 1)

    return preorder, inorder


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with n nodes for complexity estimation.
    """
    n = max(1, min(n, 3000))
    preorder, inorder = _generate_traversals(n)
    return f"{json.dumps(preorder)}\n{json.dumps(inorder)}"


if __name__ == "__main__":
    for i, test in enumerate(generate(3, seed=42), 1):
        print(f"Test {i}:")
        print(test)
        print()
