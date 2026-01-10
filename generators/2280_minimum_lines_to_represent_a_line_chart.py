"""
Test Case Generator for Problem 2280 - Minimum Lines to Represent a Line Chart

LeetCode Constraints:
- 1 <= stockPrices.length <= 10^5
- 1 <= day_i, price_i <= 10^9
- All day_i distinct
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        ([[1, 7], [2, 6], [3, 5], [4, 4], [5, 4], [6, 3], [7, 2], [8, 1]],),  # Example 1
        ([[3, 4], [1, 2], [7, 8], [2, 3]],),                                  # Example 2
        ([[1, 1]],),                                                          # Single point
        ([[1, 1], [2, 2]],),                                                  # Two points
        ([[1, 1], [2, 3], [3, 2]],),                                          # V shape
        ([[1, 1], [2, 2], [3, 3], [4, 4]],),                                  # Straight line
    ]

    for args in edge_cases:
        yield json.dumps(args[0], separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        n = random.randint(3, 20)
        days = random.sample(range(1, 1000), n)
        prices = [random.randint(1, 1000) for _ in range(n)]
        stockPrices = [[d, p] for d, p in zip(days, prices)]
        yield json.dumps(stockPrices, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    n = max(2, min(n, 1000))
    days = random.sample(range(1, n * 10), n)
    prices = [random.randint(1, 10000) for _ in range(n)]
    stockPrices = [[d, p] for d, p in zip(days, prices)]
    return json.dumps(stockPrices, separators=(',', ':'))
