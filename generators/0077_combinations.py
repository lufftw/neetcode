# generators/0077_combinations.py
"""
Test Case Generator for Problem 0077 - Combinations

LeetCode Constraints:
- 1 <= n <= 20
- 1 <= k <= n
"""
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Combinations.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility
    
    Yields:
        str: Canonical format - Line 1: n, Line 2: k
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases as (n, k) tuples
    edge_cases = [
        (4, 2),   # Classic example
        (1, 1),   # Minimal
        (5, 5),   # k equals n
        (5, 1),   # k equals 1
        (10, 3),  # Larger case
    ]
    
    for n, k in edge_cases:
        yield f"{n}\n{k}"
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case."""
    n = random.randint(1, 12)
    k = random.randint(1, n)
    return f"{n}\n{k}"
