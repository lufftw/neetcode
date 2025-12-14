# generators/0131_palindrome_partitioning.py
"""
Test Case Generator for Problem 0131 - Palindrome Partitioning

LeetCode Constraints:
- 1 <= s.length <= 16
- s contains only lowercase English letters
"""
import random
import string
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Palindrome Partitioning.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility
    
    Yields:
        str: Test input - a lowercase string
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        "aab",      # Classic example
        "a",        # Single char
        "aa",       # Two same chars
        "aba",      # Palindrome itself
        "abcba",    # Longer palindrome
        "abcd",     # No repeated chars
    ]
    
    for edge in edge_cases:
        yield edge
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random lowercase string."""
    # Length 1-10 (keeping small to avoid explosion)
    length = random.randint(1, 10)
    
    # Use limited alphabet to increase palindrome chances
    alphabet = "abc"  # Limited for more palindromes
    
    return ''.join(random.choice(alphabet) for _ in range(length))

