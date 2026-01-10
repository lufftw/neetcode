"""
Test Case Generator for Problem 2310 - Sum of Numbers With Units Digit K

LeetCode Constraints:
- 0 <= num <= 3000
- 0 <= k <= 9
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        (58, 9),   # Example 1: 2
        (37, 2),   # Example 2: -1
        (0, 7),    # Example 3: 0
        (0, 0),    # Zero with k=0
        (10, 0),   # Needs number ending in 0
        (5, 0),    # Impossible
        (1, 1),    # Single 1
        (10, 1),   # 10 ones or 1 ten... actually 10 with units 1 doesn't work
        (100, 5),  # Even hundred
    ]

    for num, k in edge_cases:
        yield f'{num}\n{k}'
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        num = random.randint(0, 500)
        k = random.randint(0, 9)
        yield f'{num}\n{k}'


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    # Constant time algorithm, n not really relevant
    num = random.randint(0, 3000)
    k = random.randint(0, 9)
    return f'{num}\n{k}'
