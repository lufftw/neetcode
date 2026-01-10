# generators/0763_partition_labels.py
"""
Test Case Generator for Problem 0763 - Partition Labels

LeetCode Constraints:
- 1 <= s.length <= 500
- s consists of lowercase English letters
"""
import random
import string
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Partition Labels.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (string s)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # LeetCode Example 1
        "ababcbacadefegdehijhklij",
        # LeetCode Example 2
        "eccbbbbdec",
        # Single character
        "a",
        # All same character
        "aaaaaaa",
        # Each character appears exactly once
        "abcdefghij",
        # Two characters alternating
        "ababab",
    ]

    for s in edge_cases:
        yield s
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random string of lowercase letters."""
    length = random.randint(10, 100)
    # Use subset of alphabet for more interesting partition patterns
    alphabet_size = random.randint(5, 26)
    alphabet = string.ascii_lowercase[:alphabet_size]

    return "".join(random.choices(alphabet, k=length))


# ============================================
# Complexity Estimation
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Partition Labels:
    - n is the string length
    - Time complexity is O(n)

    Args:
        n: String length (will be clamped to [1, 500])

    Returns:
        str: Test input
    """
    # Clamp to LeetCode constraints
    n = max(1, min(n, 500))

    # Generate string with multiple partition boundaries
    # to make the algorithm work meaningfully
    alphabet = string.ascii_lowercase
    return "".join(random.choices(alphabet, k=n))


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}: length={len(test)}")
        if len(test) <= 50:
            print(f"  s = {test}")
        print()
