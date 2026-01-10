"""
Generator for 0488 - Zuma Game

Generates test cases with:
- Valid boards (no initial 3+ consecutive)
- Various hand configurations
"""

import random
from typing import Iterator, Optional


COLORS = "RYBGW"


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Zuma Game."""
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        ("R", "RRR"),                # Single ball, enough hand
        ("RR", "R"),                 # Two balls, one more needed
        ("RRBBRR", "RB"),            # Symmetric board
        ("RYGBW", "RYGBW"),          # All different colors
        ("RRYYBB", "RYB"),           # Pairs of each color
    ]

    yielded = 0
    for board, hand in edge_cases:
        if yielded >= count:
            return
        yield f"{board}\n{hand}"
        yielded += 1

    # Random cases
    while yielded < count:
        # Generate valid board (no 3+ consecutive)
        board_len = random.randint(1, 12)
        board = []
        for _ in range(board_len):
            # Choose color that won't create 3+ consecutive
            available = list(COLORS)
            if len(board) >= 2 and board[-1] == board[-2]:
                available = [c for c in available if c != board[-1]]
            board.append(random.choice(available))
        board = ''.join(board)

        # Generate hand
        hand_len = random.randint(1, 5)
        hand = ''.join(random.choice(COLORS) for _ in range(hand_len))

        yield f"{board}\n{hand}"
        yielded += 1


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with board length approximately n.

    Creates a valid board and hand configuration.
    """
    n = min(n, 16)

    # Generate valid board
    board = []
    for _ in range(n):
        available = list(COLORS)
        if len(board) >= 2 and board[-1] == board[-2]:
            available = [c for c in available if c != board[-1]]
        board.append(random.choice(available))
    board = ''.join(board)

    # Generate hand (5 balls)
    hand = ''.join(random.choice(COLORS) for _ in range(5))

    return f"{board}\n{hand}"


if __name__ == "__main__":
    print("Sample test cases:")
    for i, case in enumerate(generate(3, seed=42)):
        print(f"Case {i+1}:")
        print(case)
        print()
