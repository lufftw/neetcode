# generators/0052_n_queens_ii.py
"""
Test Case Generator for Problem 0052 - N-Queens II

LeetCode Constraints:
- 1 <= n <= 9
"""
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for N-Queens II.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility
    
    Yields:
        str: Test input - a single integer n
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first (all valid n values)
    edge_cases = ["1", "4", "8", "9"]
    
    for edge in edge_cases:
        yield edge
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        n = random.randint(1, 9)
        yield str(n)

