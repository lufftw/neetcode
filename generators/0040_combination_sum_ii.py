# generators/0040_combination_sum_ii.py
"""
Test Case Generator for Problem 0040 - Combination Sum II

LeetCode Constraints:
- 1 <= candidates.length <= 100
- 1 <= candidates[i] <= 50
- 1 <= target <= 30
"""
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Combination Sum II.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility
    
    Yields:
        str: Test input in the format: candidates\\ntarget
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        "10,1,2,7,6,1,5\n8",   # Classic with duplicates
        "2,5,2,1,2\n5",        # Multiple duplicates
        "1,1,1,1,1\n3",        # All same
        "2\n1",                # No solution
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
    """Generate a single random test case with possible duplicates."""
    # Random number of candidates (2-20 for reasonable test size)
    n = random.randint(2, 20)
    
    # Generate candidates with possible duplicates
    candidates = [random.randint(1, 50) for _ in range(n)]
    
    # Generate target in valid range
    target = random.randint(1, 30)
    
    candidates_str = ','.join(map(str, candidates))
    return f"{candidates_str}\n{target}"

