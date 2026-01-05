# generators/0452_minimum_number_of_arrows_to_burst_balloons.py
"""
Test Case Generator for Problem 0452 - Minimum Number of Arrows to Burst Balloons

LeetCode Constraints:
- 1 <= points.length <= 10^5
- points[i].length == 2
- -2^31 <= xstart < xend <= 2^31 - 1
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Minimum Number of Arrows.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: 2D points array in JSON format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [[10, 16], [2, 8], [1, 6], [7, 12]],  # 2 arrows
        [[1, 2], [3, 4], [5, 6], [7, 8]],  # 4 arrows (no overlap)
        [[1, 2], [2, 3], [3, 4], [4, 5]],  # 2 arrows (touching)
        [[1, 2]],  # Single balloon
        [[1, 10], [2, 5], [6, 9]],  # All overlap with first
        [[-10, -5], [-7, -3], [0, 5]],  # Negative values
        [[1, 100], [2, 99], [3, 98]],  # Nested balloons
        [[1, 2], [2, 3], [4, 5], [5, 6]],  # Two groups
    ]

    for points in edge_cases:
        yield json.dumps(points, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case."""
    n = random.randint(2, 100)
    max_val = 1000

    points = []
    for _ in range(n):
        start = random.randint(-max_val, max_val - 1)
        end = random.randint(start + 1, max_val)  # strict: start < end
        points.append([start, end])

    return json.dumps(points, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    Args:
        n: Number of balloons

    Returns:
        str: Points array of size n
    """
    max_val = n * 10
    points = []

    for _ in range(n):
        start = random.randint(0, max_val - 1)
        end = random.randint(start + 1, max_val)
        points.append([start, end])

    return json.dumps(points, separators=(',', ':'))


if __name__ == "__main__":
    for i, case in enumerate(generate(5)):
        print(f"Case {i + 1}: {case}")
