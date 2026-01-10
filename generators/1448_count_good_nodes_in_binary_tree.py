# generators/1448_count_good_nodes_in_binary_tree.py
"""
Test Case Generator for Problem 1448 - Count Good Nodes in Binary Tree

LeetCode Constraints:
- The number of nodes is in range [1, 10^5]
- Each node's value is between [-10^4, 10^4]
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Count Good Nodes in Binary Tree.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (tree as JSON level-order array)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # LeetCode Example 1
        [3, 1, 4, 3, None, 1, 5],
        # LeetCode Example 2
        [3, 3, None, 4, 2],
        # LeetCode Example 3: single node
        [1],
        # All same values (all good)
        [5, 5, 5, 5, 5, 5, 5],
        # Strictly decreasing (only root good)
        [10, 5, 5, 3, 3, 3, 3],
        # Strictly increasing along all paths (all good)
        [1, 2, 3, 4, 5, 6, 7],
    ]

    for tree in edge_cases:
        yield json.dumps(tree, separators=(",", ":"))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_tree()


def _generate_random_tree() -> str:
    """Generate a random binary tree in level-order format."""
    num_nodes = random.randint(5, 50)
    return _build_random_tree(num_nodes)


def _build_random_tree(num_nodes: int) -> str:
    """Build a random binary tree with specified number of nodes."""
    if num_nodes == 0:
        return "[]"

    # Generate root
    values = [random.randint(-100, 100)]
    nodes_added = 1

    # Queue tracks positions that can have children
    # Each position can have 0, 1, or 2 children
    queue_size = 1
    level_start = 0

    while nodes_added < num_nodes:
        next_level = []
        for i in range(level_start, len(values)):
            if values[i] is None:
                continue

            # Decide children
            for _ in range(2):  # left and right
                if nodes_added >= num_nodes:
                    next_level.append(None)
                elif random.random() < 0.7:  # 70% chance of having a child
                    next_level.append(random.randint(-100, 100))
                    nodes_added += 1
                else:
                    next_level.append(None)

        if not any(v is not None for v in next_level):
            break

        level_start = len(values)
        values.extend(next_level)

    # Trim trailing Nones
    while values and values[-1] is None:
        values.pop()

    return json.dumps(values, separators=(",", ":"))


# ============================================
# Complexity Estimation
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Count Good Nodes:
    - n is the number of nodes
    - Time complexity is O(n)

    Args:
        n: Number of nodes (will be clamped to [1, 100000])

    Returns:
        str: Test input (tree as JSON array)
    """
    # Clamp to LeetCode constraints
    n = max(1, min(n, 100000))

    # Generate a complete binary tree for predictable structure
    values = []
    for i in range(n):
        values.append(random.randint(-10000, 10000))

    return json.dumps(values, separators=(",", ":"))


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(5, seed=42), 1):
        tree = json.loads(test)
        non_null = sum(1 for v in tree if v is not None)
        print(f"Test {i}: {non_null} nodes")
        if len(tree) <= 15:
            print(f"  tree: {tree}")
        print()
