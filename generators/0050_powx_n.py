# generators/0050_powx_n.py
"""
Test Case Generator for Problem 0050 - Pow(x, n)

LeetCode Constraints:
- -100.0 < x < 100.0
- -2^31 <= n <= 2^31 - 1
- -10^4 <= x^n <= 10^4
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Pow(x, n)."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        (2.0, 10),  # Simple power
        (2.1, 3),  # Floating point base
        (2.0, -2),  # Negative exponent
        (1.0, 1000000),  # Large exponent with base 1
        (0.0, 5),  # Zero base
    ]

    for x, n in edge_cases:
        yield f"{x}\n{n}"
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random x and n with valid result range."""
    # Keep x and n small to avoid overflow
    x = round(random.uniform(-10, 10), 5)
    if abs(x) < 0.1:
        x = random.choice([-1.0, 1.0, 2.0])

    # Limit n to keep result in range
    max_n = 20 if abs(x) > 1 else 100
    n = random.randint(-max_n, max_n)

    # Avoid 0^negative
    if x == 0 and n < 0:
        n = abs(n)

    return f"{x}\n{n}"


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with exponent n for complexity estimation.
    """
    n = max(-1000, min(n, 1000))
    x = 1.0001 if n > 0 else 0.9999
    return f"{x}\n{n}"


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        lines = test.split("\n")
        print(f"Test {i}: {lines[0]}^{lines[1]}")
