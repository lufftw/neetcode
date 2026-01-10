"""
Test Case Generator for Problem 0008 - String to Integer (atoi)

LeetCode Constraints:
- 0 <= s.length <= 200
- s consists of letters, digits (0-9), ' ', '+', '-', and '.'.
"""
import json
import random
import string
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        "42",                    # Basic positive
        "   -42",                # Leading spaces + negative
        "4193 with words",       # Digits then text
        "words and 987",         # Text first (returns 0)
        "-91283472332",          # Overflow negative
        "91283472332",           # Overflow positive
        "+1",                    # Explicit positive
        "  +0 123",              # Zero with sign
        "",                      # Empty string
        "   ",                   # Only spaces
        "-",                     # Only minus
        "+",                     # Only plus
        "+-12",                  # Invalid double sign
        "00000-42a1234",         # Leading zeros
        "-2147483648",           # INT_MIN
        "2147483647",            # INT_MAX
        "  0000000000012345678", # Many leading zeros
        ".1",                    # Dot before digit
        "3.14159",               # Float-like
        "  -0012a42",            # Complex case
    ]

    for case in edge_cases:
        yield json.dumps(case, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        case_type = random.choice([
            'normal', 'overflow', 'garbage', 'spaces', 'mixed'
        ])

        if case_type == 'normal':
            # Normal valid number
            sign = random.choice(['', '+', '-'])
            num = ''.join(random.choices(string.digits, k=random.randint(1, 10)))
            s = sign + num
        elif case_type == 'overflow':
            # Large number that overflows
            sign = random.choice(['+', '-', ''])
            num = ''.join(random.choices(string.digits, k=random.randint(15, 20)))
            s = sign + num
        elif case_type == 'garbage':
            # Non-numeric start
            s = ''.join(random.choices(string.ascii_letters + '.', k=random.randint(3, 10)))
        elif case_type == 'spaces':
            # Leading spaces
            spaces = ' ' * random.randint(1, 5)
            sign = random.choice(['', '+', '-'])
            num = ''.join(random.choices(string.digits, k=random.randint(1, 5)))
            s = spaces + sign + num
        else:
            # Mixed valid + garbage
            sign = random.choice(['', '+', '-'])
            num = ''.join(random.choices(string.digits, k=random.randint(1, 5)))
            garbage = ''.join(random.choices(string.ascii_letters + ' .', k=random.randint(3, 10)))
            s = sign + num + garbage

        yield json.dumps(s, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific length."""
    n = max(1, min(n, 200))

    # Create a string of length n with mostly digits
    sign = random.choice(['', '+', '-'])
    digit_len = n - len(sign)
    num = ''.join(random.choices(string.digits, k=max(1, digit_len)))
    s = sign + num[:n - len(sign)]

    return json.dumps(s, separators=(',', ':'))


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"--- Test {i} ---")
        print(test)
        print()
