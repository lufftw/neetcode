# generators/0438_find_all_anagrams_in_a_string.py
"""
Test Case Generator for Problem 0438 - Find All Anagrams in a String

LeetCode Constraints:
- 1 <= s.length, p.length <= 3 * 10^4
- s and p consist of lowercase English letters

Time Complexity: O(|s| + |p|) sliding window
"""
import random
import string
from typing import Iterator, Optional


# ============================================================================
# Random Test Generation (for functional testing)
# ============================================================================

def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Find All Anagrams.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Test input (two lines: s and p)
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        ("cbaebabacd", "abc"),     # Classic example, answer = [0, 6]
        ("abab", "ab"),            # Multiple overlapping anagrams
        ("af", "be"),              # No anagrams
        ("a", "a"),                # Single char match
        ("aa", "bb"),              # No match, same length
        ("aaaaaaaaaa", "aaa"),     # Many overlapping
        ("baa", "aa"),             # Anagram at end
        ("aab", "ab"),             # Partial match
        ("abcdefg", "gfedcba"),    # Exact reversal = anagram
        ("ab", "abc"),             # Pattern longer than source
    ]
    
    for s, p in edge_cases:
        yield f"{s}\n{p}"
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        s_len = random.randint(10, 500)
        p_len = random.randint(2, min(s_len, 20))
        
        # Use limited pool to increase chance of anagrams
        pool_size = random.choice([3, 5, 10, 26])
        pool = string.ascii_lowercase[:pool_size]
        
        s = ''.join(random.choices(pool, k=s_len))
        p = ''.join(random.choices(pool, k=p_len))
        
        yield f"{s}\n{p}"


# ============================================================================
# Complexity Estimation (controlled size)
# ============================================================================

def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.
    
    For this problem:
    - Input size n is the length of string s
    - p is kept small to focus on s traversal
    
    Args:
        n: Length of the source string s
    
    Returns:
        str: Two lines (s and p)
    """
    n = max(1, n)
    
    # Small alphabet to ensure many anagram matches
    pool = string.ascii_lowercase[:5]
    s = ''.join(random.choices(pool, k=n))
    
    # Small pattern
    p_len = min(10, n)
    p = ''.join(random.choices(pool, k=p_len))
    
    return f"{s}\n{p}"

