# generators/0875_koko_eating_bananas.py
"""
Test Case Generator for Problem 0875 - Koko Eating Bananas

LeetCode Constraints:
- 1 <= piles.length <= 10^4
- piles.length <= h <= 10^9
- 1 <= piles[i] <= 10^9

Time Complexity: O(n log m) where m = max(piles)
"""
import json
import random
from typing import Iterator, Optional


# ============================================
# Random Test Generation (for functional testing)
# ============================================

def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Koko Eating Bananas.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input in the same format as .in files
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first (matching LeetCode examples)
    edge_cases = [
        ([3, 6, 7, 11], 8),       # Example 1
        ([30, 11, 23, 4, 20], 5), # Example 2: h == piles.length
        ([30, 11, 23, 4, 20], 6), # Example 3
        ([1], 1),                  # Single pile, h = n
        ([1000000000], 2),        # Large pile
        ([1, 1, 1, 1], 4),        # All same, minimal h
    ]

    for piles, h in edge_cases:
        yield f"{json.dumps(piles, separators=(',', ':'))}\n{h}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """
    Generate a single test case with valid piles and h.
    """
    size = random.randint(1, 10000)
    max_pile = 10**6  # Use smaller max for practical testing

    # Generate random piles
    piles = [random.randint(1, max_pile) for _ in range(size)]

    # h must be >= len(piles) (need at least one hour per pile)
    # Use reasonable range for h
    min_h = len(piles)
    max_h = min(sum(piles), 10**7)  # Cap at reasonable value
    h = random.randint(min_h, max(min_h, max_h))

    return f"{json.dumps(piles, separators=(',', ':'))}\n{h}"


# ============================================
# Complexity Estimation (controlled size)
# ============================================

def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    Args:
        n: Size of piles array

    Returns:
        str: Test input with piles.length = n
    """
    n = max(1, min(n, 10000))  # Clamp to valid range

    max_pile = 10**6
    piles = [random.randint(1, max_pile) for _ in range(n)]

    min_h = len(piles)
    max_h = min(sum(piles), 10**7)
    h = random.randint(min_h, max(min_h, max_h))

    return f"{json.dumps(piles, separators=(',', ':'))}\n{h}"
