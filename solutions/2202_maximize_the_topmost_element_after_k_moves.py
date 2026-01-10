"""
Problem: Maximize the Topmost Element After K Moves
Link: https://leetcode.com/problems/maximize-the-topmost-element-after-k-moves/

Given a pile (stack), in one move:
- Remove the topmost element, OR
- Add back any removed element to the top

Find maximum possible topmost element after exactly k moves.

Constraints:
- 1 <= nums.length <= 10^5
- 0 <= nums[i], k <= 10^9

Topics: Array, Greedy
"""
from typing import List
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "maximumTop",
        "complexity": "O(min(n, k)) time, O(1) space",
        "description": "Case analysis with greedy selection",
    },
}


# JUDGE_FUNC for generated tests
def _reference(nums: List[int], k: int) -> int:
    """Reference implementation."""
    n = len(nums)

    # Special case: single element
    if n == 1:
        if k % 2 == 1:
            return -1  # Must remove, can't put back with odd moves
        return nums[0]  # Even moves: remove-add cycles

    if k == 0:
        return nums[0]

    result = -1

    # We can get nums[i] for i in [0, min(k-1, n-1)] to top
    # by removing first i elements, adding back nums[i], wasting remaining moves
    for i in range(min(k - 1, n)):
        result = max(result, nums[i])

    # We can get nums[k] to top by removing exactly k elements
    if k < n:
        result = max(result, nums[k])

    return result


def judge(actual, expected, input_data: str) -> bool:
    import json
    lines = input_data.strip().split('\n')
    nums = json.loads(lines[0])
    k = json.loads(lines[1])
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(nums, k)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Case Analysis with Greedy Selection
# Time: O(min(n, k)), Space: O(1)
#   - Analyze which elements can be at the top after k moves
#   - Select the maximum among reachable elements
# ============================================================================
class Solution:
    # Key observations:
    #   1. We can reach nums[i] for i < k-1 by: remove i, add back max, waste moves
    #   2. We can reach nums[k] (if k < n) by: remove exactly k elements
    #   3. Single element with odd k: impossible (must remove, can't cycle back)
    #
    # Reachable positions:
    #   - Any of nums[0:k-1] (remove some, add back, waste remaining with pairs)
    #   - nums[k] if k < n (remove exactly k elements)

    def maximumTop(self, nums: List[int], k: int) -> int:
        n = len(nums)

        # Special case: single element
        if n == 1:
            return -1 if k % 2 == 1 else nums[0]

        if k == 0:
            return nums[0]

        result = -1

        # Can access any of nums[0:k-1] by removing, adding back, wasting pairs
        for i in range(min(k - 1, n)):
            result = max(result, nums[i])

        # Can access nums[k] by removing exactly k elements
        if k < n:
            result = max(result, nums[k])

        return result


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: nums (JSON array)
        Line 2: k (integer)

    Example:
        [5,2,2,4,0,6]
        4
        -> 5
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')
    nums = json.loads(lines[0])
    k = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.maximumTop(nums, k)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
