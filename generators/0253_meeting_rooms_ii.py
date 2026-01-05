# generators/0253_meeting_rooms_ii.py
"""
Test Case Generator for Problem 253 - Meeting Rooms II

LeetCode Constraints:
- 1 <= intervals.length <= 10^4
- 0 <= starti < endi <= 10^6
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
        str: Test input in .in file format (intervals as JSON)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [[0, 30], [5, 10], [15, 20]],      # Need 2 rooms
        [[7, 10], [2, 4]],                  # No overlap, 1 room
        [[0, 10]],                          # Single meeting
        [[0, 5], [5, 10]],                  # Adjacent, can reuse
        [[0, 5], [4, 10]],                  # Slight overlap, need 2
        [[0, 10], [0, 10], [0, 10]],        # All same time, need 3
        [[1, 5], [2, 3]],                   # Nested, need 2
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
    """Generate a single valid random test case."""
    n = random.randint(5, 100)
    max_time = 10000

    intervals = []
    for _ in range(n):
        start = random.randint(0, max_time - 1)
        duration = random.randint(1, min(1000, max_time - start))
        end = start + duration
        intervals.append([start, end])

    return json.dumps(intervals, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with n intervals for complexity estimation."""
    max_time = 1000000
    intervals = []

    for _ in range(n):
        start = random.randint(0, max_time - 1)
        duration = random.randint(1, min(10000, max_time - start))
        end = start + duration
        intervals.append([start, end])

    return json.dumps(intervals, separators=(',', ':'))
