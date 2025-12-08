# generators/0025_reverse_nodes_in_k_group.py
"""
Test Case Generator for Problem 0025 - Reverse Nodes in k-Group

LeetCode Constraints:
- The number of nodes in the list is n
- 1 <= k <= n <= 5000
- 0 <= Node.val <= 1000

Time Complexity: O(n)
"""
import random
from typing import Iterator, Optional, List


# ============================================
# Random Test Generation (for functional testing)
# ============================================

def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Reverse Nodes in k-Group.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Test input in the format expected by solve()
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        "1\n1",                    # Single node, k=1
        "1,2\n1",                  # k=1, no reversal needed
        "1,2\n2",                  # Exactly one group
        "1,2,3,4,5\n2",           # Classic example
        "1,2,3,4,5\n3",           # Another classic
        "1,2,3,4,5,6\n3",         # Multiple complete groups
        "1,2,3,4,5\n5",           # k equals n
        "1,2,3,4,5\n6",           # k > n, no reversal
    ]
    
    for edge in edge_cases:
        yield edge
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random test case."""
    # Random list length
    n = random.randint(1, 100)
    
    # Random k (1 <= k <= n)
    k = random.randint(1, n)
    
    # Random values
    values = [random.randint(0, 1000) for _ in range(n)]
    
    return f"{','.join(map(str, values))}\n{k}"


# ============================================
# Complexity Estimation (controlled size)
# ============================================

def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.
    
    For this problem:
    - Input size n is the length of the linked list
    - Time complexity is O(n)
    
    Args:
        n: Length of the linked list
    
    Returns:
        str: Test input with list length = n
    """
    n = max(1, n)
    
    # Use k = sqrt(n) for balanced testing
    k = max(1, int(n ** 0.5))
    
    # Random values
    values = [random.randint(0, 1000) for _ in range(n)]
    
    return f"{','.join(map(str, values))}\n{k}"

