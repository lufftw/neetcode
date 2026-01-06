"""
Random test generator for LC 1143: Longest Common Subsequence

Constraints:
- 1 <= text1.length, text2.length <= 1000
- text1 and text2 consist of only lowercase English characters.
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
        # Random lengths between 1 and 100 for normal tests
        len1 = random.randint(1, 100)
        len2 = random.randint(1, 100)

        text1 = _generate_string(len1)
        text2 = _generate_string(len2)

        yield f'{json.dumps(text1)}\n{json.dumps(text2)}'


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific size n for complexity estimation.
    Both strings have length n.
    """
    text1 = _generate_string(n)
    text2 = _generate_string(n)

    return f'{json.dumps(text1)}\n{json.dumps(text2)}'


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
