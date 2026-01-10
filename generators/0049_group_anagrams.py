# generators/0049_group_anagrams.py
"""
Test Case Generator for Problem 0049 - Group Anagrams

LeetCode Constraints:
- 1 <= strs.length <= 10^4
- 0 <= strs[i].length <= 100
- strs[i] consists of lowercase English letters.
"""
import json
import random
import string
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Group Anagrams.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (JSON array of strings)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [""],                                           # Single empty string
        ["a"],                                          # Single character
        ["eat", "tea", "tan", "ate", "nat", "bat"],    # LeetCode example
        ["abc", "bca", "cab"],                          # All anagrams
        ["abc", "def", "ghi"],                          # No anagrams
        ["a", "a", "a"],                                # All same
        ["ab", "ba", "ab", "ba"],                       # Duplicates with anagrams
        [""],                                           # Empty string
        ["abc", "cba", "bac", "xyz", "zyx", "yxz"],    # Two anagram groups
    ]

    for strs in edge_cases:
        yield json.dumps(strs, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case."""
    # Number of strings
    num_strings = random.randint(5, 50)

    # Number of anagram groups
    num_groups = random.randint(1, min(num_strings, 10))

    strs = []

    # Generate base strings for each group
    base_strings = []
    for _ in range(num_groups):
        length = random.randint(1, 10)
        base = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
        base_strings.append(base)

    # Assign each string to a random group
    for _ in range(num_strings):
        base = random.choice(base_strings)
        # Create an anagram by shuffling
        chars = list(base)
        random.shuffle(chars)
        strs.append(''.join(chars))

    random.shuffle(strs)
    return json.dumps(strs, separators=(',', ':'))


# ============================================
# Complexity Estimation
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Group Anagrams:
    - n is the number of strings
    - Complexity depends on n and average string length k

    Args:
        n: Target number of strings

    Returns:
        str: Test input
    """
    # Clamp to reasonable range
    n = max(1, min(n, 10000))

    # Fixed string length for consistent measurement
    k = 10

    # Create n/5 groups of anagrams
    num_groups = max(1, n // 5)
    base_strings = []
    for _ in range(num_groups):
        base = ''.join(random.choice(string.ascii_lowercase) for _ in range(k))
        base_strings.append(base)

    strs = []
    for _ in range(n):
        base = random.choice(base_strings)
        chars = list(base)
        random.shuffle(chars)
        strs.append(''.join(chars))

    return json.dumps(strs, separators=(',', ':'))


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(3, seed=42), 1):
        strs = json.loads(test)
        print(f"Test {i}: {len(strs)} strings")
        print(f"  {strs[:5]}{'...' if len(strs) > 5 else ''}")
        print()
