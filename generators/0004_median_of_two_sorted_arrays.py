# generators/0004_median_of_two_sorted_arrays.py
"""
Test Case Generator for Problem 0004 - Median of Two Sorted Arrays

LeetCode Constraints:
- nums1.length == m
- nums2.length == n
- 0 <= m <= 1000
- 0 <= n <= 1000
- 1 <= m + n <= 2000
- -10^6 <= nums1[i], nums2[i] <= 10^6

Time Complexity: O(log(m+n))
"""
import random
from typing import Iterator, Optional


# ============================================
# Random Test Generation (for functional testing)
# ============================================

def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Median of Two Sorted Arrays.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Test input in the same format as .in files
    """
    # Constraints
    min_m, max_m = 0, 1000
    min_n, max_n = 0, 1000
    min_sum, max_sum = 1, 2000
    min_val, max_val = -10**6, 10**6
    
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        "[]\n[1]",                    # nums1 is empty
        "[1]\n[]",                    # nums2 is empty
        "[1,3]\n[2]",                 # Classic odd total length
        "[1,2]\n[3,4]",               # Classic even total length, no overlap
        "[-5,-3,-1]\n[2,4,6]",        # Negative and positive
        "[1]\n[1]",                   # Same single element
    ]
    
    for edge in edge_cases:
        yield edge
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        yield _generate_random_case(min_m, max_m, min_n, max_n, 
                                     min_sum, max_sum, min_val, max_val)


def _generate_random_case(min_m, max_m, min_n, max_n, 
                          min_sum, max_sum, min_val, max_val) -> str:
    """Generate a single random test case."""
    # Ensure m + n satisfies constraint
    while True:
        m = random.randint(min_m, max_m)
        n = random.randint(min_n, max_n)
        if min_sum <= m + n <= max_sum:
            break
    
    nums1 = sorted([random.randint(min_val, max_val) for _ in range(m)])
    nums2 = sorted([random.randint(min_val, max_val) for _ in range(n)])
    
    # Format as .in file content (no spaces in list)
    return f"{nums1}\n{nums2}".replace(' ', '')


# ============================================
# Complexity Estimation (controlled size)
# ============================================

def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.
    
    For this problem:
    - Input size n represents total elements (m + n)
    - Time complexity is O(log(m+n)), so we use m+n as the size
    
    Args:
        n: Total size (m + n)
    
    Returns:
        str: Test input with total size = n
    """
    min_val, max_val = -10**6, 10**6
    
    # Ensure n is at least 1
    n = max(1, n)
    
    # Randomly split n into m and (n - m)
    m = random.randint(0, n)
    remaining = n - m
    
    nums1 = sorted([random.randint(min_val, max_val) for _ in range(m)])
    nums2 = sorted([random.randint(min_val, max_val) for _ in range(remaining)])
    
    return f"{nums1}\n{nums2}".replace(' ', '')

