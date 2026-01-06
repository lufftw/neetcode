"""
Test Generator for LeetCode 746: Min Cost Climbing Stairs
Pattern: DP 1D Linear - Min Cost Path
"""

import json
import random
from typing import Iterator, List, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test cases for Min Cost Climbing Stairs.

    Constraints:
    - 2 <= cost.length <= 1000
    - 0 <= cost[i] <= 999

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        Test case strings (one cost array per line)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [10, 15],                     # Minimum length
        [10, 15, 20],                 # Length 3
        [1, 100, 1, 1, 1, 100, 1, 1, 100, 1],  # Alternating
        [0, 0, 0, 0],                 # All zeros
        [999, 999, 999],              # All max values
        [1, 2, 3, 4, 5],              # Increasing
        [5, 4, 3, 2, 1],              # Decreasing
    ]

    for cost in edge_cases:
        if count <= 0:
            break
        yield json.dumps(cost, separators=(",", ":"))
        count -= 1

    # Random cases
    while count > 0:
        n = random.randint(2, 100)  # Keep reasonable for tests
        cost = [random.randint(0, 999) for _ in range(n)]
        yield json.dumps(cost, separators=(",", ":"))
        count -= 1


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific size n for complexity estimation.

    Args:
        n: Size of the cost array

    Returns:
        Test case string
    """
    n = max(2, min(n, 1000))
    cost = [random.randint(0, 999) for _ in range(n)]
    return json.dumps(cost, separators=(",", ":"))


if __name__ == "__main__":
    for case in generate(5, seed=42):
        print(case)
