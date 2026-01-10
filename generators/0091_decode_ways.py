# generators/0091_decode_ways.py
"""
Test Case Generator for Problem 0091 - Decode Ways

LeetCode Constraints:
- 1 <= s.length <= 100
- s contains only digits and may contain leading zero(s).
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Decode Ways.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (JSON string of digits)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        "12",       # LeetCode example 1
        "226",      # LeetCode example 2
        "06",       # LeetCode example 3 (invalid leading zero)
        "0",        # Single zero (invalid)
        "1",        # Single valid digit
        "10",       # Two digit ending in zero
        "27",       # Invalid two-digit (>26)
        "11106",    # Complex with zeros
        "1111",     # All ones (many ways)
        "2626",     # All valid two-digit pairs
        "101",      # Zero in middle
        "100",      # Two zeros at end
        "301",      # Invalid: 30 > 26
    ]

    for s in edge_cases:
        yield json.dumps(s)
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case."""
    # Random length
    length = random.randint(1, 30)

    # Different generation strategies
    strategy = random.choice(['random', 'valid_encoding', 'with_zeros'])

    if strategy == 'random':
        # Completely random digits
        s = ''.join(str(random.randint(0, 9)) for _ in range(length))
    elif strategy == 'valid_encoding':
        # Build by choosing valid encodings
        s = ''
        while len(s) < length:
            if random.random() < 0.3 and len(s) < length - 1:
                # Two-digit encoding
                two_digit = random.randint(10, 26)
                s += str(two_digit)
            else:
                # Single digit encoding (1-9)
                s += str(random.randint(1, 9))
        s = s[:length]  # Trim to exact length
    else:
        # Random with intentional zeros
        s = ''
        for _ in range(length):
            if random.random() < 0.15:
                s += '0'
            elif random.random() < 0.3:
                s += str(random.randint(1, 2))  # Start of valid two-digit
            else:
                s += str(random.randint(1, 9))

    return json.dumps(s)


# ============================================
# Complexity Estimation
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Decode Ways:
    - n is the string length
    - DP is O(n)

    Args:
        n: Target string length

    Returns:
        str: Test input
    """
    # Clamp to LeetCode constraints
    n = max(1, min(n, 100))

    # Generate all 1s and 2s for maximum branching (most ways to decode)
    s = ''.join(str(random.choice([1, 2])) for _ in range(n))

    return json.dumps(s)


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(3, seed=42), 1):
        s = json.loads(test)
        print(f"Test {i}: \"{s}\" (length {len(s)})")
        print()
