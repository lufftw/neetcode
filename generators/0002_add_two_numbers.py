# generators/0002_add_two_numbers.py
"""
Test Case Generator for Problem 0002 - Add Two Numbers

LeetCode Constraints:
- The number of nodes in each linked list is in the range [1, 100]
- 0 <= Node.val <= 9
- It is guaranteed that the list represents a number that does not have leading zeros

Time Complexity: O(max(m, n))
"""
import json
import random
from typing import Iterator, Optional, List


# ============================================
# Random Test Generation (for functional testing)
# ============================================

def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Add Two Numbers.
    
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
        "0\n0",                      # 0 + 0 = 0
        "9\n1",                      # 9 + 1 = 10 (carry)
        "2,4,3\n5,6,4",              # 342 + 465 = 807 (classic example)
        "9,9,9,9,9,9,9\n9,9,9,9",    # 9999999 + 9999 (different lengths)
        "1\n9,9,9,9,9,9,9,9,9,9",    # 1 + 9999999999 (very different lengths)
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
    """Generate a random test case with two linked lists."""
    # Random lengths for both lists
    len1 = random.randint(1, 50)
    len2 = random.randint(1, 50)
    
    # Generate random digits (0-9)
    # First digit can be 0 only if length is 1
    l1 = _generate_number_digits(len1)
    l2 = _generate_number_digits(len2)
    
    return f"{json.dumps(l1, separators=(",",":"))}\n{json.dumps(l2, separators=(",",":"))}"


def _generate_number_digits(length: int) -> List[int]:
    """
    Generate a list of digits representing a number in reverse order.
    No leading zeros (except for the number 0 itself).
    """
    if length == 1:
        return [random.randint(0, 9)]
    
    # First digit (least significant) can be anything
    digits = [random.randint(0, 9) for _ in range(length - 1)]
    # Last digit (most significant) cannot be 0
    digits.append(random.randint(1, 9))
    
    return digits


# ============================================
# Complexity Estimation (controlled size)
# ============================================

def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.
    
    For this problem:
    - Input size n is the length of the longer linked list
    - Time complexity is O(n)
    
    Args:
        n: Length of the linked lists
    
    Returns:
        str: Test input with max list length = n
    """
    n = max(1, n)
    
    l1 = _generate_number_digits(n)
    l2 = _generate_number_digits(n)
    
    return f"{json.dumps(l1, separators=(",",":"))}\n{json.dumps(l2, separators=(",",":"))}"

