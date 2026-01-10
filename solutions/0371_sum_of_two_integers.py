"""
Problem: Sum of Two Integers
Link: https://leetcode.com/problems/sum-of-two-integers/

Given two integers a and b, return the sum of the two integers without using the
operators + and -.

Example 1:
    Input: a = 1, b = 2
    Output: 3

Example 2:
    Input: a = 2, b = 3
    Output: 5

Constraints:
- -1000 <= a, b <= 1000

Topics: Math, Bit Manipulation
"""

import json
from _runner import get_solver


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionBitManipulation",
        "method": "getSum",
        "complexity": "O(1) time, O(1) space",
        "description": "XOR for sum without carry, AND+shift for carry, iterate",
    },
    "recursive": {
        "class": "SolutionRecursive",
        "method": "getSum",
        "complexity": "O(1) time, O(1) space",
        "description": "Recursive version of bit manipulation approach",
    },
}


# ============================================================================
# Solution 1: Iterative Bit Manipulation
# Time: O(1) - at most 32 iterations for 32-bit integers
# Space: O(1)
#
# Key Insight:
#   Binary addition can be decomposed into two operations:
#   1. Sum without carry: a XOR b (adds bits where exactly one is 1)
#   2. Carry: (a AND b) << 1 (identifies positions where both bits are 1,
#      then shifts left since carry goes to next position)
#
#   We iterate: new_a = a XOR b, new_b = (a AND b) << 1
#   Until carry (b) becomes 0, then a holds the final sum.
#
# Why This Works:
#   Consider adding 5 (101) + 3 (011):
#   - XOR: 101 ^ 011 = 110 (sum without carry)
#   - AND << 1: (101 & 011) << 1 = 001 << 1 = 010 (carry)
#   - Next iteration: 110 ^ 010 = 100, (110 & 010) << 1 = 100
#   - Next: 100 ^ 100 = 000, carry = 1000
#   - Next: 000 ^ 1000 = 1000, carry = 0
#   - Result: 1000 = 8 ✓
#
# Python Caveat:
#   Python integers have arbitrary precision, so negative numbers don't
#   naturally overflow to fit in 32 bits. We must mask to 32 bits and
#   handle sign extension for the final result.
# ============================================================================
class SolutionBitManipulation:
    """
    Iterative bit manipulation using XOR and AND operations.

    XOR gives us the sum without considering carries. AND identifies where
    carries occur, and left shift positions them correctly. We iterate
    until no more carries remain.

    Python's arbitrary precision integers require masking to simulate
    32-bit arithmetic for proper handling of negative numbers.
    """

    def getSum(self, a: int, b: int) -> int:
        # 32-bit mask to simulate fixed-width integer
        MASK = 0xFFFFFFFF  # 32 ones
        MAX_INT = 0x7FFFFFFF  # Max positive 32-bit signed int

        while b != 0:
            # Calculate sum without carry and carry
            sum_without_carry = (a ^ b) & MASK
            carry = ((a & b) << 1) & MASK

            a = sum_without_carry
            b = carry

        # If a is negative in 32-bit two's complement, convert to Python negative
        # Check if sign bit (bit 31) is set
        if a > MAX_INT:
            # Convert from unsigned to signed (two's complement)
            a = ~(a ^ MASK)

        return a


# ============================================================================
# Solution 2: Recursive Bit Manipulation
# Time: O(1), Space: O(1) - tail recursion, constant stack depth
#
# Key Insight:
#   Same logic as iterative, expressed recursively. Base case is when
#   carry (b) becomes 0. Recursive case computes new sum and carry.
#
# This is more elegant but may hit recursion limits in some languages.
# Python handles it fine for 32-bit numbers (at most 32 recursive calls).
# ============================================================================
class SolutionRecursive:
    """
    Recursive bit manipulation approach.

    Base case: when carry is 0, return the accumulated sum.
    Recursive case: compute new sum (XOR) and new carry (AND << 1).

    Same algorithm as iterative, different control flow structure.
    """

    def getSum(self, a: int, b: int) -> int:
        MASK = 0xFFFFFFFF
        MAX_INT = 0x7FFFFFFF

        # Apply mask for negative number handling
        a = a & MASK
        b = b & MASK

        def add(x: int, y: int) -> int:
            if y == 0:
                return x
            return add((x ^ y) & MASK, ((x & y) << 1) & MASK)

        result = add(a, b)

        # Convert back from unsigned to signed if necessary
        if result > MAX_INT:
            result = ~(result ^ MASK)

        return result


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: integer a
        Line 2: integer b

    Example:
        1
        2
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")

    a = json.loads(lines[0])
    b = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.getSum(a, b)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
