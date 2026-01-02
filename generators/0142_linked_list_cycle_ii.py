# generators/0142_linked_list_cycle_ii.py
"""
Test Case Generator for Problem 0142 - Linked List Cycle II

LeetCode Constraints:
- The number of nodes is in the range [0, 10^4]
- -10^5 <= Node.val <= 10^5
- pos is -1 or a valid index in the linked-list

Time Complexity: O(n) fast-slow pointers
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Linked List Cycle II.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Line 1: space-separated node values, Line 2: cycle position (-1 if no cycle)
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        "3 2 0 -4\n1",              # Classic example
        "1 2\n-1",                  # No cycle
        "1\n0",                     # Single node cycle
    ]
    
    for edge in edge_cases:
        yield json.dumps(edge, separators=(",",":"))
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        size = random.randint(1, 50)
        has_cycle = random.random() < 0.5
        pos = random.randint(0, size - 1) if has_cycle else -1
        yield _generate_case(size, pos)


def _generate_case(size: int, pos: int) -> str:
    """Generate a single test case."""
    values = [random.randint(-1000, 1000) for _ in range(size)]
    values_str = json.dumps(values, separators=(",",":"))
    return f"{values_str}\n{pos}"


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.
    
    Args:
        n: Number of nodes
    
    Returns:
        str: Test input with n nodes
    """
    n = max(1, n)
    pos = random.randint(0, n - 1) if random.random() < 0.5 else -1
    return _generate_case(n, pos)

