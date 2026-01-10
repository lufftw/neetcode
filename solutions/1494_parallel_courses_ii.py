"""
Problem: Parallel Courses II
Link: https://leetcode.com/problems/parallel-courses-ii/

Given n courses and prerequisite relations, find minimum semesters to complete all.
Can take at most k courses per semester if prerequisites satisfied.

Constraints:
- 1 <= n <= 15
- 1 <= k <= n
- 0 <= relations.length <= n*(n-1)/2
- relations[i] = [prevCourse, nextCourse]
- Graph is a DAG

Topics: Dynamic Programming, Bit Manipulation, Bitmask
"""
from typing import List
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "minNumberOfSemesters",
        "complexity": "O(3^n) time, O(2^n) space",
        "description": "Bitmask DP with subset enumeration",
    },
}


# ============================================================================
# JUDGE_FUNC: Verify minimum semesters through brute-force BFS
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate answer using BFS over states.
    For small n (<=15), we can verify by exploring all valid orderings.
    """
    lines = input_data.strip().split('\n')
    n = json.loads(lines[0])
    relations = json.loads(lines[1])
    k = json.loads(lines[2])

    # Build prerequisite bitmasks
    prereq = [0] * n
    for prev, nxt in relations:
        prereq[nxt - 1] |= (1 << (prev - 1))

    # BFS to find minimum semesters
    from collections import deque

    full = (1 << n) - 1
    visited = {0: 0}  # state -> min semesters
    queue = deque([0])

    while queue:
        taken = queue.popleft()
        if taken == full:
            return visited[full] == actual

        semesters = visited[taken]

        # Find available courses (prerequisites met, not taken)
        available = 0
        for i in range(n):
            if not (taken & (1 << i)):  # Not taken
                if (prereq[i] & taken) == prereq[i]:  # Prerequisites met
                    available |= (1 << i)

        # Enumerate all subsets up to size k
        subset = available
        while subset > 0:
            if bin(subset).count('1') <= k:
                new_state = taken | subset
                if new_state not in visited:
                    visited[new_state] = semesters + 1
                    queue.append(new_state)
            subset = (subset - 1) & available

    return visited.get(full, -1) == actual


JUDGE_FUNC = judge


# ============================================================================
# Solution: Bitmask DP
# Time: O(3^n), Space: O(2^n)
# ============================================================================
class Solution:
    # Key insight: n <= 15 allows bitmask DP over 2^15 = 32768 states.
    #
    # dp[mask] = minimum semesters to complete courses in mask
    # Transition: for each state, find courses whose prerequisites are met,
    # then enumerate all subsets of size <= k.
    #
    # Subset enumeration trick: to enumerate all subsets of mask,
    # use "sub = (sub - 1) & mask" starting from sub = mask.

    def minNumberOfSemesters(
        self, n: int, relations: List[List[int]], k: int
    ) -> int:
        # prereq[i] = bitmask of prerequisites for course i
        prereq = [0] * n
        for prev, nxt in relations:
            prereq[nxt - 1] |= (1 << (prev - 1))

        full = (1 << n) - 1
        INF = float('inf')
        dp = [INF] * (1 << n)
        dp[0] = 0

        for taken in range(1 << n):
            if dp[taken] == INF:
                continue

            # Find courses available to take (prerequisites met, not yet taken)
            available = 0
            for i in range(n):
                if not (taken & (1 << i)):  # Not yet taken
                    if (prereq[i] & taken) == prereq[i]:  # All prerequisites met
                        available |= (1 << i)

            # Enumerate all subsets of available courses
            subset = available
            while subset > 0:
                if bin(subset).count('1') <= k:
                    new_state = taken | subset
                    dp[new_state] = min(dp[new_state], dp[taken] + 1)
                subset = (subset - 1) & available

        return dp[full]


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: n (integer)
        Line 2: relations as JSON 2D array
        Line 3: k (integer)

    Example:
        4
        [[2,1],[3,1],[1,4]]
        2
        -> 3
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    n = json.loads(lines[0])
    relations = json.loads(lines[1])
    k = json.loads(lines[2])

    solver = get_solver(SOLUTIONS)
    result = solver.minNumberOfSemesters(n, relations, k)

    print(result)


if __name__ == "__main__":
    solve()
