"""
Problem: Assign Cookies
Link: https://leetcode.com/problems/assign-cookies/

Assume you are an awesome parent and want to give your children some cookies.
But, you should give each child at most one cookie.

Each child i has a greed factor g[i], which is the minimum size of a cookie
that the child will be content with; and each cookie j has a size s[j]. If
s[j] >= g[i], we can assign the cookie j to the child i, and the child i will
be content. Your goal is to maximize the number of your content children and
output the maximum number.

Example 1:
    Input: g = [1,2,3], s = [1,1]
    Output: 1
    Explanation: You have 3 children and 2 cookies. The greed factors of 3 children
                 are 1, 2, 3.
                 And even though you have 2 cookies, since their size is both 1, you
                 could only make the child whose greed factor is 1 content.
                 You need to output 1.

Example 2:
    Input: g = [1,2], s = [1,2,3]
    Output: 2
    Explanation: You have 2 children and 3 cookies. The greed factors of 2 children
                 are 1, 2.
                 You have 3 cookies and their sizes are big enough to gratify all of
                 the children, You need to output 2.

Constraints:
- 1 <= g.length <= 3 * 10^4
- 0 <= s.length <= 3 * 10^4
- 1 <= g[i], s[j] <= 2^31 - 1

Topics: Array, Two Pointers, Greedy, Sorting
Pattern: GreedyCore - Sort + Match Kernel
"""

import json
from typing import List

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionGreedy",
        "method": "findContentChildren",
        "complexity": "O(n log n + m log m) time, O(1) space",
        "description": "Sort both arrays, greedily match smallest cookie to smallest child",
    },
    "greedy": {
        "class": "SolutionGreedy",
        "method": "findContentChildren",
        "complexity": "O(n log n + m log m) time, O(1) space",
        "description": "Sort both arrays, greedily match smallest cookie to smallest child",
    },
}


# ============================================================================
# JUDGE_FUNC - Validate content children count
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate maximum content children."""
    lines = input_data.strip().split("\n")
    g = json.loads(lines[0])
    s = json.loads(lines[1])
    correct = _reference_assign_cookies(g, s)

    if isinstance(actual, int):
        actual_int = actual
    elif isinstance(actual, str):
        try:
            actual_int = int(actual.strip())
        except ValueError:
            return False
    else:
        return False

    return actual_int == correct


def _reference_assign_cookies(g: List[int], s: List[int]) -> int:
    """O(n log n) reference using greedy matching."""
    g.sort()
    s.sort()
    child = cookie = 0
    while child < len(g) and cookie < len(s):
        if s[cookie] >= g[child]:
            child += 1
        cookie += 1
    return child


JUDGE_FUNC = judge


# ============================================================================
# Solution: Greedy Sort + Match
# Time: O(n log n + m log m), Space: O(1) excluding sort
#
# Core Insight (Sort + Match Kernel):
#   1. Sort children by greed factor (ascending)
#   2. Sort cookies by size (ascending)
#   3. For the least greedy child, use the smallest cookie that satisfies them
#
# Greedy Choice Property:
#   Using a larger cookie than necessary on a less greedy child is wasteful.
#   The larger cookie might be needed for a greedier child later.
#   So always use the smallest satisfying cookie.
#
# Two-Pointer Approach:
#   - child pointer: current child to satisfy
#   - cookie pointer: current cookie to try
#   - If cookie satisfies child, move both pointers
#   - If cookie too small, try next cookie
#
# Pattern Reference: GreedyCore - Sort + Match
# ============================================================================
class SolutionGreedy:
    def findContentChildren(self, g: List[int], s: List[int]) -> int:
        # Sort both arrays in ascending order
        greed_factors = sorted(g)
        cookie_sizes = sorted(s)

        content_children = 0
        cookie_index = 0

        for greed in greed_factors:
            # Find the smallest cookie that satisfies this child
            while cookie_index < len(cookie_sizes):
                if cookie_sizes[cookie_index] >= greed:
                    # This cookie satisfies this child
                    content_children += 1
                    cookie_index += 1
                    break
                # Cookie too small, try next
                cookie_index += 1

        return content_children


def solve():
    """
    Input format (JSON per line):
        Line 1: g (greed factors) as JSON array
        Line 2: s (cookie sizes) as JSON array

    Output format:
        Integer (maximum content children)
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    g = json.loads(lines[0])
    s = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.findContentChildren(g, s)

    print(result)


if __name__ == "__main__":
    solve()
