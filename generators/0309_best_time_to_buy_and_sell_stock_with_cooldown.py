# generators/0309_best_time_to_buy_and_sell_stock_with_cooldown.py
"""
Test Case Generator for Problem 0309 - Best Time to Buy and Sell Stock with Cooldown

LeetCode Constraints:
- 1 <= prices.length <= 5000
- 0 <= prices[i] <= 1000
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Best Time to Buy and Sell Stock with Cooldown.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (prices as JSON array)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # LeetCode Example 1
        [1, 2, 3, 0, 2],
        # LeetCode Example 2: single element
        [1],
        # Two elements: can make profit
        [1, 2],
        # Two elements: no profit
        [2, 1],
        # Strictly increasing (optimal: buy first, sell last with cooldowns)
        [1, 2, 3, 4, 5],
        # Strictly decreasing (no profit possible)
        [5, 4, 3, 2, 1],
        # All same price
        [5, 5, 5, 5, 5],
        # Alternating pattern
        [1, 5, 1, 5, 1, 5],
    ]

    for prices in edge_cases:
        yield json.dumps(prices, separators=(",", ":"))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random prices array."""
    n = random.randint(5, 100)
    prices = [random.randint(0, 100) for _ in range(n)]
    return json.dumps(prices, separators=(",", ":"))


# ============================================
# Complexity Estimation
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Best Time to Buy and Sell Stock with Cooldown:
    - n is the number of days (prices array length)
    - Time complexity is O(n)

    Args:
        n: Number of days (will be clamped to [1, 5000])

    Returns:
        str: Test input (prices as JSON array)
    """
    # Clamp to LeetCode constraints
    n = max(1, min(n, 5000))

    # Generate random prices
    prices = [random.randint(0, 1000) for _ in range(n)]
    return json.dumps(prices, separators=(",", ":"))


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(5, seed=42), 1):
        prices = json.loads(test)
        print(f"Test {i}: {len(prices)} days")
        if len(prices) <= 15:
            print(f"  prices: {prices}")
        print()
