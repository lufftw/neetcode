# generators/0210_course_schedule_ii.py
"""
Test Case Generator for Problem 0210 - Course Schedule II

LeetCode Constraints:
- 1 <= numCourses <= 2000
- 0 <= prerequisites.length <= numCourses * (numCourses - 1)
- prerequisites[i].length == 2
- 0 <= ai, bi < numCourses
- ai != bi
- All the pairs [ai, bi] are distinct
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Course Schedule II.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: numCourses and prerequisites in newline-separated format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        (2, [[1, 0]]),  # Simple: 0 -> 1
        (4, [[1, 0], [2, 0], [3, 1], [3, 2]]),  # Diamond: multiple valid orders
        (1, []),  # Single course
        (3, []),  # Multiple courses, no dependencies
        (2, [[1, 0], [0, 1]]),  # Cycle - impossible
        (3, [[0, 1], [1, 2], [2, 0]]),  # 3-node cycle - impossible
    ]

    for num_courses, prereqs in edge_cases:
        yield _format_case(num_courses, prereqs)
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _format_case(num_courses: int, prereqs: List[List[int]]) -> str:
    """Format a test case as input string."""
    return f"{num_courses}\n{json.dumps(prereqs, separators=(',', ':'))}"


def _generate_random_case() -> str:
    """Generate a single random test case."""
    num_courses = random.randint(2, 100)

    # Mostly valid DAGs, some with cycles
    has_cycle = random.random() < 0.2  # 20% chance of cycle

    if has_cycle:
        prereqs = _generate_cycle_graph(num_courses)
    else:
        prereqs = _generate_dag(num_courses)

    return _format_case(num_courses, prereqs)


def _generate_dag(n: int) -> List[List[int]]:
    """Generate a valid DAG (no cycles)."""
    num_edges = random.randint(0, min(n * 2, 100))
    edges = set()

    for _ in range(num_edges * 2):
        if len(edges) >= num_edges:
            break
        u = random.randint(0, n - 2)
        v = random.randint(u + 1, n - 1)
        edges.add((v, u))

    return [list(e) for e in edges]


def _generate_cycle_graph(n: int) -> List[List[int]]:
    """Generate a graph with at least one cycle."""
    prereqs = _generate_dag(n)

    cycle_len = random.randint(2, min(5, n))
    cycle_nodes = random.sample(range(n), cycle_len)

    for i in range(cycle_len):
        prereqs.append([cycle_nodes[i], cycle_nodes[(i + 1) % cycle_len]])

    return prereqs


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    Args:
        n: Target number of courses

    Returns:
        str: Test case with approximately n courses
    """
    num_courses = max(2, n)
    num_edges = min(n * 2, 1000)

    edges = set()
    for _ in range(num_edges * 2):
        if len(edges) >= num_edges:
            break
        u = random.randint(0, num_courses - 2)
        v = random.randint(u + 1, num_courses - 1)
        edges.add((v, u))

    prereqs = [list(e) for e in edges]
    return _format_case(num_courses, prereqs)
