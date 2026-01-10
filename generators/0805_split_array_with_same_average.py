"""
Test Case Generator for Problem 805 - Split Array With Same Average

LeetCode Constraints:
- 1 <= nums.length <= 30
- 0 <= nums[i] <= 10^4
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        ([1, 2, 3, 4, 5, 6, 7, 8],),   # Example 1: true
        ([3, 1],),                      # Example 2: false
        ([1, 1],),                      # Same values: true
        ([1],),                         # Single element: false
        ([0, 0, 0],),                   # All zeros: true
        ([1, 2, 3],),                   # Small array
        ([1, 5, 7, 4, 3],),             # Random small
        ([1, 2, 3, 4, 5],),             # Consecutive
    ]

    for args in edge_cases:
        yield json.dumps(args[0], separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        n = random.randint(2, 15)  # Keep small for reference
        nums = [random.randint(0, 100) for _ in range(n)]
        yield json.dumps(nums, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    n = max(2, min(n, 15))  # Keep small for reference
    nums = [random.randint(0, 100) for _ in range(n)]
    return json.dumps(nums, separators=(',', ':'))
