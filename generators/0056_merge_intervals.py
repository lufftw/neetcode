# generators/0056_merge_intervals.py
"""
Test Case Generator for Problem 0056 - Merge Intervals

LeetCode Constraints:
- 1 <= intervals.length <= 10^4
- intervals[i].length == 2
- 0 <= starti <= endi <= 10^4
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Merge Intervals.

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
        [[1, 3], [2, 6], [8, 10], [15, 18]],  # Standard case
        [[1, 4], [4, 5]],  # Touching intervals
        [[1, 4], [0, 4]],  # Complete overlap
        [[1, 4], [2, 3]],  # Nested interval
        [[1, 4]],  # Single interval
        [[1, 2], [3, 4], [5, 6]],  # No overlaps
        [[1, 10], [2, 3], [4, 5], [6, 7]],  # All nested in first
        [[1, 2], [1, 2], [1, 2]],  # All identical
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
    max_val = 1000

    intervals = []
    for _ in range(n):
        start = random.randint(0, max_val - 1)
        end = random.randint(start, max_val)
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
    max_val = n * 10
    intervals = []

    for _ in range(n):
        start = random.randint(0, max_val - 1)
        end = random.randint(start, max_val)
        intervals.append([start, end])

    return json.dumps(intervals, separators=(',', ':'))


if __name__ == "__main__":
    for i, case in enumerate(generate(5)):
        print(f"Case {i + 1}: {case}")
