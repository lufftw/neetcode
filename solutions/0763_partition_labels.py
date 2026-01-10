"""
Problem: Partition Labels
Link: https://leetcode.com/problems/partition-labels/

You are given a string s. We want to partition the string into as many parts as
possible so that each letter appears in at most one part.

Note that the partition is done so that after concatenating all the parts in order,
the resultant string should be s.

Return a list of integers representing the size of these parts.

Example 1:
    Input: s = "ababcbacadefegdehijhklij"
    Output: [9,7,8]
    Explanation:
    - The partition is "ababcbaca", "defegde", "hijhklij".
    - Each letter appears in at most one part.
    - A partition like "ababcbacadefegde", "hijhklij" is incorrect because it
      splits s into fewer parts.

Example 2:
    Input: s = "eccbbbbdec"
    Output: [10]

Constraints:
- 1 <= s.length <= 500
- s consists of lowercase English letters.

Topics: Hash Table, Two Pointers, String, Greedy
"""

import json
from typing import List, Dict
from _runner import get_solver


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionGreedy",
        "method": "partitionLabels",
        "complexity": "O(n) time, O(1) space (26 letters)",
        "description": "Track last occurrence of each char, extend partition greedily",
    },
    "merge_intervals": {
        "class": "SolutionMergeIntervals",
        "method": "partitionLabels",
        "complexity": "O(n) time, O(1) space",
        "description": "Convert to intervals problem, merge overlapping char ranges",
    },
}


# ============================================================================
# Solution 1: Greedy with Last Occurrence
# Time: O(n), Space: O(1) - only 26 letters
#
# Key Insight:
#   If character c appears at index i, then the partition containing c must
#   extend at least to the last occurrence of c. As we scan, we continuously
#   extend the partition boundary to include the last occurrence of each
#   character we encounter.
#
# Algorithm:
#   1. First pass: record last occurrence index of each character
#   2. Second pass: greedily form partitions
#      - Track partition end (max last occurrence seen so far)
#      - When current index reaches partition end, we've found a complete partition
#      - Record size and start new partition
#
# Why Greedy Works:
#   We must include all occurrences of each character in one partition. The
#   earliest we can end a partition is when we've seen the last occurrence of
#   every character in it. Extending to include characters' last occurrences
#   guarantees validity while achieving maximum partitions.
# ============================================================================
class SolutionGreedy:
    """
    Greedy partition using last occurrence indices.

    The key observation is that a partition can end only when we've reached
    the last occurrence of every character within it. We track the farthest
    "must include" point as we scan, and partition whenever we reach it.
    """

    def partitionLabels(self, s: str) -> List[int]:
        # First pass: find last occurrence of each character
        last_occurrence: Dict[str, int] = {}
        for i, char in enumerate(s):
            last_occurrence[char] = i

        result = []
        partition_start = 0
        partition_end = 0  # Farthest index we must include

        # Second pass: form partitions greedily
        for i, char in enumerate(s):
            # Extend partition to include last occurrence of current char
            partition_end = max(partition_end, last_occurrence[char])

            # If we've reached the partition boundary
            if i == partition_end:
                result.append(partition_end - partition_start + 1)
                partition_start = i + 1

        return result


# ============================================================================
# Solution 2: Merge Intervals Approach
# Time: O(n), Space: O(1)
#
# Key Insight:
#   We can view each character as defining an interval [first_occurrence, last_occurrence].
#   The problem becomes: merge overlapping intervals and return their lengths.
#
#   Characters whose intervals overlap must be in the same partition because
#   they share positions. Non-overlapping intervals form separate partitions.
#
# Algorithm:
#   1. For each unique character, compute its interval [first, last]
#   2. Sort intervals by start (or process in order of first occurrence)
#   3. Merge overlapping intervals
#   4. Return lengths of merged intervals
#
# This approach provides an elegant reduction to a well-known problem (merge intervals)
# and helps build intuition about why the greedy solution works.
# ============================================================================
class SolutionMergeIntervals:
    """
    Reduce to merge intervals problem.

    Each character defines an interval from its first to last occurrence.
    Overlapping intervals must be in the same partition. We merge as we scan.
    """

    def partitionLabels(self, s: str) -> List[int]:
        if not s:
            return []

        # Compute intervals for each character
        first_occurrence: Dict[str, int] = {}
        last_occurrence: Dict[str, int] = {}

        for i, char in enumerate(s):
            if char not in first_occurrence:
                first_occurrence[char] = i
            last_occurrence[char] = i

        # Merge intervals as we scan the string
        # We process characters in order, which naturally handles the merge
        result = []
        current_start = 0
        current_end = 0

        for i, char in enumerate(s):
            # First time seeing this char starts or extends the interval
            if first_occurrence[char] == i:
                # This char's interval might extend current partition
                current_end = max(current_end, last_occurrence[char])

            # When we reach the end of current merged interval
            if i == current_end:
                result.append(current_end - current_start + 1)
                current_start = i + 1
                current_end = i + 1  # Reset for next partition

        return result


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: string s (as JSON string with quotes or raw string)

    Example:
        "ababcbacadefegdehijhklij"
        OR
        ababcbacadefegdehijhklij
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")

    # Handle both JSON quoted string and raw string
    raw = lines[0]
    if raw.startswith('"') and raw.endswith('"'):
        s = json.loads(raw)
    else:
        s = raw

    solver = get_solver(SOLUTIONS)
    result = solver.partitionLabels(s)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
