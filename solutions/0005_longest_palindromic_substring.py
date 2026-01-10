"""
Problem: Longest Palindromic Substring
Link: https://leetcode.com/problems/longest-palindromic-substring/

Given a string s, return the longest palindromic substring in s.

Example 1:
    Input: s = "babad"
    Output: "bab"
    Explanation: "aba" is also a valid answer.

Example 2:
    Input: s = "cbbd"
    Output: "bb"

Constraints:
- 1 <= s.length <= 1000
- s consist of only digits and English letters.

Topics: String, Dynamic Programming
"""
import json
from _runner import get_solver


# ============================================================================
# JUDGE_FUNC - Multiple valid answers possible ("bab" or "aba" for "babad")
# ============================================================================
def _is_palindrome(s: str) -> bool:
    """Check if a string is a palindrome."""
    return s == s[::-1]


def judge(actual: str, expected: str, input_data: str) -> bool:
    """
    Custom validation for Longest Palindromic Substring.

    Multiple valid answers may exist (e.g., "bab" and "aba" for "babad").
    We verify:
    1. The returned substring is actually a palindrome
    2. The returned substring exists in the original string
    3. The length equals the expected maximum length
    """
    # Parse input string (JSON format with quotes)
    s = json.loads(input_data.strip())

    # Verify actual is a palindrome
    if not _is_palindrome(actual):
        return False

    # Verify actual is a substring of s
    if actual not in s:
        return False

    # Verify length matches expected (any max-length palindrome is valid)
    if expected is not None:
        return len(actual) == len(expected)

    # Judge-only mode: verify it's the longest by brute force
    n = len(s)
    max_len = len(actual)
    for i in range(n):
        for j in range(i + max_len + 1, n + 1):
            if _is_palindrome(s[i:j]):
                return False  # Found a longer palindrome
    return True


JUDGE_FUNC = judge


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionExpandCenter",
        "method": "longestPalindrome",
        "complexity": "O(n²) time, O(1) space",
        "description": "Expand around center - optimal for interviews",
    },
    "expand": {
        "class": "SolutionExpandCenter",
        "method": "longestPalindrome",
        "complexity": "O(n²) time, O(1) space",
        "description": "Expand around center - optimal for interviews",
    },
    "dp": {
        "class": "SolutionDP",
        "method": "longestPalindrome",
        "complexity": "O(n²) time, O(n²) space",
        "description": "Dynamic programming with 2D table",
    },
    "manacher": {
        "class": "SolutionManacher",
        "method": "longestPalindrome",
        "complexity": "O(n) time, O(n) space",
        "description": "Manacher's algorithm - optimal but complex",
    },
}


# ============================================================================
# Solution 1: Expand Around Center
# Time: O(n²), Space: O(1)
#   - Core insight: palindrome expands symmetrically from its center
#   - Two cases: odd length (single center) and even length (double center)
#   - No extra space needed beyond tracking the best result
# ============================================================================
class SolutionExpandCenter:
    """
    Expand around center approach - the recommended interview solution.

    Key insight: Every palindrome has a center. For odd-length palindromes,
    the center is a single character. For even-length, it's between two chars.
    We try each possible center and expand outward while characters match.
    """

    def longestPalindrome(self, s: str) -> str:
        if not s:
            return ""

        n = len(s)
        start, max_len = 0, 1  # Track best palindrome found

        def expand_from_center(left: int, right: int) -> int:
            """
            Expand outward from center while characters match.
            Returns the length of the palindrome found.

            For odd-length: left == right (single center)
            For even-length: right == left + 1 (gap between two chars)
            """
            while left >= 0 and right < n and s[left] == s[right]:
                left -= 1
                right += 1
            # When loop exits, left and right are one step past the palindrome
            # Length = (right - 1) - (left + 1) + 1 = right - left - 1
            return right - left - 1

        for i in range(n):
            # Case 1: Odd-length palindrome (center at i)
            len1 = expand_from_center(i, i)

            # Case 2: Even-length palindrome (center between i and i+1)
            len2 = expand_from_center(i, i + 1)

            # Update best result if we found a longer palindrome
            curr_max = max(len1, len2)
            if curr_max > max_len:
                max_len = curr_max
                # Calculate starting index of the palindrome
                # Center is at i (or between i and i+1)
                # Start = center - (length - 1) // 2
                start = i - (curr_max - 1) // 2

        return s[start:start + max_len]


