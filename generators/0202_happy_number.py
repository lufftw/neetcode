# generators/0202_happy_number.py
"""
Test Case Generator for Problem 0202 - Happy Number

LeetCode Constraints:
- 1 <= n <= 2^31 - 1

Time Complexity: O(log n) fast-slow pointers on digit sequence
"""
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Happy Number.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Single integer
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases (single integers)
    edge_cases = [19, 2, 1, 7]
    
    for n in edge_cases:
        yield str(n)
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        n = random.randint(1, 10000)
        yield str(n)


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.
    
    Args:
        n: The number to test
    
    Returns:
        str: Test input
    """
    n = max(1, n)
    return str(n)
