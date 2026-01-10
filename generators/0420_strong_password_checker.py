"""
Test Case Generator for Problem 0420 - Strong Password Checker

LeetCode Constraints:
- 1 <= password.length <= 50
- password consists of letters, digits, dot '.' or exclamation mark '!'.

Valid characters: a-z, A-Z, 0-9, '.', '!'
"""
import json
import random
import string
from typing import Iterator, Optional


# Valid character set per problem constraints
VALID_CHARS = string.ascii_letters + string.digits + ".!"


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Strong Password Checker.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: JSON-formatted password string
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # Length edge cases
        "a",                          # Single char, missing types, too short
        "aA1",                        # All types but too short
        "aA1aA1",                     # Exactly length 6, all types
        "1337C0d3",                   # Already strong
        "a" * 20,                     # Max valid length, single char type, repeats
        "a" * 21,                     # Just over max length
        "a" * 50,                     # Max length constraint

        # Repeat edge cases
        "aaa",                        # Triple repeat, too short
        "aaaBBB",                     # Two triple repeats, no digit
        "aaaaaa",                     # Length 6 all same
        "aaaaaaBBBBBB",               # Two repeats of 6

        # Missing type cases
        "abcdef",                     # All lowercase, no upper/digit
        "ABCDEF",                     # All uppercase, no lower/digit
        "123456",                     # All digits, no letters

        # Complex cases
        "aaa111",                     # Repeats + missing uppercase
        "aaaB1",                      # Repeat + short
        "aaaaaaaaaaaaaaaaaaaaa",      # 21 chars, delete needed
        "aaaaaaaaaaaaaaaaaaaaaaaaaaa", # 27 chars, many deletes
        "aA1" + "b" * 18,             # Length 21, one delete needed
    ]

    for case in edge_cases:
        yield json.dumps(case, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases with various characteristics
    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a single random test case."""
    # Choose length distribution biased toward interesting cases
    length_type = random.choice([
        "too_short",    # 1-5
        "valid",        # 6-20
        "too_long",     # 21-50
    ])

    if length_type == "too_short":
        length = random.randint(1, 5)
    elif length_type == "valid":
        length = random.randint(6, 20)
    else:
        length = random.randint(21, 50)

    # Decide whether to include repeats
    include_repeats = random.random() < 0.5

    if include_repeats:
        password = _generate_with_repeats(length)
    else:
        password = _generate_diverse(length)

    return json.dumps(password, separators=(',', ':'))


def _generate_with_repeats(length: int) -> str:
    """Generate password with intentional repeat sequences."""
    chars = []
    remaining = length

    while remaining > 0:
        # Choose a random character
        char = random.choice(VALID_CHARS)

        # Decide repeat length (sometimes create 3+ repeats)
        if random.random() < 0.4:
            repeat_len = random.randint(3, min(6, remaining))
        else:
            repeat_len = random.randint(1, min(3, remaining))

        chars.extend([char] * repeat_len)
        remaining -= repeat_len

    return ''.join(chars[:length])


def _generate_diverse(length: int) -> str:
    """Generate password with diverse characters (fewer repeats)."""
    return ''.join(random.choices(VALID_CHARS, k=length))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Strong Password Checker:
    - n is the password length
    - Constrained to [1, 50] per problem

    Args:
        n: Target password length

    Returns:
        str: Test input (JSON string)
    """
    # Clamp to valid range
    n = max(1, min(n, 50))

    # Generate a challenging case with repeats
    password = _generate_with_repeats(n)

    return json.dumps(password, separators=(',', ':'))


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(10, seed=42), 1):
        print(f"Test {i}: {test}")
