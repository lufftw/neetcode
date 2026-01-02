# generators/0023_merge_k_sorted_lists.py
"""
Test Case Generator for Problem 0023 - Merge k Sorted Lists

LeetCode Constraints:
- k == lists.length
- 0 <= k <= 10^4
- 0 <= lists[i].length <= 500
- -10^4 <= lists[i][j] <= 10^4
- lists[i] is sorted in ascending order
- The sum of lists[i].length will not exceed 10^4

Time Complexity: O(N log k) with heap
"""
import json
import random
from typing import Iterator, Optional, List


# ============================================
# Random Test Generation (for functional testing)
# ============================================

def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Merge k Sorted Lists.
    
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
        [0],                          # Empty input (k=0)
        "1\nempty",                   # Single empty list
        "1\n1",                       # Single list with one element
        "2\n1,2,3\n4,5,6",           # Two non-overlapping lists
        "3\n1,4,5\n1,3,4\n2,6",      # Classic example
    ]
    
    for edge in edge_cases:
        yield json.dumps(edge, separators=(",",":"))
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random test case with k sorted lists."""
    # Random k (number of lists)
    k = random.randint(1, 20)
    
    # Total elements constraint: sum <= 10000
    max_total = 500
    
    lines = [str(k)]
    total = 0
    
    for _ in range(k):
        # Random list length
        remaining = max_total - total
        max_len = min(100, remaining)
        
        if max_len <= 0:
            lines.append("empty")
            continue
        
        list_len = random.randint(0, max_len)
        total += list_len
        
        if list_len == 0:
            lines.append("empty")
        else:
            # Generate sorted list
            values = sorted([random.randint(-1000, 1000) for _ in range(list_len)])
            lines.append(json.dumps(values, separators=(",",":")))
    
    return '\n'.join(lines)


# ============================================
# Complexity Estimation (controlled size)
# ============================================

def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific total size for complexity estimation.
    
    For this problem:
    - Input size n is the total number of elements across all lists (N)
    - Time complexity is O(N log k) with heap
    - We use k = sqrt(n) for balanced testing
    
    Args:
        n: Total number of elements
    
    Returns:
        str: Test input with approximately n total elements
    """
    n = max(1, n)
    
    # Use k = sqrt(n) for balanced testing
    k = max(1, int(n ** 0.5))
    
    # Distribute elements across k lists
    base_size = n // k
    extra = n % k
    
    lines = [str(k)]
    
    for i in range(k):
        list_len = base_size + (1 if i < extra else 0)
        if list_len == 0:
            lines.append("empty")
        else:
            values = sorted([random.randint(-1000, 1000) for _ in range(list_len)])
            lines.append(json.dumps(values, separators=(",",":")))
    
    return '\n'.join(lines)

