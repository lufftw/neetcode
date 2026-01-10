"""
Test Case Generator for Problem 2741 - Special Permutations

LeetCode Constraints:
- 2 <= nums.length <= 14
- 1 <= nums[i] <= 10^9
- All nums[i] are distinct
"""
import json
import random
from typing import Iterator, Optional


def _generate_divisible_chain(length: int, start: int = 1) -> list:
    """Generate nums where consecutive elements have divisibility."""
    nums = [start]
    for _ in range(length - 1):
        last = nums[-1]
        if random.random() < 0.5:
            # Multiply by small factor
            nums.append(last * random.choice([2, 3, 4, 5]))
        else:
            # Use a divisor if possible
            divisors = [d for d in range(1, min(last + 1, 100)) if last % d == 0 and d not in nums]
            if divisors:
                nums.append(random.choice(divisors))
            else:
                nums.append(last * 2)
    return nums


def _generate_coprime_set(length: int) -> list:
    """Generate nums with few/no divisibility relationships (harder cases)."""
    # Use distinct primes - no divisibility relationships
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]
    return random.sample(primes[:length + 2], length)


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        [2, 3, 6],           # Example 1: answer = 2
        [1, 4, 3],           # Example 2: answer = 2
        [1, 2],              # Minimal: both divide each other
        [2, 3],              # Minimal: coprime, answer = 0
        [1, 2, 4, 8],        # Chain of powers of 2
        [1, 2, 3, 6],        # Multiple divisibility paths
        [2, 3, 5, 7],        # All primes, minimal connections
        [1, 2, 4, 8, 16],    # Long chain, powers of 2
        [6, 2, 3, 1],        # All connected via 1 and 6
    ]

    for nums in edge_cases:
        yield json.dumps(nums, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        length = random.randint(2, 10)
        if random.random() < 0.3:
            # Divisible chain (many valid permutations)
            nums = _generate_divisible_chain(length, random.randint(1, 10))
        elif random.random() < 0.5:
            # Coprime set (few/zero valid permutations)
            nums = _generate_coprime_set(length)
        else:
            # Mixed: some connected via 1
            nums = [1] + [random.randint(2, 100) for _ in range(length - 1)]

        # Ensure distinct
        nums = list(set(nums))
        while len(nums) < 2:
            nums.append(random.randint(1, 1000))
            nums = list(set(nums))

        random.shuffle(nums)
        yield json.dumps(nums, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation.

    Since n <= 14 is the constraint, we cap at 14.
    Bitmask DP is O(n^2 * 2^n), so even n=14 is ~3.2M operations.
    """
    n = max(2, min(n, 14))

    # Use powers of 2 for guaranteed divisibility chain
    nums = [2 ** i for i in range(n)]
    random.shuffle(nums)
    return json.dumps(nums, separators=(',', ':'))
