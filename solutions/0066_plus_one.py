# solutions/0066_plus_one.py
"""
Problem: Plus One
https://leetcode.com/problems/plus-one/

You are given a large integer represented as an integer array digits, where
each digits[i] is the ith digit of the integer. The digits are ordered from
most significant to least significant in left-to-right order. The large
integer does not contain any leading 0's.

Increment the large integer by one and return the resulting array of digits.

Constraints:
- 1 <= digits.length <= 100
- 0 <= digits[i] <= 9
- digits does not contain any leading 0's
"""
from typing import List
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionIterative",
        "method": "plusOne",
        "complexity": "O(n) time, O(1) space",
        "description": "Right-to-left iteration with carry propagation",
    },
    "pythonic": {
        "class": "SolutionPythonic",
        "method": "plusOne",
        "complexity": "O(n) time, O(n) space",
        "description": "Convert to integer, add one, convert back",
    },
}


class SolutionIterative:
    """
    In-place iteration handling carry propagation from right to left.

    Starting from the least significant digit (rightmost), we add one.
    If the result is less than 10, we're done. Otherwise, we set that
    digit to 0 and propagate the carry to the next position.

    The only case requiring array expansion is when all digits are 9
    (e.g., 999 -> 1000). In this case, after the loop completes with
    carry still pending, we prepend 1 to the array.
    """

    def plusOne(self, digits: List[int]) -> List[int]:
        n = len(digits)

        # Traverse from right to left
        for i in range(n - 1, -1, -1):
            # If digit is less than 9, simply increment and return
            # No carry propagation needed
            if digits[i] < 9:
                digits[i] += 1
                return digits

            # Digit is 9, set to 0 and continue (carry propagates)
            digits[i] = 0

        # All digits were 9, need to prepend 1
        # e.g., [9,9,9] -> [1,0,0,0]
        return [1] + digits


class SolutionPythonic:
    """
    Pythonic approach leveraging arbitrary precision integers.

    Convert the digit array to an integer, add one, then convert back.
    While less efficient due to string conversions, this approach is
    concise and leverages Python's built-in arbitrary precision math.

    This solution demonstrates Python's flexibility but wouldn't
    translate directly to languages with fixed-size integers.
    """

    def plusOne(self, digits: List[int]) -> List[int]:
        # Convert to integer: join digits as string, then parse
        num = int("".join(map(str, digits)))

        # Add one
        num += 1

        # Convert back to list of digits
        return [int(d) for d in str(num)]


def judge(actual, expected, input_data: str) -> bool:
    """
    Validate plus one result.
    """
    import json

    digits = json.loads(input_data.strip())

    # Compute expected using integer conversion
    num = int("".join(map(str, digits))) + 1
    expected_result = [int(d) for d in str(num)]

    return actual == expected_result


JUDGE_FUNC = judge


def solve():
    import sys
    import json

    lines = sys.stdin.read().strip().split("\n")

    # Parse input: digits array
    digits = json.loads(lines[0])

    # Get solver and compute
    solver = get_solver(SOLUTIONS)
    result = solver.plusOne(digits)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
