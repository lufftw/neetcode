# generators/1203_sort_items_by_groups.py
"""
Test Case Generator for Problem 1203 - Sort Items by Groups Respecting Dependencies

LeetCode Constraints:
- 1 <= m <= n <= 3 * 10^4
- group.length == beforeItems.length == n
- -1 <= group[i] <= m - 1
- 0 <= beforeItems[i].length <= n - 1
- 0 <= beforeItems[i][j] <= n - 1
- i != beforeItems[i][j]
- beforeItems[i] does not contain duplicate elements
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Sort Items by Groups.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: n, m, group, beforeItems in newline-separated format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # Example 1: Valid
        (8, 2, [-1, -1, 1, 0, 0, 1, 0, -1],
         [[], [6], [5], [6], [3, 6], [], [], []]),
        # Example 2: Impossible (cycle)
        (8, 2, [-1, -1, 1, 0, 0, 1, 0, -1],
         [[], [6], [5], [6], [3], [], [4], []]),
        # Single item
        (1, 1, [0], [[]]),
        # Single item, no group
        (1, 0, [-1], [[]]),
        # Two items, same group
        (2, 1, [0, 0], [[1], []]),
        # Two items, different groups
        (2, 2, [0, 1], [[1], []]),
    ]

    for n, m, group, before_items in edge_cases:
        yield _format_case(n, m, group, before_items)
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _format_case(n: int, m: int, group: List[int], before_items: List[List[int]]) -> str:
    """Format a test case as input string."""
    return (f"{n}\n{m}\n"
            f"{json.dumps(group, separators=(',', ':'))}\n"
            f"{json.dumps(before_items, separators=(',', ':'))}")


def _generate_random_case() -> str:
    """Generate a single random test case."""
    n = random.randint(2, 30)
    m = random.randint(1, max(1, n // 2))

    # Generate group assignments
    group = []
    for _ in range(n):
        if random.random() < 0.3:  # 30% chance of no group
            group.append(-1)
        else:
            group.append(random.randint(0, m - 1))

    # Decide if we want valid or invalid case
    make_valid = random.random() < 0.7  # 70% valid

    if make_valid:
        before_items = _generate_valid_dependencies(n, m, group)
    else:
        before_items = _generate_possibly_invalid_dependencies(n, m, group)

    return _format_case(n, m, group, before_items)


def _generate_valid_dependencies(n: int, m: int, group: List[int]) -> List[List[int]]:
    """Generate dependencies that form a valid DAG."""
    before_items: List[List[int]] = [[] for _ in range(n)]

    # Only allow dependencies from lower to higher index (guarantees DAG)
    for i in range(n):
        num_deps = random.randint(0, min(3, i))
        deps = random.sample(range(i), num_deps) if i > 0 else []
        before_items[i] = deps

    return before_items


def _generate_possibly_invalid_dependencies(n: int, m: int, group: List[int]) -> List[List[int]]:
    """Generate dependencies that may create cycles."""
    before_items = _generate_valid_dependencies(n, m, group)

    # Add back edges to potentially create cycles
    num_back_edges = random.randint(1, min(3, n))
    for _ in range(num_back_edges):
        if n > 1:
            u = random.randint(0, n - 2)
            v = random.randint(u + 1, n - 1)
            if u not in before_items[v]:
                before_items[v].append(u)
            if v not in before_items[u]:
                before_items[u].append(v)

    return before_items


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    Args:
        n: Target number of items

    Returns:
        str: Test case with approximately n items
    """
    num_items = max(2, n)
    num_groups = max(1, n // 3)

    # Generate group assignments
    group = []
    for _ in range(num_items):
        if random.random() < 0.2:
            group.append(-1)
        else:
            group.append(random.randint(0, num_groups - 1))

    # Generate valid dependencies
    before_items = _generate_valid_dependencies(num_items, num_groups, group)

    return _format_case(num_items, num_groups, group, before_items)
