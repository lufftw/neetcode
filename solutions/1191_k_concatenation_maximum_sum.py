"""
Problem: K-Concatenation Maximum Sum
Link: https://leetcode.com/problems/k-concatenation-maximum-sum/

Find max subarray sum in array repeated k times.
Return 0 if all negative. Return answer mod 10^9+7.

Constraints:
- 1 <= arr.length <= 10^5
- 1 <= k <= 10^5
- -10^4 <= arr[i] <= 10^4

Topics: Array, Dynamic Programming
"""
from typing import List
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "kConcatenationMaxSum",
        "complexity": "O(n) time, O(1) space",
        "description": "Kadane's algorithm with prefix/suffix optimization",
    },
}


MOD = 10**9 + 7


# JUDGE_FUNC for generated tests
def _reference(arr: List[int], k: int) -> int:
    """Reference implementation."""
    n = len(arr)
    total = sum(arr)

    def kadane(a):
        max_sum = cur_sum = 0
        for x in a:
            cur_sum = max(0, cur_sum + x)
            max_sum = max(max_sum, cur_sum)
        return max_sum

    # For k = 1, just Kadane
    if k == 1:
        return kadane(arr) % MOD

    # For k >= 2, consider crossing boundaries
    # Max suffix of arr
    max_suffix = cur = 0
    for i in range(n - 1, -1, -1):
        cur += arr[i]
        max_suffix = max(max_suffix, cur)

    # Max prefix of arr
    max_prefix = cur = 0
    for i in range(n):
        cur += arr[i]
        max_prefix = max(max_prefix, cur)

    # Case 1: Within a single copy or crossing once
    max_kadane = kadane(arr + arr)

    # Case 2: If total > 0, we can add (k-2) copies in between
    if total > 0:
        result = max(max_kadane, max_suffix + max_prefix + (k - 2) * total)
    else:
        result = max(max_kadane, max_suffix + max_prefix)

    return result % MOD


def judge(actual, expected, input_data: str) -> bool:
    import json
    lines = input_data.strip().split('\n')
    arr = json.loads(lines[0])
    k = json.loads(lines[1])
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(arr, k)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Kadane's Algorithm with Prefix/Suffix Optimization
# Time: O(n), Space: O(1)
# ============================================================================
class Solution:
    # Key insight:
    #   - For k=1: Standard Kadane
    #   - For k>=2: Max of (Kadane on 2 copies, prefix + suffix + (k-2)*total if total > 0)
    #
    # Cases:
    #   1. Subarray entirely within one copy
    #   2. Subarray crossing one boundary (suffix + prefix)
    #   3. Subarray spanning multiple copies: suffix + (k-2)*total + prefix (if total > 0)

    def kConcatenationMaxSum(self, arr: List[int], k: int) -> int:
        MOD = 10**9 + 7
        n = len(arr)
        total = sum(arr)

        def kadane(a):
            max_sum = cur_sum = 0
            for x in a:
                cur_sum = max(0, cur_sum + x)
                max_sum = max(max_sum, cur_sum)
            return max_sum

        if k == 1:
            return kadane(arr) % MOD

        # Max suffix sum
        max_suffix = cur = 0
        for i in range(n - 1, -1, -1):
            cur += arr[i]
            max_suffix = max(max_suffix, cur)

        # Max prefix sum
        max_prefix = cur = 0
        for i in range(n):
            cur += arr[i]
            max_prefix = max(max_prefix, cur)

        # Kadane on 2 copies (handles crossing one boundary)
        max_two = kadane(arr + arr)

        # If total > 0, can add (k-2) full copies in between
        if total > 0:
            result = max(max_two, max_suffix + max_prefix + (k - 2) * total)
        else:
            result = max(max_two, max_suffix + max_prefix)

        return result % MOD


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: arr (JSON array)
        Line 2: k (integer)

    Example:
        [1,2]
        3
        -> 9
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')
    arr = json.loads(lines[0])
    k = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.kConcatenationMaxSum(arr, k)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
