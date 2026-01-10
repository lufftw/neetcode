# generators/1899_merge_triplets_to_form_target_triplet.py
"""
Test Case Generator for Problem 1899 - Merge Triplets to Form Target Triplet

LeetCode Constraints:
- 1 <= triplets.length <= 10^5
- triplets[i].length == target.length == 3
- 1 <= a_i, b_i, c_i, x, y, z <= 1000
"""
import json
import random
from typing import Iterator, Optional, List, Tuple


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Merge Triplets to Form Target Triplet.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (triplets and target as JSON)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # LeetCode Example 1 - true
        ([[2, 5, 3], [1, 8, 4], [1, 7, 5]], [2, 7, 5]),
        # LeetCode Example 2 - false (no 2 available)
        ([[3, 4, 5], [4, 5, 6]], [3, 2, 5]),
        # LeetCode Example 3 - true
        ([[2, 5, 3], [2, 3, 4], [1, 2, 5], [5, 2, 3]], [5, 5, 5]),
        # Single triplet equals target - true
        ([[3, 4, 5]], [3, 4, 5]),
        # Single triplet doesn't match - false
        ([[3, 4, 5]], [3, 4, 6]),
        # All triplets have one value too large - false
        ([[5, 1, 1], [1, 5, 1], [1, 1, 5]], [1, 1, 1]),
        # Target achievable with single valid triplet
        ([[10, 10, 10], [3, 3, 3]], [3, 3, 3]),
        # Multiple triplets needed, each contributes one position
        ([[3, 1, 1], [1, 3, 1], [1, 1, 3]], [3, 3, 3]),
    ]

    for triplets, target in edge_cases:
        yield f"{json.dumps(triplets, separators=(',', ':'))}\n{json.dumps(target, separators=(',', ':'))}"
        count -= 1
        if count <= 0:
            return

    # Random cases - mix of solvable and unsolvable
    for _ in range(count):
        if random.random() < 0.6:
            yield _generate_solvable_case()
        else:
            yield _generate_random_case()


def _generate_solvable_case() -> str:
    """Generate a case that is guaranteed to be solvable."""
    # Pick a target
    target = [random.randint(1, 100) for _ in range(3)]

    # Generate triplets that include valid contributors for each position
    num_triplets = random.randint(3, 20)
    triplets = []

    # Ensure at least one valid triplet for each position
    for pos in range(3):
        triplet = [random.randint(1, target[i]) for i in range(3)]
        triplet[pos] = target[pos]  # Make this position exact match
        triplets.append(triplet)

    # Add some noise triplets (may or may not be valid)
    for _ in range(num_triplets - 3):
        if random.random() < 0.5:
            # Valid triplet (all <= target)
            triplet = [random.randint(1, target[i]) for i in range(3)]
        else:
            # Invalid triplet (at least one > target)
            triplet = [random.randint(1, 150) for _ in range(3)]
        triplets.append(triplet)

    random.shuffle(triplets)
    return f"{json.dumps(triplets, separators=(',', ':'))}\n{json.dumps(target, separators=(',', ':'))}"


def _generate_random_case() -> str:
    """Generate a random case (may or may not be solvable)."""
    target = [random.randint(1, 100) for _ in range(3)]
    num_triplets = random.randint(1, 30)

    triplets = []
    for _ in range(num_triplets):
        triplet = [random.randint(1, 150) for _ in range(3)]
        triplets.append(triplet)

    return f"{json.dumps(triplets, separators=(',', ':'))}\n{json.dumps(target, separators=(',', ':'))}"


# ============================================
# Complexity Estimation
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Merge Triplets:
    - n is the number of triplets
    - Time complexity is O(n)

    Args:
        n: Number of triplets

    Returns:
        str: Test input
    """
    # Clamp to LeetCode constraints
    n = max(1, min(n, 100000))

    target = [random.randint(1, 1000) for _ in range(3)]

    # Generate n triplets, ensuring solvability
    triplets = []

    # Add contributors for each position
    for pos in range(3):
        triplet = [random.randint(1, target[i]) for i in range(3)]
        triplet[pos] = target[pos]
        triplets.append(triplet)

    # Fill remaining with random triplets
    for _ in range(n - 3):
        triplet = [random.randint(1, 1000) for _ in range(3)]
        triplets.append(triplet)

    random.shuffle(triplets)
    return f"{json.dumps(triplets, separators=(',', ':'))}\n{json.dumps(target, separators=(',', ':'))}"


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(3, seed=42), 1):
        lines = test.split('\n')
        triplets = json.loads(lines[0])
        target = json.loads(lines[1])
        print(f"Test {i}:")
        print(f"  triplets: {len(triplets)} triplets")
        print(f"  target: {target}")
        print(f"  Sample: {triplets[:3]}...")
        print()
