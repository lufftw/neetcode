"""
Test Case Generator for Problem 2117 - Abbreviating the Product of a Range

LeetCode Constraints:
- 1 <= left <= right <= 10^4
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        (1, 4),    # Example 1
        (2, 11),   # Example 2
        (371, 375),  # Example 3
        (1, 1),    # Single
        (1, 10),   # Small factorial
        (1, 5),    # 5!
        (10, 15),  # Mid range
        (100, 105),  # Larger range
    ]

    for left, right in edge_cases:
        yield f"{left}\n{right}"
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        left = random.randint(1, 500)
        right = random.randint(left, min(left + 20, 1000))
        yield f"{left}\n{right}"


def generate_for_complexity(n: int) -> str:
    n = max(1, min(n, 10000))
    left = random.randint(1, n // 2)
    right = left + min(n - left, random.randint(1, 100))
    return f"{left}\n{right}"
