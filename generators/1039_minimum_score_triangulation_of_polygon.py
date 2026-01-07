"""
Generator for LC 1039: Minimum Score Triangulation of Polygon

Generates arrays of polygon vertex values for interval DP testing.
"""
import random
import json
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Polygon Triangulation."""
    if seed is not None:
        random.seed(seed)

    for _ in range(count):
        # n between 3 and 15 (polygon needs at least 3 vertices)
        n = random.randint(3, 15)

        # Values between 1 and 100
        values = [random.randint(1, 100) for _ in range(n)]

        yield json.dumps(values, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate a test case of specific size n."""
    values = [random.randint(1, 100) for _ in range(n)]
    return json.dumps(values, separators=(',', ':'))


if __name__ == "__main__":
    for case in generate(5, seed=42):
        print(case)
        print()
