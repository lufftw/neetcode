# generators/1011_capacity_to_ship_packages_within_d_days.py
"""
Test Case Generator for Problem 1011 - Capacity To Ship Packages Within D Days

LeetCode Constraints:
- 1 <= days <= weights.length <= 5 * 10^4
- 1 <= weights[i] <= 500

Time Complexity: O(n log S) where S = sum(weights)
"""
import json
import random
from typing import Iterator, Optional


# ============================================
# Random Test Generation (for functional testing)
# ============================================

def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Capacity To Ship Packages Within D Days.

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
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5),  # Example 1
        ([3, 2, 2, 4, 1, 4], 3),                # Example 2
        ([1, 2, 3, 1, 1], 4),                   # Example 3
        ([1], 1),                               # Single package
        ([500], 1),                             # Max weight single package
        ([1, 1, 1, 1, 1], 5),                   # Each package on separate day
        ([1, 1, 1, 1, 1], 1),                   # All packages in one day
    ]

    for weights, days in edge_cases:
        yield f"{json.dumps(weights, separators=(',', ':'))}\n{days}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """
    Generate a single test case with valid weights and days.
    """
    size = random.randint(1, 50000)

    # Generate random weights within constraints
    weights = [random.randint(1, 500) for _ in range(size)]

    # days must be between 1 and len(weights)
    days = random.randint(1, len(weights))

    return f"{json.dumps(weights, separators=(',', ':'))}\n{days}"


# ============================================
# Complexity Estimation (controlled size)
# ============================================

def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    Args:
        n: Size of weights array

    Returns:
        str: Test input with weights.length = n
    """
    n = max(1, min(n, 50000))  # Clamp to valid range

    weights = [random.randint(1, 500) for _ in range(n)]
    days = random.randint(1, len(weights))

    return f"{json.dumps(weights, separators=(',', ':'))}\n{days}"
