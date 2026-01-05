"""
Problem: Subarray Sum Equals K
Link: https://leetcode.com/problems/subarray-sum-equals-k/

Given an array of integers nums and an integer k, return the total number of
subarrays whose sum equals to k.

A subarray is a contiguous non-empty sequence of elements within an array.

Example 1:
    Input: nums = [1,1,1], k = 2
    Output: 2
    Explanation: Subarrays [1,1] at indices (0,1) and (1,2) sum to 2.

Example 2:
    Input: nums = [1,2,3], k = 3
    Output: 2
    Explanation: Subarrays [1,2] and [3] sum to 3.

Constraints:
- 1 <= nums.length <= 2 * 10^4
- -1000 <= nums[i] <= 1000
- -10^7 <= k <= 10^7

Topics: Array, Hash Table, Prefix Sum
"""

import json
from typing import List

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionPrefixSum",
        "method": "subarraySum",
        "complexity": "O(n) time, O(n) space",
        "description": "Prefix sum with hash map counting complement occurrences",
    },
    "prefix": {
        "class": "SolutionPrefixSum",
        "method": "subarraySum",
        "complexity": "O(n) time, O(n) space",
        "description": "Prefix sum with hash map counting complement occurrences",
    },
    "brute": {
        "class": "SolutionBruteForce",
        "method": "subarraySum",
        "complexity": "O(n^2) time, O(1) space",
        "description": "Check all subarrays with cumulative sum",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate result: count of subarrays with sum k."""
    lines = input_data.strip().split("\n")
    nums = json.loads(lines[0])
    k = int(lines[1])

    correct = _reference_subarray_sum(nums, k)

    if isinstance(actual, int):
        return actual == correct

    try:
        actual_val = int(str(actual).strip())
        return actual_val == correct
    except (ValueError, TypeError):
        return False


def _reference_subarray_sum(nums: List[int], k: int) -> int:
    """O(n) reference using prefix sum + hash map."""
    count = 0
    prefix_sum = 0
    sum_frequency = {0: 1}

    for num in nums:
        prefix_sum += num
        count += sum_frequency.get(prefix_sum - k, 0)
        sum_frequency[prefix_sum] = sum_frequency.get(prefix_sum, 0) + 1

    return count


JUDGE_FUNC = judge


# ============================================================================
# Solution 1: Prefix Sum + Hash Map
# Time: O(n), Space: O(n)
#
# Core Insight:
#   If prefix[j] - prefix[i] = k, then subarray nums[i+1..j] sums to k.
#   Instead of checking all pairs (O(n²)), we count how many times
#   (prefix_sum - k) has appeared before the current position.
#
# Why This Works:
#   For each position j, we want to count positions i where:
#       prefix[j] - prefix[i] = k
#   Rearranging: prefix[i] = prefix[j] - k
#   So we count occurrences of (prefix_sum - k) in our frequency map.
#
# Why Sliding Window Fails:
#   Sliding window requires monotonicity (adding elements increases/decreases
#   the window property predictably). With negative numbers, adding an element
#   might increase or decrease the sum, breaking the monotonicity assumption.
#   Prefix sum + hash map handles arbitrary integers correctly.
#
# Initialization {0: 1}:
#   Handles subarrays starting from index 0. If prefix_sum == k at position j,
#   we need to count the "empty prefix" at position -1 (sum = 0).
#   Without this, we'd miss subarrays like nums[0..j] that sum to exactly k.
#
# Pattern: prefix_sum_subarray_count
# See: docs/patterns/prefix_sum/templates.md Section 2 (Subarray Sum Equals K)
# ============================================================================
class SolutionPrefixSum:
    def subarraySum(self, nums: List[int], k: int) -> int:
        """
        Count subarrays with sum equal to k using prefix sum technique.

        The key insight is that sum(nums[i+1..j]) = prefix[j] - prefix[i].
        We use a hash map to count prefix sum occurrences, enabling O(1) lookup
        of how many valid subarray starts exist for each ending position.
        """
        subarray_count = 0
        prefix_sum = 0

        # Map: prefix_sum value -> number of times it has occurred
        # Initialize with {0: 1} to handle subarrays starting at index 0
        sum_frequency: dict[int, int] = {0: 1}

        for num in nums:
            # Extend prefix sum to include current element
            prefix_sum += num

            # Count subarrays ending here with sum k:
            # If (prefix_sum - k) appeared before at positions i1, i2, ...,
            # then subarrays (i1, current], (i2, current], ... all sum to k
            complement = prefix_sum - k
            subarray_count += sum_frequency.get(complement, 0)

            # Record this prefix sum for future positions
            sum_frequency[prefix_sum] = sum_frequency.get(prefix_sum, 0) + 1

        return subarray_count


# ============================================================================
# Solution 2: Brute Force with Cumulative Sum
# Time: O(n²), Space: O(1)
#
# Educational Value:
#   Demonstrates why O(n²) is necessary without the hash map optimization.
#   For each starting position, we accumulate the sum and check against k.
#   This is the "natural" approach that the hash map solution improves upon.
#
# When to Use:
#   - Small arrays (n < 100) where simplicity matters more than speed
#   - When debugging to verify the optimized solution's correctness
# ============================================================================
class SolutionBruteForce:
    def subarraySum(self, nums: List[int], k: int) -> int:
        """
        Count subarrays with sum k using brute force enumeration.

        For each starting index, compute cumulative sums to all ending indices.
        Simple but O(n²) - use prefix sum + hash map for large inputs.
        """
        subarray_count = 0
        array_length = len(nums)

        for start_index in range(array_length):
            cumulative_sum = 0

            for end_index in range(start_index, array_length):
                cumulative_sum += nums[end_index]

                if cumulative_sum == k:
                    subarray_count += 1

        return subarray_count


def solve():
    """
    Input format (JSON per line):
        Line 1: nums as JSON array
        Line 2: k as integer

    Output format:
        Integer count of subarrays with sum k
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    nums = json.loads(lines[0])
    k = int(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.subarraySum(nums, k)

    print(result)


if __name__ == "__main__":
    solve()
