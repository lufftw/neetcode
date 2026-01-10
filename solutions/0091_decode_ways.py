"""
Problem: Decode Ways
Link: https://leetcode.com/problems/decode-ways/

A message containing letters from A-Z can be encoded into numbers using the
following mapping:
    'A' -> "1"
    'B' -> "2"
    ...
    'Z' -> "26"

To decode an encoded message, all the digits must be grouped then mapped back
into letters using the reverse of the mapping above (there may be multiple ways).

Given a string s containing only digits, return the number of ways to decode it.

Example 1:
    Input: s = "12"
    Output: 2
    Explanation: "12" could be decoded as "AB" (1 2) or "L" (12).

Example 2:
    Input: s = "226"
    Output: 3
    Explanation: "226" could be decoded as "BZ" (2 26), "VF" (22 6), or "BBF" (2 2 6).

Example 3:
    Input: s = "06"
    Output: 0
    Explanation: "06" cannot be mapped to "F" because of leading zero.

Constraints:
- 1 <= s.length <= 100
- s contains only digits and may contain leading zero(s).

Topics: String, Dynamic Programming
"""
import json
from functools import lru_cache
from _runner import get_solver


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionDPConstant",
        "method": "numDecodings",
        "complexity": "O(n) time, O(1) space",
        "description": "Space-optimized DP with two variables",
    },
    "dp_constant": {
        "class": "SolutionDPConstant",
        "method": "numDecodings",
        "complexity": "O(n) time, O(1) space",
        "description": "Space-optimized DP",
    },
    "dp_array": {
        "class": "SolutionDPArray",
        "method": "numDecodings",
        "complexity": "O(n) time, O(n) space",
        "description": "DP with explicit array",
    },
    "memo": {
        "class": "SolutionMemo",
        "method": "numDecodings",
        "complexity": "O(n) time, O(n) space",
        "description": "Recursive with memoization",
    },
}


# ============================================================================
# Solution 1: DP with Constant Space
# Time: O(n), Space: O(1)
#   - Similar to Fibonacci: dp[i] depends only on dp[i-1] and dp[i-2]
#   - Single digit valid: 1-9 (not 0)
#   - Two digits valid: 10-26
# ============================================================================
class SolutionDPConstant:
    """
    Space-optimized dynamic programming.

    State: dp[i] = number of ways to decode s[0:i]
    Transition:
        - If s[i-1] != '0': dp[i] += dp[i-1] (use single digit)
        - If s[i-2:i] in "10"-"26": dp[i] += dp[i-2] (use two digits)

    Since we only need the previous two values, we use two variables.
    """

    def numDecodings(self, s: str) -> int:
        if not s or s[0] == '0':
            return 0

        n = len(s)

        # prev2 = dp[i-2], prev1 = dp[i-1]
        prev2, prev1 = 1, 1  # Base: dp[0] = 1 (empty prefix), dp[1] = 1

        for i in range(1, n):
            current = 0

            # Option 1: Decode s[i] as single digit (1-9)
            if s[i] != '0':
                current += prev1

            # Option 2: Decode s[i-1:i+1] as two digits (10-26)
            two_digit = int(s[i - 1:i + 1])
            if 10 <= two_digit <= 26:
                current += prev2

            # Slide window
            prev2, prev1 = prev1, current

        return prev1


# ============================================================================
# Solution 2: DP with Array
# Time: O(n), Space: O(n)
#   - Explicit array for clarity
#   - dp[i] = ways to decode s[0:i]
# ============================================================================
class SolutionDPArray:
    """
    Dynamic programming with explicit array.

    dp[i] represents the number of ways to decode the first i characters.
    - dp[0] = 1 (empty string has one way to decode: do nothing)
    - dp[1] = 1 if s[0] != '0', else 0

    For each position i > 1:
    - If s[i-1] is valid single digit (1-9): add dp[i-1]
    - If s[i-2:i] is valid two-digit (10-26): add dp[i-2]
    """

    def numDecodings(self, s: str) -> int:
        if not s or s[0] == '0':
            return 0

        n = len(s)
        dp = [0] * (n + 1)
        dp[0] = 1  # Base case: empty prefix
        dp[1] = 1  # First char is valid (we checked s[0] != '0')

        for i in range(2, n + 1):
            # Single digit decode: s[i-1]
            if s[i - 1] != '0':
                dp[i] += dp[i - 1]

            # Two digit decode: s[i-2:i]
            two_digit = int(s[i - 2:i])
            if 10 <= two_digit <= 26:
                dp[i] += dp[i - 2]

        return dp[n]


# ============================================================================
# Solution 3: Recursive with Memoization
# Time: O(n), Space: O(n)
#   - Top-down approach
#   - More intuitive for understanding the problem structure
# ============================================================================
class SolutionMemo:
    """
    Recursive solution with memoization (top-down DP).

    decode(i) = number of ways to decode s[i:] (suffix starting at i)
    Base case: decode(n) = 1 (successfully decoded entire string)

    At each position, we try:
    1. Take single digit if valid (1-9)
    2. Take two digits if valid (10-26)
    """

    def numDecodings(self, s: str) -> int:
        n = len(s)

        @lru_cache(maxsize=None)
        def decode(i: int) -> int:
            # Base case: reached end of string
            if i == n:
                return 1

            # Leading zero is invalid
            if s[i] == '0':
                return 0

            ways = 0

            # Option 1: Single digit (always valid since s[i] != '0')
            ways += decode(i + 1)

            # Option 2: Two digits (if in range 10-26)
            if i + 1 < n:
                two_digit = int(s[i:i + 2])
                if 10 <= two_digit <= 26:
                    ways += decode(i + 2)

            return ways

        return decode(0)


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: s as JSON string

    Example:
        "226"
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')

    s = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.numDecodings(s)

    print(result)


if __name__ == "__main__":
    solve()
