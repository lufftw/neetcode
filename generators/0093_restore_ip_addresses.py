# generators/0093_restore_ip_addresses.py
"""
Test Case Generator for Problem 0093 - Restore IP Addresses

LeetCode Constraints:
- 1 <= s.length <= 20
- s consists of digits only
"""
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Restore IP Addresses.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility
    
    Yields:
        str: Test input - a digit string
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        "25525511135",  # Classic example
        "0000",         # All zeros
        "101023",       # Multiple solutions
        "1111",         # Minimal valid
        "111111111111", # All ones (12 digits)
    ]
    
    for edge in edge_cases:
        yield edge
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random digit string."""
    # Length 4-12 for reasonable IP addresses
    length = random.randint(4, 12)
    
    # Generate random digits
    digits = ''.join(str(random.randint(0, 9)) for _ in range(length))
    
    return digits

