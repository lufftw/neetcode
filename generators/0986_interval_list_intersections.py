# generators/0986_interval_list_intersections.py
"""
Test Case Generator for Problem 0986 - Interval List Intersections

LeetCode Constraints:
- 0 <= firstList.length, secondList.length <= 1000
- firstList.length + secondList.length >= 1
- 0 <= starti < endi <= 10^9
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Interval List Intersections.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Two lines - firstList and secondList
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        ([[0, 2], [5, 10], [13, 23], [24, 25]], [[1, 5], [8, 12], [15, 24], [25, 26]]),
        ([[1, 3], [5, 9]], []),  # Second empty
        ([], [[1, 3], [5, 9]]),  # First empty
        ([[1, 3]], [[3, 5]]),  # Point intersection
        ([[1, 10]], [[2, 3], [5, 7]]),  # Multiple intersections with one
        ([[1, 2], [4, 5]], [[3, 6]]),  # Overlap with gap
        ([[0, 5]], [[0, 5]]),  # Identical intervals
        ([[1, 2], [3, 4]], [[5, 6], [7, 8]]),  # No intersection
    ]

    for first, second in edge_cases:
        yield f"{json.dumps(first, separators=(',', ':'))}\n{json.dumps(second, separators=(',', ':'))}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_sorted_intervals(n: int, max_val: int) -> list:
    """Generate sorted non-overlapping intervals."""
    intervals = []
    pos = 0
    for _ in range(n):
        start = pos + random.randint(1, 20)
        end = start + random.randint(1, 20)
        if end > max_val:
            break
        intervals.append([start, end])
        pos = end
    return intervals


def _generate_case() -> str:
    """Generate a single random test case."""
    n1 = random.randint(1, 30)
    n2 = random.randint(1, 30)
    max_val = 500

    first = _generate_sorted_intervals(n1, max_val)
    second = _generate_sorted_intervals(n2, max_val)

    return f"{json.dumps(first, separators=(',', ':'))}\n{json.dumps(second, separators=(',', ':'))}"


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    Args:
        n: Total number of intervals (split between both lists)

    Returns:
        str: firstList and secondList
    """
    n1 = n // 2
    n2 = n - n1
    max_val = n * 10

    first = _generate_sorted_intervals(n1, max_val)
    second = _generate_sorted_intervals(n2, max_val)

    return f"{json.dumps(first, separators=(',', ':'))}\n{json.dumps(second, separators=(',', ':'))}"


if __name__ == "__main__":
    for i, case in enumerate(generate(5)):
        print(f"Case {i + 1}:\n{case}\n")
