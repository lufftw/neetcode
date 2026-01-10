"""
Problem: Find Substring With Given Hash Value
Link: https://leetcode.com/problems/find-substring-with-given-hash-value/

Find first substring of length k with given hash value.
hash(s) = sum(val(s[i]) * power^i) mod modulo, where val('a')=1..val('z')=26.

Constraints:
- 1 <= k <= s.length <= 2 * 10^4
- 1 <= power, modulo <= 10^9
- 0 <= hashValue < modulo

Topics: String, Sliding Window, Rolling Hash
"""
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "subStrHash",
        "complexity": "O(n) time, O(1) space",
        "description": "Reverse rolling hash to avoid modular inverse",
    },
}


# JUDGE_FUNC for generated tests
def _val(c):
    return ord(c) - ord('a') + 1


def _compute_hash(s, power, modulo):
    """Compute hash for verification."""
    h = 0
    p = 1
    for c in s:
        h = (h + _val(c) * p) % modulo
        p = (p * power) % modulo
    return h


def judge(actual, expected, input_data: str) -> bool:
    lines = input_data.strip().split('\n')
    s = json.loads(lines[0])
    power = json.loads(lines[1])
    modulo = json.loads(lines[2])
    k = json.loads(lines[3])
    hashValue = json.loads(lines[4])

    if isinstance(actual, str) and actual.startswith('"'):
        actual = json.loads(actual)

    # Verify actual is a valid substring with correct hash
    if len(actual) != k:
        return False
    if _compute_hash(actual, power, modulo) != hashValue:
        return False
    if actual not in s:
        return False

    # If expected is provided, check it matches (first occurrence)
    if expected is not None:
        if isinstance(expected, str) and expected.startswith('"'):
            expected = json.loads(expected)
        return actual == expected

    # Find first valid substring
    for i in range(len(s) - k + 1):
        sub = s[i:i+k]
        if _compute_hash(sub, power, modulo) == hashValue:
            return actual == sub

    return False


JUDGE_FUNC = judge


# ============================================================================
# Solution: Reverse Rolling Hash
# Time: O(n), Space: O(1)
# ============================================================================
class Solution:
    # Key insight:
    #   hash(s[i:i+k]) = s[i]*p^0 + s[i+1]*p^1 + ... + s[i+k-1]*p^(k-1)
    #
    # Rolling hash from RIGHT to LEFT avoids modular inverse:
    #   hash(i-1) = hash(i) * p + val(s[i-1]) - val(s[i+k-1]) * p^k
    #
    # Start at rightmost window, roll left, track the first match.
    # Since we go right-to-left, keep updating answer; final answer is first.

    def subStrHash(self, s: str, power: int, modulo: int, k: int, hashValue: int) -> str:
        n = len(s)

        def val(c):
            return ord(c) - ord('a') + 1

        # Precompute power^k mod modulo
        pk = pow(power, k, modulo)

        # Compute hash of last window s[n-k:n]
        h = 0
        p = 1
        for i in range(n - k, n):
            h = (h + val(s[i]) * p) % modulo
            p = (p * power) % modulo

        # Track result (last match found = first in original order)
        result_start = -1
        if h == hashValue:
            result_start = n - k

        # Roll from right to left
        for i in range(n - k - 1, -1, -1):
            # Rolling: hash(i) = hash(i+1)*p + val(s[i]) - val(s[i+k])*p^k
            h = (h * power + val(s[i]) - val(s[i + k]) * pk) % modulo
            if h == hashValue:
                result_start = i

        return s[result_start:result_start + k]


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: s (JSON string)
        Line 2: power (integer)
        Line 3: modulo (integer)
        Line 4: k (integer)
        Line 5: hashValue (integer)

    Example:
        "leetcode"
        7
        20
        2
        0
        -> "ee"
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    s = json.loads(lines[0])
    power = json.loads(lines[1])
    modulo = json.loads(lines[2])
    k = json.loads(lines[3])
    hashValue = json.loads(lines[4])

    solver = get_solver(SOLUTIONS)
    result = solver.subStrHash(s, power, modulo, k, hashValue)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
