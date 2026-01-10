"""
Test Case Generator for Problem 2659 - Make Array Empty

LeetCode Constraints:
- 1 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9
- All values distinct
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        ([3, 4, -1],),       # Example 1
        ([1, 2, 4, 3],),     # Example 2
        ([1, 2, 3],),        # Example 3: already sorted
        ([3, 2, 1],),        # Reverse sorted
        ([1],),              # Single element
        ([5, 1],),           # Two elements
        ([1, 3, 2, 4],),     # Partial order
        ([-5, -3, -1, 0, 2],),  # Negative values
    ]

    for args in edge_cases:
        yield json.dumps(args[0], separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        n = random.randint(3, 50)
        nums = random.sample(range(-1000, 1000), n)
        yield json.dumps(nums, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    n = max(3, min(n, 50))  # Keep small for reference verification
    nums = random.sample(range(-n * 100, n * 100), n)
    return json.dumps(nums, separators=(',', ':'))
