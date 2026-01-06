"""
Problem: Count of Smaller Numbers After Self
Link: https://leetcode.com/problems/count-of-smaller-numbers-after-self/

Given an integer array nums, return an integer array counts where counts[i]
is the number of smaller elements to the right of nums[i].

Example 1:
    Input: nums = [5,2,6,1]
    Output: [2,1,1,0]
    Explanation:
        To the right of 5 there are 2 smaller elements (2 and 1).
        To the right of 2 there is only 1 smaller element (1).
        To the right of 6 there is 1 smaller element (1).
        To the right of 1 there is 0 smaller element.

Example 2:
    Input: nums = [-1]
    Output: [0]

Example 3:
    Input: nums = [-1,-1]
    Output: [0,0]

Constraints:
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4

Topics: Array, Binary Search, Divide and Conquer, Binary Indexed Tree,
        Segment Tree, Merge Sort, Ordered Set
"""

import json
from typing import List

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionBIT",
        "method": "countSmaller",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Fenwick Tree with coordinate compression",
    },
    "bit": {
        "class": "SolutionBIT",
        "method": "countSmaller",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Fenwick Tree with coordinate compression",
    },
    "merge_sort": {
        "class": "SolutionMergeSort",
        "method": "countSmaller",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Merge sort with inversion counting",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result.

    Args:
        actual: Program output (list)
        expected: Expected output (None if from generator)
        input_data: Raw input string

    Returns:
        bool: True if correct
    """
    lines = input_data.strip().split("\n")
    nums = json.loads(lines[0])

    # Compute correct answer using reference solution
    correct = _reference_count_smaller(nums)

    # Parse actual output
    if isinstance(actual, list):
        actual_list = actual
    else:
        actual_str = actual.strip()
        try:
            actual_list = json.loads(actual_str) if actual_str else []
        except (ValueError, json.JSONDecodeError):
            return False

    return actual_list == correct


def _reference_count_smaller(nums: List[int]) -> List[int]:
    """Reference implementation using BIT with coordinate compression."""
    if not nums:
        return []

    # Coordinate compression
    sorted_unique = sorted(set(nums))
    rank_map = {v: i + 1 for i, v in enumerate(sorted_unique)}
    n = len(sorted_unique)

    # BIT
    tree = [0] * (n + 1)

    def lowbit(x):
        return x & (-x)

    def update(i):
        while i <= n:
            tree[i] += 1
            i += lowbit(i)

    def query(i):
        total = 0
        while i > 0:
            total += tree[i]
            i -= lowbit(i)
        return total

    result = []
    for num in reversed(nums):
        rank = rank_map[num]
        count = query(rank - 1)
        result.append(count)
        update(rank)

    return result[::-1]


JUDGE_FUNC = judge


# ============================================================================
# Solution 1: Fenwick Tree (BIT) with Coordinate Compression
# Time: O(n log n), Space: O(n)
#
# Key Insight: Process right to left. For each element, query "how many
# smaller elements have we seen?" then add current element to BIT.
# ============================================================================
class SolutionBIT:
    def countSmaller(self, nums: List[int]) -> List[int]:
        if not nums:
            return []

        # Coordinate compression: map values to ranks 1..m
        sorted_unique = sorted(set(nums))
        rank_map = {v: i + 1 for i, v in enumerate(sorted_unique)}
        m = len(sorted_unique)

        # Fenwick Tree for counting
        tree = [0] * (m + 1)

        def lowbit(x: int) -> int:
            return x & (-x)

        def update(i: int) -> None:
            """Increment count at rank i."""
            while i <= m:
                tree[i] += 1
                i += lowbit(i)

        def query(i: int) -> int:
            """Count elements with rank <= i."""
            total = 0
            while i > 0:
                total += tree[i]
                i -= lowbit(i)
            return total

        result = []
        # Process right to left
        for num in reversed(nums):
            rank = rank_map[num]
            # Count elements smaller than current (rank - 1)
            count = query(rank - 1)
            result.append(count)
            # Add current element
            update(rank)

        return result[::-1]


# ============================================================================
# Solution 2: Merge Sort with Inversion Counting
# Time: O(n log n), Space: O(n)
#
# Key Insight: During merge, when we take from the right array, all
# remaining elements in left array have "smaller after self" increased.
# ============================================================================
class SolutionMergeSort:
    def countSmaller(self, nums: List[int]) -> List[int]:
        if not nums:
            return []

        counts = [0] * len(nums)
        # Store (value, original_index) pairs
        indexed = [(num, i) for i, num in enumerate(nums)]

        def merge_sort(arr: List[tuple]) -> List[tuple]:
            if len(arr) <= 1:
                return arr

            mid = len(arr) // 2
            left = merge_sort(arr[:mid])
            right = merge_sort(arr[mid:])
            return merge(left, right)

        def merge(left: List[tuple], right: List[tuple]) -> List[tuple]:
            result = []
            i = j = 0
            right_smaller_count = 0

            while i < len(left) and j < len(right):
                if left[i][0] <= right[j][0]:
                    # Left element is smaller or equal, count how many right
                    # elements were smaller (already moved to result)
                    counts[left[i][1]] += right_smaller_count
                    result.append(left[i])
                    i += 1
                else:
                    # Right element is smaller, increment counter
                    right_smaller_count += 1
                    result.append(right[j])
                    j += 1

            # Remaining left elements
            while i < len(left):
                counts[left[i][1]] += right_smaller_count
                result.append(left[i])
                i += 1

            # Remaining right elements (no count update needed)
            result.extend(right[j:])

            return result

        merge_sort(indexed)
        return counts


def solve():
    """
    Input format (JSON per line):
        Line 1: nums array

    Output format:
        JSON array of counts
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.countSmaller(nums)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
