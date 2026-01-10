# generators/0143_reorder_list.py
"""
Test Case Generator for Problem 0143 - Reorder List

LeetCode Constraints:
- The number of nodes in the list is in the range [1, 5 * 10^4]
- 1 <= Node.val <= 1000
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Reorder List."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        [1],              # Single node
        [1, 2],           # Two nodes
        [1, 2, 3],        # Three nodes
        [1, 2, 3, 4],     # Even length
        [1, 2, 3, 4, 5],  # Odd length
    ]

    for values in edge_cases:
        yield json.dumps(values)
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random linked list."""
    length = random.randint(1, 50)
    values = [random.randint(1, 1000) for _ in range(length)]
    return json.dumps(values)


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with n nodes for complexity estimation.

    Both approaches should show O(n) time behavior.
    """
    n = max(1, min(n, 50000))
    values = [random.randint(1, 1000) for _ in range(n)]
    return json.dumps(values)


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}: {test}")
