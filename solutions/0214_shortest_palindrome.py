"""
Problem: Shortest Palindrome
Link: https://leetcode.com/problems/shortest-palindrome/

You are given a string s. You can convert s to a palindrome by adding
characters in front of it.

Return the shortest palindrome you can find by performing this transformation.

Example 1:
    Input: s = "aacecaaa"
    Output: "aaacecaaa"

Example 2:
    Input: s = "abcd"
    Output: "dcbabcd"

Constraints:
- 0 <= s.length <= 5 * 10^4
- s consists of lowercase English letters only.

Topics: String, Rolling Hash, String Matching, Hash Function
"""
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "shortestPalindrome",
        "complexity": "O(n) time, O(n) space",
        "description": "KMP on s + '#' + reverse(s) to find longest palindromic prefix",
    },
    "rolling_hash": {
        "class": "SolutionRollingHash",
        "method": "shortestPalindrome",
        "complexity": "O(n) time, O(1) space",
        "description": "Rolling hash to find palindromic prefix",
    },
}


# ============================================================================
# Solution: KMP Failure Function
# Time: O(n), Space: O(n)
#   - Create s + '#' + reverse(s) and compute failure function
#   - failure[-1] = length of longest palindromic prefix
#   - Prepend reverse of remaining suffix
# ============================================================================
class Solution:
    def shortestPalindrome(self, s: str) -> str:
        """
        Find shortest palindrome by prepending characters to s.

        Key insight: The longest palindromic prefix of s equals the longest
        proper prefix of (s + '#' + reverse(s)) that is also a suffix.

        Why? If s starts with palindrome P of length k:
        - P is prefix of s
        - reverse(P) = P is suffix of reverse(s)
        - So P appears as both prefix and suffix of concatenated string

        The '#' separator prevents false matches where prefix extends
        into reverse(s) portion.

        Example: s = "aacecaaa"
        concat = "aacecaaa#aaacecaa"
        failure[-1] = 7 (longest palindromic prefix "aacecaa")
        Result = reverse("a") + s = "aaacecaaa"
        """
        if not s or len(s) <= 1:
            return s

        # Create concatenated string with separator
        reversed_s = s[::-1]
        concat = s + '#' + reversed_s

        # Build failure function (LPS array)
        concat_length = len(concat)
        failure: list[int] = [0] * concat_length

        prefix_length = 0
        for idx in range(1, concat_length):
            while prefix_length > 0 and concat[idx] != concat[prefix_length]:
                prefix_length = failure[prefix_length - 1]

            if concat[idx] == concat[prefix_length]:
                prefix_length += 1

            failure[idx] = prefix_length

        # failure[-1] = length of longest palindromic prefix
        palindrome_prefix_length = failure[-1]

        # Prepend reverse of non-palindromic suffix
        suffix_to_prepend = reversed_s[:len(s) - palindrome_prefix_length]

        return suffix_to_prepend + s


# ============================================================================
# Solution: Rolling Hash
# Time: O(n), Space: O(1)
#   - Compute forward and backward hashes simultaneously
#   - When they match at position i, s[0:i+1] is potentially a palindrome
#   - Track the longest such position
# ============================================================================
class SolutionRollingHash:
    def shortestPalindrome(self, s: str) -> str:
        """
        Use rolling hash to find longest palindromic prefix.

        Compute forward and backward hashes simultaneously:
        - Forward hash: h = h * BASE + char (standard polynomial hash)
        - Backward hash: h = h + char * BASE^i (reverse direction)

        When forward_hash == backward_hash, the substring s[0:i+1]
        reads the same forwards and backwards, i.e., it's a palindrome.

        Note: Hash collisions may cause false positives, but since we
        track the longest match, any false positive would only cause
        us to find a palindrome that's "too long", which still works
        (we'd prepend fewer characters than necessary but result is valid).
        """
        if not s or len(s) <= 1:
            return s

        BASE = 29
        MOD = 10**9 + 7

        forward_hash = 0
        backward_hash = 0
        power = 1
        longest_palindrome_end = 0

        for idx, char in enumerate(s):
            char_val = ord(char) - ord('a') + 1

            # Forward hash: reading left to right
            forward_hash = (forward_hash * BASE + char_val) % MOD

            # Backward hash: reading right to left (building from position 0)
            backward_hash = (backward_hash + char_val * power) % MOD

            if forward_hash == backward_hash:
                # Found potential palindromic prefix ending at idx
                longest_palindrome_end = idx

            power = (power * BASE) % MOD

        # Prepend reverse of suffix after longest palindromic prefix
        suffix = s[longest_palindrome_end + 1:]
        return suffix[::-1] + s


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
    result = solver.shortestPalindrome(s)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
