"""
Test Case Generator for Problem 2572 - Count the Number of Square-Free Subsets

LeetCode Constraints:
- 1 <= nums.length <= 1000
- 1 <= nums[i] <= 30
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        ([3, 4, 4, 5],),     # Example 1
        ([1],),              # Example 2
        ([1, 1, 1],),        # Multiple 1s
        ([2, 3, 5],),        # Primes only
        ([4, 8, 9, 16],),    # All non-square-free
        ([6, 10, 15],),      # Products of two primes
        ([1, 2, 3, 5, 6],),  # Mixed
        ([30, 29, 28],),     # Large values near 30
    ]

    for args in edge_cases:
        yield json.dumps(args[0], separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        n = random.randint(3, 15)  # Small for reference to work
        nums = [random.randint(1, 30) for _ in range(n)]
        yield json.dumps(nums, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    n = max(3, min(n, 15))  # Keep small for reference verification
    nums = [random.randint(1, 30) for _ in range(n)]
    return json.dumps(nums, separators=(',', ':'))
