"""
Problem: Create Maximum Number
Link: https://leetcode.com/problems/create-maximum-number/

You are given two integer arrays nums1 and nums2 of lengths m and n respectively. nums1 and nums2 represent the digits of two numbers. You are also given an integer k.

Create the maximum number of length k <= m + n from digits of the two numbers. The relative order of the digits from the same array must be preserved.

Return an array of the k digits representing the answer.

Example 1:

    Input: nums1 = [3,4,6,5], nums2 = [9,1,2,5,8,3], k = 5
    Output: [9,8,6,5,3]

Example 2:

    Input: nums1 = [6,7], nums2 = [6,0,4], k = 5
    Output: [6,7,6,0,4]

Example 3:

    Input: nums1 = [3,9], nums2 = [8,9], k = 3
    Output: [9,8,9]


Constraints:

- m == nums1.length

- n == nums2.length

- 1 <= m, n <= 500

- 0 <= nums1[i], nums2[i] <= 9

- 1 <= k <= m + n

Topics: Stack, Greedy, Monotonic Stack
"""


from typing import List
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionGreedyMerge",
        "method": "maxNumber",
        "complexity": "O(k^2 * (m + n)) time, O(k) space",
        "description": "Enumerate splits + greedy max subsequence + greedy merge",
    },
}


# ============================================================================
# Solution: Greedy Split + Max Subsequence + Greedy Merge
# Time: O(k^2 * (m + n)), Space: O(k)
#   - Enumerate all ways to split k digits: i from nums1, k-i from nums2
#   - For each split, extract max subsequence of length i and k-i respectively
#   - Merge two subsequences greedily to form the largest possible number
#   - Track the overall maximum across all splits
#
# Three Sub-problems:
#   1. max_subsequence(arr, length): Extract max subsequence of given length
#      using monotonic decreasing stack (greedy)
#   2. merge(seq1, seq2): Merge two sequences to maximize result (greedy)
#   3. Main: Try all valid splits and find best result
#
# Key Insight: The problem decomposes into independent max-subsequence
# extractions from each array, followed by an optimal merge. The greedy
# merge compares remaining suffixes lexicographically to decide which
# digit to take next.
# ============================================================================
class SolutionGreedyMerge:
    def maxNumber(self, nums1: List[int], nums2: List[int], k: int) -> List[int]:
        len1, len2 = len(nums1), len(nums2)
        max_result: list[int] = []

        # Enumerate all valid splits: i digits from nums1, k-i from nums2
        min_from_nums1 = max(0, k - len2)
        max_from_nums1 = min(k, len1)

        for num_from_first in range(min_from_nums1, max_from_nums1 + 1):
            num_from_second = k - num_from_first

            # Extract maximum subsequences from each array
            subseq1 = self._max_subsequence(nums1, num_from_first)
            subseq2 = self._max_subsequence(nums2, num_from_second)

            # Merge to form the largest possible number
            merged = self._greedy_merge(subseq1, subseq2)

            # Update maximum result
            if merged > max_result:
                max_result = merged

        return max_result

    def _max_subsequence(self, nums: List[int], length: int) -> List[int]:
        """
        Extract maximum subsequence of given length using monotonic stack.
        This is essentially "keep k largest digits in order" problem.

        Algorithm:
        - Use monotonic decreasing stack
        - Remove digits when: smaller digit seen AND we have enough remaining
        - to_remove = len(nums) - length = number of digits we can discard
        """
        if length == 0:
            return []

        to_remove = len(nums) - length
        digit_stack: list[int] = []

        for digit in nums:
            # Pop smaller digits if we can still remove more
            while to_remove > 0 and digit_stack and digit_stack[-1] < digit:
                digit_stack.pop()
                to_remove -= 1
            digit_stack.append(digit)

        # Return only the first 'length' elements
        return digit_stack[:length]

    def _greedy_merge(self, seq1: List[int], seq2: List[int]) -> List[int]:
        """
        Merge two sequences to form the lexicographically largest result.

        Greedy Strategy: At each step, compare remaining subsequences.
        Take from whichever is lexicographically larger.
        """
        merged: list[int] = []
        i, j = 0, 0
        len1, len2 = len(seq1), len(seq2)

        while i < len1 or j < len2:
            if i >= len1:
                merged.append(seq2[j])
                j += 1
            elif j >= len2:
                merged.append(seq1[i])
                i += 1
            elif self._compare_suffix(seq1, i, seq2, j) >= 0:
                # seq1[i:] >= seq2[j:], take from seq1
                merged.append(seq1[i])
                i += 1
            else:
                # seq2[j:] > seq1[i:], take from seq2
                merged.append(seq2[j])
                j += 1

        return merged

    def _compare_suffix(
        self, seq1: List[int], i: int, seq2: List[int], j: int
    ) -> int:
        """
        Compare seq1[i:] with seq2[j:] lexicographically.
        Returns: positive if seq1 > seq2, negative if seq1 < seq2, 0 if equal
        """
        len1, len2 = len(seq1), len(seq2)

        while i < len1 and j < len2:
            if seq1[i] != seq2[j]:
                return seq1[i] - seq2[j]
            i += 1
            j += 1

        # One or both exhausted; longer remaining suffix wins
        return (len1 - i) - (len2 - j)


def solve():
    """
    Input format (JSON literal, one per line):
        nums1: List[int]
        nums2: List[int]
        k: int

    Output: List[int]
    """
    import sys
    import json

    data = sys.stdin.read().strip().split('\n')

    nums1 = json.loads(data[0].strip())
    nums2 = json.loads(data[1].strip())
    k = int(data[2].strip())

    solver = get_solver(SOLUTIONS)
    result = solver.maxNumber(nums1, nums2, k)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
