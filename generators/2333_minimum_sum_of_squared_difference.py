"""
Test Case Generator for Problem 2333 - Minimum Sum of Squared Difference

LeetCode Constraints:
- 1 <= n <= 10^5
- 0 <= nums1[i], nums2[i] <= 10^5
- 0 <= k1, k2 <= 10^9
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        ([1, 2, 3, 4], [2, 10, 20, 19], 0, 0),       # Example 1
        ([1, 4, 10, 12], [5, 8, 6, 9], 1, 1),        # Example 2
        ([1], [1], 0, 0),                            # Same values
        ([0], [100], 100, 0),                        # Can eliminate diff
        ([1, 1, 1], [5, 5, 5], 6, 6),                # Multiple same diffs
        ([10, 20], [5, 15], 2, 3),                   # Small example
    ]

    for nums1, nums2, k1, k2 in edge_cases:
        yield f"{json.dumps(nums1, separators=(',', ':'))}\n{json.dumps(nums2, separators=(',', ':'))}\n{k1}\n{k2}"
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        n = random.randint(3, 20)  # Keep small for reference
        nums1 = [random.randint(0, 100) for _ in range(n)]
        nums2 = [random.randint(0, 100) for _ in range(n)]
        total_diff = sum(abs(nums1[i] - nums2[i]) for i in range(n))
        k1 = random.randint(0, total_diff // 2)
        k2 = random.randint(0, total_diff // 2)
        yield f"{json.dumps(nums1, separators=(',', ':'))}\n{json.dumps(nums2, separators=(',', ':'))}\n{k1}\n{k2}"


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    n = max(3, min(n, 20))  # Keep small for reference
    nums1 = [random.randint(0, 100) for _ in range(n)]
    nums2 = [random.randint(0, 100) for _ in range(n)]
    total_diff = sum(abs(nums1[i] - nums2[i]) for i in range(n))
    k1 = random.randint(0, total_diff // 3)
    k2 = random.randint(0, total_diff // 3)
    return f"{json.dumps(nums1, separators=(',', ':'))}\n{json.dumps(nums2, separators=(',', ':'))}\n{k1}\n{k2}"
