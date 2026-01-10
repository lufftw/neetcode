"""
Generator for 2569 - Handling Sum Queries After Update

Generates test cases with:
- Binary arrays nums1
- Integer arrays nums2
- Mixed queries (type 1, 2, 3)
"""

import random
from typing import Iterator, Optional
import json


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Handling Sum Queries After Update."""
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # Single element, simple queries
        ([1], [5], [[3, 0, 0]]),
        ([0], [0], [[1, 0, 0], [3, 0, 0]]),
        # All zeros
        ([0, 0, 0], [1, 2, 3], [[2, 1, 0], [3, 0, 0]]),
        # All ones
        ([1, 1, 1], [0, 0, 0], [[2, 2, 0], [3, 0, 0]]),
        # Toggle all then query
        ([1, 0, 1, 0], [0, 0, 0, 0], [[1, 0, 3], [2, 1, 0], [3, 0, 0]]),
        # Multiple toggles on same range
        ([1, 0], [0, 0], [[1, 0, 1], [1, 0, 1], [2, 1, 0], [3, 0, 0]]),
        # Multiple type 2 queries
        ([1, 1], [0, 0], [[2, 1, 0], [2, 1, 0], [3, 0, 0]]),
    ]

    yielded = 0
    for nums1, nums2, queries in edge_cases:
        if yielded >= count:
            return
        yield f"{json.dumps(nums1)}\n{json.dumps(nums2)}\n{json.dumps(queries)}"
        yielded += 1

    # Random cases
    while yielded < count:
        n = random.randint(1, 100)
        q = random.randint(1, 50)

        nums1 = [random.randint(0, 1) for _ in range(n)]
        nums2 = [random.randint(0, 10**6) for _ in range(n)]

        queries = []
        for _ in range(q):
            qtype = random.randint(1, 3)
            if qtype == 1:
                l = random.randint(0, n - 1)
                r = random.randint(l, n - 1)
                queries.append([1, l, r])
            elif qtype == 2:
                p = random.randint(0, 10**4)
                queries.append([2, p, 0])
            else:
                queries.append([3, 0, 0])

        # Ensure at least one type 3 query
        if not any(q[0] == 3 for q in queries):
            queries.append([3, 0, 0])

        yield f"{json.dumps(nums1)}\n{json.dumps(nums2)}\n{json.dumps(queries)}"
        yielded += 1


def generate_for_complexity(n: int) -> str:
    """
    Generate test case targeting complexity level n.

    n controls both array size and number of queries.
    Alternates between toggle and sum queries to stress segment tree.
    """
    nums1 = [random.randint(0, 1) for _ in range(n)]
    nums2 = [random.randint(0, 10**6) for _ in range(n)]

    queries = []
    for i in range(n):
        # Alternate: toggle half the array, then add, then query
        if i % 3 == 0:
            l = random.randint(0, n // 2)
            r = random.randint(n // 2, n - 1)
            queries.append([1, l, r])
        elif i % 3 == 1:
            queries.append([2, random.randint(1, 100), 0])
        else:
            queries.append([3, 0, 0])

    # End with a query
    queries.append([3, 0, 0])

    return f"{json.dumps(nums1)}\n{json.dumps(nums2)}\n{json.dumps(queries)}"


if __name__ == "__main__":
    print("Sample test cases:")
    for i, case in enumerate(generate(3, seed=42)):
        print(f"Case {i+1}:")
        print(case)
        print()
