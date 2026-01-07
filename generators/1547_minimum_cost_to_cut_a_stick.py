"""
Generator for LC 1547: Minimum Cost to Cut a Stick

Generates stick length n and cut positions for interval DP testing.
"""
import random
import json
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Cut Stick."""
    if seed is not None:
        random.seed(seed)

    for _ in range(count):
        # Stick length between 10 and 1000
        n = random.randint(10, 1000)

        # Number of cuts between 1 and min(n-1, 20)
        num_cuts = random.randint(1, min(n - 1, 20))

        # Cut positions are unique integers in (0, n)
        cuts = sorted(random.sample(range(1, n), num_cuts))

        yield f"{json.dumps(n, separators=(',', ':'))}\n{json.dumps(cuts, separators=(',', ':'))}"


def generate_for_complexity(n: int) -> str:
    """Generate a test case with n cuts."""
    stick_len = n * 10
    cuts = sorted(random.sample(range(1, stick_len), n))
    return f"{json.dumps(stick_len, separators=(',', ':'))}\n{json.dumps(cuts, separators=(',', ':'))}"


if __name__ == "__main__":
    for case in generate(5, seed=42):
        print(case)
        print()
