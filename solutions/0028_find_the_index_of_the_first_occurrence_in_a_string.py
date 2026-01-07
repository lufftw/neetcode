"""
Problem: Find the Index of the First Occurrence in a String
Link: https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/

Given two strings needle and haystack, return the index of the first occurrence
of needle in haystack, or -1 if needle is not part of haystack.

Example 1:
    Input: haystack = "sadbutsad", needle = "sad"
    Output: 0
    Explanation: "sad" occurs at index 0 and 6. The first occurrence is at index 0.

Example 2:
    Input: haystack = "leetcode", needle = "leeto"
    Output: -1
    Explanation: "leeto" did not occur in "leetcode", so we return -1.

Constraints:
- 1 <= haystack.length, needle.length <= 10^4
- haystack and needle consist of only lowercase English characters.

Topics: Two Pointers, String, String Matching
"""
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "strStr",
        "complexity": "O(m+n) time, O(n) space",
        "description": "KMP algorithm with failure function",
    },
    "rabin_karp": {
        "class": "SolutionRabinKarp",
        "method": "strStr",
        "complexity": "O(m+n) average time, O(1) space",
        "description": "Rabin-Karp rolling hash",
    },
}


# ============================================================================
# Solution: KMP Algorithm
# Time: O(m+n), Space: O(n) where m = haystack length, n = needle length
#   - Preprocess needle to build failure function
#   - Search haystack using failure function to skip redundant comparisons
# ============================================================================
class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        """
        Find first occurrence of needle in haystack using KMP algorithm.

        The KMP algorithm's key insight: when a mismatch occurs at position j
        in the pattern, we don't need to restart from position 0. Instead,
        we use the failure function to jump to the position where we know
        characters already match.

        The failure function (LPS array) stores the length of the longest
        proper prefix that is also a suffix for each prefix of the pattern.
        """
        if not needle:
            return 0

        needle_length = len(needle)
        haystack_length = len(haystack)

        if needle_length > haystack_length:
            return -1

        # Build failure function (LPS array)
        failure: list[int] = [0] * needle_length

        prefix_length = 0
        for idx in range(1, needle_length):
            # Backtrack until we find a match or reach the start
            while prefix_length > 0 and needle[idx] != needle[prefix_length]:
                prefix_length = failure[prefix_length - 1]

            if needle[idx] == needle[prefix_length]:
                prefix_length += 1

            failure[idx] = prefix_length

        # Search using the failure function
        pattern_idx = 0

        for text_idx in range(haystack_length):
            text_char = haystack[text_idx]

            # On mismatch, use failure function to find next comparison point
            while pattern_idx > 0 and text_char != needle[pattern_idx]:
                pattern_idx = failure[pattern_idx - 1]

            if text_char == needle[pattern_idx]:
                pattern_idx += 1

            if pattern_idx == needle_length:
                return text_idx - needle_length + 1

        return -1


# ============================================================================
# Solution: Rabin-Karp Rolling Hash
# Time: O(m+n) average, O(mn) worst case
# Space: O(1)
#   - Use polynomial rolling hash for O(1) window comparison
#   - Verify on hash match to handle collisions
# ============================================================================
class SolutionRabinKarp:
    def strStr(self, haystack: str, needle: str) -> int:
        """
        Find first occurrence using Rabin-Karp rolling hash.

        Key insight: Instead of comparing characters, compare hash values.
        The rolling hash allows updating hash in O(1) when sliding window.

        hash(s[1:m+1]) = (hash(s[0:m]) - s[0] * BASE^(m-1)) * BASE + s[m]
        """
        if not needle:
            return 0

        needle_length = len(needle)
        haystack_length = len(haystack)

        if needle_length > haystack_length:
            return -1

        BASE = 256
        MOD = 10**9 + 7

        # Compute initial hashes
        needle_hash = 0
        window_hash = 0
        highest_power = 1

        for idx in range(needle_length):
            needle_hash = (needle_hash * BASE + ord(needle[idx])) % MOD
            window_hash = (window_hash * BASE + ord(haystack[idx])) % MOD

            if idx < needle_length - 1:
                highest_power = (highest_power * BASE) % MOD

        # Slide window and compare
        for start in range(haystack_length - needle_length + 1):
            if needle_hash == window_hash:
                # Verify character by character to handle collisions
                if haystack[start:start + needle_length] == needle:
                    return start

            # Update hash for next window
            if start < haystack_length - needle_length:
                outgoing_char = ord(haystack[start])
                incoming_char = ord(haystack[start + needle_length])

                window_hash = (window_hash - outgoing_char * highest_power) % MOD
                window_hash = (window_hash * BASE + incoming_char) % MOD
                window_hash = (window_hash + MOD) % MOD

        return -1


def solve():
    """
    Input format:
    Line 1: haystack (string)
    Line 2: needle (string)
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')

    haystack = json.loads(lines[0])
    needle = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.strStr(haystack, needle)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
