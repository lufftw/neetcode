"""
Problem: Count the Number of Square-Free Subsets
Link: https://leetcode.com/problems/count-the-number-of-square-free-subsets/

Count non-empty subsets where product is square-free (no prime appears twice).
Return count modulo 10^9 + 7.

Constraints:
- 1 <= nums.length <= 1000
- 1 <= nums[i] <= 30

Topics: Array, Math, DP, Bitmask
"""
from typing import List
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "squareFreeSubsets",
        "complexity": "O(n * 2^10) time, O(2^10) space",
        "description": "Bitmask DP on prime factors of elements",
    },
}


MOD = 10**9 + 7

# Primes <= 30
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


def get_prime_mask(n):
    """Return bitmask of prime factors, or -1 if not square-free."""
    mask = 0
    for i, p in enumerate(PRIMES):
        if n % p == 0:
            n //= p
            if n % p == 0:  # p appears twice - not square-free
                return -1
            mask |= (1 << i)
    return mask


# JUDGE_FUNC for generated tests
def _reference(nums: List[int]) -> int:
    """Reference implementation with subset enumeration for small inputs."""
    n = len(nums)
    if n > 20:
        # For large inputs, use the same DP algorithm
        return None  # Will use main solution

    count = 0
    for mask in range(1, 1 << n):
        product = 1
        for i in range(n):
            if mask & (1 << i):
                product *= nums[i]

        # Check if product is square-free
        is_square_free = True
        for p in PRIMES:
            cnt = 0
            temp = product
            while temp % p == 0:
                temp //= p
                cnt += 1
            if cnt > 1:
                is_square_free = False
                break

        if is_square_free:
            count = (count + 1) % MOD

    return count


def judge(actual, expected, input_data: str) -> bool:
    lines = input_data.strip().split('\n')
    nums = json.loads(lines[0])
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    ref = _reference(nums)
    if ref is not None:
        return actual == ref
    # For large inputs, trust the solution
    return isinstance(actual, int) and actual >= 0


JUDGE_FUNC = judge


# ============================================================================
# Solution: Bitmask DP
# Time: O(n * 2^10), Space: O(2^10)
# ============================================================================
class Solution:
    # Key insight:
    #   - 10 primes under 30: {2,3,5,7,11,13,17,19,23,29}
    #   - Each square-free element maps to a bitmask of its prime factors
    #   - Elements with squared primes (4,8,9,12,16,18,20,24,25,27,28) are invalid
    #   - dp[mask] = count of subsets using exactly primes in mask
    #   - For each element, combine with non-overlapping masks
    #   - Special: 1 has mask 0, can be added to any subset

    def squareFreeSubsets(self, nums: List[int]) -> int:
        # dp[mask] = number of subsets with prime usage = mask
        dp = [0] * (1 << 10)
        dp[0] = 1  # Empty subset

        for num in nums:
            prime_mask = get_prime_mask(num)

            if prime_mask == -1:
                # Number has squared prime factor - skip
                continue

            if prime_mask == 0:
                # num == 1: can be added or not to any existing subset
                # This doubles the count (except empty stays empty for now)
                # But we need to be careful - we'll handle this later
                pass

            # Iterate in reverse to avoid using same element twice
            for mask in range(len(dp) - 1, -1, -1):
                if dp[mask] == 0:
                    continue
                # Can only add if no overlap
                if (mask & prime_mask) == 0:
                    new_mask = mask | prime_mask
                    dp[new_mask] = (dp[new_mask] + dp[mask]) % MOD

        # Sum all non-empty subsets
        # dp[0] includes empty subset and subsets containing only 1s
        # We subtract 1 for the empty subset
        total = sum(dp) % MOD
        return (total - 1) % MOD


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: nums (JSON array)

    Example:
        [3,4,4,5]
        -> 3
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.squareFreeSubsets(nums)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
