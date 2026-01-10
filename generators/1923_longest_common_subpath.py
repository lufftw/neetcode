"""
Test Case Generator for Problem 1923 - Longest Common Subpath

LeetCode Constraints:
- 1 <= n <= 10^5
- 2 <= m <= 10^5
- sum(paths[i].length) <= 10^5
- 0 <= paths[i][j] < n
- No consecutive duplicates in any path
"""
import json
import random
from typing import Iterator, Optional


def _generate_path(n: int, length: int) -> list:
    """Generate a path with no consecutive duplicates."""
    if length == 0:
        return []
    path = [random.randint(0, n - 1)]
    for _ in range(length - 1):
        next_city = random.randint(0, n - 2)
        if next_city >= path[-1]:
            next_city += 1
        path.append(next_city)
    return path


def _insert_subpath(path: list, subpath: list, n: int) -> list:
    """Insert a subpath into a path at a random position."""
    if not subpath:
        return path
    pos = random.randint(0, len(path))

    # Build new path, avoiding consecutive duplicates
    new_path = []
    for i, city in enumerate(path):
        if i == pos:
            for sc in subpath:
                if not new_path or new_path[-1] != sc:
                    new_path.append(sc)
        if not new_path or new_path[-1] != city:
            new_path.append(city)

    if pos == len(path):
        for sc in subpath:
            if not new_path or new_path[-1] != sc:
                new_path.append(sc)

    return new_path


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        (5, [[0, 1, 2, 3, 4], [2, 3, 4], [4, 0, 1, 2, 3]]),  # Example 1
        (3, [[0], [1], [2]]),  # No common subpath
        (5, [[0, 1, 2, 3, 4], [4, 3, 2, 1, 0]]),  # Reversed paths
        (2, [[0, 1, 0, 1], [1, 0, 1, 0]]),  # Alternating
        (5, [[0, 1, 2], [0, 1, 2], [0, 1, 2]]),  # Identical paths
        (10, [[0, 1, 2, 3], [1, 2, 3, 4], [2, 3, 4, 5]]),  # Sliding window
    ]

    for n, paths in edge_cases:
        yield f'{n}\n{json.dumps(paths, separators=(",", ":"))}'
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        n = random.randint(2, 50)
        m = random.randint(2, 5)  # Number of paths
        total_budget = random.randint(m * 2, 100)

        # Decide common subpath length
        common_len = random.randint(0, min(5, total_budget // m - 1))
        common_subpath = _generate_path(n, common_len) if common_len > 0 else []

        paths = []
        remaining = total_budget - common_len * m
        base_len = max(1, remaining // m)

        for _ in range(m):
            path_len = random.randint(1, max(1, base_len + 3))
            path = _generate_path(n, path_len)
            if common_subpath:
                path = _insert_subpath(path, common_subpath, n)
            paths.append(path)

        yield f'{n}\n{json.dumps(paths, separators=(",", ":"))}'


def generate_for_complexity(size: int) -> str:
    """Generate test case with specific total size for complexity estimation.

    Total path length = size. Binary search is O(T * log(min_len)).
    """
    size = max(4, min(size, 1000))

    n = min(size, 100)
    m = min(5, size // 10)
    m = max(2, m)

    # Each path length
    path_len = size // m

    # Generate paths with a common subpath to ensure non-trivial answer
    common_len = min(path_len // 3, 10)
    common = _generate_path(n, common_len) if common_len > 0 else []

    paths = []
    for _ in range(m):
        path = _generate_path(n, path_len)
        if common:
            path = _insert_subpath(path, common, n)
        paths.append(path)

    return f'{n}\n{json.dumps(paths, separators=(",", ":"))}'
