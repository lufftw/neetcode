"""
Test Generator for LeetCode 518: Coin Change 2
Pattern: DP Knapsack/Subset - Unbounded Knapsack Count Combinations
"""

import json
import random
from typing import Iterator, List, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test cases for Coin Change 2.

    Constraints:
    - 1 <= coins.length <= 300
    - 1 <= coins[i] <= 5000
    - 0 <= amount <= 5000

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        Test case strings (amount on line 1, coins on line 2)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        (5, [1, 2, 5]),               # 4 ways
        (3, [2]),                      # 0 ways (impossible)
        (10, [10]),                    # 1 way
        (0, [7]),                      # 1 way (empty set)
        (5, [1, 5]),                   # 2 ways
        (100, [1, 5, 10, 25]),         # Many ways
        (4, [1, 2, 3]),                # 4 ways: 1111, 112, 22, 13
        (1, [1, 2]),                   # 1 way
    ]

    for amount, coins in edge_cases:
        if count <= 0:
            break
        yield f"{amount}\n{json.dumps(coins, separators=(',', ':'))}"
        count -= 1

    # Random cases
    while count > 0:
        n = random.randint(1, 10)
        coins = list(set(random.randint(1, 100) for _ in range(n)))
        if not coins:
            coins = [1]
        amount = random.randint(0, 200)
        yield f"{amount}\n{json.dumps(coins, separators=(',', ':'))}"
        count -= 1


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific amount n."""
    coins = [1, 2, 5, 10]
    return f"{n}\n{json.dumps(coins, separators=(',', ':'))}"


if __name__ == "__main__":
    for case in generate(5, seed=42):
        print(case)
        print("---")
