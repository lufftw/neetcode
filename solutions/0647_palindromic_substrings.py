# solutions/0647_palindromic_substrings.py
"""
Problem 0647 - Palindromic Substrings

Given a string s, return the number of palindromic substrings in it.
A string is a palindrome when it reads the same backward as forward.
A substring is a contiguous sequence of characters within the string.

LeetCode Constraints:
- 1 <= s.length <= 1000
- s consists of lowercase English letters

Key Insight:
Every single character is a palindrome (n trivial cases).
For longer palindromes, we can either:
1. Expand from each possible center (2n-1 centers for odd/even lengths)
2. Use DP where dp[i][j] = True if s[i:j+1] is a palindrome

The expand-from-center approach is more space-efficient and intuitive:
- Odd length palindromes: center at each character (n centers)
- Even length palindromes: center between adjacent chars (n-1 centers)

Solution Approaches:
1. Expand around center: O(n^2) time, O(1) space - most practical
2. Dynamic programming: O(n^2) time, O(n^2) space - builds full palindrome table
3. Manacher's algorithm: O(n) time, O(n) space - optimal but complex
"""
from typing import List, Optional
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionExpandCenter",
        "method": "countSubstrings",
        "complexity": "O(n^2) time, O(1) space",
        "description": "Expand around each center (2n-1 centers)",
    },
    "dp": {
        "class": "SolutionDP",
        "method": "countSubstrings",
        "complexity": "O(n^2) time, O(n^2) space",
        "description": "DP table where dp[i][j] = is s[i:j+1] palindrome",
    },
    "manacher": {
        "class": "SolutionManacher",
        "method": "countSubstrings",
        "complexity": "O(n) time, O(n) space",
        "description": "Manacher's algorithm with palindrome radius array",
    },
}


class SolutionExpandCenter:
    """
    Expand around center approach.

    A palindrome mirrors around its center. For a string of length n,
    there are 2n-1 possible centers:
    - n centers on characters (odd-length palindromes)
    - n-1 centers between characters (even-length palindromes)

    For each center, expand outward while characters match.
    Count each expansion as a new palindrome found.

    Time: O(n^2) - each center can expand up to n/2 times
    Space: O(1) - only use index variables
    """

    def countSubstrings(self, s: str) -> int:
        n = len(s)
        count = 0

        def expand_from_center(left: int, right: int) -> int:
            """Count palindromes by expanding from center."""
            palindromes = 0
            while left >= 0 and right < n and s[left] == s[right]:
                palindromes += 1
                left -= 1
                right += 1
            return palindromes

        for i in range(n):
            # Odd-length palindromes (center on character i)
            count += expand_from_center(i, i)
            # Even-length palindromes (center between i and i+1)
            count += expand_from_center(i, i + 1)

        return count


class SolutionDP:
    """
    Dynamic programming approach.

    Build a 2D table where dp[i][j] = True if s[i:j+1] is a palindrome.

    Base cases:
    - dp[i][i] = True (single characters)
    - dp[i][i+1] = (s[i] == s[i+1]) (adjacent pairs)

    Recurrence:
    - dp[i][j] = dp[i+1][j-1] and s[i] == s[j]
      (inner substring is palindrome and outer chars match)

    Must fill diagonally: process by substring length, not by indices.
    """

    def countSubstrings(self, s: str) -> int:
        n = len(s)
        dp = [[False] * n for _ in range(n)]
        count = 0

        # Base case: single characters
        for i in range(n):
            dp[i][i] = True
            count += 1

        # Base case: adjacent pairs
        for i in range(n - 1):
            if s[i] == s[i + 1]:
                dp[i][i + 1] = True
                count += 1

        # Fill for lengths 3 and above
        for length in range(3, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                if s[i] == s[j] and dp[i + 1][j - 1]:
                    dp[i][j] = True
                    count += 1

        return count


class SolutionManacher:
    """
    Manacher's algorithm for linear time palindrome counting.

    Key insight: transform string to handle odd/even uniformly by
    inserting sentinel characters. "aba" -> "#a#b#a#"

    Maintain:
    - p[i] = radius of palindrome centered at i (in transformed string)
    - center = center of rightmost palindrome found
    - right = right boundary of that palindrome

    When computing p[i]:
    - If i < right, use mirror property: p[i] >= min(p[mirror], right - i)
    - Then expand to find actual radius
    - Update center/right if i + p[i] extends further right

    Each palindrome of radius r in transformed string corresponds to
    (r+1)//2 original palindromic substrings centered at that position.
    """

    def countSubstrings(self, s: str) -> int:
        # Transform: "abc" -> "^#a#b#c#$"
        # ^ and $ are sentinels to avoid boundary checks
        t = "^#" + "#".join(s) + "#$"
        n = len(t)
        p = [0] * n  # p[i] = palindrome radius at i

        center = right = 0

        for i in range(1, n - 1):
            # Mirror position relative to center
            mirror = 2 * center - i

            if i < right:
                # Use mirror's radius, bounded by distance to right boundary
                p[i] = min(right - i, p[mirror])

            # Expand around center i
            while t[i + p[i] + 1] == t[i - p[i] - 1]:
                p[i] += 1

            # Update center and right if we've extended past right boundary
            if i + p[i] > right:
                center = i
                right = i + p[i]

        # Count palindromes: each radius r contributes (r+1)//2 palindromes
        # Because in transformed string, palindrome of radius 2 = length 1 original
        # Radius 0 at '#' = no palindrome, radius 1 at char = length 1, etc.
        return sum((r + 1) // 2 for r in p)


def solve():
    import sys
    import json

    data = sys.stdin.read().strip()

    # Handle both raw string and JSON-quoted string
    if data.startswith('"') and data.endswith('"'):
        s = json.loads(data)
    else:
        s = data

    solver = get_solver(SOLUTIONS)
    result = solver.countSubstrings(s)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
