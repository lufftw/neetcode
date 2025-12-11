# generators/0876_middle_of_the_linked_list.py
"""
Test Case Generator for Problem 0876 - Middle of the Linked List

LeetCode Constraints:
- The number of nodes is in the range [1, 100]
- 1 <= Node.val <= 100

Time Complexity: O(n) fast-slow pointers
"""
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Middle of Linked List.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Space-separated node values
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        "1 2 3 4 5",                # Classic example (odd length)
        "1 2 3 4 5 6",              # Even length
        "1",                        # Single node
        "1 2",                      # Two nodes
    ]
    
    for edge in edge_cases:
        yield edge
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        size = random.randint(1, 50)
        yield _generate_case(size)


def _generate_case(size: int) -> str:
    """Generate a single test case."""
    values = [random.randint(1, 100) for _ in range(size)]
    return ' '.join(map(str, values))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.
    
    Args:
        n: Number of nodes
    
    Returns:
        str: Test input with n nodes
    """
    n = max(1, n)
    return _generate_case(n)

