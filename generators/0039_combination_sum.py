# generators/0039_combination_sum.py
"""
Test Case Generator for Problem 0039 - Combination Sum

LeetCode Constraints:
- 1 <= candidates.length <= 30
- 2 <= candidates[i] <= 40
- All elements of candidates are distinct
- 1 <= target <= 40
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Combination Sum.
    
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
        ([2, 3, 6, 7], 7),     # Classic example
        ([2, 3, 5], 8),        # Multiple combinations
        ([2], 1),              # No solution
        ([7, 8, 9], 7),        # Single element solution
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
    """Generate a single random test case."""
    n = random.randint(2, 15)
    candidates = random.sample(range(2, 41), min(n, 39))
    min_candidate = min(candidates)
    target = random.randint(min_candidate, 40)
    return f"{json.dumps(candidates, separators=(',', ':'))}\n{target}"
