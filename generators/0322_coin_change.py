"""
Test Generator for LeetCode 322: Coin Change
Pattern: DP Knapsack/Subset - Unbounded Knapsack Minimum
"""

import json
import random
from typing import Iterator, List, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test cases for Coin Change.

    Constraints:
    - 1 <= coins.length <= 12
    - 1 <= coins[i] <= 2^31 - 1
    - 0 <= amount <= 10^4

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        Test case strings (coins on line 1, amount on line 2)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        ([1, 2, 5], 11),              # 3 coins: 5+5+1
        ([2], 3),                      # Impossible
        ([1], 0),                      # Zero amount
        ([1], 1),                      # Single coin single amount
        ([1, 2, 5], 100),             # Larger amount
        ([2, 5, 10, 1], 27),          # Multiple denominations
        ([186, 419, 83, 408], 6249),  # Tricky case
        ([1], 10),                    # Only 1s
    ]

    for coins, amount in edge_cases:
        if count <= 0:
            break
        yield f"{json.dumps(coins, separators=(',', ':'))}\n{amount}"
        count -= 1

    # Random cases
    while count > 0:
        n = random.randint(1, 8)
        coins = list(set(random.randint(1, 100) for _ in range(n)))
        if not coins:
            coins = [1]
        amount = random.randint(0, 500)
        yield f"{json.dumps(coins, separators=(',', ':'))}\n{amount}"
        count -= 1


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific amount n."""
    coins = [1, 2, 5, 10, 25]
    return f"{json.dumps(coins, separators=(',', ':'))}\n{n}"


if __name__ == "__main__":
    for case in generate(5, seed=42):
        print(case)
        print("---")
