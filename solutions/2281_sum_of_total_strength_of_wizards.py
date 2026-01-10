"""
Problem: Sum of Total Strength of Wizards
Link: https://leetcode.com/problems/sum-of-total-strength-of-wizards/

For each subarray, compute min(subarray) * sum(subarray). Return sum of all.

Constraints:
- 1 <= strength.length <= 10^5
- 1 <= strength[i] <= 10^9

Topics: Array, Stack, Monotonic Stack, Prefix Sum
"""
from typing import List
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "totalStrength",
        "complexity": "O(n) time, O(n) space",
        "description": "Monotonic stack + prefix of prefix sums",
    },
}


# JUDGE_FUNC for generated tests
def _reference(strength: List[int]) -> int:
    """Brute force reference for small inputs."""
    MOD = 10**9 + 7
    n = len(strength)
    result = 0
    for i in range(n):
        for j in range(i, n):
            sub = strength[i:j+1]
            result = (result + min(sub) * sum(sub)) % MOD
    return result


def judge(actual, expected, input_data: str) -> bool:
    strength = json.loads(input_data.strip())
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(strength)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Monotonic Stack + Prefix of Prefix Sums
# Time: O(n), Space: O(n)
# ============================================================================
class Solution:
    # Key insight:
    #   - For each element, find the range where it's the minimum
    #   - Use monotonic stack to find left/right boundaries
    #   - For subarrays [L, R] with element i as min:
    #     sum of sums = left_count * Σ prefix[R+1] - right_count * Σ prefix[L]
    #   - Use prefix of prefix sums for efficient range sum computation
    #
    # Boundary definition:
    #   - left[i]: first SMALLER element to left (use >= when popping)
    #   - right[i]: first SMALLER OR EQUAL element to right (use > when popping)
    #   This ensures each subarray is counted exactly once.

    def totalStrength(self, strength: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(strength)

        # Monotonic stack for left boundaries (first smaller)
        left = [-1] * n
        stack = []
        for i in range(n):
            while stack and strength[stack[-1]] >= strength[i]:
                stack.pop()
            left[i] = stack[-1] if stack else -1
            stack.append(i)

        # Monotonic stack for right boundaries (first smaller or equal)
        right = [n] * n
        stack = []
        for i in range(n - 1, -1, -1):
            while stack and strength[stack[-1]] > strength[i]:
                stack.pop()
            right[i] = stack[-1] if stack else n
            stack.append(i)

        # prefix[i] = sum(strength[0:i])
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = (prefix[i] + strength[i]) % MOD

        # pp[i] = sum(prefix[0:i]) = prefix of prefix sums
        pp = [0] * (n + 2)
        for i in range(n + 1):
            pp[i + 1] = (pp[i] + prefix[i]) % MOD

        result = 0
        for i in range(n):
            l, r = left[i], right[i]
            left_count = i - l
            right_count = r - i

            # Σ prefix[R+1] for R in [i, r-1]
            right_sum = (pp[r + 1] - pp[i + 1]) % MOD
            # Σ prefix[L] for L in (l, i]
            left_sum = (pp[i + 1] - pp[l + 1]) % MOD

            contribution = (left_count * right_sum - right_count * left_sum) % MOD
            result = (result + strength[i] * contribution) % MOD

        return result


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: strength (JSON array)

    Example:
        [1,3,1,2]
        -> 44
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    strength = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.totalStrength(strength)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
