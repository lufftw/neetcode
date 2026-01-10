# generators/0066_plus_one.py
"""
Test Case Generator for Problem 0066 - Plus One

LeetCode Constraints:
- 1 <= digits.length <= 100
- 0 <= digits[i] <= 9
- digits does not contain any leading 0's
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Plus One."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        [0],  # Single zero
        [9],  # Single nine -> carry
        [1, 2, 3],  # No carry
        [9, 9, 9],  # All nines -> expand
        [1, 9, 9],  # Partial carry
    ]

    for digits in edge_cases:
        yield json.dumps(digits)
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random digits array."""
    n = random.randint(1, 20)
    # First digit cannot be 0 (unless single digit)
    digits = [random.randint(1, 9)] if n > 1 else [random.randint(0, 9)]
    for _ in range(n - 1):
        digits.append(random.randint(0, 9))
    return json.dumps(digits)


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with n digits for complexity estimation.
    """
    n = max(1, min(n, 100))
    digits = [random.randint(1, 9)]
    for _ in range(n - 1):
        digits.append(random.randint(0, 9))
    return json.dumps(digits)


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        digits = json.loads(test)
        print(f"Test {i}: {digits}")
