# generators/1392_longest_happy_prefix.py
"""
Test Case Generator for Problem 1392 - Longest Happy Prefix

LeetCode Constraints:
- 1 <= s.length <= 10^5
- s contains only lowercase English letters

Pattern: String Matching (KMP failure function direct application)
Time Complexity: O(n)
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
    Generate random test case inputs for Longest Happy Prefix.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (single line: s)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        "level",              # Happy prefix: "l"
        "ababab",             # Happy prefix: "abab"
        "leetcodeleet",       # Happy prefix: "leet"
        "a",                  # No happy prefix (single char)
        "ab",                 # No happy prefix
        "aa",                 # Happy prefix: "a"
        "aaa",                # Happy prefix: "aa"
        "abcabc",             # Happy prefix: "abc"
        "abcd",               # No happy prefix
        "abcab",              # Happy prefix: "ab"
        "aabaab",             # Happy prefix: "aab"
        "abacaba",            # Happy prefix: "a"
    ]

    for s in edge_cases:
        yield json.dumps(s)
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        s_len = random.randint(2, 500)

        # Different types to ensure variety
        case_type = random.random()

        if case_type < 0.3:
            # Random string (may or may not have happy prefix)
            s = _generate_random_string(s_len)
        elif case_type < 0.6:
            # String with guaranteed happy prefix
            s = _generate_string_with_happy_prefix(s_len)
        else:
            # Periodic-like string (long happy prefix)
            s = _generate_periodic_like_string(s_len)

        yield json.dumps(s)


def _generate_random_string(size: int) -> str:
    """Generate a random lowercase string."""
    return ''.join(random.choices(string.ascii_lowercase, k=size))


def _generate_string_with_happy_prefix(size: int) -> str:
    """Generate a string with a guaranteed happy prefix."""
    # Create prefix that appears at both ends
    prefix_len = random.randint(1, size // 3)
    prefix = _generate_random_string(prefix_len)

    # Middle part (different from prefix)
    middle_len = size - 2 * prefix_len
    if middle_len > 0:
        middle = _generate_random_string(middle_len)
        # Make sure middle doesn't accidentally create longer prefix match
        return prefix + middle + prefix
    else:
        # Just repeat prefix
        return prefix + prefix[:size - prefix_len]


def _generate_periodic_like_string(size: int) -> str:
    """Generate a string that's almost periodic (long happy prefix)."""
    # Choose a pattern and repeat it
    pattern_len = random.randint(1, min(10, size // 2))
    pattern = _generate_random_string(pattern_len)

    # Fill with pattern
    s = (pattern * (size // pattern_len + 1))[:size]

    # Maybe modify last character to not be perfectly periodic
    if random.random() < 0.5 and len(s) > 1:
        last_char = s[-1]
        new_char = random.choice([c for c in string.ascii_lowercase if c != last_char])
        s = s[:-1] + new_char

    return s


# ============================================================================
# Complexity Estimation (controlled size)
# ============================================================================

def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For this problem:
    - Input size n is the length of string s
    - Uses string with moderate happy prefix

    Args:
        n: Length of the string s

    Returns:
        str: Single line (s)
    """
    n = max(2, n)

    # Generate periodic string for complexity estimation
    pattern_len = max(1, n // 10)
    pattern = _generate_random_string(pattern_len)

    # Create string with pattern at start and end
    s = pattern + _generate_random_string(n - 2 * pattern_len) + pattern
    s = s[:n]  # Ensure exact length

    return json.dumps(s)
