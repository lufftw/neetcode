# generators/0003_longest_substring_without_repeating_characters.py
"""
Test Case Generator for Problem 0003 - Longest Substring Without Repeating Characters

LeetCode Constraints:
- 0 <= s.length <= 5 * 10^4
- s consists of English letters, digits, symbols and spaces

Time Complexity: O(n) sliding window
"""
import random
import string
from typing import Iterator, Optional


# ============================================
# Random Test Generation (for functional testing)
# ============================================

def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Longest Substring.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Test input (a single string)
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        "",                      # Empty string
        "a",                     # Single character
        "abcabcbb",              # Classic example
        "bbbbb",                 # All same characters
        "pwwkew",                # Classic example
        " ",                     # Single space
        "aab",                   # Short with repeat
        "dvdf",                  # Tricky case
    ]
    
    for edge in edge_cases:
        yield edge
        count -= 1
        if count <= 0:
            return
    
    # Random cases with varying sizes
    for _ in range(count):
        size = random.randint(1, 1000)
        yield _generate_random_string(size)


def _generate_random_string(size: int) -> str:
    """Generate a random string with various character types."""
    # Character pool: lowercase, uppercase, digits, some symbols
    chars = string.ascii_letters + string.digits + " !@#$%"
    
    # Randomly choose character pool size to create varying repeat patterns
    pool_size = random.choice([5, 10, 26, 52, len(chars)])
    pool = chars[:pool_size]
    
    return ''.join(random.choice(pool) for _ in range(size))


# ============================================
# Complexity Estimation (controlled size)
# ============================================

def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.
    
    For this problem:
    - Input size n is the length of string s
    - Time complexity is O(n) with sliding window
    
    Args:
        n: Length of the string
    
    Returns:
        str: A string of length n
    """
    n = max(0, n)
    return _generate_random_string(n) if n > 0 else ""

