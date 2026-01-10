"""
Test Case Generator for Problem 1977 - Number of Ways to Separate Numbers

LeetCode Constraints:
- 1 <= num.length <= 3500
- num consists of digits '0' through '9'.
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
        "327",          # Example 1: 2 ways
        "094",          # Example 2: 0 (leading zero)
        "0",            # Example 3: 0
        "1",            # Single digit: 1 way
        "9",            # Single digit: 1 way
        "12",           # 2 ways: "12" or "1,2" (1 < 2)
        "21",           # 1 way: "21" (2 > 1 invalid split)
        "123",          # Multiple ways
        "111",          # All same: many ways
        "12345",        # Increasing: many ways
        "54321",        # Decreasing: 1 way
        "1000",         # Leading zeros in splits
        "10",           # 1 way (can't split as "1,0")
        "100",          # 1 way
    ]

    for case in edge_cases:
        yield json.dumps(case, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        case_type = random.choice(['small', 'zeros', 'increasing', 'random'])

        if case_type == 'small':
            length = random.randint(1, 10)
            num = ''.join(random.choices('123456789', k=1))
            num += ''.join(random.choices('0123456789', k=length - 1))
        elif case_type == 'zeros':
            # May have leading zeros in splits
            length = random.randint(2, 15)
            num = ''.join(random.choices('0123456789', k=length))
        elif case_type == 'increasing':
            # Tends to have more valid partitions
            length = random.randint(3, 20)
            digits = sorted([random.randint(1, 9) for _ in range(length)])
            num = ''.join(str(d) for d in digits)
        else:
            length = random.randint(1, 50)
            if random.random() < 0.8:
                num = str(random.randint(1, 9))  # No leading zero
                num += ''.join(random.choices('0123456789', k=length - 1))
            else:
                num = '0' + ''.join(random.choices('0123456789', k=length - 1))

        yield json.dumps(num, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific length."""
    n = max(1, min(n, 3500))

    # Generate string starting with non-zero digit
    num = str(random.randint(1, 9))
    num += ''.join(random.choices('0123456789', k=n - 1))

    return json.dumps(num, separators=(',', ':'))


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"--- Test {i} ---")
        print(test)
        print()
