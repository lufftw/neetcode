"""
Test Case Generator for Problem 0605 - Can Place Flowers

LeetCode Constraints:
- 1 <= flowerbed.length <= 2 * 10^4
- 0 <= n <= flowerbed.length
- No two adjacent flowers initially
"""
import json
import random
from typing import Iterator, Optional


def _generate_valid_flowerbed(length: int) -> list:
    """Generate a valid flowerbed with no adjacent flowers."""
    fb = [0] * length
    i = 0
    while i < length:
        if random.random() < 0.3:  # 30% chance to place flower
            fb[i] = 1
            i += 2  # Skip next position
        else:
            i += 1
    return fb


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        ([1, 0, 0, 0, 1], 1),  # Example 1: true
        ([1, 0, 0, 0, 1], 2),  # Example 2: false
        ([0], 1),              # Single empty
        ([1], 0),              # Single occupied, n=0
        ([0, 0, 0], 2),        # Can plant 2
        ([0, 0, 0, 0, 0], 3),  # All empty
    ]

    for fb, n in edge_cases:
        yield f'{json.dumps(fb, separators=(",", ":"))}\n{n}'
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        length = random.randint(1, 20)
        fb = _generate_valid_flowerbed(length)
        n = random.randint(0, length // 2 + 1)
        yield f'{json.dumps(fb, separators=(",", ":"))}\n{n}'


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    n = max(1, min(n, 500))
    fb = _generate_valid_flowerbed(n)
    flowers = random.randint(0, n // 2)
    return f'{json.dumps(fb, separators=(",", ":"))}\n{flowers}'
