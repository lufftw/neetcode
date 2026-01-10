"""
Test Case Generator for Problem 0468 - Validate IP Address

LeetCode Constraints:
- queryIP consists of letters, digits, '.', and ':'
"""
import json
import random
from typing import Iterator, Optional


def _random_ipv4(valid: bool = True) -> str:
    if valid:
        return ".".join(str(random.randint(0, 255)) for _ in range(4))
    else:
        # Generate various invalid cases
        case = random.randint(0, 3)
        if case == 0:  # Leading zeros
            return f"01.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
        elif case == 1:  # Out of range
            return f"{random.randint(256,999)}.0.0.0"
        elif case == 2:  # Wrong number of parts
            return ".".join(str(random.randint(0, 255)) for _ in range(3))
        else:  # Invalid char
            return f"192.168.1.{random.choice(['a', 'x', '-'])}"


def _random_ipv6(valid: bool = True) -> str:
    hex_chars = "0123456789abcdefABCDEF"
    if valid:
        parts = []
        for _ in range(8):
            length = random.randint(1, 4)
            parts.append(''.join(random.choice(hex_chars) for _ in range(length)))
        return ":".join(parts)
    else:
        case = random.randint(0, 2)
        if case == 0:  # Too many chars
            return ":".join(["12345"] + ["0"] * 7)
        elif case == 1:  # Invalid char
            return ":".join(["gggg"] + ["0"] * 7)
        else:  # Wrong number of parts
            return ":".join(["0"] * 7)


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        "172.16.254.1",                              # Example 1: IPv4
        "2001:0db8:85a3:0:0:8A2E:0370:7334",        # Example 2: IPv6
        "256.256.256.256",                           # Example 3: Neither
        "192.168.01.1",                              # Leading zero
        "192.168.1.00",                              # Leading zero (00)
        "0.0.0.0",                                   # Valid IPv4
        "::1",                                       # Invalid IPv6 (compressed)
        "1e1.4.5.6",                                 # Has 'e' char
    ]

    for ip in edge_cases:
        yield json.dumps(ip)
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        case = random.randint(0, 3)
        if case == 0:
            yield json.dumps(_random_ipv4(valid=True))
        elif case == 1:
            yield json.dumps(_random_ipv4(valid=False))
        elif case == 2:
            yield json.dumps(_random_ipv6(valid=True))
        else:
            yield json.dumps(_random_ipv6(valid=False))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    # Constant length for IP addresses
    return json.dumps(_random_ipv4(valid=True))
