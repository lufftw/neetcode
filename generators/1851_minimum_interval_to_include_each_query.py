# generators/1851_minimum_interval_to_include_each_query.py
"""
Test Case Generator for Problem 1851 - Minimum Interval to Include Each Query

LeetCode Constraints:
- 1 <= intervals.length <= 10^5
- 1 <= queries.length <= 10^5
- intervals[i].length == 2
- 1 <= left_i <= right_i <= 10^7
- 1 <= queries[j] <= 10^7
"""
import json
import random
from typing import Iterator, Optional, List, Tuple


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Minimum Interval to Include Each Query.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (intervals and queries as JSON)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # LeetCode Example 1
        ([[1, 4], [2, 4], [3, 6], [4, 4]], [2, 3, 4, 5]),
        # LeetCode Example 2
        ([[2, 3], [2, 5], [1, 8], [20, 25]], [2, 19, 5, 22]),
        # Single interval, single query - contained
        ([[1, 10]], [5]),
        # Single interval, single query - not contained
        ([[5, 10]], [3]),
        # Multiple queries, no matching intervals
        ([[10, 20], [30, 40]], [5, 25, 50]),
        # Overlapping intervals with same left
        ([[1, 5], [1, 10], [1, 3]], [1, 2, 4]),
        # Query at exact boundaries
        ([[5, 10]], [5, 10]),
        # Point interval (left == right)
        ([[5, 5], [3, 7]], [5]),
    ]

    for intervals, queries in edge_cases:
        yield f"{json.dumps(intervals, separators=(',', ':'))}\n{json.dumps(queries, separators=(',', ':'))}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a single random test case."""
    # Random sizes
    num_intervals = random.randint(1, 100)
    num_queries = random.randint(1, 100)

    # Generate intervals
    intervals = []
    for _ in range(num_intervals):
        left = random.randint(1, 1000)
        right = left + random.randint(0, 100)  # Ensure right >= left
        intervals.append([left, right])

    # Generate queries - mix of values inside and outside interval ranges
    queries = []
    for _ in range(num_queries):
        if random.random() < 0.7 and intervals:
            # 70% chance: pick a value near an existing interval
            interval = random.choice(intervals)
            offset = random.randint(-20, 20)
            query = max(1, interval[0] + offset)
        else:
            # 30% chance: completely random value
            query = random.randint(1, 1200)
        queries.append(query)

    return f"{json.dumps(intervals, separators=(',', ':'))}\n{json.dumps(queries, separators=(',', ':'))}"


# ============================================
# Complexity Estimation
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Minimum Interval to Include Each Query:
    - n controls both number of intervals and queries
    - Time complexity is O((n + q) log n)

    Args:
        n: Target size for intervals and queries

    Returns:
        str: Test input
    """
    # Clamp to LeetCode constraints
    n = max(1, min(n, 100000))

    num_intervals = n
    num_queries = n

    # Generate non-overlapping intervals for worst-case heap behavior
    intervals = []
    current = 1
    for _ in range(num_intervals):
        size = random.randint(1, 100)
        intervals.append([current, current + size])
        current += size + random.randint(1, 10)  # Gap between intervals

    # Generate sorted queries to trigger maximum interval processing
    max_val = intervals[-1][1] if intervals else 1000
    queries = sorted(random.randint(1, max_val) for _ in range(num_queries))

    return f"{json.dumps(intervals, separators=(',', ':'))}\n{json.dumps(queries, separators=(',', ':'))}"


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(3, seed=42), 1):
        lines = test.split('\n')
        intervals = json.loads(lines[0])
        queries = json.loads(lines[1])
        print(f"Test {i}:")
        print(f"  intervals: {len(intervals)} intervals")
        print(f"  queries: {len(queries)} queries")
        print(f"  Sample: {intervals[:3]}... {queries[:5]}...")
        print()
