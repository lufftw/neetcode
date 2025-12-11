# generators/0021_merge_two_sorted_lists.py
"""
Test Case Generator for Problem 0021 - Merge Two Sorted Lists

LeetCode Constraints:
- The number of nodes in both lists is in the range [0, 50]
- -100 <= Node.val <= 100
- Both list1 and list2 are sorted in non-decreasing order

Time Complexity: O(m + n) merge
"""
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Merge Two Sorted Lists.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Line 1: space-separated integers (list1), Line 2: space-separated integers (list2)
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        "1 2 4\n1 3 4",             # Classic example
        "\n1",                      # Empty first list
        "1\n",                      # Empty second list
        "\n",                       # Both empty
        "1 2 3\n4 5 6",             # No overlap
    ]
    
    for edge in edge_cases:
        yield edge
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        size1 = random.randint(0, 25)
        size2 = random.randint(0, 25)
        yield _generate_case(size1, size2)


def _generate_case(size1: int, size2: int) -> str:
    """Generate a single test case with two sorted lists."""
    list1 = sorted([random.randint(-100, 100) for _ in range(size1)])
    list2 = sorted([random.randint(-100, 100) for _ in range(size2)])
    
    list1_str = ' '.join(map(str, list1)) if list1 else ''
    list2_str = ' '.join(map(str, list2)) if list2 else ''
    
    return f"{list1_str}\n{list2_str}"


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.
    
    Args:
        n: Total number of nodes (split roughly in half)
    
    Returns:
        str: Test input with two sorted lists
    """
    n = max(0, n)
    size1 = n // 2
    size2 = n - size1
    return _generate_case(size1, size2)

