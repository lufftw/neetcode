# generators/0022_generate_parentheses.py
"""
Test Case Generator for Problem 0022 - Generate Parentheses

LeetCode Constraints:
- 1 <= n <= 8

The output is the n-th Catalan number of valid parentheses strings.
Catalan numbers: 1, 1, 2, 5, 14, 42, 132, 429, 1430, ...
"""
import json
import random
from typing import Iterator, Optional


# Catalan numbers for n = 0 to 8
CATALAN = [1, 1, 2, 5, 14, 42, 132, 429, 1430]


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Generate Parentheses.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (integer as string)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first - test all values from 1 to 8
    edge_cases = [1, 2, 3, 4, 5, 6, 7, 8]

    for n in edge_cases:
        yield str(n)
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield str(random.randint(1, 8))


# ============================================
# Complexity Estimation (controlled size)
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Generate Parentheses:
    - n is the number of pairs
    - Output size is Catalan(n) which grows exponentially
    - LeetCode limits n to 8

    Args:
        n: Target number of pairs

    Returns:
        str: Test input
    """
    # Clamp to LeetCode constraints
    n = max(1, min(n, 8))
    return str(n)


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}: n = {test}, expected output count = {CATALAN[int(test)]}")
