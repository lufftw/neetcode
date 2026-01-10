# generators/0242_valid_anagram.py
"""
Test Case Generator for Problem 0242 - Valid Anagram

LeetCode Constraints:
- 1 <= s.length, t.length <= 5 * 10^4
- s and t consist of lowercase English letters
"""
import json
import random
import string
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Valid Anagram."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        ("anagram", "nagaram"),  # True - classic
        ("rat", "car"),  # False - different chars
        ("a", "a"),  # Single char - same
        ("a", "b"),  # Single char - different
        ("ab", "ba"),  # Two chars - anagram
    ]

    for s, t in edge_cases:
        yield f'"{s}"\n"{t}"'
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate random pair of strings."""
    n = random.randint(5, 50)
    s = "".join(random.choices(string.ascii_lowercase, k=n))

    # 50% chance to be anagram
    if random.random() < 0.5:
        t = "".join(random.sample(s, len(s)))  # Shuffle s
    else:
        t = "".join(random.choices(string.ascii_lowercase, k=n))

    return f'"{s}"\n"{t}"'


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with strings of length n for complexity estimation.
    """
    n = max(1, min(n, 50000))
    s = "".join(random.choices(string.ascii_lowercase, k=n))
    t = "".join(random.sample(s, len(s)))
    return f'"{s}"\n"{t}"'


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}")
