# generators/0901_online_stock_span.py
"""
Test Case Generator for Problem 0901 - Online Stock Span

LeetCode Constraints:
- 1 <= price <= 10^5
- At most 10^4 calls will be made to next

Time Complexity: O(1) amortized per call with monotonic stack
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Online Stock Span.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Test input in LeetCode method call format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [100, 80, 60, 70, 60, 75, 85],  # Classic example
        [100],                           # Single call
        [50, 50, 50, 50],                # All equal
        [10, 20, 30, 40, 50],            # Increasing
        [50, 40, 30, 20, 10],            # Decreasing
        [1, 100000],                     # Min to max
    ]

    for prices in edge_cases:
        methods = ["StockSpanner"] + ["next"] * len(prices)
        args = [[]] + [[p] for p in prices]
        yield f"{json.dumps(methods)}\n{json.dumps(args)}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        num_calls = random.randint(1, 5000)
        yield _generate_case(num_calls)


def _generate_case(num_calls: int) -> str:
    """Generate a single random test case."""
    prices = [random.randint(1, 10**5) for _ in range(num_calls)]
    methods = ["StockSpanner"] + ["next"] * num_calls
    args = [[]] + [[p] for p in prices]
    return f"{json.dumps(methods)}\n{json.dumps(args)}"


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific input size for complexity estimation."""
    n = max(1, n)
    return _generate_case(n)
