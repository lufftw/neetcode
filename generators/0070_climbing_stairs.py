"""
Test Generator for LeetCode 70: Climbing Stairs
Pattern: DP 1D Linear - Fibonacci-Style (Count Ways)
"""

import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test cases for Climbing Stairs.

    Constraints:
    - 1 <= n <= 45

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        Test case strings (one n per line)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        1,   # Smallest input
        2,   # Base case
        3,   # First non-base case
        45,  # Maximum constraint
        10,  # Small number
        20,  # Medium number
    ]

    for n in edge_cases:
        if count <= 0:
            break
        yield json.dumps(n, separators=(",", ":"))
        count -= 1

    # Random cases
    while count > 0:
        n = random.randint(1, 45)
        yield json.dumps(n, separators=(",", ":"))
        count -= 1


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific size n for complexity estimation.

    Args:
        n: The value to use as input

    Returns:
        Test case string
    """
    # Clamp to valid range
    n = max(1, min(n, 45))
    return json.dumps(n, separators=(",", ":"))


if __name__ == "__main__":
    for case in generate(5, seed=42):
        print(case)