# ============================================================================
# Solution 2: Dynamic Programming
# Time: O(n²), Space: O(n²)
#   - dp[i][j] = True if s[i:j+1] is a palindrome
#   - Base: single chars and two same adjacent chars
#   - Transition: dp[i][j] = (s[i] == s[j]) and dp[i+1][j-1]
# ============================================================================
class SolutionDP:
    """
    Dynamic programming approach using a 2D table.

    Classic DP formulation where dp[i][j] indicates whether s[i..j] is
    a palindrome. Build from smaller substrings to larger ones.
    """
    # State: dp[i][j] = True iff s[i:j+1] is a palindrome
    # Base case: dp[i][i] = True (single char)
    #            dp[i][i+1] = (s[i] == s[i+1]) (two adjacent chars)
    # Transition: dp[i][j] = (s[i] == s[j]) and dp[i+1][j-1]

    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        if n <= 1:
            return s

        # dp[i][j] = True if s[i:j+1] is palindrome
        dp = [[False] * n for _ in range(n)]

        start, max_len = 0, 1

        # Base case: single characters are palindromes
        for i in range(n):
            dp[i][i] = True

        # Base case: check adjacent pairs
        for i in range(n - 1):
            if s[i] == s[i + 1]:
                dp[i][i + 1] = True
                start, max_len = i, 2

        # Fill table for lengths 3 to n
        # Must iterate by length to ensure dp[i+1][j-1] is computed first
        for length in range(3, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1  # End index

                # s[i:j+1] is palindrome if ends match and middle is palindrome
                if s[i] == s[j] and dp[i + 1][j - 1]:
                    dp[i][j] = True
                    if length > max_len:
                        start, max_len = i, length

        return s[start:start + max_len]


# ============================================================================
# Solution 3: Manacher's Algorithm
# Time: O(n), Space: O(n)
#   - Transforms string to handle odd/even uniformly: "aba" -> "#a#b#a#"
#   - Exploits palindrome symmetry to skip redundant comparisons
#   - Uses previously computed results to accelerate expansion
# ============================================================================
class SolutionManacher:
    """
    Manacher's algorithm - the theoretically optimal O(n) solution.

    Key insight: When we find a long palindrome centered at C, any position
    i to the right of C has a "mirror" position i' to the left. If i' has
    a known palindrome radius, we can use it to skip some comparisons at i.

    The algorithm is complex but achieves linear time by never re-examining
    characters that are already known to match.
    """

    def longestPalindrome(self, s: str) -> str:
        if not s:
            return ""

        # Transform: "abc" -> "^#a#b#c#$"
        # ^ and $ are sentinels to avoid boundary checks
        # # between chars makes all palindromes odd-length
        t = "^#" + "#".join(s) + "#$"
        n = len(t)

        # p[i] = radius of palindrome centered at i in transformed string
        p = [0] * n

        # C = center of rightmost palindrome found so far
        # R = right edge of that palindrome (C + p[C])
        center, right = 0, 0

        for i in range(1, n - 1):
            # Mirror position of i with respect to center
            mirror = 2 * center - i

            # If i is within the current palindrome, use mirror's value
            if i < right:
                # p[i] is at least min(p[mirror], right - i)
                # Can't extend past the current right boundary yet
                p[i] = min(right - i, p[mirror])

            # Try to expand palindrome centered at i
            while t[i + p[i] + 1] == t[i - p[i] - 1]:
                p[i] += 1

            # Update center and right if this palindrome extends further
            if i + p[i] > right:
                center, right = i, i + p[i]

        # Find the maximum radius and its center
        max_radius = max(p)
        center_idx = p.index(max_radius)

        # Convert back to original string indices
        # In transformed string, position i corresponds to original (i-1)//2
        # Palindrome of radius r in transformed = length r in original
        start = (center_idx - max_radius) // 2

        return s[start:start + max_radius]


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: s (JSON string with quotes)

    Example:
        "babad"
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')

    # Parse JSON string input
    s = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.longestPalindrome(s)

    # Output as JSON string
    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
