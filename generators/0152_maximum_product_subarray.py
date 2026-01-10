# generators/0152_maximum_product_subarray.py
"""
Test Case Generator for Problem 0152 - Maximum Product Subarray

LeetCode Constraints:
- 1 <= nums.length <= 2 * 10^4
- -10 <= nums[i] <= 10
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Maximum Product Subarray.

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
        [2, 3, -2, 4],          # LeetCode example 1
        [-2, 0, -1],            # LeetCode example 2
        [1],                     # Single positive
        [-1],                    # Single negative
        [0],                     # Single zero
        [2, 3, 4],               # All positive
        [-2, -3, -4],            # All negative (odd count)
        [-2, -3, -4, -5],        # All negative (even count)
        [0, 2],                  # Zero at start
        [2, 0],                  # Zero at end
        [-2, 3, -4],             # Two negatives with positive
        [2, -5, -2, -4, 3],      # Mixed with negatives
        [0, 0, 0],               # All zeros
        [-1, -2, -3, 0, 1, 2],   # Zero in middle
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
        population=[1, 5, 10, 50, 100, 500],
        weights=[1, 2, 3, 3, 2, 1],
        k=1
    )[0]

    # Generate with various patterns
    pattern = random.choice(['random', 'with_zeros', 'positive_heavy', 'negative_heavy'])

    if pattern == 'random':
        nums = [random.randint(-10, 10) for _ in range(n)]
    elif pattern == 'with_zeros':
        nums = [random.choice([0] + list(range(-10, 11))) for _ in range(n)]
    elif pattern == 'positive_heavy':
        nums = [random.randint(-2, 10) for _ in range(n)]
    else:  # negative_heavy
        nums = [random.randint(-10, 2) for _ in range(n)]

    return json.dumps(nums, separators=(',', ':'))


# ============================================
# Complexity Estimation
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Maximum Product Subarray:
    - n is the array length
    - Solution is O(n)

    Args:
        n: Target array size

    Returns:
        str: Test input
    """
    # Clamp to LeetCode constraints
    n = max(1, min(n, 20000))

    # Random values within constraint
    nums = [random.randint(-10, 10) for _ in range(n)]
    return json.dumps(nums, separators=(',', ':'))


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(3, seed=42), 1):
        nums = json.loads(test)
        print(f"Test {i}: {len(nums)} elements")
        print(f"  {nums[:10]}{'...' if len(nums) > 10 else ''}")
        print()
