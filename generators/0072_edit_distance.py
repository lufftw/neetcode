"""
Random test generator for LC 72: Edit Distance

Constraints:
- 0 <= word1.length, word2.length <= 500
- word1 and word2 consist of lowercase English letters.
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
        # Random lengths between 0 and 50 for normal tests
        len1 = random.randint(0, 50)
        len2 = random.randint(0, 50)

        word1 = _generate_string(len1)
        word2 = _generate_string(len2)

        yield f'{json.dumps(word1)}\n{json.dumps(word2)}'


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific size n for complexity estimation.
    Both strings have length n.
    """
    word1 = _generate_string(n)
    word2 = _generate_string(n)

    return f'{json.dumps(word1)}\n{json.dumps(word2)}'


def _generate_string(length: int, alphabet_size: int = 26) -> str:
    """Generate a random lowercase string of given length."""
    if length == 0:
        return ""
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
