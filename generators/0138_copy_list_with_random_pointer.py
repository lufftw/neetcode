# generators/0138_copy_list_with_random_pointer.py
"""
Test Case Generator for Problem 0138 - Copy List with Random Pointer

LeetCode Constraints:
- 0 <= n <= 1000
- -10^4 <= Node.val <= 10^4
- Node.random is null or points to some node in the linked list
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Copy List with Random Pointer."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        [],                                  # Empty list
        [[1, None]],                         # Single node, no random
        [[1, 0]],                            # Single node, random to self
        [[1, 1], [2, 0]],                    # Two nodes with cross random
    ]

    for nodes in edge_cases:
        yield json.dumps(nodes)
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random linked list with random pointers."""
    n = random.randint(3, 15)
    nodes: List[List[Optional[int]]] = []

    for _ in range(n):
        val = random.randint(-100, 100)
        # Random pointer: None or index in [0, n-1]
        random_idx = random.choice([None] + list(range(n)))
        nodes.append([val, random_idx])

    return json.dumps(nodes)


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with n nodes for complexity estimation.
    """
    n = max(0, min(n, 1000))
    if n == 0:
        return "[]"

    nodes: List[List[Optional[int]]] = []
    for _ in range(n):
        val = random.randint(-10000, 10000)
        random_idx = random.choice([None] + list(range(n)))
        nodes.append([val, random_idx])

    return json.dumps(nodes)


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}: {test}")
