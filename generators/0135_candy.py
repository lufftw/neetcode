"""
Test Case Generator for Problem 135 - Candy

LeetCode Constraints:
- n == ratings.length
- 1 <= n <= 2 * 10^4
- 0 <= ratings[i] <= 2 * 10^4
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
        str: Test input in .in file format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [1, 0, 2],  # Classic example, answer = 5
        [1, 2, 2],  # Adjacent equal ratings, answer = 4
        [1],  # Single child
        [1, 1, 1, 1],  # All same ratings
        [1, 2, 3, 4, 5],  # Strictly increasing
        [5, 4, 3, 2, 1],  # Strictly decreasing
        [1, 3, 2, 2, 1],  # Peak in middle
        [1, 2, 3, 2, 1],  # Mountain shape
    ]

    for ratings in edge_cases:
        yield json.dumps(ratings, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a single random test case."""
    n = random.randint(1, 1000)

    # Different patterns
    pattern = random.choice(['random', 'peaks', 'valleys', 'mixed'])

    if pattern == 'random':
        ratings = [random.randint(0, 1000) for _ in range(n)]
    elif pattern == 'peaks':
        # Create multiple peaks
        ratings = []
        for i in range(n):
            if i % 4 < 2:
                ratings.append(i % 4)
            else:
                ratings.append(3 - (i % 4))
    elif pattern == 'valleys':
        # Create valleys
        ratings = []
        for i in range(n):
            ratings.append(abs((i % 6) - 3))
    else:
        # Mixed with some equal values
        ratings = [random.randint(0, 10) for _ in range(n)]

    return json.dumps(ratings, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size for complexity estimation."""
    ratings = [random.randint(0, 10000) for _ in range(n)]
    return json.dumps(ratings, separators=(',', ':'))
