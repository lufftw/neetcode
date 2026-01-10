"""
Problem: Longest Common Subpath
Link: https://leetcode.com/problems/longest-common-subpath/

Find the longest contiguous subpath shared by all friends' paths.

Constraints:
- 1 <= n <= 10^5
- 2 <= m <= 10^5
- sum(paths[i].length) <= 10^5
- 0 <= paths[i][j] < n

Topics: Array, Binary Search, Rolling Hash, Hash Function, Suffix Array
"""
from typing import List
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "longestCommonSubpath",
        "complexity": "O(T * log(min_len)) time, O(T) space",
        "description": "Binary search on length + rolling hash with double hashing",
    },
}


# JUDGE_FUNC for generated tests
def _reference(n: int, paths: List[List[int]]) -> int:
    """Reference implementation using same rolling hash approach."""
    if not paths:
        return 0

    min_len = min(len(p) for p in paths)
    if min_len == 0:
        return 0

    MOD1 = (1 << 61) - 1
    MOD2 = (1 << 31) - 1
    BASE1 = 31337
    BASE2 = 10007

    def get_hashes(path: List[int], length: int) -> set:
        """Get all rolling hashes of subpaths of given length."""
        if length > len(path):
            return set()

        hashes = set()
        h1, h2 = 0, 0
        pow1, pow2 = 1, 1

        for i in range(length):
            h1 = (h1 * BASE1 + path[i] + 1) % MOD1
            h2 = (h2 * BASE2 + path[i] + 1) % MOD2
            if i < length - 1:
                pow1 = (pow1 * BASE1) % MOD1
                pow2 = (pow2 * BASE2) % MOD2

        hashes.add((h1, h2))

        for i in range(length, len(path)):
            h1 = ((h1 - (path[i - length] + 1) * pow1) * BASE1 + path[i] + 1) % MOD1
            h2 = ((h2 - (path[i - length] + 1) * pow2) * BASE2 + path[i] + 1) % MOD2
            hashes.add((h1, h2))

        return hashes

    def check(length: int) -> bool:
        """Check if there exists a common subpath of given length."""
        if length == 0:
            return True

        common = get_hashes(paths[0], length)
        for path in paths[1:]:
            common &= get_hashes(path, length)
            if not common:
                return False
        return len(common) > 0

    lo, hi = 0, min_len
    result = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if check(mid):
            result = mid
            lo = mid + 1
        else:
            hi = mid - 1

    return result


def judge(actual, expected, input_data: str) -> bool:
    lines = input_data.strip().split('\n')
    n = json.loads(lines[0])
    paths = json.loads(lines[1])
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(n, paths)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Binary Search + Rolling Hash
# Time: O(T * log(min_len)) where T = sum of path lengths
# Space: O(T) for hash sets
# ============================================================================
class Solution:
    # Key insight: Binary search works because if length L subpath is common,
    # then all lengths < L are also common (monotonicity).
    #
    # Rolling hash: Rabin-Karp with double hashing to minimize collision risk.
    # For each candidate length, compute all L-length hashes for each path.
    # Find intersection across all paths.
    #
    # Double hash with different primes virtually eliminates false positives.

    def longestCommonSubpath(self, n: int, paths: List[List[int]]) -> int:
        if not paths:
            return 0

        min_len = min(len(p) for p in paths)
        if min_len == 0:
            return 0

        # Large primes for rolling hash to avoid collisions
        MOD1 = (1 << 61) - 1  # Mersenne prime
        MOD2 = (1 << 31) - 1
        BASE1 = 31337
        BASE2 = 10007

        def get_hashes(path: List[int], length: int) -> set:
            """Compute all rolling hashes of subpaths with given length."""
            if length > len(path):
                return set()

            hashes = set()
            h1, h2 = 0, 0
            pow1, pow2 = 1, 1  # BASE^(length-1)

            # Initial hash for first window
            for i in range(length):
                h1 = (h1 * BASE1 + path[i] + 1) % MOD1
                h2 = (h2 * BASE2 + path[i] + 1) % MOD2
                if i < length - 1:
                    pow1 = (pow1 * BASE1) % MOD1
                    pow2 = (pow2 * BASE2) % MOD2

            hashes.add((h1, h2))

            # Slide window
            for i in range(length, len(path)):
                # Remove leftmost, add rightmost
                h1 = ((h1 - (path[i - length] + 1) * pow1) * BASE1 + path[i] + 1) % MOD1
                h2 = ((h2 - (path[i - length] + 1) * pow2) * BASE2 + path[i] + 1) % MOD2
                hashes.add((h1, h2))

            return hashes

        def check(length: int) -> bool:
            """Check if common subpath of given length exists."""
            if length == 0:
                return True

            # Get hashes from first path
            common = get_hashes(paths[0], length)

            # Intersect with each subsequent path
            for path in paths[1:]:
                common &= get_hashes(path, length)
                if not common:
                    return False

            return len(common) > 0

        # Binary search on answer length
        lo, hi = 0, min_len
        result = 0

        while lo <= hi:
            mid = (lo + hi) // 2
            if check(mid):
                result = mid
                lo = mid + 1
            else:
                hi = mid - 1

        return result


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: n (integer)
        Line 2: paths (JSON 2D array)

    Example:
        5
        [[0,1,2,3,4],[2,3,4],[4,0,1,2,3]]
        -> 2
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    n = json.loads(lines[0])
    paths = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.longestCommonSubpath(n, paths)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
