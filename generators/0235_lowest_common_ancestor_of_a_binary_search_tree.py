# generators/0235_lowest_common_ancestor_of_a_binary_search_tree.py
"""
Test Case Generator for Problem 0235 - Lowest Common Ancestor of a Binary Search Tree

LeetCode Constraints:
- The number of nodes in the tree is in the range [2, 10^5]
- -10^9 <= Node.val <= 10^9
- All node values are unique
- p != q
- p and q will exist in the BST
"""
import json
import random
from typing import Iterator, Optional, List, Tuple


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Lowest Common Ancestor of a BST."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        ([2, 1], 2, 1),  # Minimal BST, root is LCA
        ([2, 1, 3], 1, 3),  # Root is split point
        ([5, 3, 7, 2, 4, 6, 8], 2, 4),  # LCA is internal node
        ([5, 3, 7, 2, 4, 6, 8], 6, 8),  # LCA is internal node (right subtree)
    ]

    for tree, p, q in edge_cases:
        yield f"{json.dumps(tree)}\n{p}\n{q}"
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random BST with two distinct nodes."""
    n = random.randint(5, 50)
    tree, values = _generate_random_bst(n)

    # Pick two distinct values from the tree
    p, q = random.sample(values, 2)

    return f"{json.dumps(tree)}\n{p}\n{q}"


def _generate_random_bst(n: int) -> Tuple[List[Optional[int]], List[int]]:
    """
    Generate a random BST as level-order list.
    Returns (tree_list, list_of_values).
    """
    if n == 0:
        return [], []

    # Generate n unique values and shuffle for insertion order
    values = random.sample(range(-10**6, 10**6), n)
    insert_order = values.copy()
    random.shuffle(insert_order)

    # Build BST by insertion
    class Node:
        def __init__(self, val):
            self.val = val
            self.left = None
            self.right = None

    def insert(root, val):
        if root is None:
            return Node(val)
        if val < root.val:
            root.left = insert(root.left, val)
        else:
            root.right = insert(root.right, val)
        return root

    root = None
    for val in insert_order:
        root = insert(root, val)

    # Convert to level-order list
    tree = []
    if root:
        queue = [root]
        while queue:
            node = queue.pop(0)
            if node:
                tree.append(node.val)
                queue.append(node.left)
                queue.append(node.right)
            else:
                tree.append(None)

    # Trim trailing Nones
    while tree and tree[-1] is None:
        tree.pop()

    return tree, insert_order


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with n nodes for complexity estimation.

    Creates a BST and picks two nodes at different depths to exercise
    the algorithm's traversal.
    """
    n = max(2, min(n, 10**5))
    tree, values = _generate_random_bst(n)

    # Pick two distinct values
    p, q = random.sample(values, 2) if len(values) >= 2 else (values[0], values[0])

    return f"{json.dumps(tree)}\n{p}\n{q}"


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}:\n{test}\n")
