"""
LeetCode 168: Excel Sheet Column Title
https://leetcode.com/problems/excel-sheet-column-title/

Pattern: Math / Number Theory - Base Conversion
API Kernel: MathNumberTheory

Given an integer columnNumber, return its corresponding column title as it appears in an Excel sheet.
A -> 1, B -> 2, ..., Z -> 26, AA -> 27, AB -> 28, ...
"""

import json
import sys
from typing import List

from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionMath",
        "method": "convertToTitle",
        "complexity": "O(log n) time, O(log n) space",
        "description": "Base-26 conversion with 1-indexed adjustment",
    },
}


def _reference_convert(columnNumber: int) -> str:
    """Reference implementation for validation."""
    result = []
    while columnNumber > 0:
        columnNumber -= 1  # Adjust for 1-indexed
        result.append(chr(ord("A") + columnNumber % 26))
        columnNumber //= 26
    return "".join(reversed(result))


def judge(actual, expected, input_data: str) -> bool:
    """Custom judge using reference implementation."""
    columnNumber = json.loads(input_data.strip())
    correct = _reference_convert(columnNumber)
    try:
        actual_str = str(actual).strip().strip('"')
        return actual_str == correct
    except (ValueError, TypeError):
        return False


JUDGE_FUNC = judge


class SolutionMath:
    """
    Base-26 conversion with 1-indexed adjustment.

    Excel columns are 1-indexed (A=1, not A=0), so we need to adjust:
    - Subtract 1 before taking modulo
    - This converts from 1-26 range to 0-25 range

    Process: n -> (n-1)%26 gives current digit, (n-1)//26 gives remaining
    """

    def convertToTitle(self, columnNumber: int) -> str:
        result = []
        while columnNumber > 0:
            columnNumber -= 1  # Convert to 0-indexed
            result.append(chr(ord("A") + columnNumber % 26))
            columnNumber //= 26
        return "".join(reversed(result))


def solve():
    lines = sys.stdin.read().strip().split("\n")

    columnNumber = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.convertToTitle(columnNumber)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
