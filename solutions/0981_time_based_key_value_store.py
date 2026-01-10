"""
Problem: Time Based Key-Value Store
Link: https://leetcode.com/problems/time-based-key-value-store/

Design a time-based key-value data structure that can store multiple values for
the same key at different time stamps and retrieve the key's value at a certain
timestamp.

Implement the TimeMap class:
- TimeMap() Initializes the object of the data structure.
- void set(String key, String value, int timestamp) Stores the key with value at
  the given timestamp.
- String get(String key, int timestamp) Returns a value such that set was called
  previously, with timestamp_prev <= timestamp. If there are multiple such values,
  it returns the value with the largest timestamp_prev. If there are no values,
  it returns "".

Example 1:
    Input:
        ["TimeMap", "set", "get", "get", "set", "get", "get"]
        [[], ["foo", "bar", 1], ["foo", 1], ["foo", 3], ["foo", "bar2", 4], ["foo", 4], ["foo", 5]]
    Output:
        [null, null, "bar", "bar", null, "bar2", "bar2"]

Constraints:
- 1 <= key.length, value.length <= 100
- key and value consist of lowercase English letters and digits.
- 1 <= timestamp <= 10^7
- All timestamps of set are strictly increasing.
- At most 2 * 10^5 calls will be made to set and get.

Topics: Hash Table, String, Binary Search, Design
"""

import json
import bisect
from typing import List, Dict
from collections import defaultdict
from _runner import get_solver


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "TimeMapBisect",
        "method": "_run_operations",
        "complexity": "O(1) set, O(log n) get",
        "description": "HashMap + bisect for binary search on timestamps",
    },
    "manual_binary_search": {
        "class": "TimeMapManual",
        "method": "_run_operations",
        "complexity": "O(1) set, O(log n) get",
        "description": "HashMap + manual binary search implementation",
    },
}


# ============================================================================
# Solution 1: HashMap + Python bisect
# Time: O(1) for set, O(log n) for get where n = entries for that key
# Space: O(total entries)
#
# Key Insight:
#   Since timestamps are strictly increasing for set operations, entries for
#   each key are automatically sorted by timestamp. For get, we need to find
#   the largest timestamp <= query timestamp, which is a binary search.
#
# Data Structure:
#   - HashMap: key -> list of (timestamp, value) tuples
#   - Use bisect_right to find insertion point, then look at previous entry
#
# Why bisect_right:
#   bisect_right returns the index where we would insert the query timestamp
#   to keep the list sorted. The entry just before this index (if exists) is
#   the largest timestamp <= query.
# ============================================================================
class TimeMapBisect:
    """
    Time-based key-value store using Python's bisect module.

    Each key maps to a list of (timestamp, value) pairs. Since timestamps
    are strictly increasing, the list is naturally sorted. Binary search
    via bisect_right finds the appropriate value efficiently.
    """

    def __init__(self):
        # key -> [(timestamp, value), ...]
        self.store: Dict[str, List[tuple]] = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        """O(1) - Append to list (timestamps are increasing)."""
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        """
        O(log n) - Binary search for largest timestamp <= query.

        Use bisect_right to find where query timestamp would be inserted,
        then return the value at the previous index (if it exists).
        """
        if key not in self.store:
            return ""

        entries = self.store[key]

        # bisect_right returns index where timestamp would be inserted
        # to maintain sorted order (after any equal elements)
        idx = bisect.bisect_right(entries, (timestamp, chr(127)))

        if idx == 0:
            # No timestamp <= query
            return ""

        return entries[idx - 1][1]

    def _run_operations(self, operations: List[str], args: List[List]) -> List:
        """Execute a sequence of operations and return results."""
        results = []
        for op, arg in zip(operations, args):
            if op == "TimeMap":
                results.append(None)
            elif op == "set":
                self.set(arg[0], arg[1], arg[2])
                results.append(None)
            elif op == "get":
                results.append(self.get(arg[0], arg[1]))
        return results


# ============================================================================
# Solution 2: HashMap + Manual Binary Search
# Time: O(1) for set, O(log n) for get
# Space: O(total entries)
#
# Key Insight:
#   Same approach as Solution 1, but with explicit binary search implementation.
#   This demonstrates the binary search logic clearly and is useful when bisect
#   is not available or when learning the algorithm.
#
# Binary Search Logic:
#   Find the rightmost entry with timestamp <= query. This is equivalent to
#   finding the last position where entries[mid].timestamp <= timestamp.
# ============================================================================
class TimeMapManual:
    """
    Time-based key-value store with manual binary search.

    Explicit binary search helps understand the algorithm: we're finding
    the rightmost entry whose timestamp doesn't exceed the query timestamp.
    """

    def __init__(self):
        self.store: Dict[str, List[tuple]] = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        """O(1) - Append to list."""
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        """
        O(log n) - Manual binary search for largest timestamp <= query.

        Find the rightmost entry where entry.timestamp <= timestamp.
        """
        if key not in self.store:
            return ""

        entries = self.store[key]

        # Binary search for rightmost entry with timestamp <= query
        left, right = 0, len(entries) - 1
        result = ""

        while left <= right:
            mid = (left + right) // 2

            if entries[mid][0] <= timestamp:
                # This entry is valid, record it and search right for better
                result = entries[mid][1]
                left = mid + 1
            else:
                # This entry's timestamp is too large, search left
                right = mid - 1

        return result

    def _run_operations(self, operations: List[str], args: List[List]) -> List:
        """Execute a sequence of operations and return results."""
        results = []
        for op, arg in zip(operations, args):
            if op == "TimeMap":
                results.append(None)
            elif op == "set":
                self.set(arg[0], arg[1], arg[2])
                results.append(None)
            elif op == "get":
                results.append(self.get(arg[0], arg[1]))
        return results


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: operations as JSON array
        Line 2: arguments as JSON 2D array

    Example:
        ["TimeMap","set","get","get","set","get","get"]
        [[],["foo","bar",1],["foo",1],["foo",3],["foo","bar2",4],["foo",4],["foo",5]]
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")

    operations = json.loads(lines[0])
    args = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver._run_operations(operations, args)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
