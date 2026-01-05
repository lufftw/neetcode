# generators/0316_remove_duplicate_letters.py
"""
Test Case Generator for Problem 0316 - Remove Duplicate Letters

LeetCode Constraints:
- 1 <= s.length <= 10^4
- s consists of lowercase English letters

Time Complexity: O(n) with monotonic stack
"""
import json
import random
import string
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Remove Duplicate Letters.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Test input in JSON format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        "bcabc",        # Classic example -> "abc"
        "cbacdcbc",     # Second example -> "acdb"
        "a",            # Single char
        "aa",           # Duplicate single char
        "abcdefghijklmnopqrstuvwxyz",  # All unique
        "zyxwvutsrqponmlkjihgfedcba",  # Reverse order
        "aabbccdd",     # Pairs
        "dcba",         # Decreasing
        "abcd",         # Increasing
        "bab",          # Simple case
    ]

    for edge in edge_cases:
        yield json.dumps(edge)
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        length = random.randint(1, 5000)
        yield _generate_case(length)


def _generate_case(length: int) -> str:
    """Generate a single random test case."""
    s = "".join(random.choices(string.ascii_lowercase, k=length))
    return json.dumps(s)


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific input size for complexity estimation."""
    n = max(1, n)
    return _generate_case(n)
