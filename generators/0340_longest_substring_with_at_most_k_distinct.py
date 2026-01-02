# generators/0340_longest_substring_with_at_most_k_distinct.py
"""
Test Case Generator for Problem 0340 - Longest Substring with At Most K Distinct Characters
Also covers LeetCode 159 (K=2 special case)

LeetCode Constraints:
- 1 <= s.length <= 5 * 10^4
- 0 <= k <= 50
- s consists of English letters

Time Complexity: O(n) sliding window
"""
import json
import random
import string
from typing import Iterator, Optional


# ============================================================================
# Random Test Generation (for functional testing)
# ============================================================================

def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Longest Substring K Distinct.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Test input (two lines: s and k)
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        ("eceba", 2),           # Classic example, answer = 3 ("ece")
        ("aa", 1),              # All same char
        ("a", 0),               # k=0 edge case
        ("aabbcc", 1),          # Single distinct allowed
        ("aabbcc", 2),          # Two distinct
        ("aabbcc", 3),          # All chars allowed
        ("abcabcabc", 2),       # Repeating pattern
        ("abaccc", 2),          # Answer at end
        ("", 2),                # Empty string (if allowed)
        ("a", 1),               # Single char, k=1
    ]
    
    for s, k in edge_cases:
        yield f"{json.dumps(s)}\n{k}"
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        s_len = random.randint(10, 500)
        
        # Vary the character pool to create interesting cases
        pool_size = random.choice([3, 5, 10, 26])
        pool = string.ascii_lowercase[:pool_size]
        s = ''.join(random.choices(pool, k=s_len))
        
        # k relative to actual distinct chars in s
        distinct_count = len(set(s))
        k = random.randint(0, distinct_count + 2)
        
        yield f"{json.dumps(s)}\n{k}"


# ============================================================================
# Complexity Estimation (controlled size)
# ============================================================================

def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.
    
    For this problem:
    - Input size n is the length of string s
    
    Args:
        n: Length of the string
    
    Returns:
        str: Two lines (s and k)
    """
    n = max(1, n)
    
    # Use limited character pool to ensure sliding window does work
    pool = string.ascii_lowercase[:10]
    s = ''.join(random.choices(pool, k=n))
    
    # k should be less than pool size to exercise the algorithm
    k = random.randint(2, 5)
    
    return f"{json.dumps(s)}\n{k}"

