# generators/0647_palindromic_substrings.py
"""
Test Case Generator for Problem 0647 - Palindromic Substrings

LeetCode Constraints:
- 1 <= s.length <= 1000
- s consists of lowercase English letters
"""
import random
import string
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Palindromic Substrings."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        "a",          # Single character
        "aa",         # Two same chars
        "ab",         # Two different chars
        "aba",        # Simple palindrome
        "aaa",        # All same
        "abba",       # Even length palindrome
        "racecar",    # Classic palindrome
    ]

    for s in edge_cases:
        yield s
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random test case."""
    length = random.randint(5, 50)

    # Mix of random and structured patterns for variety
    if random.random() < 0.3:
        # Generate with some repeated characters to create palindromes
        chars = random.choices(string.ascii_lowercase[:5], k=length)
    else:
        # Fully random
        chars = random.choices(string.ascii_lowercase, k=length)

    return "".join(chars)


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific size n for complexity estimation.

    O(n^2) approaches should show quadratic growth.
    Manacher's algorithm should show linear growth.
    """
    n = max(1, min(n, 1000))

    # Use limited alphabet to create more palindromes
    return "".join(random.choices(string.ascii_lowercase[:3], k=n))


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}: {test}")
