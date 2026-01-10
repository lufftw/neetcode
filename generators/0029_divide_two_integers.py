"""
Test Case Generator for Problem 0029 - Divide Two Integers

LeetCode Constraints:
- -2^31 <= dividend, divisor <= 2^31 - 1
- divisor != 0
"""
import json
import random
from typing import Iterator, Optional


INT_MIN = -(2 ** 31)
INT_MAX = 2 ** 31 - 1


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        (10, 3),           # Basic positive
        (7, -3),           # Positive / negative
        (-7, 3),           # Negative / positive
        (-7, -3),          # Both negative
        (1, 1),            # Equal values
        (0, 1),            # Zero dividend
        (INT_MIN, -1),     # Overflow case -> clamp to INT_MAX
        (INT_MIN, 1),      # INT_MIN / 1
        (INT_MAX, 1),      # INT_MAX / 1
        (INT_MAX, 2),      # Large dividend
        (1, INT_MAX),      # Small dividend, large divisor
        (100, 3),          # Multiple iterations needed
    ]

    for dividend, divisor in edge_cases:
        yield f"{json.dumps(dividend)}\n{json.dumps(divisor)}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        # Mix of small and large values
        if random.random() < 0.3:
            # Large values near boundaries
            dividend = random.randint(INT_MIN, INT_MAX)
            divisor = random.choice([
                random.randint(1, 1000),
                random.randint(-1000, -1),
                random.randint(INT_MIN // 2, INT_MAX // 2)
            ])
        else:
            # Regular range
            dividend = random.randint(-10**9, 10**9)
            divisor = random.randint(-10**6, 10**6)

        # Ensure divisor is not zero
        if divisor == 0:
            divisor = 1

        yield f"{json.dumps(dividend)}\n{json.dumps(divisor)}"


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific dividend magnitude."""
    # n represents the magnitude of the dividend
    n = max(1, min(n, INT_MAX))

    dividend = random.choice([n, -n])
    divisor = random.randint(1, max(1, n // 1000)) * random.choice([1, -1])

    return f"{json.dumps(dividend)}\n{json.dumps(divisor)}"


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"--- Test {i} ---")
        print(test)
        print()
