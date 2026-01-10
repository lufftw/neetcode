"""
Generator for 0166 - Fraction to Recurring Decimal

Generates numerator/denominator pairs that produce interesting decimal patterns:
- Terminating decimals (denominator with only 2,5 factors)
- Short repeating patterns
- Long repeating patterns (prime denominators)
- Edge cases (zero, negative, large values)
"""

import random
from typing import Iterator, Optional
import json


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Fraction to Recurring Decimal."""
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        (0, 1),           # Zero numerator
        (1, 1),           # Integer result
        (-1, 1),          # Negative integer
        (1, -1),          # Negative denominator
        (-1, -1),         # Double negative
        (1, 2),           # 0.5 - terminating
        (1, 3),           # 0.(3) - single digit repeat
        (1, 6),           # 0.1(6) - mixed
        (1, 7),           # 0.(142857) - 6-digit repeat
        (1, 9),           # 0.(1) - single digit
        (1, 11),          # 0.(09) - 2-digit repeat
        (22, 7),          # Pi approximation
        (1, 99),          # 0.(01)
        (1, 333),         # 0.(003)
        (-50, 8),         # -6.25
        (2147483647, 1),  # Max int32 as numerator
        (1, 2147483647),  # Max int32 as denominator (long period)
        (-2147483648, 1), # Min int32 as numerator
    ]

    yielded = 0
    for num, den in edge_cases:
        if yielded >= count:
            return
        yield f"{num}\n{den}"
        yielded += 1

    # Random cases
    while yielded < count:
        case_type = random.choice([
            'terminating', 'short_repeat', 'long_repeat',
            'negative', 'large', 'random'
        ])

        if case_type == 'terminating':
            # Denominator with only factors of 2 and 5
            pow2 = random.randint(0, 10)
            pow5 = random.randint(0, 10)
            den = (2 ** pow2) * (5 ** pow5)
            if den == 0:
                den = 1
            num = random.randint(-10000, 10000)

        elif case_type == 'short_repeat':
            # Small primes give short repeating patterns
            primes = [3, 7, 9, 11, 13, 27, 37, 41]
            den = random.choice(primes)
            num = random.randint(-1000, 1000)

        elif case_type == 'long_repeat':
            # Larger primes give longer repeating patterns
            primes = [97, 101, 103, 107, 109, 113, 127, 131]
            den = random.choice(primes)
            num = random.randint(-1000, 1000)

        elif case_type == 'negative':
            num = random.randint(-10000, 10000)
            den = random.choice([-1, 1]) * random.randint(1, 1000)

        elif case_type == 'large':
            num = random.randint(-2**30, 2**30)
            den = random.randint(1, 2**30)

        else:  # random
            num = random.randint(-10000, 10000)
            den = random.randint(1, 10000)

        yield f"{num}\n{den}"
        yielded += 1


def generate_for_complexity(n: int) -> str:
    """
    Generate test case targeting complexity level n.

    For this problem, n represents the expected length of the repeating period.
    Primes p have period dividing p-1, so we use primes of appropriate size.
    """
    # Find a prime that gives approximately the desired period length
    # For a prime p, the period divides p-1
    # We want period ~ n, so we want prime ~ n+1

    def is_prime(x: int) -> bool:
        if x < 2:
            return False
        if x == 2:
            return True
        if x % 2 == 0:
            return False
        for i in range(3, int(x**0.5) + 1, 2):
            if x % i == 0:
                return False
        return True

    # Find smallest prime >= n+1
    candidate = max(2, n + 1)
    while not is_prime(candidate):
        candidate += 1

    # Use 1/prime to get a potentially long period
    return f"1\n{candidate}"


if __name__ == "__main__":
    # Test the generator
    print("Sample test cases:")
    for i, case in enumerate(generate(5, seed=42)):
        print(f"Case {i+1}:")
        print(case)
        print()
