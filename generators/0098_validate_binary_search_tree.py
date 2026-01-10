# generators/0098_validate_binary_search_tree.py
"""
Test Case Generator for Problem 0098 - Validate Binary Search Tree

LeetCode Constraints:
- The number of nodes in the tree is in the range [1, 10^4]
- -2^31 <= Node.val <= 2^31 - 1
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Validate BST."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        [2, 1, 3],                      # Valid simple BST
        [5, 1, 4, None, None, 3, 6],    # Invalid: right child < root
        [1],                            # Single node (valid)
        [1, None, 2],                   # Right only (valid)
        [2, 1, None],                   # Left only (valid)
        [5, 4, 6, None, None, 3, 7],    # Invalid: 3 violates 5's constraint
        [1, 1],                         # Invalid: equal values
    ]

    for tree in edge_cases:
        yield json.dumps(tree, separators=(",", ":"))
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate random binary tree (may or may not be valid BST)."""
    n = random.randint(3, 15)

    if random.random() < 0.5:
        # Generate valid BST
        tree = _generate_valid_bst(n)
    else:
        # Generate random tree (likely invalid)
        tree = _generate_random_tree(n)

    return json.dumps(tree, separators=(",", ":"))


def _generate_valid_bst(n: int) -> List[Optional[int]]:
    """Generate a valid BST with approximately n nodes."""
    # Generate sorted unique values
    values = sorted(random.sample(range(-1000, 1001), min(n, 100)))

    def build_bst(vals):
        if not vals:
            return None
        mid = len(vals) // 2
        return {
            "val": vals[mid],
            "left": build_bst(vals[:mid]),
            "right": build_bst(vals[mid+1:])
        }

    root = build_bst(values)
    return _tree_to_list(root)


def _generate_random_tree(n: int) -> List[Optional[int]]:
    """Generate random binary tree (not necessarily valid BST)."""
    tree = [random.randint(-100, 100)]
    nodes = 1

    while nodes < n:
        pos = random.randint(0, len(tree) - 1)
        if tree[pos] is None:
            continue

        # Try to add children
        left_idx = 2 * pos + 1
        right_idx = 2 * pos + 2

        # Extend tree if needed
        while len(tree) <= right_idx:
            tree.append(None)

        if tree[left_idx] is None and random.random() < 0.7:
            tree[left_idx] = random.randint(-100, 100)
            nodes += 1
        if nodes < n and tree[right_idx] is None and random.random() < 0.7:
            tree[right_idx] = random.randint(-100, 100)
            nodes += 1

        if nodes >= n:
            break

    # Trim trailing Nones
    while tree and tree[-1] is None:
        tree.pop()

    return tree


def _tree_to_list(node) -> List[Optional[int]]:
    """Convert tree dict to level-order list."""
    if not node:
        return []

    result = []
    queue = [node]

    while queue:
        curr = queue.pop(0)
        if curr is None:
            result.append(None)
        else:
            result.append(curr["val"])
            queue.append(curr.get("left"))
            queue.append(curr.get("right"))

    # Trim trailing Nones
    while result and result[-1] is None:
        result.pop()

    return result


def generate_for_complexity(n: int) -> str:
    """Generate BST with n nodes for complexity estimation."""
    n = max(1, min(n, 1000))
    tree = _generate_valid_bst(n)
    return json.dumps(tree, separators=(",", ":"))


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}: {test}")
