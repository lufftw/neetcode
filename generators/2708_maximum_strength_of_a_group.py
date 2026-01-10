"""
Test Case Generator for Problem 2708 - Maximum Strength of a Group

LeetCode Constraints:
- 1 <= nums.length <= 13
- -9 <= nums[i] <= 9
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        ([3, -1, -5, 2, 5, -9],),      # Example 1
        ([-4, -5, -4],),               # Example 2
        ([1],),                        # Single positive
        ([-1],),                       # Single negative
        ([0],),                        # Single zero
        ([0, 0, 0],),                  # All zeros
        ([-9, -9],),                   # Two negatives
        ([9, 9, 9],),                  # All positives
        ([0, -1],),                    # Zero and negative
        ([-1, -2, -3],),               # Odd number of negatives
        ([1, -1, 0],),                 # Mixed with zero
        ([0, -2, -3, 4],),             # Mixed with zero
    ]

    for args in edge_cases:
        yield json.dumps(args[0], separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        n = random.randint(1, 13)
        nums = [random.randint(-9, 9) for _ in range(n)]
        yield json.dumps(nums, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    n = max(1, min(n, 13))
    nums = [random.randint(-9, 9) for _ in range(n)]
    return json.dumps(nums, separators=(',', ':'))
