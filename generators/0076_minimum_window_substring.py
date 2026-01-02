# generators/0076_minimum_window_substring.py
"""
Test Case Generator for Problem 0076 - Minimum Window Substring

LeetCode Constraints:
- 1 <= s.length, t.length <= 10^5
- s and t consist of uppercase and lowercase English letters

Time Complexity: O(|s| + |t|) sliding window
"""
import json
import random
import string
from typing import Iterator, Optional


# ============================================================================
# Random Test Generation (for functional testing)
# ============================================================================

def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Minimum Window Substring.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Test input (two lines: s and t)
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        ("ADOBECODEBANC", "ABC"),      # Classic example
        ("a", "a"),                     # Single character match
        ("a", "aa"),                    # No valid window
        ("aa", "aa"),                   # Exact match
        ("ab", "b"),                    # Single char target at end
        ("bba", "ab"),                  # Multiple valid windows
        ("abc", "cba"),                 # Exact anagram
        ("aaaaaaaaaaaabbbbbcdd", "abcdd"),  # Clustered at end
    ]
    
    for s, t in edge_cases:
        yield f"{json.dumps(s)}\n{json.dumps(t)}"
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        s_len = random.randint(10, 500)
        t_len = random.randint(1, min(s_len, 50))
        
        # Generate s
        s = _generate_random_string(s_len)
        
        # Generate t (ensure it's possible to find in s for most cases)
        if random.random() < 0.8:
            # Pick characters from s
            t = ''.join(random.choices(s, k=t_len))
        else:
            # Completely random t (may not have valid window)
            t = _generate_random_string(t_len)
        
        yield f"{json.dumps(s)}\n{json.dumps(t)}"


def _generate_random_string(size: int) -> str:
    """Generate a random string with uppercase and lowercase letters."""
    chars = string.ascii_letters
    return ''.join(random.choices(chars, k=size))


# ============================================================================
# Complexity Estimation (controlled size)
# ============================================================================

def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.
    
    For this problem:
    - Input size n is the length of string s
    - t is kept small (n/10) to focus on s traversal
    
    Args:
        n: Length of the source string s
    
    Returns:
        str: Two lines (s and t)
    """
    n = max(1, n)
    s = _generate_random_string(n)
    
    # t should be small relative to s
    t_len = max(1, n // 10)
    t = ''.join(random.choices(s, k=t_len))
    
    return f"{json.dumps(s)}\n{json.dumps(t)}"

