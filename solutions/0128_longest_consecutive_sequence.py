# solutions/0128_longest_consecutive_sequence.py
"""
Problem: Longest Consecutive Sequence
https://leetcode.com/problems/longest-consecutive-sequence/

Given an unsorted array of integers nums, return the length of the
longest consecutive elements sequence.

You must write an algorithm that runs in O(n) time.

Constraints:
- 0 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9
"""
from typing import List
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionHashSet",
        "method": "longestConsecutive",
        "complexity": "O(n) time, O(n) space",
        "description": "HashSet with sequence start detection",
    },
    "union_find": {
        "class": "SolutionUnionFind",
        "method": "longestConsecutive",
        "complexity": "O(n) time, O(n) space",
        "description": "Union-Find to merge consecutive elements",
    },
}


class SolutionHashSet:
    """
    HashSet approach with intelligent sequence start detection.

    Key insight: only start counting from sequence beginnings. A number
    is a sequence start if (num - 1) is not in the set. This ensures
    each number is visited at most twice (once for set check, once
    during counting), giving O(n) total time.

    The naive approach of counting from every number would be O(n^2)
    in worst case. The sequence-start optimization is crucial.
    """

    def longestConsecutive(self, nums: List[int]) -> int:
        if not nums:
            return 0

        # Build set for O(1) lookups
        num_set = set(nums)
        max_length = 0

        for num in num_set:
            # Only start counting if this is a sequence start
            # (no predecessor exists)
            if num - 1 not in num_set:
                current = num
                length = 1

                # Count consecutive numbers
                while current + 1 in num_set:
                    current += 1
                    length += 1

                max_length = max(max_length, length)

        return max_length


class SolutionUnionFind:
    """
    Union-Find approach grouping consecutive elements.

    We create a union-find structure and merge each number with its
    consecutive neighbors (num-1 and num+1) if they exist. After all
    merges, the largest component gives the longest sequence.

    This approach is conceptually interesting but slightly more complex
    than the hash set approach. Both achieve O(n) time with path
    compression and union by rank.
    """

    def longestConsecutive(self, nums: List[int]) -> int:
        if not nums:
            return 0

        # Map number to its parent in union-find
        parent = {}
        size = {}  # Size of each component

        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])  # Path compression
            return parent[x]

        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                # Union by size
                if size[px] < size[py]:
                    px, py = py, px
                parent[py] = px
                size[px] += size[py]

        # Initialize each number as its own component
        for num in nums:
            if num not in parent:
                parent[num] = num
                size[num] = 1

        # Merge with consecutive neighbors
        for num in nums:
            if num - 1 in parent:
                union(num, num - 1)
            if num + 1 in parent:
                union(num, num + 1)

        # Find maximum component size
        return max(size[find(num)] for num in parent)


def judge(actual, expected, input_data: str) -> bool:
    """
    Validate longest consecutive sequence using hash set approach.
    """
    import json

    nums = json.loads(input_data.strip())

    if not nums:
        return actual == 0

    num_set = set(nums)
    expected_result = 0

    for num in num_set:
        if num - 1 not in num_set:
            current = num
            length = 1
            while current + 1 in num_set:
                current += 1
                length += 1
            expected_result = max(expected_result, length)

    return actual == expected_result


JUDGE_FUNC = judge


def solve():
    import sys
    import json

    lines = sys.stdin.read().strip().split("\n")

    # Parse input: array
    nums = json.loads(lines[0])

    # Get solver and find longest consecutive sequence
    solver = get_solver(SOLUTIONS)
    result = solver.longestConsecutive(nums)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
