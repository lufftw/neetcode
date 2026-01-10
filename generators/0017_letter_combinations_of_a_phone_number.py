# generators/0017_letter_combinations_of_a_phone_number.py
"""
Test Case Generator for Problem 0017 - Letter Combinations of a Phone Number

LeetCode Constraints:
- 0 <= digits.length <= 4
- digits[i] is a digit in the range ['2', '9'].
"""
import json
import random
from typing import Iterator, Optional


# Valid digits for phone combinations (no 0 or 1)
VALID_DIGITS = '23456789'


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Letter Combinations.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input in JSON format (quoted string)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        "",         # Empty input
        "2",        # Single digit (3 letters)
        "7",        # Single digit (4 letters)
        "9",        # Single digit (4 letters)
        "23",       # LeetCode example
        "79",       # Two 4-letter digits (16 combinations)
        "234",      # Three digits
        "2345",     # Maximum length (4 digits)
        "7777",     # Same digit repeated
        "9999",     # Same digit repeated (4 letters each)
    ]

    for digits in edge_cases:
        yield json.dumps(digits, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case."""
    # Weighted towards shorter strings (more common in tests)
    length = random.choices(
        population=[0, 1, 2, 3, 4],
        weights=[1, 2, 3, 3, 2],
        k=1
    )[0]

    digits = ''.join(random.choice(VALID_DIGITS) for _ in range(length))
    return json.dumps(digits, separators=(',', ':'))


# ============================================
# Complexity Estimation (controlled size)
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Letter Combinations:
    - n is the number of digits
    - Output size grows exponentially: O(4^n)
    - LeetCode limits n to 4, so we scale accordingly

    Args:
        n: Target digit count (will be clamped to [0, 4])

    Returns:
        str: Test input (JSON quoted string)
    """
    # Clamp to LeetCode constraints
    n = max(0, min(n, 4))

    # Use digits with 4 letters (7, 9) for worst case
    if n == 0:
        digits = ""
    else:
        # Mix of 3-letter and 4-letter digits
        digits = ''.join(random.choice('79') for _ in range(n))

    return json.dumps(digits, separators=(',', ':'))


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}: {test}")
