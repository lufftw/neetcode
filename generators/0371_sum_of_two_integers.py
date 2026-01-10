# generators/0371_sum_of_two_integers.py
"""
Test Case Generator for Problem 0371 - Sum of Two Integers

LeetCode Constraints:
- -1000 <= a, b <= 1000
"""
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Sum of Two Integers.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (two integers, one per line)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # LeetCode examples
        (1, 2),
        (2, 3),
        # Zero cases
        (0, 0),
        (5, 0),
        (0, -5),
        # Negative cases
        (-1, 1),
        (-5, -3),
        # Boundary cases
        (1000, -1000),
        (-1000, -1000),
        (1000, 1000),
    ]

    for a, b in edge_cases:
        yield f"{a}\n{b}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random pair of integers."""
    a = random.randint(-1000, 1000)
    b = random.randint(-1000, 1000)
    return f"{a}\n{b}"


# ============================================
# Complexity Estimation
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case for complexity estimation.

    For Sum of Two Integers:
    - n is not really applicable (constant time algorithm)
    - We just generate random integers within constraints

    Args:
        n: Not used meaningfully for this problem

    Returns:
        str: Test input
    """
    a = random.randint(-1000, 1000)
    b = random.randint(-1000, 1000)
    return f"{a}\n{b}"


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(5, seed=42), 1):
        lines = test.split("\n")
        a, b = int(lines[0]), int(lines[1])
        print(f"Test {i}: a={a}, b={b}, expected sum={a+b}")
