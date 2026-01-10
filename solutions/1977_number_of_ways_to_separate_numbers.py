"""
Problem: Number of Ways to Separate Numbers
Link: https://leetcode.com/problems/number-of-ways-to-separate-numbers/

Partition string into non-decreasing sequence of positive integers with no leading zeros.

Constraints:
- 1 <= num.length <= 3500
- num consists of digits '0' through '9'.

Topics: String, Dynamic Programming, Suffix Array
"""
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "numberOfCombinations",
        "complexity": "O(n^2) time, O(n^2) space",
        "description": "DP with LCP optimization for O(1) comparisons",
    },
}


MOD = 10**9 + 7


# JUDGE_FUNC for generated tests
def _reference(num: str) -> int:
    """Reference implementation."""
    n = len(num)
    if n == 0 or num[0] == '0':
        return 0

    # Build LCP array for O(1) string comparison
    lcp = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if num[i] == num[j]:
                lcp[i][j] = lcp[i + 1][j + 1] + 1

    def compare(i1, i2, length):
        """Compare num[i1:i1+length] <= num[i2:i2+length]."""
        common = lcp[i1][i2]
        if common >= length:
            return True
        return num[i1 + common] <= num[i2 + common]

    # dp[i][j] = ways to partition num[0:i] with last number of length j
    # i is 1-indexed (i=n means we've used all n chars)
    dp = [[0] * (n + 1) for _ in range(n + 1)]

    # Base case: first number only
    for length in range(1, n + 1):
        if num[0] != '0':
            dp[length][length] = 1

    # Fill DP: for each ending position
    for end in range(1, n + 1):
        for length in range(1, end + 1):
            start = end - length
            if start == 0:
                # First number, already handled in base case
                continue
            if num[start] == '0':
                # Leading zero
                continue

            # Try all previous lengths
            for prev_len in range(1, min(start, length) + 1):
                prev_start = start - prev_len
                if num[prev_start] == '0':
                    continue

                if prev_len < length:
                    # Shorter is always smaller
                    dp[end][length] = (dp[end][length] + dp[start][prev_len]) % MOD
                else:
                    # Same length, need to compare
                    if compare(prev_start, start, length):
                        dp[end][length] = (dp[end][length] + dp[start][prev_len]) % MOD

    return sum(dp[n]) % MOD


def judge(actual, expected, input_data: str) -> bool:
    import json
    num = json.loads(input_data.strip())
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(num)


JUDGE_FUNC = judge


# ============================================================================
# Solution: DP with LCP Optimization
# Time: O(n^2), Space: O(n^2)
#   - LCP array for O(1) substring comparison
#   - Prefix sum optimization to reduce to O(n^2)
# ============================================================================
class Solution:
    # Key insight: dp[end][len] = ways where sequence ends at position end
    # with last number having length len
    #
    # For transition from position start to end with current length len:
    #   - Previous can have length 1..len-1 (shorter always valid)
    #   - Previous can have length len if num[start-len:start] <= num[start:end]
    #
    # Optimization with prefix sums and LCP for O(n^2) total

    def numberOfCombinations(self, num: str) -> int:
        n = len(num)
        if n == 0 or num[0] == '0':
            return 0

        MOD = 10**9 + 7

        # LCP array: lcp[i][j] = longest common prefix starting at i and j
        lcp = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                if num[i] == num[j]:
                    lcp[i][j] = lcp[i + 1][j + 1] + 1

        def compare(i1, i2, length):
            """Return True if num[i1:i1+length] <= num[i2:i2+length]."""
            common = lcp[i1][i2]
            if common >= length:
                return True
            return num[i1 + common] <= num[i2 + common]

        # dp[end][length] = ways to partition num[0:end] with last number of length `length`
        dp = [[0] * (n + 1) for _ in range(n + 1)]
        # prefix[end][length] = sum of dp[end][1..length]
        prefix = [[0] * (n + 2) for _ in range(n + 1)]

        for end in range(1, n + 1):
            for length in range(1, end + 1):
                start = end - length
                if num[start] == '0':
                    continue

                if start == 0:
                    # First number in sequence
                    dp[end][length] = 1
                elif length > start:
                    # Previous must be shorter
                    dp[end][length] = prefix[start][start]
                else:
                    # Previous can be shorter or same length (if <=)
                    prev_start = start - length
                    dp[end][length] = prefix[start][length - 1]
                    if num[prev_start] != '0' and compare(prev_start, start, length):
                        dp[end][length] = (dp[end][length] + dp[start][length]) % MOD

            # Update prefix sums
            for j in range(1, end + 1):
                prefix[end][j] = (prefix[end][j - 1] + dp[end][j]) % MOD

        return prefix[n][n]


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: num (JSON string)

    Example:
        "327"
        -> 2
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')
    num = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.numberOfCombinations(num)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
