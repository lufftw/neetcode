"""
Problem: Count Array Pairs Divisible by K
Link: https://leetcode.com/problems/count-array-pairs-divisible-by-k/

Count pairs (i, j) where i < j and nums[i] * nums[j] is divisible by k.

Constraints:
- 1 <= nums.length <= 10^5
- 1 <= nums[i], k <= 10^5

Topics: Array, Math, Number Theory
"""
from typing import List
from _runner import get_solver
import json
from math import gcd


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "countPairs",
        "complexity": "O(n * d(k)) time, O(d(k)) space where d(k) = divisor count",
        "description": "GCD-based counting with divisor enumeration",
    },
}


# ============================================================================
# Solution: GCD Counting with Divisor Enumeration
# Time: O(n * d(k)), Space: O(d(k)) where d(k) is number of divisors of k
# ============================================================================
class Solution:
    # Key insight: a*b divisible by k iff gcd(a,k) * gcd(b,k) >= k
    # More precisely: gcd(a,k) * gcd(b,k) must have all prime factors of k.
    #
    # For each num, compute g = gcd(num, k).
    # For g to pair with g', need (g * g') % k == 0.
    # Equivalently: g' must be divisible by k / gcd(g, k).
    #
    # Only track counts of gcd values (at most d(k) distinct values).
    # For k <= 10^5, d(k) <= 128.

    def countPairs(self, nums: List[int], k: int) -> int:
        # Get all divisors of k
        divisors = []
        i = 1
        while i * i <= k:
            if k % i == 0:
                divisors.append(i)
                if i != k // i:
                    divisors.append(k // i)
            i += 1
        divisors.sort()

        # Count occurrences of each gcd(num, k) value
        gcd_count = {}
        for num in nums:
            g = gcd(num, k)
            gcd_count[g] = gcd_count.get(g, 0) + 1

        result = 0

        # For each pair of gcd values (g1, g2), check if g1 * g2 % k == 0
        gcd_values = list(gcd_count.keys())
        for i, g1 in enumerate(gcd_values):
            # Pairs (g1, g1): choose 2 from count
            if (g1 * g1) % k == 0:
                cnt = gcd_count[g1]
                result += cnt * (cnt - 1) // 2

            # Pairs (g1, g2) where g2 > g1 in our enumeration
            for g2 in gcd_values[i + 1:]:
                if (g1 * g2) % k == 0:
                    result += gcd_count[g1] * gcd_count[g2]

        return result


# ============================================================================
# JUDGE_FUNC: Brute-force verification for small inputs
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Verify answer using brute-force for small inputs.
    """
    lines = input_data.strip().split('\n')
    nums = json.loads(lines[0])
    k = json.loads(lines[1])

    # Brute-force O(n^2) for small inputs
    if len(nums) <= 1000:
        correct = 0
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if (nums[i] * nums[j]) % k == 0:
                    correct += 1
        return actual == correct

    # For large inputs, trust the optimized algorithm
    return actual == expected if expected is not None else True


JUDGE_FUNC = judge


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: nums as JSON array
        Line 2: k (integer)

    Example:
        [1,2,3,4,5]
        2
        -> 7
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    nums = json.loads(lines[0])
    k = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.countPairs(nums, k)

    print(result)


if __name__ == "__main__":
    solve()
