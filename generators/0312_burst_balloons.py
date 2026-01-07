"""
Generator for LC 312: Burst Balloons

Generates arrays of balloon values for interval DP testing.
"""
import random
import json
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Burst Balloons."""
    if seed is not None:
        random.seed(seed)

    for _ in range(count):
        # n between 1 and 15 (due to O(n³) complexity)
        n = random.randint(1, 15)

        # Values between 1 and 100
        nums = [random.randint(1, 100) for _ in range(n)]

        yield json.dumps(nums, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate a test case of specific size n."""
    nums = [random.randint(1, 100) for _ in range(n)]
    return json.dumps(nums, separators=(',', ':'))


if __name__ == "__main__":
    for case in generate(5, seed=42):
        print(case)
        print()
