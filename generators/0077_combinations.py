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
        str: Test input in the format: n\\nk
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        "4\n2",   # Classic example
        "1\n1",   # Minimal
        "5\n5",   # k equals n
        "5\n1",   # k equals 1
        "10\n3",  # Larger case
    ]
    
    for edge in edge_cases:
        yield edge
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case."""
    # Keep n reasonable to avoid explosion (C(20,10) is large)
    n = random.randint(1, 12)
    k = random.randint(1, n)
    return f"{n}\n{k}"

