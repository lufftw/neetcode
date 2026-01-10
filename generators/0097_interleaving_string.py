# generators/0097_interleaving_string.py
"""
Test Case Generator for Problem 0097 - Interleaving String

LeetCode Constraints:
- 0 <= s1.length, s2.length <= 100
- 0 <= s3.length <= 200
- s1, s2, and s3 consist of lowercase English letters.
"""
import json
import random
import string
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Interleaving String.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (s1, s2, s3 as JSON strings)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        ("aabcc", "dbbca", "aadbbcbcac"),     # Example 1: true
        ("aabcc", "dbbca", "aadbbbaccc"),     # Example 2: false
        ("", "", ""),                          # Example 3: true
        ("a", "", "a"),                        # Single char s1
        ("", "b", "b"),                        # Single char s2
        ("a", "b", "ab"),                      # Simple interleave
        ("a", "b", "ba"),                      # Simple interleave reversed
        ("a", "b", "c"),                       # No match
        ("abc", "def", "adbecf"),              # Perfect interleave
        ("ab", "cd", "cdab"),                  # s2 before s1
    ]

    for s1, s2, s3 in edge_cases:
        yield f"{json.dumps(s1)}\n{json.dumps(s2)}\n{json.dumps(s3)}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case."""
    # Decide if this should be solvable
    solvable = random.random() < 0.5

    if solvable:
        return _generate_valid_interleave()
    else:
        return _generate_random_case()


def _generate_valid_interleave() -> str:
    """Generate a case where s3 is a valid interleave of s1 and s2."""
    len1 = random.randint(1, 15)
    len2 = random.randint(1, 15)

    s1 = ''.join(random.choices(string.ascii_lowercase, k=len1))
    s2 = ''.join(random.choices(string.ascii_lowercase, k=len2))

    # Create valid interleave
    s3 = []
    i, j = 0, 0
    while i < len1 or j < len2:
        # Randomly choose to take from s1 or s2 if both available
        if i < len1 and j < len2:
            if random.random() < 0.5:
                s3.append(s1[i])
                i += 1
            else:
                s3.append(s2[j])
                j += 1
        elif i < len1:
            s3.append(s1[i])
            i += 1
        else:
            s3.append(s2[j])
            j += 1

    s3 = ''.join(s3)
    return f"{json.dumps(s1)}\n{json.dumps(s2)}\n{json.dumps(s3)}"


def _generate_random_case() -> str:
    """Generate a random case (may or may not be valid interleave)."""
    len1 = random.randint(1, 15)
    len2 = random.randint(1, 15)
    len3 = len1 + len2  # Must have correct length to have any chance

    s1 = ''.join(random.choices(string.ascii_lowercase, k=len1))
    s2 = ''.join(random.choices(string.ascii_lowercase, k=len2))
    s3 = ''.join(random.choices(string.ascii_lowercase, k=len3))

    return f"{json.dumps(s1)}\n{json.dumps(s2)}\n{json.dumps(s3)}"


# ============================================
# Complexity Estimation
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Interleaving String:
    - n is split between s1 and s2
    - DP is O(m*n)

    Args:
        n: Total combined length of s1 and s2

    Returns:
        str: Test input
    """
    # Clamp to LeetCode constraints
    n = max(2, min(n, 200))

    len1 = n // 2
    len2 = n - len1

    s1 = ''.join(random.choices(string.ascii_lowercase, k=len1))
    s2 = ''.join(random.choices(string.ascii_lowercase, k=len2))

    # Create valid interleave for consistent testing
    s3 = []
    i, j = 0, 0
    while i < len1 or j < len2:
        if i < len1 and (j >= len2 or random.random() < 0.5):
            s3.append(s1[i])
            i += 1
        else:
            s3.append(s2[j])
            j += 1
    s3 = ''.join(s3)

    return f"{json.dumps(s1)}\n{json.dumps(s2)}\n{json.dumps(s3)}"


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(3, seed=42), 1):
        lines = test.split('\n')
        s1 = json.loads(lines[0])
        s2 = json.loads(lines[1])
        s3 = json.loads(lines[2])
        print(f"Test {i}:")
        print(f"  s1=\"{s1}\" (len {len(s1)})")
        print(f"  s2=\"{s2}\" (len {len(s2)})")
        print(f"  s3=\"{s3}\" (len {len(s3)})")
        print()
