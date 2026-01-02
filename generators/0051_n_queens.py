# generators/0051_n_queens.py
"""
Test Case Generator for Problem 0051 - N-Queens

LeetCode Constraints:
- 1 <= n <= 9
"""
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for N-Queens.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Single integer n
    """
    min_n = 1
    max_n = 9
    
    if seed is not None:
        random.seed(seed)
    
    # Edge cases (known important values)
    edge_cases = [1, 4, 8, 9]
    
    for n in edge_cases:
        yield str(n)
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        n = random.choices(
            population=range(min_n, max_n + 1),
            weights=[1, 1, 2, 3, 4, 5, 6, 7, 8],
            k=1
        )[0]
        yield str(n)


def generate_all_sizes() -> Iterator[str]:
    """Generate one test case for each possible n value."""
    for n in range(1, 10):
        yield str(n)
