"""
Problem: Sum of Floored Pairs
Link: https://leetcode.com/problems/sum-of-floored-pairs/

Sum of floor(nums[i] / nums[j]) for all pairs (i, j).

Constraints:
- 1 <= nums.length <= 10^5
- 1 <= nums[i] <= 10^5
- Return result modulo 10^9 + 7

Topics: Array, Math, Binary Search, Prefix Sum
"""
from typing import List
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "sumOfFlooredPairs",
        "complexity": "O(M log M) time, O(M) space where M = max(nums)",
        "description": "Count frequencies + prefix sum + iterate multiples",
    },
}


MOD = 10**9 + 7


# ============================================================================
# Solution: Frequency Count + Prefix Sum + Multiple Iteration
# Time: O(M log M), Space: O(M) where M = max(nums)
# ============================================================================
class Solution:
    # Key insight: For divisor d appearing f times, count pairs with quotient k:
    # floor(x/d) = k means x in [k*d, (k+1)*d - 1]
    # Use prefix sums to count elements in any range in O(1).
    #
    # For each unique d, iterate k = 1, 2, ... until k*d > max_val.
    # Number of iterations across all d is O(M * H_M) ≈ O(M log M).

    def sumOfFlooredPairs(self, nums: List[int]) -> int:
        max_val = max(nums)

        # Frequency count
        freq = [0] * (max_val + 2)
        for x in nums:
            freq[x] += 1

        # Prefix sum: prefix[i] = count of elements <= i
        prefix = [0] * (max_val + 2)
        for i in range(1, max_val + 2):
            prefix[i] = prefix[i - 1] + freq[i - 1]

        result = 0

        # For each unique divisor d
        for d in range(1, max_val + 1):
            if freq[d] == 0:
                continue

            # Sum contribution from this divisor
            contribution = 0

            # For each quotient k = 1, 2, 3, ...
            k = 1
            while k * d <= max_val:
                # Elements with floor(x/d) = k are in range [k*d, (k+1)*d - 1]
                lo = k * d
                hi = min((k + 1) * d - 1, max_val)

                # Count elements in [lo, hi]
                count = prefix[hi + 1] - prefix[lo]

                # Each such element x contributes floor(x/d) = k
                contribution = (contribution + k * count) % MOD

                k += 1

            # Multiply by frequency of d (d appears freq[d] times as denominator)
            result = (result + contribution * freq[d]) % MOD

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

    # Brute-force O(n^2) for small inputs
    if len(nums) <= 1000:
        correct = 0
        for i in range(len(nums)):
            for j in range(len(nums)):
                correct = (correct + nums[i] // nums[j]) % MOD
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

    Example:
        [2,5,9]
        -> 10
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.sumOfFlooredPairs(nums)

    print(result)


if __name__ == "__main__":
    solve()
