# generators/0252_meeting_rooms.py
"""
Test Case Generator for Problem 0252 - Meeting Rooms

LeetCode Constraints:
- 0 <= intervals.length <= 10^4
- intervals[i].length == 2
- 0 <= starti < endi <= 10^6
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Meeting Rooms."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        [[0, 30], [5, 10], [15, 20]],   # Overlap
        [[7, 10], [2, 4]],               # No overlap
        [],                               # Empty
        [[1, 5]],                         # Single meeting
        [[0, 10], [10, 20]],             # Adjacent (no overlap)
        [[0, 10], [9, 20]],              # Small overlap
    ]

    for intervals in edge_cases:
        yield json.dumps(intervals, separators=(",", ":"))
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate random intervals with/without overlaps."""
    n = random.randint(2, 20)

    if random.random() < 0.5:
        # Generate non-overlapping intervals
        intervals = _generate_non_overlapping(n)
    else:
        # Generate potentially overlapping intervals
        intervals = _generate_random_intervals(n)

    return json.dumps(intervals, separators=(",", ":"))


def _generate_non_overlapping(n: int) -> List[List[int]]:
    """Generate n non-overlapping intervals."""
    intervals = []
    current_time = 0

    for _ in range(n):
        start = current_time + random.randint(0, 10)
        duration = random.randint(1, 20)
        end = start + duration
        intervals.append([start, end])
        current_time = end

    random.shuffle(intervals)  # Randomize order
    return intervals


def _generate_random_intervals(n: int) -> List[List[int]]:
    """Generate n random intervals (may overlap)."""
    intervals = []

    for _ in range(n):
        start = random.randint(0, 100)
        end = start + random.randint(1, 30)
        intervals.append([start, end])

    return intervals


def generate_for_complexity(n: int) -> str:
    """Generate test case with n intervals for complexity estimation."""
    n = max(1, min(n, 10000))
    intervals = _generate_random_intervals(n)
    return json.dumps(intervals, separators=(",", ":"))


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}: {test}")
