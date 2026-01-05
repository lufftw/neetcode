# generators/0057_insert_interval.py
"""
Test Case Generator for Problem 0057 - Insert Interval

LeetCode Constraints:
- 0 <= intervals.length <= 10^4
- intervals[i].length == 2
- 0 <= starti <= endi <= 10^5
- intervals is sorted by starti in ascending order
- newInterval.length == 2
- 0 <= start <= end <= 10^5
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Insert Interval.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Two lines - intervals array and newInterval
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        ([[1, 3], [6, 9]], [2, 5]),  # Overlap with first
        ([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]),  # Multiple overlaps
        ([], [5, 7]),  # Empty intervals
        ([[1, 5]], [2, 3]),  # New inside existing
        ([[1, 5]], [2, 7]),  # Extend existing
        ([[1, 5]], [6, 8]),  # After all
        ([[3, 5], [12, 15]], [6, 6]),  # Point interval in gap
        ([[1, 2], [3, 4]], [0, 0]),  # Before all
        ([[1, 5]], [0, 6]),  # Cover existing
    ]

    for intervals, new in edge_cases:
        yield f"{json.dumps(intervals, separators=(',', ':'))}\n{json.dumps(new, separators=(',', ':'))}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case."""
    n = random.randint(0, 50)
    max_val = 1000

    # Generate sorted non-overlapping intervals
    intervals = []
    pos = 0
    for _ in range(n):
        start = pos + random.randint(1, 20)
        end = start + random.randint(1, 20)
        if end > max_val:
            break
        intervals.append([start, end])
        pos = end

    # Generate new interval
    new_start = random.randint(0, max_val)
    new_end = random.randint(new_start, min(new_start + 100, max_val))

    return f"{json.dumps(intervals, separators=(',', ':'))}\n{json.dumps([new_start, new_end], separators=(',', ':'))}"


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    Args:
        n: Number of intervals

    Returns:
        str: Intervals and newInterval
    """
    intervals = []
    pos = 0
    for _ in range(n):
        start = pos + random.randint(1, 10)
        end = start + random.randint(1, 10)
        intervals.append([start, end])
        pos = end

    # New interval in the middle
    if intervals:
        mid = len(intervals) // 2
        new_start = intervals[mid][0]
        new_end = new_start + random.randint(1, 50)
    else:
        new_start, new_end = 1, 5

    return f"{json.dumps(intervals, separators=(',', ':'))}\n{json.dumps([new_start, new_end], separators=(',', ':'))}"


if __name__ == "__main__":
    for i, case in enumerate(generate(5)):
        print(f"Case {i + 1}:\n{case}\n")
