# generators/0304_range_sum_query_2d_immutable.py
"""
Test Case Generator for Problem 0304 - Range Sum Query 2D - Immutable

LeetCode Constraints:
- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 200
- -10^4 <= matrix[i][j] <= 10^4
- 0 <= row1 <= row2 < m
- 0 <= col1 <= col2 < n
- At most 10^4 calls will be made to sumRegion

Time Complexity: O(m*n) preprocessing, O(1) per query
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Range Sum Query 2D.

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
        (
            [[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]],
            [(2, 1, 4, 3), (1, 1, 2, 2), (1, 2, 2, 4)]
        ),
        # Single cell
        ([[5]], [(0, 0, 0, 0)]),
        # Single row
        ([[1, 2, 3, 4]], [(0, 0, 0, 3), (0, 1, 0, 2)]),
        # Single column
        ([[1], [2], [3], [4]], [(0, 0, 3, 0), (1, 0, 2, 0)]),
        # All zeros
        ([[0, 0], [0, 0]], [(0, 0, 1, 1)]),
        # Negative values
        ([[-1, -2], [-3, -4]], [(0, 0, 1, 1), (0, 0, 0, 0)]),
    ]

    for matrix, queries in edge_cases:
        yield _format_case(matrix, queries)
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _format_case(matrix: List[List[int]], queries: List[tuple]) -> str:
    """Format a test case as JSON input."""
    commands = ["NumMatrix"] + ["sumRegion"] * len(queries)
    args = [[matrix]] + [list(q) for q in queries]
    return f"{json.dumps(commands, separators=(',', ':'))}\n{json.dumps(args, separators=(',', ':'))}"


def _generate_random_case() -> str:
    """Generate a single random test case."""
    m = random.randint(1, 50)
    n = random.randint(1, 50)
    matrix = [[random.randint(-1000, 1000) for _ in range(n)] for _ in range(m)]

    # Random queries
    num_queries = random.randint(1, 50)
    queries = []
    for _ in range(num_queries):
        row1 = random.randint(0, m - 1)
        row2 = random.randint(row1, m - 1)
        col1 = random.randint(0, n - 1)
        col2 = random.randint(col1, n - 1)
        queries.append((row1, col1, row2, col2))

    return _format_case(matrix, queries)


def generate_for_complexity(m: int, n: int, q: int = 100) -> str:
    """Generate test case with specific size for complexity estimation."""
    matrix = [[random.randint(-1000, 1000) for _ in range(n)] for _ in range(m)]
    queries = []
    for _ in range(q):
        row1 = random.randint(0, m - 1)
        row2 = random.randint(row1, m - 1)
        col1 = random.randint(0, n - 1)
        col2 = random.randint(col1, n - 1)
        queries.append((row1, col1, row2, col2))
    return _format_case(matrix, queries)
