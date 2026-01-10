# generators/0424_longest_repeating_character_replacement.py
"""
Test Case Generator for Problem 0424 - Longest Repeating Character Replacement

LeetCode Constraints:
- 1 <= s.length <= 10^5
- s consists of only uppercase English letters
- 0 <= k <= s.length
"""
import random
import string
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Longest Repeating Character Replacement."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        ("A", 0),           # Single character
        ("A", 1),           # Single character with k=1
        ("AB", 1),          # Two different chars
        ("AA", 0),          # Two same chars
        ("AAAA", 2),        # All same with k
        ("ABCD", 0),        # All different, k=0
    ]

    for s, k in edge_cases:
        yield f"{s}\n{k}"
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random test case."""
    length = random.randint(5, 50)
    # Use limited alphabet for more interesting patterns
    alphabet = string.ascii_uppercase[:random.randint(2, 6)]
    s = "".join(random.choices(alphabet, k=length))
    k = random.randint(0, length)
    return f"{s}\n{k}"


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with string length n for complexity estimation.
    """
    n = max(1, min(n, 100000))
    # Use limited alphabet
    alphabet = string.ascii_uppercase[:4]
    s = "".join(random.choices(alphabet, k=n))
    k = random.randint(0, n // 2)
    return f"{s}\n{k}"


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}:")
        print(test)
        print()
