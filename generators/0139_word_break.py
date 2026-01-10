# generators/0139_word_break.py
"""
Test Case Generator for Problem 0139 - Word Break

LeetCode Constraints:
- 1 <= s.length <= 300
- 1 <= wordDict.length <= 1000
- 1 <= wordDict[i].length <= 20
- s and wordDict[i] consist of only lowercase English letters.
"""
import json
import random
import string
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Word Break.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (s JSON + wordDict JSON)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        ("leetcode", ["leet", "code"]),              # Example 1: True
        ("applepenapple", ["apple", "pen"]),         # Example 2: True (reuse)
        ("catsandog", ["cats", "dog", "sand", "and", "cat"]),  # Example 3: False
        ("a", ["a"]),                                 # Single char match
        ("a", ["b"]),                                 # Single char no match
        ("ab", ["a", "b"]),                           # Simple split
        ("aaaaaaa", ["aaa", "aaaa"]),                 # Overlapping lengths
        ("cars", ["car", "ca", "rs"]),                # Multiple options
        ("abcd", ["a", "abc", "b", "cd"]),            # Choose path
        ("bb", ["a", "b", "bbb", "bbbb"]),            # Must use "b" twice
    ]

    for s, wordDict in edge_cases:
        yield f"{json.dumps(s)}\n{json.dumps(wordDict, separators=(',', ':'))}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case."""
    # Decide if this should be solvable
    solvable = random.random() < 0.6

    if solvable:
        return _generate_solvable_case()
    else:
        return _generate_random_case()


def _generate_solvable_case() -> str:
    """Generate a case that is guaranteed to be solvable."""
    # Generate word dictionary first
    num_words = random.randint(3, 15)
    word_lengths = [random.randint(1, 8) for _ in range(num_words)]
    wordDict = [''.join(random.choices(string.ascii_lowercase, k=length))
                for length in word_lengths]

    # Build s by concatenating random words from dictionary
    num_parts = random.randint(2, 6)
    parts = [random.choice(wordDict) for _ in range(num_parts)]
    s = ''.join(parts)

    # Limit length
    if len(s) > 50:
        s = s[:50]

    return f"{json.dumps(s)}\n{json.dumps(wordDict, separators=(',', ':'))}"


def _generate_random_case() -> str:
    """Generate a random case (may or may not be solvable)."""
    # Random string
    s_length = random.randint(5, 30)
    s = ''.join(random.choices(string.ascii_lowercase, k=s_length))

    # Random dictionary
    num_words = random.randint(3, 20)
    wordDict = [''.join(random.choices(string.ascii_lowercase,
                                        k=random.randint(1, 6)))
                for _ in range(num_words)]

    return f"{json.dumps(s)}\n{json.dumps(wordDict, separators=(',', ':'))}"


# ============================================
# Complexity Estimation
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Word Break:
    - n is the string length
    - Worst case is O(n^2) checking

    Args:
        n: Target string length

    Returns:
        str: Test input
    """
    # Clamp to LeetCode constraints
    n = max(1, min(n, 300))

    # Generate string of repeated pattern
    s = 'a' * n

    # Dictionary that requires checking many prefixes
    wordDict = ['a' * i for i in range(1, min(n + 1, 20))]

    return f"{json.dumps(s)}\n{json.dumps(wordDict, separators=(',', ':'))}"


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(3, seed=42), 1):
        lines = test.split('\n')
        s = json.loads(lines[0])
        wordDict = json.loads(lines[1])
        print(f"Test {i}: s=\"{s}\" (length {len(s)})")
        print(f"  wordDict: {wordDict[:5]}{'...' if len(wordDict) > 5 else ''}")
        print()
