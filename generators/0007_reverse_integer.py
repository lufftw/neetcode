# generators/0007_reverse_integer.py
"""
Test Case Generator for Problem 0007 - Reverse Integer

LeetCode Constraints:
- -2^31 <= x <= 2^31 - 1
"""
import random
from typing import Iterator, Optional

INT_MAX = 2**31 - 1
INT_MIN = -(2**31)


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Reverse Integer."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        123,          # Basic positive
        -123,         # Basic negative
        120,          # Trailing zero
        0,            # Zero
        1534236469,   # Overflow case
        -2147483648,  # INT_MIN
        2147483647,   # INT_MAX
        10,           # Simple trailing zero
        -10,          # Negative trailing zero
    ]

    for x in edge_cases:
        yield str(x)
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate random integer within 32-bit range."""
    # Mix of different magnitudes
    choice = random.random()
    if choice < 0.3:
        # Small numbers
        x = random.randint(-1000, 1000)
    elif choice < 0.6:
        # Medium numbers
        x = random.randint(-1000000, 1000000)
    elif choice < 0.9:
        # Large numbers (potential overflow when reversed)
        x = random.randint(-INT_MAX, INT_MAX)
    else:
        # Numbers near overflow boundary
        x = random.choice([
            random.randint(1000000000, INT_MAX),
            random.randint(INT_MIN, -1000000000),
        ])

    return str(x)


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with n-digit number for complexity estimation.
    """
    n = max(1, min(n, 10))  # Max 10 digits for 32-bit
    if n == 1:
        return str(random.randint(1, 9))

    # Generate n-digit number
    first_digit = random.randint(1, 9)
    other_digits = "".join(str(random.randint(0, 9)) for _ in range(n - 1))
    x = int(str(first_digit) + other_digits)

    # Keep within 32-bit bounds
    x = min(x, INT_MAX)

    # Random sign
    if random.random() < 0.5:
        x = -x

    return str(x)


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}: {test}")
