"""
Problem: Minimum Reverse Operations
Link: https://leetcode.com/problems/minimum-reverse-operations/

You are given an integer n and an integer p in the range [0, n - 1].
Representing a 0-indexed array arr of length n where all positions are set to 0's,
except position p which is set to 1.

You can perform operations: choose a subarray of size k and reverse it.
The 1 should never go to any banned position.

Return an array where ans[i] is the minimum operations to move 1 to position i, or -1 if impossible.

Constraints:
- 1 <= n <= 10^5
- 0 <= p <= n - 1
- 0 <= banned.length <= n - 1
- 1 <= k <= n
- banned[i] != p, all values unique

Topics: Array, Breadth First Search, Ordered Set
"""
from typing import List
from collections import deque
from sortedcontainers import SortedList
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "minReverseOperations",
        "complexity": "O(n log n) time, O(n) space",
        "description": "BFS with SortedList for efficient range queries by parity",
    },
}


# ============================================================================
# JUDGE_FUNC - For generated tests without expected output
# ============================================================================
def _reference_solution(n: int, p: int, banned: List[int], k: int) -> List[int]:
    """Reference implementation for validation."""
    from collections import deque
    from sortedcontainers import SortedList

    result = [-1] * n
    result[p] = 0

    if k == 1:
        return result

    banned_set = set(banned)
    available = [SortedList(), SortedList()]

    for i in range(n):
        if i != p and i not in banned_set:
            available[i % 2].add(i)

    queue = deque([p])

    while queue:
        curr = queue.popleft()
        l_min = max(0, curr - k + 1)
        l_max = min(n - k, curr)
        j_min = 2 * l_min + k - 1 - curr
        j_max = 2 * l_max + k - 1 - curr
        parity = j_min % 2
        sl = available[parity]
        to_visit = list(sl.irange(j_min, j_max))

        for next_pos in to_visit:
            sl.remove(next_pos)
            result[next_pos] = result[curr] + 1
            queue.append(next_pos)

    return result


def judge(actual, expected, input_data: str) -> bool:
    """Validate Minimum Reverse Operations result."""
    import json
    lines = input_data.strip().split('\n')
    n = int(lines[0])
    p = int(lines[1])
    banned = json.loads(lines[2])
    k = int(lines[3])

    if expected is not None:
        return actual == expected
    else:
        correct = _reference_solution(n, p, banned, k)
        return actual == correct


JUDGE_FUNC = judge


# ============================================================================
# Solution: BFS with Ordered Set (SortedList)
# Time: O(n log n), Space: O(n)
#   - Key insight: from position i, reversing subarray [L, L+k-1] moves 1 to position 2L+k-1-i
#   - All reachable positions from i share the same parity as (i + k - 1)
#   - Use two SortedLists (even/odd indices) for O(log n) range deletion
#   - BFS explores each position at most once
# ============================================================================
class Solution:
    # Problem reduction to graph traversal:
    #   - Nodes: positions 0 to n-1
    #   - Edge from i to j if one reverse operation can move 1 from i to j
    #   - Find shortest path from p to each position
    #
    # Key mathematical insight:
    #   Reversing subarray [L, L+k-1] containing position i maps i to j = 2L + k - 1 - i
    #   Valid L range: max(0, i-k+1) <= L <= min(n-k, i)
    #   This gives reachable range: [j_min, j_max] with step 2 (same parity)
    #
    # Optimization: Instead of checking each neighbor individually,
    # use SortedList to efficiently extract all unvisited positions in the range.

    def minReverseOperations(self, n: int, p: int, banned: List[int], k: int) -> List[int]:
        result = [-1] * n
        result[p] = 0

        # Special case: k=1 means no movement possible
        if k == 1:
            return result

        # Create banned set for O(1) lookup
        banned_set = set(banned)

        # Two sorted lists for even and odd positions (unvisited and not banned)
        # Index 0: even positions, Index 1: odd positions
        available = [SortedList(), SortedList()]

        for i in range(n):
            if i != p and i not in banned_set:
                available[i % 2].add(i)

        # BFS from starting position p
        queue = deque([p])

        while queue:
            curr = queue.popleft()

            # Calculate the range of positions reachable from curr in one operation
            # j = 2L + k - 1 - curr, where max(0, curr-k+1) <= L <= min(n-k, curr)
            l_min = max(0, curr - k + 1)
            l_max = min(n - k, curr)

            j_min = 2 * l_min + k - 1 - curr
            j_max = 2 * l_max + k - 1 - curr

            # All reachable positions have the same parity as j_min (or j_max)
            parity = j_min % 2
            sl = available[parity]

            # Find all unvisited positions in range [j_min, j_max]
            # Use irange for efficient iteration
            to_visit = list(sl.irange(j_min, j_max))

            for next_pos in to_visit:
                sl.remove(next_pos)
                result[next_pos] = result[curr] + 1
                queue.append(next_pos)

        return result


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: n
        Line 2: p
        Line 3: banned (JSON array)
        Line 4: k

    Example:
        4
        0
        [1,2]
        4
        -> [0,-1,-1,1]
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')
    n = int(lines[0])
    p = int(lines[1])
    banned = json.loads(lines[2])
    k = int(lines[3])

    solver = get_solver(SOLUTIONS)
    result = solver.minReverseOperations(n, p, banned, k)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
