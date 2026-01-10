"""
Test Case Generator for Problem 0887 - Super Egg Drop

LeetCode Constraints:
- 1 <= k <= 100
- 1 <= n <= 10^4
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        (1, 2),      # Example 1
        (2, 6),      # Example 2
        (3, 14),     # Example 3
        (1, 1),      # Minimal
        (1, 100),    # 1 egg, many floors
        (100, 1),    # Many eggs, 1 floor
        (2, 100),    # Classic 2-egg problem
        (10, 1000),  # Larger case
    ]

    for k, n in edge_cases:
        yield f'{k}\n{n}'
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        k = random.randint(1, 50)
        n = random.randint(1, 5000)
        yield f'{k}\n{n}'


def generate_for_complexity(size: int) -> str:
    """Generate test case with specific size for complexity estimation."""
    # Size maps to n (number of floors)
    n = max(1, min(size * 10, 10000))
    k = random.randint(2, 10)  # Reasonable number of eggs
    return f'{k}\n{n}'
