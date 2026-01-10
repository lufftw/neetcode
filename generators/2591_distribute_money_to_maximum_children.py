"""
Test Case Generator for Problem 2591 - Distribute Money to Maximum Children

LeetCode Constraints:
- 1 <= money <= 200
- 2 <= children <= 30
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        (20, 3),    # Example 1: answer = 1
        (16, 2),    # Example 2: answer = 2 (all get $8)
        (1, 2),     # Impossible: money < children
        (2, 2),     # Each gets $1, answer = 0
        (17, 2),    # One gets $8, one gets $9
        (12, 2),    # One gets $8, one would get $4 -> answer = 0
        (8, 2),     # One gets $8, one gets $0 (impossible, must give $1)
        (9, 2),     # One gets $8, one gets $1
        (24, 3),    # All get $8
        (25, 3),    # Would need extra, so 2 get $8
        (5, 4),     # All get $1, one gets $2
        (8, 1),     # Edge: 1 child? (constraint says >= 2)
        (200, 30),  # Max values
        (30, 30),   # Minimum valid: each gets $1
    ]

    for money, children in edge_cases:
        if children >= 2:  # Constraint: children >= 2
            yield f"{json.dumps(money)}\n{json.dumps(children)}"
            count -= 1
            if count <= 0:
                return

    # Random cases
    for _ in range(count):
        children = random.randint(2, 30)
        # Vary money distribution
        case_type = random.choice(['impossible', 'tight', 'generous', 'random'])

        if case_type == 'impossible':
            money = random.randint(1, children - 1)
        elif case_type == 'tight':
            # Just enough for some to get $8
            k = random.randint(0, children)
            money = 8 * k + (children - k) * random.randint(1, 3)
        elif case_type == 'generous':
            money = random.randint(8 * children, 200)
        else:
            money = random.randint(1, 200)

        money = max(1, min(money, 200))
        yield f"{json.dumps(money)}\n{json.dumps(children)}"


def generate_for_complexity(n: int) -> str:
    """Generate test case (n not very meaningful for O(1) problem)."""
    children = max(2, min(n, 30))
    money = random.randint(1, 200)
    return f"{json.dumps(money)}\n{json.dumps(children)}"


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"--- Test {i} ---")
        print(test)
        print()
