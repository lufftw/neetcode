# generators/0053_maximum_subarray.py
"""
Test Case Generator for Problem 0053 - Maximum Subarray

LeetCode Constraints:
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Maximum Subarray.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (JSON array)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [1],                                    # Single positive
        [-1],                                   # Single negative
        [-2, 1, -3, 4, -1, 2, 1, -5, 4],        # LeetCode example 1
        [5, 4, -1, 7, 8],                       # LeetCode example 3 (all included)
        [-2, -1],                               # All negative
        [1, 2, 3, 4, 5],                        # All positive
        [-1, -2, -3, -4, -5],                   # All negative (pick least)
        [0],                                    # Single zero
        [-1, 0, -2],                            # Zero in middle
        [1, -1, 1, -1, 1],                      # Alternating
        [100, -1, 100],                         # Large separated by small negative
    ]

    for nums in edge_cases:
        yield json.dumps(nums, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case."""
    # Random array size
    n = random.choices(
        population=[1, 5, 10, 50, 100, 500, 1000],
        weights=[1, 2, 3, 4, 4, 2, 1],
        k=1
    )[0]

    # Generate with various patterns
    pattern = random.choice(['random', 'mostly_positive', 'mostly_negative', 'alternating'])

    if pattern == 'random':
        nums = [random.randint(-10000, 10000) for _ in range(n)]
    elif pattern == 'mostly_positive':
        nums = [random.randint(-100, 1000) for _ in range(n)]
    elif pattern == 'mostly_negative':
        nums = [random.randint(-1000, 100) for _ in range(n)]
    else:  # alternating
        nums = []
        for i in range(n):
            if i % 2 == 0:
                nums.append(random.randint(1, 100))
            else:
                nums.append(random.randint(-50, -1))

    return json.dumps(nums, separators=(',', ':'))


# ============================================
# Complexity Estimation
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Maximum Subarray:
    - n is the array length
    - Kadane's is O(n), Divide and Conquer is O(n log n)

    Args:
        n: Target array size

    Returns:
        str: Test input
    """
    # Clamp to LeetCode constraints
    n = max(1, min(n, 100000))

    # Random values
    nums = [random.randint(-10000, 10000) for _ in range(n)]
    return json.dumps(nums, separators=(',', ':'))


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(3, seed=42), 1):
        nums = json.loads(test)
        print(f"Test {i}: {len(nums)} elements")
        print(f"  {nums[:10]}{'...' if len(nums) > 10 else ''}")
        print()
