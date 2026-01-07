"""
Generator for LC 664: Strange Printer

Generates strings for interval DP character matching testing.
"""
import random
import json
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Strange Printer."""
    if seed is not None:
        random.seed(seed)

    for _ in range(count):
        # Length between 1 and 30 (due to O(n³) complexity)
        n = random.randint(1, 30)

        # Use lowercase letters, with bias towards repetition
        chars = 'abcdefgh'  # Limited charset for more interesting cases
        s = ''.join(random.choice(chars) for _ in range(n))

        yield json.dumps(s, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate a test case of specific size n."""
    chars = 'abcdefghijklmnop'
    s = ''.join(random.choice(chars) for _ in range(n))
    return json.dumps(s, separators=(',', ':'))


if __name__ == "__main__":
    for case in generate(5, seed=42):
        print(case)
        print()
