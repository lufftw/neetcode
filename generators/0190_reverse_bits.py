# generators/0190_reverse_bits.py
"""
Test Case Generator for Problem 0190 - Reverse Bits

LeetCode Constraints:
- The input must be a binary string of length 32
"""
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Reverse Bits."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        "0" * 32,                                    # All zeros
        "1" * 32,                                    # All ones
        "0" * 31 + "1",                              # Just LSB set
        "1" + "0" * 31,                              # Just MSB set
        "01" * 16,                                   # Alternating pattern
        "10" * 16,                                   # Alternating pattern reversed
    ]

    for binary_str in edge_cases:
        yield binary_str
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random 32-bit binary string."""
    return "".join(random.choice("01") for _ in range(32))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case for complexity estimation.

    Since all operations are O(1) for 32 bits, n is ignored.
    Returns a random 32-bit binary string.
    """
    return "".join(random.choice("01") for _ in range(32))


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}: {test}")
