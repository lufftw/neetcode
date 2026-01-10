"""
Problem: Decode Ways II
Link: https://leetcode.com/problems/decode-ways-ii/

A message containing letters from A-Z is being encoded to numbers using the
following mapping: 'A' -> 1, 'B' -> 2, ..., 'Z' -> 26.

Now the encoded string can also contain the character '*', which can be treated
as one of the numbers from 1 to 9 (0 is excluded).

Given a string s consisting of digits and '*' characters, return the number of
ways to decode it. Since the answer may be very large, return it modulo 10^9 + 7.

Example 1:
    Input: s = "*"
    Output: 9
    Explanation: '*' can be 1-9, each mapping to A-I.

Example 2:
    Input: s = "1*"
    Output: 18
    Explanation: 9 choices for '*' (1-9), each has 2 decodings (single + pair).

Example 3:
    Input: s = "2*"
    Output: 15
    Explanation: "21"-"26" have 2 ways each, "27"-"29" have 1 way each.
                 6*2 + 3*1 = 15

Constraints:
- 1 <= s.length <= 10^5
- s[i] is a digit or '*'.

Topics: String, Dynamic Programming
"""
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "numDecodings",
        "complexity": "O(n) time, O(1) space",
        "description": "DP with case analysis for wildcards",
    },
}


# ============================================================================
# Solution: Dynamic Programming with Case Analysis
# Time: O(n), Space: O(1)
#
# Key insight: At each position i, the number of ways to decode s[0:i+1] depends
# on whether we decode s[i] alone or combine s[i-1:i+1] as a pair.
#
# The '*' wildcard adds complexity - we must count how many valid mappings
# exist for single chars and pairs involving wildcards.
#
# dp[i] = ways to decode s[0:i]
# dp[i] = (ways to decode s[i-1] alone) * dp[i-1]
#       + (ways to decode s[i-2:i] as pair) * dp[i-2]
# ============================================================================
class Solution:
    def numDecodings(self, s: str) -> int:
        """
        Count decoding ways for string with wildcards.

        Uses space-optimized DP tracking dp[i-1] and dp[i-2].
        For each position, count:
        1. Single-char decodings: how many values can s[i] represent (1-9)?
        2. Two-char decodings: how many valid pairs can s[i-1:i+1] form (10-26)?

        Args:
            s: Encoded string with digits and '*' wildcards

        Returns:
            Number of ways to decode, modulo 10^9 + 7
        """
        MOD = 10**9 + 7
        n = len(s)

        if n == 0:
            return 0

        def single_ways(c: str) -> int:
            """Count valid single-char decodings for character c."""
            if c == '*':
                return 9  # 1-9
            elif c == '0':
                return 0  # 0 cannot stand alone
            else:
                return 1  # 1-9

        def pair_ways(c1: str, c2: str) -> int:
            """Count valid two-char decodings for pair c1+c2 (10-26 only)."""
            if c1 == '*' and c2 == '*':
                # ** can be 11-19 (9) + 21-26 (6) = 15
                return 15
            elif c1 == '*':
                # *d where d is digit
                if c2 == '0':
                    return 2  # 10, 20
                elif '1' <= c2 <= '6':
                    return 2  # 1d, 2d both valid
                else:
                    return 1  # only 1d valid (17-19)
            elif c2 == '*':
                # d* where d is digit
                if c1 == '1':
                    return 9  # 11-19
                elif c1 == '2':
                    return 6  # 21-26
                else:
                    return 0  # 0*, 3*-9* have no valid pairs
            else:
                # Both are digits
                val = int(c1) * 10 + int(c2)
                return 1 if 10 <= val <= 26 else 0

        # dp[i] = ways to decode s[0:i]
        # Use two variables for space optimization
        prev2 = 1  # dp[i-2], initially dp[-1] = 1 (empty prefix)
        prev1 = single_ways(s[0])  # dp[0]

        for i in range(1, n):
            curr = 0

            # Single char decoding: s[i] alone
            curr = (curr + single_ways(s[i]) * prev1) % MOD

            # Pair decoding: s[i-1:i+1] together
            curr = (curr + pair_ways(s[i - 1], s[i]) * prev2) % MOD

            prev2, prev1 = prev1, curr

        return prev1


def solve():
    """
    Input format:
    Line 1: s (JSON string)
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')

    s = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.numDecodings(s)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
