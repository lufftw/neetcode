"""
Random test generator for LC 516: Longest Palindromic Subsequence

Constraints:
- 1 <= s.length <= 1000
- s consists only of lowercase English letters.
"""
import random
import json
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test cases.

    Yields test input strings in the format expected by the solution.
    """
    if seed is not None:
        random.seed(seed)

    for _ in range(count):
        # Random length between 1 and 100 for normal tests
        length = random.randint(1, 100)

        s = _generate_string(length)

        yield json.dumps(s)


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific size n for complexity estimation.
    """
    s = _generate_string(n)

    return json.dumps(s)


def _generate_string(length: int, alphabet_size: int = 26) -> str:
    """Generate a random lowercase string of given length."""
    return ''.join(
        chr(ord('a') + random.randint(0, alphabet_size - 1))
        for _ in range(length)
    )


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}:")
        print(test)
        print()
