# generators/0125_valid_palindrome.py
"""
Test Case Generator for Problem 0125 - Valid Palindrome

LeetCode Constraints:
- 1 <= s.length <= 2 * 10^5
- s consists only of printable ASCII characters

Time Complexity: O(n) two pointers
"""
import random
import string
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Valid Palindrome.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Input string
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        "A man, a plan, a canal: Panama",  # Classic example
        "race a car",                        # Not palindrome
        "",                                  # Empty string
        "a",                                 # Single character
        "aA",                                # Case difference
        ".,",                                # Only non-alphanumeric
    ]
    
    for edge in edge_cases:
        yield edge
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        size = random.randint(1, 500)
        yield _generate_case(size)


def _generate_case(size: int) -> str:
    """Generate a single test case."""
    # Mix of alphanumeric and non-alphanumeric
    chars = string.ascii_letters + string.digits + " ,.!?;:"
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

