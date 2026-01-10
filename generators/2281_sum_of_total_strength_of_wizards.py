"""
Test Case Generator for Problem 2281 - Sum of Total Strength of Wizards

LeetCode Constraints:
- 1 <= strength.length <= 10^5
- 1 <= strength[i] <= 10^9
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        ([1, 3, 1, 2],),      # Example 1
        ([5, 4, 6],),         # Example 2
        ([1],),               # Single element
        ([1, 2, 3],),         # Increasing
        ([3, 2, 1],),         # Decreasing
        ([1, 1, 1],),         # All same
        ([1, 2, 1, 2],),      # Alternating
    ]

    for args in edge_cases:
        yield json.dumps(args[0], separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        # Keep small for O(n^2) reference
        n = random.randint(2, 15)
        strength = [random.randint(1, 100) for _ in range(n)]
        yield json.dumps(strength, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    n = max(1, min(n, 100))
    strength = [random.randint(1, 1000) for _ in range(n)]
    return json.dumps(strength, separators=(',', ':'))
