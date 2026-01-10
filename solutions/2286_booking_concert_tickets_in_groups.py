"""
Problem: Booking Concert Tickets in Groups
Link: https://leetcode.com/problems/booking-concert-tickets-in-groups/

A concert hall has n rows (0 to n-1), each with m seats (0 to m-1).
- gather(k, maxRow): Find k consecutive seats in rows [0, maxRow]
- scatter(k, maxRow): Allocate k seats (not necessarily consecutive) in rows [0, maxRow]

Constraints:
- 1 <= n <= 5 * 10^4
- 1 <= m, k <= 10^9
- 0 <= maxRow <= n - 1
- At most 5 * 10^4 calls

Topics: Binary Search, Design, Binary Indexed Tree, Segment Tree
"""
from typing import List
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "BookMyShow",
        "method": "__init__",
        "is_design": True,
        "complexity": "O(log n) per operation",
        "description": "Segment Tree with range max and range sum queries",
    },
}


# ============================================================================
# JUDGE_FUNC - For generated tests (Design problem)
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate BookMyShow result."""
    import json
    lines = input_data.strip().split('\n')
    methods = json.loads(lines[0])
    args = json.loads(lines[1])

    if expected is not None:
        return actual == expected
    else:
        # Run reference implementation
        results = []
        obj = None
        for method, arg in zip(methods, args):
            if method == "BookMyShow":
                obj = BookMyShow(arg[0], arg[1])
                results.append(None)
            elif method == "gather":
                results.append(obj.gather(arg[0], arg[1]))
            elif method == "scatter":
                results.append(obj.scatter(arg[0], arg[1]))
        return actual == results


JUDGE_FUNC = judge


# ============================================================================
# Solution: Segment Tree with Range Max and Range Sum
# Time: O(log n) per operation
# Space: O(n) for segment tree
#   - Segment tree stores (max_remaining, sum_remaining) for each range
#   - gather: binary search on segment tree for leftmost row with enough seats
#   - scatter: range sum query + greedy allocation
# ============================================================================
class BookMyShow:
    # Key insight: Track remaining seats per row
    #   remaining[i] = number of available seats in row i
    #
    # For gather(k, maxRow):
    #   1. Find leftmost row r in [0, maxRow] where remaining[r] >= k
    #   2. The first available seat in row r is at column (m - remaining[r])
    #   3. Allocate k seats: remaining[r] -= k
    #
    # For scatter(k, maxRow):
    #   1. Check if sum(remaining[0:maxRow+1]) >= k
    #   2. If yes, greedily fill rows from 0 to maxRow
    #
    # Segment tree operations:
    #   - Range max query: find if any row in range has >= k seats
    #   - Range sum query: total available seats in range
    #   - Point update: decrease remaining[row]

    def __init__(self, n: int, m: int):
        self.n = n
        self.m = m
        # remaining[i] = available seats in row i
        self.remaining = [m] * n

        # Segment tree: each node stores (max_in_range, sum_in_range)
        self.tree_max = [0] * (4 * n)
        self.tree_sum = [0] * (4 * n)
        self._build(1, 0, n - 1)

        # Track the first non-full row for scatter optimization
        self.first_available_row = 0

    def _build(self, node: int, start: int, end: int) -> None:
        """Build segment tree."""
        if start == end:
            self.tree_max[node] = self.m
            self.tree_sum[node] = self.m
            return

        mid = (start + end) // 2
        left, right = 2 * node, 2 * node + 1
        self._build(left, start, mid)
        self._build(right, mid + 1, end)
        self.tree_max[node] = max(self.tree_max[left], self.tree_max[right])
        self.tree_sum[node] = self.tree_sum[left] + self.tree_sum[right]

    def _update(self, node: int, start: int, end: int, idx: int, val: int) -> None:
        """Update remaining seats at row idx."""
        if start == end:
            self.tree_max[node] = val
            self.tree_sum[node] = val
            return

        mid = (start + end) // 2
        left, right = 2 * node, 2 * node + 1
        if idx <= mid:
            self._update(left, start, mid, idx, val)
        else:
            self._update(right, mid + 1, end, idx, val)
        self.tree_max[node] = max(self.tree_max[left], self.tree_max[right])
        self.tree_sum[node] = self.tree_sum[left] + self.tree_sum[right]

    def _query_max(self, node: int, start: int, end: int, l: int, r: int) -> int:
        """Query max remaining seats in range [l, r]."""
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            return self.tree_max[node]

        mid = (start + end) // 2
        left_max = self._query_max(2 * node, start, mid, l, r)
        right_max = self._query_max(2 * node + 1, mid + 1, end, l, r)
        return max(left_max, right_max)

    def _query_sum(self, node: int, start: int, end: int, l: int, r: int) -> int:
        """Query sum of remaining seats in range [l, r]."""
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            return self.tree_sum[node]

        mid = (start + end) // 2
        left_sum = self._query_sum(2 * node, start, mid, l, r)
        right_sum = self._query_sum(2 * node + 1, mid + 1, end, l, r)
        return left_sum + right_sum

    def _find_leftmost_with_k(self, node: int, start: int, end: int, k: int, max_row: int) -> int:
        """Find leftmost row in [start, min(end, max_row)] with >= k seats."""
        if start > max_row or self.tree_max[node] < k:
            return -1
        if start == end:
            return start if self.remaining[start] >= k else -1

        mid = (start + end) // 2
        # Try left subtree first (smaller row numbers)
        left_result = self._find_leftmost_with_k(2 * node, start, mid, k, max_row)
        if left_result != -1:
            return left_result
        # Try right subtree
        return self._find_leftmost_with_k(2 * node + 1, mid + 1, end, k, max_row)

    def gather(self, k: int, maxRow: int) -> List[int]:
        """Find k consecutive seats in rows [0, maxRow]."""
        # Find leftmost row with >= k seats
        row = self._find_leftmost_with_k(1, 0, self.n - 1, k, maxRow)
        if row == -1:
            return []

        # Allocate k seats starting from first available position
        first_seat = self.m - self.remaining[row]
        self.remaining[row] -= k
        self._update(1, 0, self.n - 1, row, self.remaining[row])

        return [row, first_seat]

    def scatter(self, k: int, maxRow: int) -> bool:
        """Allocate k seats (not necessarily consecutive) in rows [0, maxRow]."""
        # Check if enough total seats available
        total = self._query_sum(1, 0, self.n - 1, self.first_available_row, maxRow)
        if total < k:
            return False

        # Greedily allocate seats from first available row
        remaining_to_allocate = k
        row = self.first_available_row

        while remaining_to_allocate > 0 and row <= maxRow:
            if self.remaining[row] > 0:
                take = min(remaining_to_allocate, self.remaining[row])
                self.remaining[row] -= take
                remaining_to_allocate -= take
                self._update(1, 0, self.n - 1, row, self.remaining[row])

                # If row is now full, move first_available_row forward
                if self.remaining[row] == 0:
                    if row == self.first_available_row:
                        self.first_available_row = row + 1
            row += 1

        return True


# ============================================================================
# solve() - stdin/stdout interface for Design problems
# ============================================================================
def solve(input_data: str = None, variant: str = "default") -> List:
    """Run BookMyShow operations from input data."""
    import sys
    import json

    if input_data is None:
        input_data = sys.stdin.read()

    lines = input_data.strip().split('\n')
    methods = json.loads(lines[0])
    args = json.loads(lines[1])

    results = []
    obj = None

    for method, arg in zip(methods, args):
        if method == "BookMyShow":
            obj = BookMyShow(arg[0], arg[1])
            results.append(None)
        elif method == "gather":
            result = obj.gather(arg[0], arg[1])
            results.append(result if result else [])
        elif method == "scatter":
            results.append(obj.scatter(arg[0], arg[1]))

    return results


if __name__ == "__main__":
    result = solve()
    print(result)
