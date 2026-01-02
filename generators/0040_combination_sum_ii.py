# generators/0040_combination_sum_ii.py
"""
Test Case Generator for Problem 0040 - Combination Sum II

LeetCode Constraints:
- 1 <= candidates.length <= 100
- 1 <= candidates[i] <= 50
- 1 <= target <= 30
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Combination Sum II.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility
    
    Yields:
        str: Canonical JSON format - Line 1: candidates array, Line 2: target
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases as (candidates, target) tuples
    edge_cases = [
        ([10, 1, 2, 7, 6, 1, 5], 8),  # Classic with duplicates
        ([2, 5, 2, 1, 2], 5),          # Multiple duplicates
        ([1, 1, 1, 1, 1], 3),          # All same
        ([2], 1),                      # No solution
    ]
    
    for candidates, target in edge_cases:
        yield f"{json.dumps(candidates, separators=(',', ':'))}\n{target}"
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case with possible duplicates."""
    n = random.randint(2, 20)
    candidates = [random.randint(1, 50) for _ in range(n)]
    target = random.randint(1, 30)
    return f"{json.dumps(candidates, separators=(',', ':'))}\n{target}"
