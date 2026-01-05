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
# Solution: Greedy Monotonic Increasing Stack
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

    print(result)


if __name__ == "__main__":
    solve()
