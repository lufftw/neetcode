# generators/0062_unique_paths.py
"""
Test Case Generator for Problem 0062 - Unique Paths

LeetCode Constraints:
- 1 <= m, n <= 100
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Unique Paths.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (two lines: m and n)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        (1, 1),      # Single cell
        (1, 5),      # Single row
        (5, 1),      # Single column
        (2, 2),      # 2x2 grid
        (3, 2),      # LeetCode example 2
        (3, 7),      # LeetCode example 1
        (3, 3),      # 3x3 grid
        (10, 10),    # Medium size
        (100, 1),    # Max rows, single column
        (1, 100),    # Single row, max columns
    ]

    for m, n in edge_cases:
        yield f"{m}\n{n}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case."""
    # Random dimensions with weighted distribution
    m = random.choices(
        population=[1, 2, 5, 10, 20, 50, 100],
        weights=[1, 2, 3, 3, 2, 2, 1],
        k=1
    )[0]
    n = random.choices(
        population=[1, 2, 5, 10, 20, 50, 100],
        weights=[1, 2, 3, 3, 2, 2, 1],
        k=1
    )[0]

    return f"{m}\n{n}"


# ============================================
# Complexity Estimation
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Unique Paths:
    - n is used as both dimensions (n x n grid)
    - DP is O(n^2), Math is O(n)

    Args:
        n: Target dimension

    Returns:
        str: Test input
    """
    # Clamp to LeetCode constraints
    n = max(1, min(n, 100))

    return f"{n}\n{n}"


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(3, seed=42), 1):
        lines = test.split('\n')
        m, n = int(lines[0]), int(lines[1])
        print(f"Test {i}: {m}x{n} grid")
        print()
