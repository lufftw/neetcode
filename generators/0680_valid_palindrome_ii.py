# generators/0680_valid_palindrome_ii.py
"""
Test Case Generator for Problem 0680 - Valid Palindrome II

LeetCode Constraints:
- 1 <= s.length <= 10^5
- s consists of lowercase English letters

Time Complexity: O(n) two pointers with skip
"""
import json
import random
import string
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Valid Palindrome II.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Input string (lowercase letters only)
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        "abca",                     # Can remove one
        "abc",                      # Cannot remove
        "a",                        # Single character
        "aba",                      # Already palindrome
        "deeee",                    # Can remove one
    ]
    
    for edge in edge_cases:
        yield json.dumps(edge, separators=(",",":"))
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        size = random.randint(1, 1000)
        yield _generate_case(size)


def _generate_case(size: int) -> str:
    """Generate a single test case."""
    chars = string.ascii_lowercase
    return ''.join(random.choice(chars) for _ in range(size))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.
    
    Args:
        n: Length of string
    
    Returns:
        str: A string of length n
    """
    n = max(1, n)
    return _generate_case(n)

