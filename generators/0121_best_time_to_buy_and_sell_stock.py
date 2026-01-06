"""
Test Generator for LeetCode 121: Best Time to Buy and Sell Stock
Pattern: DP 1D Linear - Running Min/Max (Kadane-Style)
"""

import json
import random
from typing import Iterator, List, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test cases for Best Time to Buy and Sell Stock.

    Constraints:
    - 1 <= prices.length <= 10^5
    - 0 <= prices[i] <= 10^4

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        Test case strings (one prices array per line)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [7, 1, 5, 3, 6, 4],           # Example 1: buy at 1, sell at 6
        [7, 6, 4, 3, 1],              # Example 2: decreasing, no profit
        [1],                          # Single day
        [1, 2],                       # Two days, profit
        [2, 1],                       # Two days, no profit
        [1, 2, 3, 4, 5],              # Always increasing
        [5, 4, 3, 2, 1],              # Always decreasing
        [3, 3, 3, 3],                 # All same
        [1, 10000],                   # Max profit possible
        [0, 0, 0, 0],                 # All zeros
    ]

    for prices in edge_cases:
        if count <= 0:
            break
        yield json.dumps(prices, separators=(",", ":"))
        count -= 1

    # Random cases
    while count > 0:
        n = random.randint(1, 100)
        prices = [random.randint(0, 10000) for _ in range(n)]
        yield json.dumps(prices, separators=(",", ":"))
        count -= 1


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific size n for complexity estimation.

    Args:
        n: Size of the prices array

    Returns:
        Test case string
    """
    n = max(1, min(n, 100000))
    prices = [random.randint(0, 10000) for _ in range(n)]
    return json.dumps(prices, separators=(",", ":"))


if __name__ == "__main__":
    for case in generate(5, seed=42):
        print(case)
