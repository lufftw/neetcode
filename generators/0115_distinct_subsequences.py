# generators/0115_distinct_subsequences.py
"""
Test Case Generator for Problem 0115 - Distinct Subsequences

LeetCode Constraints:
- 1 <= s.length, t.length <= 1000
- s and t consist of English letters
"""
import random
import string
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Distinct Subsequences.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (two strings, one per line)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # LeetCode Example 1
        ("rabbbit", "rabbit"),
        # LeetCode Example 2
        ("babgbag", "bag"),
        # Single character match
        ("aaa", "a"),
        # No match possible
        ("abc", "d"),
        # Exact match
        ("abc", "abc"),
        # t longer than s (should be 0)
        ("ab", "abc"),
        # All same characters
        ("aaaa", "aa"),
    ]

    for s, t in edge_cases:
        yield f"{s}\n{t}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random pair of strings where t is likely a subsequence of s."""
    # Generate t first
    t_len = random.randint(2, 10)
    t = "".join(random.choices(string.ascii_lowercase[:5], k=t_len))

    # Generate s by expanding t with extra characters
    s_chars = list(t)
    # Insert random characters
    extra = random.randint(t_len // 2, t_len * 2)
    for _ in range(extra):
        pos = random.randint(0, len(s_chars))
        s_chars.insert(pos, random.choice(string.ascii_lowercase[:5]))

    s = "".join(s_chars)
    return f"{s}\n{t}"


# ============================================
# Complexity Estimation
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Distinct Subsequences:
    - n is the length of string s
    - t is typically shorter than s
    - Time complexity is O(mn)

    Args:
        n: Length of s (will be clamped to [1, 1000])

    Returns:
        str: Test input
    """
    # Clamp to LeetCode constraints
    n = max(1, min(n, 1000))

    # Generate s
    s = "".join(random.choices(string.ascii_lowercase[:10], k=n))

    # Generate t as a subsequence of s (shorter)
    t_len = max(1, n // 4)
    indices = sorted(random.sample(range(n), min(t_len, n)))
    t = "".join(s[i] for i in indices)

    return f"{s}\n{t}"


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(5, seed=42), 1):
        lines = test.split("\n")
        s, t = lines[0], lines[1]
        print(f"Test {i}: s={s[:30]}{'...' if len(s)>30 else ''}, t={t}")
