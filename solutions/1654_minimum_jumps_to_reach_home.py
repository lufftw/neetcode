"""
Problem: Minimum Jumps to Reach Home
Link: https://leetcode.com/problems/minimum-jumps-to-reach-home/

Bug starts at 0, wants to reach x. Can jump +a forward or -b backward.
Cannot jump backward twice in a row or to forbidden positions.

Constraints:
- 1 <= forbidden.length <= 1000
- 1 <= a, b, forbidden[i] <= 2000
- 0 <= x <= 2000
- x is not forbidden

Topics: Array, Dynamic Programming, BFS
"""
from typing import List
from _runner import get_solver
import json
from collections import deque


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "minimumJumps",
        "complexity": "O(max(x, max(forbidden) + a + b)) time and space",
        "description": "BFS with state (position, was_backward)",
    },
}


# ============================================================================
# Solution: BFS with Direction State
# Time: O(N), Space: O(N) where N = max reachable position
# ============================================================================
class Solution:
    # Key insight: State = (position, last_jump_was_backward)
    # We can't jump backward twice, so track the direction.
    #
    # Upper bound for position: max(forbidden) + a + b
    # Beyond this, no useful paths exist.
    #
    # BFS ensures shortest path (minimum jumps).

    def minimumJumps(
        self, forbidden: List[int], a: int, b: int, x: int
    ) -> int:
        # Upper bound: we never need to go beyond this
        upper = max(max(forbidden, default=0), x) + a + b

        forbidden_set = set(forbidden)

        # State: (position, was_last_backward)
        # was_last_backward: 0 = no/forward, 1 = backward
        visited = set()
        visited.add((0, 0))

        queue = deque([(0, 0, 0)])  # (position, was_last_backward, jumps)

        while queue:
            pos, was_back, jumps = queue.popleft()

            if pos == x:
                return jumps

            # Forward jump (+a)
            new_pos = pos + a
            if (new_pos, 0) not in visited and new_pos <= upper and new_pos not in forbidden_set:
                visited.add((new_pos, 0))
                queue.append((new_pos, 0, jumps + 1))

            # Backward jump (-b) only if last wasn't backward
            if was_back == 0:
                new_pos = pos - b
                if new_pos >= 0 and (new_pos, 1) not in visited and new_pos not in forbidden_set:
                    visited.add((new_pos, 1))
                    queue.append((new_pos, 1, jumps + 1))

        return -1


# ============================================================================
# JUDGE_FUNC: Verify answer using reference solution
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Verify answer by running reference solution.
    """
    lines = input_data.strip().split('\n')
    forbidden = json.loads(lines[0])
    a = json.loads(lines[1])
    b = json.loads(lines[2])
    x = json.loads(lines[3])

    sol = Solution()
    correct = sol.minimumJumps(forbidden, a, b, x)

    return actual == correct


JUDGE_FUNC = judge


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: forbidden as JSON array
        Line 2: a (integer)
        Line 3: b (integer)
        Line 4: x (integer)

    Example:
        [14,4,18,1,15]
        3
        15
        9
        -> 3
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    forbidden = json.loads(lines[0])
    a = json.loads(lines[1])
    b = json.loads(lines[2])
    x = json.loads(lines[3])

    solver = get_solver(SOLUTIONS)
    result = solver.minimumJumps(forbidden, a, b, x)

    print(result)


if __name__ == "__main__":
    solve()
