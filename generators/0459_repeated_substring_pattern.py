# generators/0459_repeated_substring_pattern.py
"""
Test Case Generator for Problem 0459 - Repeated Substring Pattern

LeetCode Constraints:
- 1 <= s.length <= 10^4
- s consists of lowercase English letters

Pattern: String Matching (KMP failure function for periodicity)
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
    Generate random test case inputs for Repeated Substring Pattern.

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
        "abab",               # True: "ab" * 2
        "aba",                # False: not periodic
        "abcabcabcabc",       # True: "abc" * 4
        "a",                  # False: single char
        "aa",                 # True: "a" * 2
        "aaa",                # True: "a" * 3
        "abba",               # False: not periodic
        "abcabc",             # True: "abc" * 2
        "abcd",               # False: not periodic
        "xyzxyzxyz",          # True: "xyz" * 3
        "abaaba",             # True: "aba" * 2
        "abacaba",            # False: not periodic
    ]

    for s in edge_cases:
        yield json.dumps(s)
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        # 50% periodic, 50% non-periodic
        if random.random() < 0.5:
            # Generate periodic string
            s = _generate_periodic_string()
        else:
            # Generate non-periodic string
            s = _generate_non_periodic_string()

        yield json.dumps(s)


def _generate_periodic_string() -> str:
    """Generate a periodic string (repeating pattern)."""
    # Choose a pattern length and repeat count
    pattern_len = random.randint(1, 20)
    repeat_count = random.randint(2, 50)

    # Generate random pattern
    pattern = ''.join(random.choices(string.ascii_lowercase, k=pattern_len))

    return pattern * repeat_count


def _generate_non_periodic_string() -> str:
    """Generate a non-periodic string."""
    length = random.randint(2, 500)

    # Strategy: make sure the string is not periodic
    # Use distinct characters or break periodicity
    s = ''.join(random.choices(string.ascii_lowercase, k=length))

    # Add a character at the end that breaks any potential period
    # by making sure length doesn't divide evenly
    if len(s) % 2 == 0:
        s = s + random.choice(string.ascii_lowercase)

    return s


# ============================================================================
# Complexity Estimation (controlled size)
# ============================================================================

def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For this problem:
    - Input size n is the length of string s
    - Uses periodic string for typical case

    Args:
        n: Length of the string s

    Returns:
        str: Single line (s)
    """
    n = max(2, n)

    # Generate periodic string of size n
    # Choose pattern length that divides n
    divisors = [i for i in range(1, min(n // 2 + 1, 100)) if n % i == 0]
    pattern_len = random.choice(divisors) if divisors else 1

    pattern = ''.join(random.choices(string.ascii_lowercase, k=pattern_len))
    repeat_count = n // pattern_len
    s = pattern * repeat_count

    return json.dumps(s)
