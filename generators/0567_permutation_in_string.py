# generators/0567_permutation_in_string.py
"""
Test Case Generator for Problem 0567 - Permutation in String

LeetCode Constraints:
- 1 <= s1.length, s2.length <= 10^4
- s1 and s2 consist of lowercase English letters

Time Complexity: O(|s1| + |s2|) sliding window
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
    Generate random test case inputs for Permutation in String.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Test input (two lines: s1 and s2)
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        ("ab", "eidbaooo"),        # Classic example, True (ba is permutation)
        ("ab", "eidboaoo"),        # Classic example, False
        ("a", "a"),                # Single char match
        ("a", "b"),                # Single char no match
        ("adc", "dcda"),           # Permutation at start
        ("ab", "ab"),              # Exact match
        ("ab", "ba"),              # Exact permutation
        ("abc", "bbbca"),          # Permutation in middle
        ("hello", "ooolleoooleh"), # False - not enough chars together
        ("aaa", "aaaa"),           # Repeated chars, True
    ]
    
    for s1, s2 in edge_cases:
        yield f"{json.dumps(s1)}\n{json.dumps(s2)}"
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        s1_len = random.randint(2, 20)
        s2_len = random.randint(s1_len, 200)
        
        pool_size = random.choice([3, 5, 10, 26])
        pool = string.ascii_lowercase[:pool_size]
        
        s1 = ''.join(random.choices(pool, k=s1_len))
        
        # Sometimes ensure permutation exists
        if random.random() < 0.5:
            # Insert a permutation of s1 somewhere in s2
            perm = list(s1)
            random.shuffle(perm)
            perm_str = ''.join(perm)
            
            prefix_len = random.randint(0, s2_len - s1_len)
            suffix_len = s2_len - s1_len - prefix_len
            
            prefix = ''.join(random.choices(pool, k=prefix_len))
            suffix = ''.join(random.choices(pool, k=suffix_len))
            s2 = prefix + perm_str + suffix
        else:
            s2 = ''.join(random.choices(pool, k=s2_len))
        
        yield f"{json.dumps(s1)}\n{json.dumps(s2)}"


# ============================================================================
# Complexity Estimation (controlled size)
# ============================================================================

def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.
    
    For this problem:
    - Input size n is the length of string s2
    - s1 is kept small to focus on s2 traversal
    
    Args:
        n: Length of the source string s2
    
    Returns:
        str: Two lines (s1 and s2)
    """
    n = max(1, n)
    
    pool = string.ascii_lowercase[:5]
    
    # Small s1
    s1_len = min(10, n)
    s1 = ''.join(random.choices(pool, k=s1_len))
    
    # Large s2
    s2 = ''.join(random.choices(pool, k=n))
    
    return f"{s1}\n{s2}"

