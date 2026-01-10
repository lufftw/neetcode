"""
Problem: Split Two Strings to Make Palindrome
Link: https://leetcode.com/problems/split-two-strings-to-make-palindrome/

You are given two strings a and b of the same length. Choose an index and
split both strings at the same index, splitting a into aprefix + asuffix
and b into bprefix + bsuffix.

Check if aprefix + bsuffix or bprefix + asuffix forms a palindrome.

When you split a string s, either prefix or suffix can be empty.

Return true if it is possible to form a palindrome string, otherwise false.

Example 1:
    Input: a = "x", b = "y"
    Output: true
    Explanation: "" + "y" = "y" is a palindrome.

Example 2:
    Input: a = "ulacfd", b = "jizalu"
    Output: true
    Explanation: "ula" + "alu" = "ulaalu" is a palindrome.

Example 3:
    Input: a = "xbdef", b = "xecab"
    Output: false

Constraints:
- 1 <= a.length, b.length <= 10^5
- a.length == b.length
- a and b consist of lowercase English letters

Topics: Two Pointers, String
"""
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "checkPalindromeFormation",
        "complexity": "O(n) time, O(1) space",
        "description": "Two pointers with middle palindrome check",
    },
}


# ============================================================================
# Solution: Two Pointers with Middle Palindrome Check
# Time: O(n), Space: O(1)
#
# Key insight: For aprefix + bsuffix to be palindrome:
# 1. a[0:k] must match reversed b[n-k:n] for some k (outer parts match)
# 2. The remaining middle part must be a palindrome
#
# We use two pointers from outside-in on (a, b) or (b, a).
# When characters match, continue inward. When they mismatch, check if
# the remaining middle portion of either string is a palindrome.
#
# Check both: aprefix + bsuffix AND bprefix + asuffix
# ============================================================================
class Solution:
    def checkPalindromeFormation(self, a: str, b: str) -> bool:
        """
        Check if we can form a palindrome by combining prefix of one string
        with suffix of another.

        Try both combinations: (a, b) and (b, a).
        For each, use two pointers to find matching outer portion,
        then check if middle is palindrome.

        Args:
            a: First string
            b: Second string

        Returns:
            True if palindrome can be formed
        """
        def is_palindrome(s: str, left: int, right: int) -> bool:
            """Check if s[left:right+1] is a palindrome."""
            while left < right:
                if s[left] != s[right]:
                    return False
                left += 1
                right -= 1
            return True

        def check(a: str, b: str) -> bool:
            """
            Check if aprefix + bsuffix can form a palindrome.

            Use two pointers: i from start of a, j from end of b.
            While a[i] == b[j], move inward (these outer parts match).
            When mismatch occurs, the middle part must be palindrome
            in either a or b.
            """
            n = len(a)
            i, j = 0, n - 1

            # Move pointers inward while outer parts match
            while i < j and a[i] == b[j]:
                i += 1
                j -= 1

            # If pointers crossed, whole thing is palindrome
            if i >= j:
                return True

            # Middle part must be palindrome in a OR b
            # Either a[i:j+1] is palindrome, or b[i:j+1] is palindrome
            return is_palindrome(a, i, j) or is_palindrome(b, i, j)

        # Try both combinations
        return check(a, b) or check(b, a)


def solve():
    """
    Input format:
    Line 1: a (JSON string)
    Line 2: b (JSON string)
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')

    a = json.loads(lines[0])
    b = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.checkPalindromeFormation(a, b)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
