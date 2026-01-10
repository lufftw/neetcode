# generators/0338_counting_bits.py
"""
Test Case Generator for Problem 0338 - Counting Bits

LeetCode Constraints:
- 0 <= n <= 10^5
"""
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Counting Bits."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [0, 1, 2, 7, 8, 15, 16]

    for n in edge_cases:
        yield str(n)
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield str(random.randint(0, 1000))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with size n for complexity estimation.

    Both DP approaches should show O(n) behavior.
    """
    n = max(0, min(n, 100000))
    return str(n)


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}: {test}")
