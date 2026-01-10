"""
Test Case Generator for Problem 1871 - Jump Game VII

LeetCode Constraints:
- 2 <= s.length <= 10^5
- s[i] is '0' or '1'
- s[0] == '0'
- 1 <= minJump <= maxJump < s.length
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        ("011010", 2, 3),      # Example 1: true
        ("01101110", 2, 3),    # Example 2: false
        ("00", 1, 1),          # Minimal reachable
        ("01", 1, 1),          # Minimal unreachable
        ("0000000", 1, 6),     # All zeros
        ("0111110", 1, 6),     # Blocked path
        ("00000", 1, 1),       # Step by step
        ("010101", 2, 2),      # Alternating
    ]

    for s, minJ, maxJ in edge_cases:
        yield f'"{s}"\n{minJ}\n{maxJ}'
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        n = random.randint(5, 50)
        s = '0' + ''.join(random.choice('01') for _ in range(n - 1))
        maxJ = random.randint(1, n - 1)
        minJ = random.randint(1, maxJ)
        yield f'"{s}"\n{minJ}\n{maxJ}'


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    n = max(5, min(n, 100000))
    s = '0' + ''.join(random.choice('01') for _ in range(n - 1))
    maxJ = random.randint(1, min(n - 1, 1000))
    minJ = random.randint(1, maxJ)
    return f'"{s}"\n{minJ}\n{maxJ}'
