# solutions/0347_top_k_frequent_elements.py
"""
Problem: Top K Frequent Elements
Link: https://leetcode.com/problems/top-k-frequent-elements/

Given an integer array nums and an integer k, return the k most frequent elements.
You may return the answer in any order.

Example 1:
    Input: nums = [1,1,1,2,2,3], k = 2
    Output: [1,2]

Example 2:
    Input: nums = [1], k = 1
    Output: [1]

Constraints:
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4
- k is in the range [1, the number of unique elements in the array].
- It is guaranteed that the answer is unique.

Follow up: Your algorithm's time complexity must be better than O(n log n).

Topics: Array, Hash Table, Divide And Conquer, Sorting, Heap Priority Queue, Bucket Sort, Counting, Quickselect
"""

import json
from collections import Counter
from typing import List
import heapq

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionHeap",
        "method": "topKFrequent",
        "complexity": "O(n + m log k) time, O(m + k) space",
        "description": "Min-heap of size k sorted by frequency",
    },
    "heap": {
        "class": "SolutionHeap",
        "method": "topKFrequent",
        "complexity": "O(n + m log k) time, O(m + k) space",
        "description": "Min-heap of size k sorted by frequency",
    },
    "bucket": {
        "class": "SolutionBucket",
        "method": "topKFrequent",
        "complexity": "O(n) time, O(n) space",
        "description": "Bucket sort by frequency",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output contains k most frequent elements.

    Args:
        actual: Program output (list as string or list)
        expected: Expected output (None if from generator)
        input_data: Raw input string (nums and k on separate lines)

    Returns:
        bool: True if correct top-k frequent elements (order doesn't matter)
    """
    lines = input_data.strip().split("\n")
    nums = json.loads(lines[0]) if lines[0] else []
    k = int(lines[1]) if len(lines) > 1 else 1

    # Compute correct answer
    correct = set(_reference_top_k(nums, k))

    # Parse actual output
    if isinstance(actual, list):
        actual_set = set(actual)
    else:
        actual_str = actual.strip()
        try:
            actual_set = set(json.loads(actual_str)) if actual_str else set()
        except (ValueError, json.JSONDecodeError):
            return False

    return actual_set == correct


def _reference_top_k(nums: List[int], k: int) -> List[int]:
    """Reference implementation using Counter."""
    freq = Counter(nums)
    return [elem for elem, _ in freq.most_common(k)]


JUDGE_FUNC = judge


# ============================================================================
# Solution 1: Min-Heap of Size K
# Time: O(n + m log k), Space: O(m + k)
#   where n = len(nums), m = unique elements
#
# Pattern: heap_top_k
# See: docs/patterns/heap/templates.md Section 2 (Top K Frequent)
# ============================================================================
class SolutionHeap:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        """
        Find k most frequent elements using min-heap.

        Two-Phase Approach:
        1. Count frequencies: O(n)
        2. Top-k selection using min-heap: O(m log k)

        Why min-heap for max-frequency problem?
        - Heap root = element with smallest frequency among top-k
        - If new element has higher frequency, it should replace root
        - After processing all elements, heap contains k most frequent
        """
        # Phase 1: Count frequencies
        frequency_map: dict[int, int] = Counter(nums)

        # Phase 2: Maintain min-heap of size k
        # Heap entries: (frequency, element)
        min_heap: list[tuple[int, int]] = []

        for element, freq in frequency_map.items():
            if len(min_heap) < k:
                heapq.heappush(min_heap, (freq, element))
            elif freq > min_heap[0][0]:
                heapq.heapreplace(min_heap, (freq, element))

        # Extract elements from heap
        return [element for freq, element in min_heap]


# ============================================================================
# Solution 2: Bucket Sort
# Time: O(n), Space: O(n)
#
# Pattern: heap_top_k (bucket variant)
# See: docs/patterns/heap/templates.md Section 2 (Top K Frequent)
# ============================================================================
class SolutionBucket:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        """
        Find k most frequent elements using bucket sort.

        Key Insight:
        - Frequency is bounded: 1 <= freq <= n
        - Use array index as frequency bucket
        - Iterate from highest frequency bucket

        Why O(n)?
        - Counting: O(n)
        - Building buckets: O(m) where m = unique elements
        - Collecting top-k: O(n) worst case (all unique frequencies)
        """
        # Count frequencies
        frequency_map: dict[int, int] = Counter(nums)

        # Create buckets: index = frequency, value = list of elements
        # Max frequency is len(nums), so we need len(nums) + 1 buckets
        buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]

        for element, freq in frequency_map.items():
            buckets[freq].append(element)

        # Collect k elements starting from highest frequency
        result: list[int] = []
        for freq in range(len(nums), 0, -1):
            for element in buckets[freq]:
                result.append(element)
                if len(result) == k:
                    return result

        return result


def solve():
    """
    Input format (JSON per line):
        Line 1: nums as JSON array
        Line 2: k as integer

    Output format:
        JSON array of k most frequent elements
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    nums = json.loads(lines[0])
    k = int(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.topKFrequent(nums, k)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
