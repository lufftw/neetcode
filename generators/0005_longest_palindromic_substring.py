# generators/0005_longest_palindromic_substring.py
"""
Test Case Generator for Problem 0005 - Longest Palindromic Substring

LeetCode Constraints:
- 1 <= s.length <= 1000
- s consist of only digits and English letters.
"""
import json
import random
import string
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Longest Palindromic Substring.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input in JSON format (quoted string)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first (as data, not strings)
    edge_cases = [
        "a",                    # Single character
        "aa",                   # Two same characters
        "ab",                   # Two different characters
        "aba",                  # Odd-length palindrome
        "abba",                 # Even-length palindrome
        "cbbd",                 # LeetCode example 2
        "babad",                # LeetCode example 1
        "racecar",              # Classic palindrome
        "abcdefg",              # No palindrome longer than 1
        "aaaaaa",               # All same characters
        "abcba",                # Full string is palindrome
        "xabay",                # Hint test case
    ]

    for s in edge_cases:
        yield json.dumps(s, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case."""
    # Weighted distribution: more medium-sized strings
    length = random.choices(
        population=[1, 2, 5, 10, 50, 100, 500, 1000],
        weights=[1, 1, 2, 3, 4, 3, 2, 1],
        k=1
    )[0]

    # Mix of strategies for interesting cases
    strategy = random.choice([
        "random",           # Pure random string
        "with_palindrome",  # Insert a palindrome in random string
        "repeated_pattern", # Repeated patterns (creates multiple palindromes)
    ])

    if strategy == "random":
        s = _random_string(length)
    elif strategy == "with_palindrome":
        s = _string_with_palindrome(length)
    else:  # repeated_pattern
        s = _repeated_pattern_string(length)

    return json.dumps(s, separators=(',', ':'))


def _random_string(length: int) -> str:
    """Generate a random alphanumeric string."""
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def _string_with_palindrome(length: int) -> str:
    """Generate a string with a guaranteed palindrome."""
    if length <= 2:
        return _random_string(length)

    # Choose palindrome length (between 3 and length)
    pal_len = random.randint(3, min(length, 20))
    if pal_len % 2 == 0:
        half = _random_string(pal_len // 2)
        palindrome = half + half[::-1]
    else:
        half = _random_string(pal_len // 2)
        middle = random.choice(string.ascii_lowercase)
        palindrome = half + middle + half[::-1]

    # Insert palindrome at random position
    remaining = length - pal_len
    prefix_len = random.randint(0, remaining)
    suffix_len = remaining - prefix_len

    return _random_string(prefix_len) + palindrome + _random_string(suffix_len)


def _repeated_pattern_string(length: int) -> str:
    """Generate a string with repeated patterns."""
    pattern_len = random.randint(1, min(5, length))
    pattern = _random_string(pattern_len)
    repeats = length // pattern_len + 1
    return (pattern * repeats)[:length]


# ============================================
# Complexity Estimation (controlled size)
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Longest Palindromic Substring:
    - n is the length of the string
    - Expected complexity: O(n²) for expand/DP, O(n) for Manacher

    Args:
        n: Target string length

    Returns:
        str: Test input (JSON quoted string)
    """
    n = max(1, min(n, 1000))  # Clamp to LeetCode constraints

    # Generate string with embedded palindrome for interesting behavior
    if n <= 10:
        s = _random_string(n)
    else:
        # For larger n, insert a palindrome to make it non-trivial
        s = _string_with_palindrome(n)

    return json.dumps(s, separators=(',', ':'))


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}: {test}")
