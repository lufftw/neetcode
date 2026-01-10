"""
Problem: Longest Duplicate Substring
Link: https://leetcode.com/problems/longest-duplicate-substring/

Given a string s, consider all duplicated substrings: (contiguous) substrings
of s that occur 2 or more times. The occurrences may overlap.

Return any duplicated substring that has the longest possible length.
If s does not have a duplicated substring, return "".

Example 1:
    Input: s = "banana"
    Output: "ana"

Example 2:
    Input: s = "abcd"
    Output: ""

Constraints:
- 2 <= s.length <= 3 * 10^4
- s consists of lowercase English letters.

Topics: String, Binary Search, Rolling Hash, Suffix Array, Hash Function
"""
import json
from _runner import get_solver


# ============================================================================
# JUDGE_FUNC - Multiple valid answers possible
# ============================================================================
def judge(actual: str, expected: str, input_data: str) -> bool:
    """
    Custom validation for Longest Duplicate Substring.

    Multiple valid answers exist (any longest duplicate is acceptable).
    We verify:
    1. The returned substring appears at least twice in s
    2. The returned substring has length equal to expected length
    3. No longer duplicate substring exists (if expected is provided)
    """
    s = json.loads(input_data.strip())

    # If empty string, there should be no duplicates
    if expected == "":
        # Check that actual is also empty (no duplicate of length 1+)
        if actual == "":
            return True
        # If actual is non-empty, verify it's actually a duplicate
        count = 0
        for i in range(len(s) - len(actual) + 1):
            if s[i:i + len(actual)] == actual:
                count += 1
        return count >= 2  # Accept if it's valid but expected was wrong

    # Verify actual is a duplicate substring
    if actual == "":
        return False  # Expected non-empty but got empty

    # Count occurrences of actual in s
    count = 0
    for i in range(len(s) - len(actual) + 1):
        if s[i:i + len(actual)] == actual:
            count += 1

    if count < 2:
        return False  # Not actually a duplicate

    # Verify length matches expected length
    return len(actual) == len(expected)


JUDGE_FUNC = judge


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "longestDupSubstring",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Binary search + Rabin-Karp rolling hash",
    },
}


# ============================================================================
# Solution: Binary Search + Rabin-Karp Rolling Hash
# Time: O(n log n), Space: O(n)
#
# Key insight: Binary search on the length of the duplicate substring.
# For a given length L, use Rabin-Karp rolling hash to check if any
# substring of length L appears twice in O(n) time.
#
# Rolling hash: hash(s[i:i+L]) can be computed from hash(s[i-1:i-1+L])
# in O(1) time by removing the contribution of s[i-1] and adding s[i+L-1].
#
# If we find a duplicate of length L, search for longer (L+1 to high).
# If no duplicate of length L exists, search for shorter (low to L-1).
# ============================================================================
class Solution:
    def longestDupSubstring(self, s: str) -> str:
        """
        Find the longest duplicated substring using binary search + rolling hash.

        Binary search on length L in [1, n-1].
        For each L, use Rabin-Karp to check for duplicate substrings in O(n).
        Return the longest duplicate found.

        Args:
            s: Input string of lowercase letters

        Returns:
            Any longest duplicated substring, or "" if none exists
        """
        n = len(s)

        # Convert to integers for easier hashing
        nums = [ord(c) - ord('a') for c in s]

        # Rabin-Karp parameters
        BASE = 26
        MOD = 2**63 - 1  # Large prime to reduce collisions

        def search(length: int) -> int:
            """
            Check if any substring of given length appears twice.

            Returns:
                Starting index of duplicate if found, -1 otherwise.
            """
            if length == 0:
                return -1

            # Compute hash of first window
            h = 0
            for i in range(length):
                h = (h * BASE + nums[i]) % MOD

            # Precompute BASE^length for rolling hash
            base_pow = pow(BASE, length, MOD)

            # Store hash -> starting index
            seen = {h: 0}

            for i in range(1, n - length + 1):
                # Roll the hash: remove s[i-1], add s[i+length-1]
                h = (h * BASE - nums[i - 1] * base_pow + nums[i + length - 1]) % MOD

                if h in seen:
                    # Potential match - verify to handle hash collisions
                    prev_start = seen[h]
                    if s[prev_start:prev_start + length] == s[i:i + length]:
                        return i
                    # If collision (different strings, same hash), continue
                    # Could store multiple indices per hash, but collision is rare

                seen[h] = i

            return -1

        # Binary search on length
        lo, hi = 1, n - 1
        result = ""

        while lo <= hi:
            mid = (lo + hi) // 2
            idx = search(mid)

            if idx != -1:
                # Found duplicate of length mid, try longer
                result = s[idx:idx + mid]
                lo = mid + 1
            else:
                # No duplicate of length mid, try shorter
                hi = mid - 1

        return result


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
    result = solver.longestDupSubstring(s)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
