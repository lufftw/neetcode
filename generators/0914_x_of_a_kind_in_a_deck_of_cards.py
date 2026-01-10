"""
Test Case Generator for Problem 0914 - X of a Kind in a Deck of Cards

LeetCode Constraints:
- 1 <= deck.length <= 10^4
- 0 <= deck[i] < 10^4
"""
import json
import random
from typing import Iterator, Optional
from math import gcd
from functools import reduce


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        [1, 2, 3, 4, 4, 3, 2, 1],     # True: all counts = 2
        [1, 1, 1, 2, 2, 2, 3, 3],     # False: gcd(3,3,2) = 1
        [1, 1, 2, 2, 2, 2],           # True: gcd(2,4) = 2
        [1],                          # False: single card
        [1, 1],                       # True: pair
        [0, 0, 0, 1, 1, 1, 2, 2, 2],  # True: all counts = 3
    ]

    for deck in edge_cases:
        yield json.dumps(deck, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        n = random.randint(1, 50)
        num_distinct = random.randint(1, min(n, 10))

        # Generate counts
        if random.random() < 0.5:
            # Make GCD >= 2 (True case)
            base = random.randint(2, 5)
            counts = [base * random.randint(1, 5) for _ in range(num_distinct)]
        else:
            # Random counts (might be True or False)
            counts = [random.randint(1, 10) for _ in range(num_distinct)]

        deck = []
        for i, cnt in enumerate(counts):
            deck.extend([i] * cnt)

        random.shuffle(deck)
        yield json.dumps(deck, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    n = max(1, min(n, 1000))

    num_distinct = max(1, n // 10)
    base_count = n // num_distinct

    deck = []
    for i in range(num_distinct):
        deck.extend([i] * base_count)

    # Add remaining
    for i in range(n - len(deck)):
        deck.append(i % num_distinct)

    random.shuffle(deck)
    return json.dumps(deck, separators=(',', ':'))
