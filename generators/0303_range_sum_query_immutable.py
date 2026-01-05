# generators/0303_range_sum_query_immutable.py
"""
Test Case Generator for Problem 0303 - Range Sum Query - Immutable

LeetCode Constraints:
- 1 <= nums.length <= 10^4
- -10^5 <= nums[i] <= 10^5
- 0 <= left <= right < nums.length
- At most 10^4 calls will be made to sumRange

Time Complexity: O(n) preprocessing, O(1) per query
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Range Sum Query - Immutable.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Test input in JSON format (commands, args)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # Classic example
        ([-2, 0, 3, -5, 2, -1], [(0, 2), (2, 5), (0, 5)]),
        # Single element
        ([5], [(0, 0)]),
        # All same values
        ([1, 1, 1, 1], [(0, 3), (1, 2), (0, 0)]),
        # Negative numbers
        ([-5, -3, -1], [(0, 2), (0, 1), (1, 2)]),
        # Large values
        ([100000, -100000, 100000], [(0, 2), (0, 1), (1, 2)]),
    ]

    for nums, queries in edge_cases:
        yield _format_case(nums, queries)
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _format_case(nums: list, queries: list) -> str:
    """Format a test case as JSON input."""
    commands = ["NumArray"] + ["sumRange"] * len(queries)
    args = [[nums]] + [[left, right] for left, right in queries]
    return f"{json.dumps(commands, separators=(',', ':'))}\n{json.dumps(args, separators=(',', ':'))}"


def _generate_random_case() -> str:
    """Generate a single random test case."""
    # Random array size (avoid very large for testing)
    n = random.randint(1, 500)
    nums = [random.randint(-10000, 10000) for _ in range(n)]

    # Random queries
    num_queries = random.randint(1, 100)
    queries = []
    for _ in range(num_queries):
        left = random.randint(0, n - 1)
        right = random.randint(left, n - 1)
        queries.append((left, right))

    return _format_case(nums, queries)


def generate_for_complexity(n: int, q: int = 100) -> str:
    """Generate test case with specific size for complexity estimation."""
    nums = [random.randint(-10000, 10000) for _ in range(n)]
    queries = []
    for _ in range(q):
        left = random.randint(0, n - 1)
        right = random.randint(left, n - 1)
        queries.append((left, right))
    return _format_case(nums, queries)
