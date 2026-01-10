"""
Problem: Contains Duplicate III
Link: https://leetcode.com/problems/contains-duplicate-iii/

Find if there exist indices i, j such that:
- i != j
- abs(i - j) <= indexDiff
- abs(nums[i] - nums[j]) <= valueDiff

Constraints:
- 2 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9
- 1 <= indexDiff <= nums.length
- 0 <= valueDiff <= 10^9

Topics: Sliding Window, Bucket Sort, Ordered Set
"""
from typing import List
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "containsNearbyAlmostDuplicate",
        "complexity": "O(n) time, O(indexDiff) space",
        "description": "Bucket sort with sliding window",
    },
}


# JUDGE_FUNC for generated tests
def _reference(nums: List[int], indexDiff: int, valueDiff: int) -> bool:
    """Reference implementation using bucket sort."""
    if valueDiff < 0:
        return False

    buckets = {}
    bucket_size = valueDiff + 1

    def get_bucket(x):
        return x // bucket_size

    for i, num in enumerate(nums):
        bucket = get_bucket(num)

        # Check same bucket
        if bucket in buckets:
            return True

        # Check adjacent buckets
        if bucket - 1 in buckets and num - buckets[bucket - 1] <= valueDiff:
            return True
        if bucket + 1 in buckets and buckets[bucket + 1] - num <= valueDiff:
            return True

        # Add current to bucket
        buckets[bucket] = num

        # Remove old element outside window
        if i >= indexDiff:
            old_bucket = get_bucket(nums[i - indexDiff])
            del buckets[old_bucket]

    return False


def judge(actual, expected, input_data: str) -> bool:
    import json
    lines = input_data.strip().split('\n')
    nums = json.loads(lines[0])
    indexDiff = json.loads(lines[1])
    valueDiff = json.loads(lines[2])
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(nums, indexDiff, valueDiff)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Bucket Sort with Sliding Window
# Time: O(n), Space: O(indexDiff)
#   - Bucket numbers by valueDiff+1
#   - Same bucket means |a - b| <= valueDiff
#   - Adjacent buckets need explicit check
# ============================================================================
class Solution:
    # Key insight: Use buckets of size (valueDiff + 1)
    # If two numbers are in same bucket, their difference <= valueDiff
    # If in adjacent buckets, check explicitly
    #
    # Maintain sliding window of last indexDiff elements

    def containsNearbyAlmostDuplicate(self, nums: List[int], indexDiff: int, valueDiff: int) -> bool:
        if valueDiff < 0:
            return False

        buckets = {}  # bucket_id -> value in bucket
        bucket_size = valueDiff + 1

        def get_bucket(x):
            # Works for negative numbers too
            return x // bucket_size

        for i, num in enumerate(nums):
            bucket = get_bucket(num)

            # Same bucket -> definitely within valueDiff
            if bucket in buckets:
                return True

            # Check adjacent buckets
            if bucket - 1 in buckets and num - buckets[bucket - 1] <= valueDiff:
                return True
            if bucket + 1 in buckets and buckets[bucket + 1] - num <= valueDiff:
                return True

            # Add current number to its bucket
            buckets[bucket] = num

            # Remove element outside the window
            if i >= indexDiff:
                old_bucket = get_bucket(nums[i - indexDiff])
                del buckets[old_bucket]

        return False


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: nums (JSON array)
        Line 2: indexDiff (integer)
        Line 3: valueDiff (integer)

    Example:
        [1,2,3,1]
        3
        0
        -> true
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')
    nums = json.loads(lines[0])
    indexDiff = json.loads(lines[1])
    valueDiff = json.loads(lines[2])

    solver = get_solver(SOLUTIONS)
    result = solver.containsNearbyAlmostDuplicate(nums, indexDiff, valueDiff)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
