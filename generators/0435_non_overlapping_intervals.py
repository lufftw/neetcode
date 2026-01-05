# generators/0435_non_overlapping_intervals.py
"""
Test Case Generator for Problem 0435 - Non-overlapping Intervals

LeetCode Constraints:
- 1 <= intervals.length <= 10^5
- intervals[i].length == 2
- -5 * 10^4 <= starti < endi <= 5 * 10^4
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Non-overlapping Intervals.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: 2D intervals array in JSON format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [[1, 2], [2, 3], [3, 4], [1, 3]],  # Remove 1
        [[1, 2], [1, 2], [1, 2]],  # Remove 2
        [[1, 2], [2, 3]],  # No removal needed
        [[1, 100], [11, 22], [1, 11], [2, 12]],  # Multiple overlaps
        [[0, 2], [1, 3], [2, 4], [3, 5], [4, 6]],  # Chain overlaps
        [[-100, -50], [-75, -25], [0, 50]],  # Negative values
        [[1, 2]],  # Single interval
        [[1, 2], [3, 4], [5, 6], [7, 8]],  # No overlaps
    ]

    for intervals in edge_cases:
        yield json.dumps(intervals, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case."""
    n = random.randint(2, 100)
    max_val = 500

    intervals = []
    for _ in range(n):
        start = random.randint(-max_val, max_val - 1)
        end = random.randint(start + 1, max_val)  # strict: start < end
        intervals.append([start, end])

    return json.dumps(intervals, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    Args:
        n: Number of intervals

    Returns:
        str: Intervals array of size n
    """
    max_val = n * 5
    intervals = []

    for _ in range(n):
        start = random.randint(0, max_val - 1)
        end = random.randint(start + 1, max_val)
        intervals.append([start, end])

    return json.dumps(intervals, separators=(',', ':'))


if __name__ == "__main__":
    for i, case in enumerate(generate(5)):
        print(f"Case {i + 1}: {case}")
