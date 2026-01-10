"""
Test Case Generator for Problem 0065 - Valid Number

LeetCode Constraints:
- 1 <= s.length <= 20
- s consists of letters, digits (0-9), '+', '-', or '.'.
"""
import json
import random
import string
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    # Valid numbers
    valid_cases = [
        "2", "0089", "-0.1", "+3.14", "4.", "-.9",
        "2e10", "-90E3", "3e+7", "+6e-1", "53.5e93", "-123.456e789",
        "0", ".5", "5.", "1e1", "+1", "-1",
        "1.e1", ".1e1", "1.1e1", "1.1e+1", "1.1e-1",
    ]

    # Invalid numbers
    invalid_cases = [
        "abc", "1a", "1e", "e3", "99e2.5", "--6", "-+3", "95a54e53",
        ".", "e", "+", "-", "1.2.3", "1ee1", "1e1e1", "e",
        "1e", "e1", ".e1", "1.e", "1e.", "+-1", "1+1",
    ]

    for case in valid_cases + invalid_cases:
        yield json.dumps(case, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        case_type = random.choice(['valid_int', 'valid_dec', 'valid_exp', 'invalid'])

        if case_type == 'valid_int':
            sign = random.choice(['', '+', '-'])
            digits = ''.join(random.choices(string.digits, k=random.randint(1, 5)))
            s = sign + digits
        elif case_type == 'valid_dec':
            sign = random.choice(['', '+', '-'])
            d1 = ''.join(random.choices(string.digits, k=random.randint(0, 3)))
            d2 = ''.join(random.choices(string.digits, k=random.randint(0, 3)))
            if not d1 and not d2:
                d2 = random.choice(string.digits)
            s = sign + d1 + '.' + d2
        elif case_type == 'valid_exp':
            # Base number
            sign = random.choice(['', '+', '-'])
            d1 = ''.join(random.choices(string.digits, k=random.randint(0, 2)))
            d2 = ''.join(random.choices(string.digits, k=random.randint(0, 2)))
            if not d1 and not d2:
                d2 = random.choice(string.digits)
            base = sign + d1 + '.' + d2 if random.random() < 0.5 else sign + (d1 or d2)
            # Exponent
            exp_sign = random.choice(['', '+', '-'])
            exp_digits = ''.join(random.choices(string.digits, k=random.randint(1, 3)))
            s = base + random.choice(['e', 'E']) + exp_sign + exp_digits
        else:
            # Random possibly invalid string
            chars = string.digits + '+-.' + 'eE' + 'abc'
            s = ''.join(random.choices(chars, k=random.randint(1, 10)))

        yield json.dumps(s, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific length."""
    n = max(1, min(n, 20))

    # Generate a valid number of approximately length n
    sign = random.choice(['', '+', '-']) if n > 1 else ''
    remaining = n - len(sign)
    digits = ''.join(random.choices(string.digits, k=remaining))
    s = sign + digits

    return json.dumps(s, separators=(',', ':'))


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"--- Test {i} ---")
        print(test)
        print()
