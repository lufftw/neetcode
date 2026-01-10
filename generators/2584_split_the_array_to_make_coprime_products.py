"""
Test Case Generator for Problem 2584 - Split Array for Coprime Products

LeetCode Constraints:
- 1 <= n <= 10^4
- 1 <= nums[i] <= 10^6
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        ([4, 7, 8, 15, 3, 5],),       # Example 1: 2
        ([4, 7, 15, 8, 3, 5],),       # Example 2: -1
        ([2, 3],),                     # Simple coprime
        ([2, 4],),                     # Not coprime
        ([1, 1],),                     # All ones (coprime)
        ([6, 10, 15],),                # All share factors
        ([2, 3, 5, 7, 11],),           # Distinct primes
    ]

    for args in edge_cases:
        yield json.dumps(args[0], separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        n = random.randint(2, 20)
        nums = [random.randint(1, 1000) for _ in range(n)]
        yield json.dumps(nums, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    n = max(2, min(n, 200))
    nums = [random.randint(1, 10000) for _ in range(n)]
    return json.dumps(nums, separators=(',', ':'))
