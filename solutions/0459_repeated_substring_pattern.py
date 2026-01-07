"""
Problem: Repeated Substring Pattern
Link: https://leetcode.com/problems/repeated-substring-pattern/

Given a string s, check if it can be constructed by taking a substring of it
and appending multiple copies of the substring together.

Example 1:
    Input: s = "abab"
    Output: true
    Explanation: It is the substring "ab" twice.

Example 2:
    Input: s = "aba"
    Output: false

Example 3:
    Input: s = "abcabcabcabc"
    Output: true
    Explanation: It is the substring "abc" four times.

Constraints:
- 1 <= s.length <= 10^4
- s consists of lowercase English letters.

Topics: String, String Matching
"""
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "repeatedSubstringPattern",
        "complexity": "O(n) time, O(n) space",
        "description": "KMP failure function to check periodicity",
    },
    "concatenation": {
        "class": "SolutionConcatenation",
        "method": "repeatedSubstringPattern",
        "complexity": "O(n) time, O(n) space",
        "description": "Elegant s+s trick",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================

def _is_periodic(s: str) -> bool:
    """Check if string is built from repeating substrings using brute force."""
    n = len(s)
    for period_len in range(1, n // 2 + 1):
        if n % period_len == 0:
            pattern = s[:period_len]
            if pattern * (n // period_len) == s:
                return True
    return False


def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result for Repeated Substring Pattern.

    Args:
        actual: Program output (true/false)
        expected: Expected output (None if from generator)
        input_data: Raw input string

    Returns:
        bool: True if correct
    """
    import json

    s = json.loads(input_data.strip())

    # Convert actual to bool
    if isinstance(actual, bool):
        actual_val = actual
    elif isinstance(actual, str):
        actual_val = actual.lower() == 'true'
    else:
        return False

    # Verify using brute force
    correct = _is_periodic(s)
    return actual_val == correct


JUDGE_FUNC = judge


# ============================================================================
# Solution: KMP Failure Function
# Time: O(n), Space: O(n)
#   - Use the property: if failure[n-1] > 0 and n % (n - failure[n-1]) == 0,
#     then the string is built from repeated substrings
#   - Period length = n - failure[n-1]
# ============================================================================
class Solution:
    def repeatedSubstringPattern(self, s: str) -> bool:
        """
        Check if string is built from repeated substrings using KMP.

        Key insight: For a periodic string of length n with period p,
        the KMP failure function satisfies: failure[n-1] = n - p.

        Therefore, period p = n - failure[n-1].
        The string is periodic if p divides n and p < n.
        """
        string_length = len(s)

        if string_length <= 1:
            return False

        # Build failure function (LPS array)
        failure: list[int] = [0] * string_length

        prefix_length = 0
        for idx in range(1, string_length):
            while prefix_length > 0 and s[idx] != s[prefix_length]:
                prefix_length = failure[prefix_length - 1]

            if s[idx] == s[prefix_length]:
                prefix_length += 1

            failure[idx] = prefix_length

        # Check for periodicity
        longest_prefix_suffix = failure[-1]

        # No prefix=suffix means no period
        if longest_prefix_suffix == 0:
            return False

        # Calculate period length
        period_length = string_length - longest_prefix_suffix

        # String is periodic if period divides length
        return string_length % period_length == 0


# ============================================================================
# Solution: Concatenation Trick
# Time: O(n), Space: O(n)
#   - Elegant observation: s is periodic iff s appears in (s+s)[1:-1]
#   - If s = "abab", then s+s = "abababab", removing ends gives "bababa"
#     which still contains "abab" because it's periodic
# ============================================================================
class SolutionConcatenation:
    def repeatedSubstringPattern(self, s: str) -> bool:
        """
        Check periodicity using the concatenation trick.

        Key insight: If s is built from repeating unit U, then s+s contains
        s at positions other than 0 and len(s).

        Example: s = "abab" (U = "ab")
        s+s = "abababab"
        Remove first and last char: "bababa"
        "abab" is found in "bababa" at position 1

        By removing first and last character, we eliminate trivial matches
        at position 0 and len(s).
        """
        doubled = s + s
        # Check if s appears in the middle (not at boundaries)
        return s in doubled[1:-1]


def solve():
    """
    Input format:
    Line 1: s (string)
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')

    s = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.repeatedSubstringPattern(s)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
