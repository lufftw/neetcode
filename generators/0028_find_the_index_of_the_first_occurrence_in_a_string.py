# generators/0028_find_the_index_of_the_first_occurrence_in_a_string.py
"""
Test Case Generator for Problem 0028 - Find the Index of the First Occurrence

LeetCode Constraints:
- 1 <= haystack.length, needle.length <= 10^4
- haystack and needle consist of only lowercase English characters

Pattern: String Matching (KMP / Rabin-Karp)
Time Complexity: O(m + n) with KMP or Rabin-Karp
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
    Generate random test case inputs for Find Index problem.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (two lines: haystack and needle)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        ("sadbutsad", "sad"),           # Found at beginning
        ("leetcode", "leeto"),          # Not found
        ("hello", "ll"),                # Found in middle
        ("a", "a"),                     # Single char match
        ("aaaaa", "bba"),               # No match
        ("mississippi", "issip"),       # Overlapping pattern
        ("aaa", "aaaa"),                # Needle longer than haystack
        ("abcabc", "cab"),              # Match in middle
        ("abababab", "abab"),           # Repeating pattern
    ]

    for haystack, needle in edge_cases:
        yield f"{json.dumps(haystack)}\n{json.dumps(needle)}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        haystack_len = random.randint(10, 500)
        needle_len = random.randint(1, min(haystack_len, 50))

        # Sometimes ensure needle is in haystack
        if random.random() < 0.7:
            # Generate haystack, then pick substring as needle
            haystack = _generate_random_string(haystack_len)
            start = random.randint(0, haystack_len - needle_len)
            needle = haystack[start:start + needle_len]
        else:
            # Completely random (may not match)
            haystack = _generate_random_string(haystack_len)
            needle = _generate_random_string(needle_len)

        yield f"{json.dumps(haystack)}\n{json.dumps(needle)}"


def _generate_random_string(size: int) -> str:
    """Generate a random lowercase string."""
    return ''.join(random.choices(string.ascii_lowercase, k=size))


# ============================================================================
# Complexity Estimation (controlled size)
# ============================================================================

def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For this problem:
    - Input size n is the length of haystack
    - needle is sqrt(n) to balance preprocessing and search

    Args:
        n: Length of the haystack string

    Returns:
        str: Two lines (haystack and needle)
    """
    n = max(1, n)
    haystack = _generate_random_string(n)

    # Needle length ~ sqrt(n) to balance complexity components
    needle_len = max(1, int(n ** 0.5))
    # Pick substring from haystack to ensure match
    start = random.randint(0, max(0, n - needle_len))
    needle = haystack[start:start + needle_len]

    return f"{json.dumps(haystack)}\n{json.dumps(needle)}"
