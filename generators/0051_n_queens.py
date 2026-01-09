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


# ============================================
# Complexity Estimation (controlled size)
# ============================================

def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For N-Queens:
    - Input size n is the board size
    - Time complexity is O(N!) due to backtracking
    - Solution counts grow fast:
      - n=8:  92 solutions
      - n=9:  352 solutions
      - n=10: 724 solutions
      - n=11: 2,680 solutions
      - n=12: 14,200 solutions
      - n=13: 73,712 solutions

    Note: We use smaller n than typical problems (n=5000) because
    factorial-like growth makes large n infeasible.

    Args:
        n: Size parameter (will be scaled down for factorial problems)

    Returns:
        str: Test input (single integer n)
    """
    # Scale n for factorial complexity
    # n=5000 in other problems -> n=12-13 for N-Queens (similar runtime ~2-5s)
    if n >= 5000:
        scaled_n = 13  # ~73K solutions, ~2-5 seconds
    elif n >= 1000:
        scaled_n = 12  # ~14K solutions
    elif n >= 500:
        scaled_n = 11  # ~2.7K solutions
    elif n >= 100:
        scaled_n = 10  # 724 solutions
    else:
        scaled_n = max(1, min(n, 10))

    return str(scaled_n)
