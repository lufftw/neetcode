"""
Problem: Jump Game VII
Link: https://leetcode.com/problems/jump-game-vii/

Start at index 0. Can jump from i to j if:
- i + minJump <= j <= i + maxJump
- s[j] == '0'
Return true if can reach the last index.

Constraints:
- 2 <= s.length <= 10^5
- s[i] is '0' or '1'
- s[0] == '0'
- 1 <= minJump <= maxJump < s.length

Topics: String, DP, Sliding Window, Prefix Sum
"""
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "canReach",
        "complexity": "O(n) time, O(n) space",
        "description": "Sliding window counting reachable sources in jump range",
    },
}


# JUDGE_FUNC for generated tests
def _reference(s: str, minJump: int, maxJump: int) -> bool:
    """BFS-like reference implementation."""
    n = len(s)
    if s[-1] == '1':
        return False

    reachable = [False] * n
    reachable[0] = True

    # For each position, check if any position in [i-maxJump, i-minJump] is reachable
    # Use prefix sum to optimize
    prefix = [0] * (n + 1)  # prefix[i] = number of reachable positions in [0, i)
    prefix[1] = 1  # Position 0 is reachable

    for i in range(1, n):
        if s[i] == '1':
            prefix[i + 1] = prefix[i]
            continue

        # Can reach i from positions [i-maxJump, i-minJump]
        lo = max(0, i - maxJump)
        hi = i - minJump

        if hi >= 0 and prefix[hi + 1] - prefix[lo] > 0:
            reachable[i] = True

        prefix[i + 1] = prefix[i] + (1 if reachable[i] else 0)

    return reachable[n - 1]


def judge(actual, expected, input_data: str) -> bool:
    lines = input_data.strip().split('\n')
    s = json.loads(lines[0])
    minJump = json.loads(lines[1])
    maxJump = json.loads(lines[2])
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(s, minJump, maxJump)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Sliding Window with Reachable Count
# Time: O(n), Space: O(n)
# ============================================================================
class Solution:
    # Key insight:
    #   - Position j is reachable if s[j]=='0' AND some position in
    #     [j-maxJump, j-minJump] is reachable
    #   - Use sliding window: maintain count of reachable positions in range
    #   - As j increases by 1, the window [j-maxJump, j-minJump] shifts by 1
    #
    # Implementation:
    #   - dp[i] = True if position i is reachable
    #   - For each j >= minJump, check if window has any reachable position
    #   - Update window count when entering/leaving the range

    def canReach(self, s: str, minJump: int, maxJump: int) -> bool:
        n = len(s)
        if s[-1] == '1':
            return False

        dp = [False] * n
        dp[0] = True

        # Window count: number of reachable positions in current jump range
        # For position j, sources are in [j-maxJump, j-minJump]
        count = 0

        for j in range(minJump, n):
            # Add position entering the window (j - minJump)
            # This position just became a valid source for j
            entering = j - minJump
            if dp[entering]:
                count += 1

            # Check if j is reachable
            if s[j] == '0' and count > 0:
                dp[j] = True

            # Remove position leaving the window
            # For next j+1, the window will be [(j+1)-maxJump, (j+1)-minJump]
            # Position j - maxJump will leave when we move to j+1
            leaving = j - maxJump
            if leaving >= 0 and dp[leaving]:
                count -= 1

        return dp[n - 1]


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: s (JSON string)
        Line 2: minJump (integer)
        Line 3: maxJump (integer)

    Example:
        "011010"
        2
        3
        -> true
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    s = json.loads(lines[0])
    minJump = json.loads(lines[1])
    maxJump = json.loads(lines[2])

    solver = get_solver(SOLUTIONS)
    result = solver.canReach(s, minJump, maxJump)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
