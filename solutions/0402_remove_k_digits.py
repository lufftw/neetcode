"""
Problem: Remove K Digits
Link: https://leetcode.com/problems/remove-k-digits/

Given string num representing a non-negative integer num, and an integer k, return the smallest possible integer after removing k digits from num.

Example 1:
    Input: num = "1432219", k = 3
    Output: "1219"
    Explanation: Remove the three digits 4, 3, and 2 to form the new number 1219 which is the smallest.

Example 2:
    Input: num = "10200", k = 1
    Output: "200"
    Explanation: Remove the leading 1 and the number is 200. Note that the output must not contain leading zeroes.

Example 3:
    Input: num = "10", k = 2
    Output: "0"
    Explanation: Remove all the digits from the number and it is left with nothing which is 0.

Constraints:
- 1 <= k <= num.length <= 10^5
- num consists of only digits.
- num does not have any leading zeros except for the zero itself.

Topics: String, Stack, Greedy, Monotonic Stack
"""


from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionGreedyStack",
        "method": "removeKdigits",
        "complexity": "O(n) time, O(n) space",
        "description": "Monotonic increasing stack for greedy digit selection",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output is the smallest number.

    Args:
        actual: Program output (string with or without quotes)
        expected: Expected output (None if from generator)
        input_data: Raw input string (num on line 1, k on line 2)

    Returns:
        bool: True if correct smallest number after removing k digits
    """
    import json
    lines = input_data.strip().split("\n")
    num = json.loads(lines[0]) if lines[0] else ""
    k = int(lines[1]) if len(lines) > 1 else 0

    # Compute correct answer using reference solution
    correct = _reference_remove_k(num, k)

    # Handle JSON-encoded string output
    actual_str = actual.strip()
    if actual_str.startswith('"') and actual_str.endswith('"'):
        actual_str = json.loads(actual_str)

    return actual_str == correct


def _reference_remove_k(num: str, k: int) -> str:
    """O(n) reference using greedy stack."""
    stack: list[str] = []
    for digit in num:
        while k and stack and stack[-1] > digit:
            stack.pop()
            k -= 1
        stack.append(digit)
    # Remove remaining k digits from end
    if k:
        stack = stack[:-k]
    # Remove leading zeros and handle empty result
    result = "".join(stack).lstrip("0")
    return result if result else "0"


JUDGE_FUNC = judge


# ============================================================================
# Solution 1: Greedy Monotonic Increasing Stack
# Time: O(n), Space: O(n)
#   - Build monotonically increasing stack of digits (greedy best prefix)
#   - When new digit is smaller than stack top, pop the larger digit (if k > 0)
#   - Each pop decreases k; this locally optimal choice leads to global optimum
#   - Handle remaining k by trimming from end (stack is increasing, end is largest)
#   - Handle leading zeros with lstrip
#
# Key Insight: To minimize a number, place smaller digits as far left as possible.
# When we see a digit d smaller than stack top s, removing s makes the number
# smaller (e.g., "14..." -> "1..." when we see the 4 could be replaced by something
# smaller). The monotonic increasing property ensures the "best prefix so far".
#
# Greedy Correctness: Removing a peak digit (larger than its successor) always
# produces a smaller number than any other single removal. Repeating k times
# gives the k-optimal solution.
# ============================================================================
class SolutionGreedyStack:
    def removeKdigits(self, num: str, k: int) -> str:
        if k >= len(num):
            return "0"

        digit_stack: list[str] = []
        remaining_removals = k

        for digit in num:
            # Pop larger digits while we can still remove
            while (
                remaining_removals > 0
                and digit_stack
                and digit_stack[-1] > digit
            ):
                digit_stack.pop()
                remaining_removals -= 1

            digit_stack.append(digit)

        # If removals remain, trim from the end (stack is increasing)
        if remaining_removals > 0:
            digit_stack = digit_stack[:-remaining_removals]

        # Remove leading zeros and handle empty result
        result = "".join(digit_stack).lstrip("0")

        return result if result else "0"


def solve():
    """
    Input format (JSON literal, one per line):
        num: str
        k: int

    Output: str
    """
    import sys
    import json

    data = sys.stdin.read().strip().split('\n')

    num = json.loads(data[0].strip()) if data[0].strip().startswith('"') else data[0].strip()
    k = int(data[1].strip())

    solver = get_solver(SOLUTIONS)
    result = solver.removeKdigits(num, k)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
