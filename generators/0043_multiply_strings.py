# generators/0043_multiply_strings.py
"""
Test Case Generator for Problem 0043 - Multiply Strings

LeetCode Constraints:
- 1 <= num1.length, num2.length <= 200
- num1 and num2 consist of digits only
- Both num1 and num2 do not contain any leading zero, except "0" itself
"""
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Multiply Strings."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        ("0", "0"),
        ("0", "123"),
        ("1", "1"),
        ("9", "9"),
        ("99", "99"),
        ("123", "456"),
    ]

    for num1, num2 in edge_cases:
        yield f"{num1}\n{num2}"
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random test case."""
    len1 = random.randint(1, 20)
    len2 = random.randint(1, 20)

    # Generate random numbers without leading zeros
    num1 = _random_number_string(len1)
    num2 = _random_number_string(len2)

    return f"{num1}\n{num2}"


def _random_number_string(length: int) -> str:
    """Generate a random number string without leading zeros."""
    if length == 1:
        return str(random.randint(0, 9))

    # First digit cannot be 0
    digits = [str(random.randint(1, 9))]
    for _ in range(length - 1):
        digits.append(str(random.randint(0, 9)))

    return "".join(digits)


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with strings of length approximately sqrt(n).

    The multiplication is O(m*n), so total operations ~ n.
    """
    n = max(1, min(n, 40000))  # Max 200 * 200

    side = int(n ** 0.5)
    len1 = max(1, min(side, 200))
    len2 = max(1, min(n // len1, 200))

    num1 = _random_number_string(len1)
    num2 = _random_number_string(len2)

    return f"{num1}\n{num2}"


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}:")
        print(test)
        print()
