# generators/0019_remove_nth_node_from_end_of_list.py
"""
Test Case Generator for Problem 0019 - Remove Nth Node From End of List

LeetCode Constraints:
- The number of nodes in the list is sz.
- 1 <= sz <= 30
- 0 <= Node.val <= 100
- 1 <= n <= sz
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Remove Nth Node From End of List.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (JSON array for list + integer for n)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        ([1], 1),                      # Single node, remove it
        ([1, 2], 1),                   # Two nodes, remove last
        ([1, 2], 2),                   # Two nodes, remove first (head)
        ([1, 2, 3, 4, 5], 2),          # LeetCode example
        ([1, 2, 3, 4, 5], 1),          # Remove last node
        ([1, 2, 3, 4, 5], 5),          # Remove first node (head)
        ([1, 2, 3], 2),                # Remove middle node
        (list(range(1, 31)), 15),      # Max size, remove from middle
        (list(range(1, 31)), 1),       # Max size, remove last
        (list(range(1, 31)), 30),      # Max size, remove first
    ]

    for head, n in edge_cases:
        yield f"{json.dumps(head, separators=(',', ':'))}\n{n}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case."""
    # Random list size (weighted towards smaller sizes)
    size = random.choices(
        population=[1, 2, 3, 5, 10, 15, 20, 30],
        weights=[2, 2, 3, 4, 4, 3, 2, 1],
        k=1
    )[0]

    # Generate random values
    head = [random.randint(0, 100) for _ in range(size)]

    # Random n (valid: 1 <= n <= size)
    n = random.randint(1, size)

    return f"{json.dumps(head, separators=(',', ':'))}\n{n}"


# ============================================
# Complexity Estimation (controlled size)
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Remove Nth Node:
    - n is the list size
    - Expected complexity: O(n) for both solutions

    Args:
        n: Target list size

    Returns:
        str: Test input
    """
    # Clamp to LeetCode constraints
    size = max(1, min(n, 30))

    head = list(range(1, size + 1))
    remove_n = random.randint(1, size)

    return f"{json.dumps(head, separators=(',', ':'))}\n{remove_n}"


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}:\n{test}\n")
