"""
Test Case Generator for Problem 0866 - Prime Palindrome

LeetCode Constraints:
- 1 <= n <= 10^8
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        6,      # Example 1: 7
        8,      # Example 2: 11
        13,     # Example 3: 101
        1,      # Minimum
        2,      # Prime itself
        11,     # Even-digit prime palindrome
        12,     # Skip to 101
        100,    # Skip to 101
        1000,   # 5-digit realm
    ]

    for n in edge_cases:
        yield str(n)
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        n = random.randint(1, 10000)
        yield str(n)


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    return str(random.randint(1, min(n * 100, 10**7)))
