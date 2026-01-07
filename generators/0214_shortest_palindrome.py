# generators/0214_shortest_palindrome.py
"""
Test Case Generator for Problem 0214 - Shortest Palindrome

LeetCode Constraints:
- 0 <= s.length <= 5 * 10^4
- s consists of lowercase English letters only

Pattern: String Matching (KMP with s + '#' + reverse(s))
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
    Generate random test case inputs for Shortest Palindrome.

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
        "aacecaaa",           # Classic example
        "abcd",               # No palindrome prefix beyond first char
        "",                   # Empty string
        "a",                  # Single character
        "aa",                 # Already palindrome
        "aba",                # Already palindrome (odd)
        "abba",               # Already palindrome (even)
        "abacd",              # Palindrome prefix "aba"
        "dcba",               # No common prefix/suffix
        "aaaa",               # All same character
        "abcba",              # Full palindrome
        "abcbad",             # Palindrome prefix "abcba"
    ]

    for s in edge_cases:
        yield json.dumps(s)
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        s_len = random.randint(1, 500)

        # Different types of random strings
        case_type = random.random()

        if case_type < 0.3:
            # Random string
            s = _generate_random_string(s_len)
        elif case_type < 0.6:
            # Start with palindrome prefix, then random suffix
            palindrome_len = random.randint(1, s_len)
            palindrome = _generate_palindrome(palindrome_len)
            suffix_len = s_len - palindrome_len
            suffix = _generate_random_string(suffix_len)
            s = palindrome + suffix
        else:
            # Nearly palindrome (encourage long common prefix)
            half_len = s_len // 2
            half = _generate_random_string(half_len)
            if s_len % 2 == 0:
                s = half + half[::-1]
            else:
                s = half + random.choice(string.ascii_lowercase) + half[::-1]

        yield json.dumps(s)


def _generate_random_string(size: int) -> str:
    """Generate a random lowercase string."""
    if size <= 0:
        return ""
    return ''.join(random.choices(string.ascii_lowercase, k=size))


def _generate_palindrome(size: int) -> str:
    """Generate a random palindrome of given size."""
    if size <= 0:
        return ""
    half_len = (size + 1) // 2
    half = _generate_random_string(half_len)
    if size % 2 == 0:
        return half + half[::-1]
    else:
        return half + half[-2::-1]


# ============================================================================
# Complexity Estimation (controlled size)
# ============================================================================

def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For this problem:
    - Input size n is the length of string s
    - Uses worst-case pattern (no palindrome prefix)

    Args:
        n: Length of the string s

    Returns:
        str: Single line (s)
    """
    n = max(1, n)
    # Worst case: distinct characters, no palindrome prefix
    # Using "abc...zabca...z..." pattern
    s = ''.join(string.ascii_lowercase[i % 26] for i in range(n))

    return json.dumps(s)
