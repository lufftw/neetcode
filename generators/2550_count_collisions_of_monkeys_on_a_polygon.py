"""
Test Case Generator for Problem 2550 - Count Collisions of Monkeys on a Polygon

LeetCode Constraints:
- 3 <= n <= 10^9
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        3,          # Example 1: 2^3 - 2 = 6
        4,          # Example 2: 2^4 - 2 = 14
        5,          # 2^5 - 2 = 30
        10,         # 2^10 - 2 = 1022
        100,        # Large power
        1000,       # Larger power
        10**9,      # Maximum n
    ]

    for n in edge_cases:
        yield str(n)
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        # Mix of small and large values
        if random.random() < 0.5:
            n = random.randint(3, 1000)
        else:
            n = random.randint(10**6, 10**9)
        yield str(n)


def generate_for_complexity(size: int) -> str:
    """Generate test case with specific size for complexity estimation.

    Since this is O(log n), we test with varying magnitudes of n.
    """
    # Map size to n value (exponential growth)
    n = min(10 ** min(size, 9), 10 ** 9)
    n = max(3, n)
    return str(n)
