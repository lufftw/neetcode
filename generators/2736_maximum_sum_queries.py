"""
Test Case Generator for Problem 2736 - Maximum Sum Queries

LeetCode Constraints:
- nums1.length == nums2.length == n
- 1 <= n <= 10^5
- 1 <= nums1[i], nums2[i] <= 10^9
- 1 <= queries.length <= 10^5
- 1 <= xi, yi <= 10^9
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        ([4, 3, 1, 2], [2, 4, 9, 5], [[4, 1], [1, 3], [2, 5]]),  # Example 1
        ([3, 2, 5], [2, 3, 4], [[4, 4], [3, 2], [1, 1]]),  # Example 2
        ([1], [1], [[1, 1]]),  # Single element
        ([1, 2], [2, 1], [[3, 3]]),  # No valid pair
    ]

    for nums1, nums2, queries in edge_cases:
        yield f'{json.dumps(nums1, separators=(",", ":"))}\n{json.dumps(nums2, separators=(",", ":"))}\n{json.dumps(queries, separators=(",", ":"))}'
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        n = random.randint(1, 50)
        q = random.randint(1, 20)

        max_val = 100
        nums1 = [random.randint(1, max_val) for _ in range(n)]
        nums2 = [random.randint(1, max_val) for _ in range(n)]
        queries = [[random.randint(1, max_val), random.randint(1, max_val)] for _ in range(q)]

        yield f'{json.dumps(nums1, separators=(",", ":"))}\n{json.dumps(nums2, separators=(",", ":"))}\n{json.dumps(queries, separators=(",", ":"))}'


def generate_for_complexity(size: int) -> str:
    """Generate test case with specific size for complexity estimation."""
    n = max(1, min(size, 500))
    q = n

    max_val = 1000
    nums1 = [random.randint(1, max_val) for _ in range(n)]
    nums2 = [random.randint(1, max_val) for _ in range(n)]
    queries = [[random.randint(1, max_val), random.randint(1, max_val)] for _ in range(q)]

    return f'{json.dumps(nums1, separators=(",", ":"))}\n{json.dumps(nums2, separators=(",", ":"))}\n{json.dumps(queries, separators=(",", ":"))}'
