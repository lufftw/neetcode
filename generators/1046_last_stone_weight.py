# generators/1046_last_stone_weight.py
"""
Test Case Generator for Problem 1046 - Last Stone Weight

LeetCode Constraints:
- 1 <= stones.length <= 30
- 1 <= stones[i] <= 1000
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Test input in .in file format (stones as JSON)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [2, 7, 4, 1, 8, 1],      # Classic example, result 1
        [1],                      # Single stone
        [1, 1],                   # Two equal stones, result 0
        [10, 10, 10, 10],         # All equal
        [1, 2],                   # Two stones, result 1
        [1, 1, 1, 1, 1],          # Many small equal stones
        [1000, 1000],             # Max weight, equal
        [1, 1000],                # Min and max weights
    ]

    for stones in edge_cases:
        yield json.dumps(stones, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single valid random test case."""
    n = random.randint(2, 30)
    stones = [random.randint(1, 1000) for _ in range(n)]
    return json.dumps(stones, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with n stones (capped at 30 per constraints)."""
    n = min(n, 30)
    stones = [random.randint(1, 1000) for _ in range(n)]
    return json.dumps(stones, separators=(',', ':'))
