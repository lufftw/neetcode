"""
Test Case Generator for Problem 455 - Assign Cookies

LeetCode Constraints:
- 1 <= g.length <= 3 * 10^4
- 0 <= s.length <= 3 * 10^4
- 1 <= g[i], s[j] <= 2^31 - 1
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Test input in .in file format (g on line 1, s on line 2)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        ([1, 2, 3], [1, 1]),  # More children than cookies
        ([1, 2], [1, 2, 3]),  # More cookies than children
        ([1], [1]),  # Single child, single cookie, exact match
        ([2], [1]),  # Single child, cookie too small
        ([1], [2]),  # Single child, cookie larger than needed
        ([1, 1, 1], [1, 1, 1]),  # All equal
        ([1, 2, 3], [3, 2, 1]),  # All can be satisfied
        ([10, 9, 8, 7], [5, 6, 7, 8]),  # Partial satisfaction
    ]

    for g, s in edge_cases:
        yield f"{json.dumps(g, separators=(',', ':'))}\n{json.dumps(s, separators=(',', ':'))}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a single random test case."""
    num_children = random.randint(1, 1000)
    num_cookies = random.randint(0, 1000)

    # Keep values reasonable for faster testing
    g = [random.randint(1, 10000) for _ in range(num_children)]
    s = [random.randint(1, 10000) for _ in range(num_cookies)]

    return f"{json.dumps(g, separators=(',', ':'))}\n{json.dumps(s, separators=(',', ':'))}"


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size for complexity estimation."""
    g = [random.randint(1, 10000) for _ in range(n)]
    s = [random.randint(1, 10000) for _ in range(n)]
    return f"{json.dumps(g, separators=(',', ':'))}\n{json.dumps(s, separators=(',', ':'))}"
