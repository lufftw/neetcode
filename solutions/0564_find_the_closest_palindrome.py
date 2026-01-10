"""
Problem: Find the Closest Palindrome
Link: https://leetcode.com/problems/find-the-closest-palindrome/

Given a string n representing an integer, return the closest integer (not
including itself), which is a palindrome. If there is a tie, return the
smaller one.

The closest is defined as the absolute difference minimized between two integers.

Example 1:
    Input: n = "123"
    Output: "121"

Example 2:
    Input: n = "1"
    Output: "0"

Constraints:
- 1 <= n.length <= 18
- n consists of only digits.
- n does not have leading zeros.
- n is representing an integer in the range [1, 10^18 - 1].

Topics: Math, String
"""
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "nearestPalindromic",
        "complexity": "O(d) time, O(d) space",
        "description": "Generate candidates by mirroring with adjustments",
    },
}


# ============================================================================
# Solution: Generate Candidates by Mirroring
# Time: O(d), Space: O(d) where d = number of digits
#
# Key insight: The closest palindrome is one of these candidates:
# 1. Mirror left half as-is (e.g., "123" -> "121")
# 2. Mirror left half + 1 (e.g., "123" -> "131" from 12+1=13)
# 3. Mirror left half - 1 (e.g., "123" -> "111" from 12-1=11)
# 4. 10^d + 1 (e.g., "99" -> "101")
# 5. 10^(d-1) - 1 (e.g., "100" -> "99")
#
# We generate all candidates, exclude n itself, and pick the closest.
# ============================================================================
class Solution:
    def nearestPalindromic(self, n: str) -> str:
        """
        Find the closest palindrome to n (not including n itself).

        Strategy: Generate 5 candidate palindromes and pick the closest.
        - Candidates come from mirroring the left half with adjustments.
        - Special cases for edge boundaries like 10...0 and 99...9.

        Args:
            n: String representation of the input number

        Returns:
            String representation of the closest palindrome
        """
        length = len(n)
        num = int(n)

        # Edge case: single digit
        if length == 1:
            return str(num - 1)

        candidates = set()

        # Candidate 1: 10^length + 1 (e.g., 1001 for length 3)
        # Handles cases like 999 -> 1001
        candidates.add(10**length + 1)

        # Candidate 2: 10^(length-1) - 1 (e.g., 99 for length 3)
        # Handles cases like 1000 -> 999
        candidates.add(10**(length - 1) - 1)

        # Get left half (including middle for odd length)
        half_len = (length + 1) // 2
        left_half = int(n[:half_len])

        # Generate palindromes from left_half, left_half+1, left_half-1
        for delta in [-1, 0, 1]:
            new_left = str(left_half + delta)

            # Build palindrome by mirroring
            if length % 2 == 0:
                # Even length: mirror entire left half
                palindrome = new_left + new_left[::-1]
            else:
                # Odd length: don't duplicate the middle character
                palindrome = new_left + new_left[-2::-1]

            candidates.add(int(palindrome))

        # Remove n itself (we need a different number)
        candidates.discard(num)

        # Find the closest candidate
        # If tie, return the smaller one
        result = None
        min_diff = float('inf')

        for cand in candidates:
            diff = abs(cand - num)
            if diff < min_diff or (diff == min_diff and cand < result):
                min_diff = diff
                result = cand

        return str(result)


def solve():
    """
    Input format:
    Line 1: n (JSON string)
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')

    n = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.nearestPalindromic(n)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
