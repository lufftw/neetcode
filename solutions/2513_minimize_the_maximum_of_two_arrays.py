"""
Problem: Minimize the Maximum of Two Arrays
Link: https://leetcode.com/problems/minimize-the-maximum-of-two-arrays/

We have two arrays arr1 and arr2 which are initially empty. You need to add
positive integers to them such that they satisfy all the following conditions:

1. arr1 contains uniqueCnt1 distinct positive integers, each NOT divisible by divisor1.
2. arr2 contains uniqueCnt2 distinct positive integers, each NOT divisible by divisor2.
3. No integer is present in both arr1 and arr2.

Return the minimum possible maximum integer that can be present in either array.

Example 1:
    Input: divisor1 = 2, divisor2 = 7, uniqueCnt1 = 1, uniqueCnt2 = 3
    Output: 4
    Explanation: arr1 = [1], arr2 = [2,3,4]. Max = 4.

Example 2:
    Input: divisor1 = 3, divisor2 = 5, uniqueCnt1 = 2, uniqueCnt2 = 1
    Output: 3
    Explanation: arr1 = [1,2], arr2 = [3]. Max = 3.

Example 3:
    Input: divisor1 = 2, divisor2 = 4, uniqueCnt1 = 8, uniqueCnt2 = 2
    Output: 15
    Explanation: arr1 = [1,3,5,7,9,11,13,15], arr2 = [2,6]. Max = 15.

Constraints:
- 2 <= divisor1, divisor2 <= 10^5
- 1 <= uniqueCnt1, uniqueCnt2 < 10^9
- 2 <= uniqueCnt1 + uniqueCnt2 <= 10^9

Topics: Math, Binary Search, Number Theory
"""
from math import gcd
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "minimizeSet",
        "complexity": "O(log(uniqueCnt1 + uniqueCnt2)) time, O(1) space",
        "description": "Binary search with inclusion-exclusion counting",
    },
}


# ============================================================================
# Solution: Binary Search with Inclusion-Exclusion
# Time: O(log(answer)), Space: O(1)
#
# Key insight: Binary search on the maximum value m. For a given m, check if
# we can fill both arrays using numbers from 1 to m.
#
# Counting available numbers in [1, m]:
# - Not divisible by d1: m - m//d1
# - Not divisible by d2: m - m//d2
# - Not divisible by either: m - m//d1 - m//d2 + m//lcm(d1,d2)
# - Divisible by d1 but not d2: m//d1 - m//lcm
# - Divisible by d2 but not d1: m//d2 - m//lcm
#
# Numbers available:
# - For arr1 only (not div by d1, but div by d2): available to fill arr1
# - For arr2 only (not div by d2, but div by d1): available to fill arr2
# - For either (not div by d1 OR d2): can be assigned to either
#
# Feasibility: Can we satisfy both uniqueCnt1 and uniqueCnt2?
# ============================================================================
class Solution:
    def minimizeSet(self, divisor1: int, divisor2: int, uniqueCnt1: int, uniqueCnt2: int) -> int:
        """
        Find minimum maximum value to fill both arrays with required constraints.

        Binary search on answer. For each candidate m, use inclusion-exclusion
        to count how many numbers in [1, m] are available for each array and
        check if requirements can be satisfied.

        Args:
            divisor1: Numbers in arr1 cannot be divisible by this
            divisor2: Numbers in arr2 cannot be divisible by this
            uniqueCnt1: Required count for arr1
            uniqueCnt2: Required count for arr2

        Returns:
            Minimum possible maximum value in either array
        """
        def lcm(a: int, b: int) -> int:
            return a * b // gcd(a, b)

        d1, d2 = divisor1, divisor2
        L = lcm(d1, d2)

        def can_fill(m: int) -> bool:
            """
            Check if we can fill both arrays using numbers 1 to m.

            Categorize numbers:
            - only_arr1: not div by d1, but div by d2 (can only go to arr1)
            - only_arr2: not div by d2, but div by d1 (can only go to arr2)
            - either: not div by d1 AND not div by d2 (can go to either)

            We assign only_arr1 to arr1 first, only_arr2 to arr2 first,
            then use "either" numbers to fill remaining needs.
            """
            # Numbers divisible by d1: m // d1
            # Numbers divisible by d2: m // d2
            # Numbers divisible by both (lcm): m // L

            # not_div_d1 = m - m // d1 (can go to arr1)
            # not_div_d2 = m - m // d2 (can go to arr2)
            # not_div_either = m - m//d1 - m//d2 + m//L (can go to either)

            not_div_d1 = m - m // d1  # Can be in arr1
            not_div_d2 = m - m // d2  # Can be in arr2
            not_div_either = m - m // d1 - m // d2 + m // L  # Can be in either

            # Check if we have enough numbers:
            # 1. arr1 needs uniqueCnt1 numbers not div by d1
            # 2. arr2 needs uniqueCnt2 numbers not div by d2
            # 3. Numbers not div by either can be shared

            # First check: do we have enough numbers for arr1?
            if not_div_d1 < uniqueCnt1:
                return False

            # Second check: do we have enough numbers for arr2?
            if not_div_d2 < uniqueCnt2:
                return False

            # Third check: can we satisfy both using shared "either" pool?
            # After using "only_arrX" numbers, remaining needs come from "either"
            # Need: max(0, uniqueCnt1 - only_arr1) + max(0, uniqueCnt2 - only_arr2) <= either
            # But only_arr1 = not_div_d1 - not_div_either (can only go arr1)
            # only_arr2 = not_div_d2 - not_div_either

            # Actually, simpler: total needed from "either" pool
            # = (uniqueCnt1 that can't be filled by "only_arr1") + (same for arr2)
            # But let's use: need1 + need2 <= not_div_either where
            # need1 = max(0, uniqueCnt1 - (not_div_d1 - not_div_either))
            # Simplify: uniqueCnt1 + uniqueCnt2 <= not_div_d1 + not_div_d2 - not_div_either

            # Hmm, let me think again. The "either" pool can be used for both.
            # Total available = not_div_d1 + not_div_d2 - not_div_either
            # (not_div_d1 includes "either", not_div_d2 includes "either")
            # So total distinct = not_div_d1 + not_div_d2 - not_div_either

            # We need uniqueCnt1 + uniqueCnt2 <= total distinct
            return uniqueCnt1 + uniqueCnt2 <= not_div_d1 + not_div_d2 - not_div_either

        # Binary search for minimum m
        lo, hi = 1, 2 * (uniqueCnt1 + uniqueCnt2)

        while lo < hi:
            mid = (lo + hi) // 2
            if can_fill(mid):
                hi = mid
            else:
                lo = mid + 1

        return lo


def solve():
    """
    Input format:
    Line 1: divisor1 (integer)
    Line 2: divisor2 (integer)
    Line 3: uniqueCnt1 (integer)
    Line 4: uniqueCnt2 (integer)
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')

    divisor1 = json.loads(lines[0])
    divisor2 = json.loads(lines[1])
    uniqueCnt1 = json.loads(lines[2])
    uniqueCnt2 = json.loads(lines[3])

    solver = get_solver(SOLUTIONS)
    result = solver.minimizeSet(divisor1, divisor2, uniqueCnt1, uniqueCnt2)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
