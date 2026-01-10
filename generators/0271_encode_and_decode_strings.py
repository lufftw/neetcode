# generators/0271_encode_and_decode_strings.py
"""
Test Case Generator for Problem 0271 - Encode and Decode Strings

LeetCode Constraints:
- Strings may contain any ASCII character
- Algorithm must be stateless
"""
import json
import random
import string
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Encode and Decode Strings."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        ["Hello", "World"],           # Basic
        [""],                          # Empty string
        [],                            # Empty list
        ["a#b", "c#d"],               # Contains delimiter
        ["123", "456"],               # Numeric strings
        ["a", "b", "c"],              # Single chars
        ["abc\ndef", "ghi\tjkl"],     # Special whitespace
    ]

    for strs in edge_cases:
        yield json.dumps(strs, separators=(",", ":"))
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate random list of strings."""
    num_strings = random.randint(1, 10)
    strs = []

    for _ in range(num_strings):
        length = random.randint(0, 20)
        # Include various characters including potential delimiters
        chars = string.ascii_letters + string.digits + "#:,./\\;'[]{}!@$%^&*()"
        s = "".join(random.choices(chars, k=length))
        strs.append(s)

    return json.dumps(strs, separators=(",", ":"))


def generate_for_complexity(n: int) -> str:
    """Generate test case with n strings for complexity estimation."""
    n = max(1, min(n, 1000))
    strs = []

    for _ in range(n):
        length = random.randint(1, 50)
        chars = string.ascii_letters + string.digits
        strs.append("".join(random.choices(chars, k=length)))

    return json.dumps(strs, separators=(",", ":"))


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}: {test}")
