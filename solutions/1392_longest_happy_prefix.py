"""
Problem: Longest Happy Prefix
Link: https://leetcode.com/problems/longest-happy-prefix/

A string is called a happy prefix if is a non-empty prefix which is also a
suffix (excluding itself).

Given a string s, return the longest happy prefix of s. Return an empty string
"" if no such prefix exists.

Example 1:
    Input: s = "level"
    Output: "l"
    Explanation: s contains 4 prefix excluding itself ("l", "le", "lev", "leve"),
                 and suffix ("l", "el", "vel", "evel").
                 The largest prefix which is also suffix is "l".

Example 2:
    Input: s = "ababab"
    Output: "abab"
    Explanation: "abab" is the largest prefix which is also suffix.
                 They can overlap in the original string.

Constraints:
- 1 <= s.length <= 10^5
- s contains only lowercase English letters.

Topics: String, Rolling Hash, String Matching, Hash Function
"""
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "longestPrefix",
        "complexity": "O(n) time, O(n) space",
        "description": "KMP failure function - direct application",
    },
    "rolling_hash": {
        "class": "SolutionRollingHash",
        "method": "longestPrefix",
        "complexity": "O(n) time, O(1) space",
        "description": "Rolling hash comparing prefix and suffix",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================

def _longest_happy_prefix_brute(s: str) -> str:
    """Find longest happy prefix using brute force O(n^2)."""
    n = len(s)
    for length in range(n - 1, 0, -1):
        if s[:length] == s[n - length:]:
            return s[:length]
    return ""


def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result for Longest Happy Prefix.

    Args:
        actual: Program output (the prefix string)
        expected: Expected output (None if from generator)
        input_data: Raw input string

    Returns:
        bool: True if correct
    """
    import json

    s = json.loads(input_data.strip())

    # Parse actual result
    if isinstance(actual, str):
        if actual.startswith('"') and actual.endswith('"'):
            actual_val = json.loads(actual)
        else:
            actual_val = actual
    else:
        return False

    # Verify using brute force
    correct = _longest_happy_prefix_brute(s)
    return actual_val == correct


JUDGE_FUNC = judge


# ============================================================================
# Solution: KMP Failure Function
# Time: O(n), Space: O(n)
#   - Build failure function for the string
#   - failure[n-1] directly gives the length of longest happy prefix
#   - This is the most direct application of the KMP failure function
# ============================================================================
class Solution:
    def longestPrefix(self, s: str) -> str:
        """
        Find longest happy prefix using KMP failure function.

        The failure function (also called LPS - Longest Proper Prefix
        which is also Suffix) at position n-1 gives exactly what we need:
        the length of the longest proper prefix that is also a suffix.

        "Proper" means the prefix/suffix cannot be the entire string.

        Example: s = "ababab"
        Index:  0  1  2  3  4  5
        Char:   a  b  a  b  a  b
        LPS:    0  0  1  2  3  4

        failure[5] = 4, so longest happy prefix = s[0:4] = "abab"
        """
        string_length = len(s)

        if string_length <= 1:
            return ""

        # Build failure function (LPS array)
        failure: list[int] = [0] * string_length

        prefix_length = 0
        for idx in range(1, string_length):
            while prefix_length > 0 and s[idx] != s[prefix_length]:
                prefix_length = failure[prefix_length - 1]

            if s[idx] == s[prefix_length]:
                prefix_length += 1

            failure[idx] = prefix_length

        # The answer is directly failure[n-1]
        happy_prefix_length = failure[-1]

        return s[:happy_prefix_length]


# ============================================================================
# Solution: Rolling Hash
# Time: O(n), Space: O(1)
#   - Compute prefix and suffix hashes simultaneously
#   - Track longest position where both hashes match
#   - More space-efficient but may have hash collisions
# ============================================================================
class SolutionRollingHash:
    def longestPrefix(self, s: str) -> str:
        """
        Find longest happy prefix using rolling hash.

        Compute prefix and suffix hashes simultaneously:
        - Prefix hash: s[0:i+1] computed left to right
        - Suffix hash: s[n-i-1:n] computed right to left

        We iterate i from 0 to n-2 (excluding full string):
        - prefix_hash represents hash of s[0:i+1]
        - suffix_hash represents hash of s[n-i-1:n]

        When they match, we found a potential happy prefix.

        Hash computation:
        - prefix_hash = h * BASE + char (standard polynomial)
        - suffix_hash = h + char * power (reverse direction)

        These compute the same hash value for the same string
        regardless of which end we start from.
        """
        string_length = len(s)

        if string_length <= 1:
            return ""

        BASE = 31
        MOD = 10**9 + 7

        prefix_hash = 0
        suffix_hash = 0
        power = 1
        longest_length = 0

        # Compare prefix s[0:i+1] with suffix s[n-i-1:n]
        for idx in range(string_length - 1):
            prefix_char = ord(s[idx]) - ord('a') + 1
            suffix_char = ord(s[string_length - 1 - idx]) - ord('a') + 1

            # Prefix hash: h = h * BASE + char (left to right)
            prefix_hash = (prefix_hash * BASE + prefix_char) % MOD

            # Suffix hash: h = h + char * power (right to left)
            # This builds the hash as if we're reading the suffix from its start
            suffix_hash = (suffix_hash + suffix_char * power) % MOD

            power = (power * BASE) % MOD

            if prefix_hash == suffix_hash:
                # Found matching prefix and suffix of length idx + 1
                longest_length = idx + 1

        return s[:longest_length]


def solve():
    """
    Input format:
    Line 1: s (string, JSON format)
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')

    s = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.longestPrefix(s)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
