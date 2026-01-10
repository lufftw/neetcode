# generators/0846_hand_of_straights.py
"""
Test Case Generator for Problem 0846 - Hand of Straights

LeetCode Constraints:
- 1 <= hand.length <= 10^4
- 0 <= hand[i] <= 10^9
- 1 <= groupSize <= hand.length
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Hand of Straights.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (hand and groupSize as JSON)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # LeetCode Example 1: can form groups
        ([1, 2, 3, 6, 2, 3, 4, 7, 8], 3),
        # LeetCode Example 2: cannot form groups
        ([1, 2, 3, 4, 5], 4),
        # Single card, groupSize 1
        ([5], 1),
        # All same values, groupSize > 1 (impossible)
        ([1, 1, 1], 3),
        # Consecutive sequence, perfect grouping
        ([1, 2, 3, 4, 5, 6], 3),
        # Not divisible by groupSize
        ([1, 2, 3, 4, 5], 3),
    ]

    for hand, group_size in edge_cases:
        yield f"{json.dumps(hand, separators=(',', ':'))}\n{group_size}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random hand and groupSize."""
    # Decide if we want a solvable or unsolvable case
    solvable = random.random() < 0.6

    if solvable:
        return _generate_solvable_case()
    else:
        return _generate_random_hand()


def _generate_solvable_case() -> str:
    """Generate a case that has a valid arrangement."""
    group_size = random.randint(2, 5)
    num_groups = random.randint(2, 10)

    hand = []
    start = random.randint(0, 100)

    for _ in range(num_groups):
        # Add a consecutive group
        for i in range(group_size):
            hand.append(start + i)
        # Random offset for next group (can overlap or have gaps)
        start += random.randint(0, 5)

    random.shuffle(hand)
    return f"{json.dumps(hand, separators=(',', ':'))}\n{group_size}"


def _generate_random_hand() -> str:
    """Generate a random hand that may or may not be solvable."""
    n = random.randint(5, 30)
    group_size = random.randint(2, min(n, 6))

    hand = [random.randint(0, 50) for _ in range(n)]
    return f"{json.dumps(hand, separators=(',', ':'))}\n{group_size}"


# ============================================
# Complexity Estimation
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Hand of Straights:
    - n is the number of cards
    - Time complexity is O(n log n)

    Args:
        n: Number of cards (will be clamped to [1, 10000])

    Returns:
        str: Test input
    """
    # Clamp to LeetCode constraints
    n = max(1, min(n, 10000))

    # Generate a solvable case for consistent benchmarking
    group_size = 3
    # Adjust n to be divisible by group_size
    n = (n // group_size) * group_size
    if n == 0:
        n = group_size

    num_groups = n // group_size
    hand = []

    # Create consecutive groups with some variation
    start = 0
    for _ in range(num_groups):
        for i in range(group_size):
            hand.append(start + i)
        start += random.randint(0, 3)

    random.shuffle(hand)
    return f"{json.dumps(hand, separators=(',', ':'))}\n{group_size}"


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(5, seed=42), 1):
        lines = test.split("\n")
        hand = json.loads(lines[0])
        group_size = int(lines[1])
        print(f"Test {i}: {len(hand)} cards, groupSize={group_size}")
        if len(hand) <= 15:
            print(f"  hand: {sorted(hand)}")
        print()
