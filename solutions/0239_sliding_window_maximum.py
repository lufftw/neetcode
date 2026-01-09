"""
Problem: Sliding Window Maximum
Link: https://leetcode.com/problems/sliding-window-maximum/

You are given an array of integers nums, there is a sliding window of size k
which is moving from the very left of the array to the very right. You can
only see the k numbers in the window. Each time the sliding window moves
right by one position. Return the max sliding window.

Example 1:
    Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
    Output: [3,3,5,5,6,7]

Example 2:
    Input: nums = [1], k = 1
    Output: [1]

Constraints:
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4
- 1 <= k <= nums.length

Topics: Array, Queue, Sliding Window, Heap (Priority Queue), Monotonic Queue
"""

import json
from collections import deque
from typing import List

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionMonotonicDeque",
        "method": "maxSlidingWindow",
        "complexity": "O(n) time, O(k) space",
        "description": "Monotonic decreasing deque storing indices",
    },
    "deque": {
        "class": "SolutionMonotonicDeque",
        "method": "maxSlidingWindow",
        "complexity": "O(n) time, O(k) space",
        "description": "Monotonic decreasing deque storing indices",
    },
    "heap": {
        "class": "SolutionHeap",
        "method": "maxSlidingWindow",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Max-heap with lazy deletion",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output is the correct max sliding window.

    Args:
        actual: Program output (list as string or list)
        expected: Expected output (None if from generator)
        input_data: Raw input string (JSON array and k)

    Returns:
        bool: True if correct max values for each window position
    """
    lines = input_data.strip().split("\n")
    nums = json.loads(lines[0]) if lines[0] else []
    k = int(lines[1])

    # Compute correct answer using reference solution
    correct = _reference_max_sliding_window(nums, k)

    # Parse actual output (may be list or string)
    if isinstance(actual, list):
        actual_list = actual
    else:
        actual_str = actual.strip()
        try:
            actual_list = json.loads(actual_str) if actual_str else []
        except (ValueError, json.JSONDecodeError):
            return False

    return actual_list == correct


def _reference_max_sliding_window(nums: List[int], k: int) -> List[int]:
    """O(n) reference using monotonic deque."""
    if not nums:
        return []

    dq: deque[int] = deque()  # Store indices
    result: List[int] = []

    for i, num in enumerate(nums):
        # Remove out-of-window elements from front
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Remove smaller elements from back (they'll never be max)
        while dq and nums[dq[-1]] < num:
            dq.pop()

        dq.append(i)

        # Window is complete (has k elements)
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result


JUDGE_FUNC = judge


# ============================================================================
# Solution 1: Monotonic Decreasing Deque
# Time: O(n), Space: O(k)
#   - Deque stores indices with values in decreasing order
#   - Front of deque is always the current window's maximum
#   - Elements enter once and exit at most once (amortized O(1) per element)
#
# Key Insight: Any element smaller than the current element that came before
# will never be the maximum while the current element is in the window.
# ============================================================================
class SolutionMonotonicDeque:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        """
        Return the maximum value in each sliding window of size k.

        Core insight: Maintain a deque of indices in decreasing order of values.
        When a new element enters, remove dominated elements from back (they'll
        never be max while current element is in window). Front is always max.

        Invariant: Deque contains indices of potential maxima in decreasing value
        order; all indices are within the current window [i-k+1, i].

        Args:
            nums: Array of integers
            k: Window size

        Returns:
            List of maximum values for each window position
        """
        if not nums:
            return []

        # Deque stores indices; values at those indices are in decreasing order
        max_candidates: deque[int] = deque()
        result: List[int] = []

        for i, num in enumerate(nums):
            # 1. Remove indices outside the current window from front
            while max_candidates and max_candidates[0] < i - k + 1:
                max_candidates.popleft()

            # 2. Remove indices of smaller elements from back
            #    (they can never be max while current element is in window)
            while max_candidates and nums[max_candidates[-1]] < num:
                max_candidates.pop()

            # 3. Add current index to deque
            max_candidates.append(i)

            # 4. Window is complete when we have at least k elements
            if i >= k - 1:
                result.append(nums[max_candidates[0]])

        return result


# ============================================================================
# Solution 2: Max-Heap with Lazy Deletion
# Time: O(n log n), Space: O(n)
#   - Use max-heap (via negation) to track maximum
#   - Lazy deletion: only remove outdated elements when they're at heap top
#   - Trade-off: simpler logic but worse time complexity
# ============================================================================
class SolutionHeap:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        """
        Heap-based approach with lazy deletion.

        Uses a max-heap (simulated via negated values) storing (-value, index).
        When extracting max, check if index is still in current window.
        If not, pop and try again (lazy deletion).

        Time: O(n log n) worst case - each element pushed/popped once
        Space: O(n) - heap can accumulate all elements before cleanup
        """
        import heapq

        if not nums or k == 0:
            return []

        # Max-heap using negated values: (-value, index)
        heap: List[tuple[int, int]] = []
        result: List[int] = []

        for i, num in enumerate(nums):
            # Push current element
            heapq.heappush(heap, (-num, i))

            # Remove elements outside current window (lazy deletion)
            while heap[0][1] < i - k + 1:
                heapq.heappop(heap)

            # Window is complete
            if i >= k - 1:
                result.append(-heap[0][0])

        return result


def solve():
    """
    Input format (JSON):
        Line 1: nums as JSON array
        Line 2: k as integer

    Output format:
        JSON array of max values for each window position
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    nums = json.loads(lines[0])
    k = int(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.maxSlidingWindow(nums, k)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
