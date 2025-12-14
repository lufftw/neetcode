# generators/0039_combination_sum.py
"""
Test Case Generator for Problem 0039 - Combination Sum

LeetCode Constraints:
- 1 <= candidates.length <= 30
- 2 <= candidates[i] <= 40
- All elements of candidates are distinct
- 1 <= target <= 40
"""
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Combination Sum.
    
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
        "2,3,6,7\n7",        # Classic example
        "2,3,5\n8",          # Multiple combinations
        "2\n1",              # No solution
        "7,8,9\n7",          # Single element solution
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
    # Random number of candidates (2-15 for reasonable test size)
    n = random.randint(2, 15)
    
    # Generate distinct candidates in range [2, 40]
    candidates = random.sample(range(2, 41), min(n, 39))
    
    # Generate target that is likely achievable
    min_candidate = min(candidates)
    target = random.randint(min_candidate, 40)
    
    candidates_str = ','.join(map(str, candidates))
    return f"{candidates_str}\n{target}"

