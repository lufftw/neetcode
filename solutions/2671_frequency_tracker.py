"""
Problem: Frequency Tracker
Link: https://leetcode.com/problems/frequency-tracker/

Design a data structure to track number frequencies and answer hasFrequency queries.

Constraints:
- 1 <= number <= 10^5
- 1 <= frequency <= 10^5
- At most 2 * 10^5 total operations

Topics: Hash Table, Design
"""
from _runner import get_solver
import json
from collections import defaultdict


SOLUTIONS = {
    "default": {
        "class": "FrequencyTracker",
        "method": None,  # Class design problem
        "complexity": "O(1) per operation",
        "description": "Dual hashmap: number->count and freq->count_of_numbers",
    },
}


# ============================================================================
# Solution: Dual HashMap
# Time: O(1) per operation, Space: O(n)
# ============================================================================
class FrequencyTracker:
    # Key insight: Maintain two maps:
    # 1. count[num] = how many times num appears
    # 2. freq_count[f] = how many distinct numbers have frequency f
    #
    # On add/delete: update both maps to keep them synchronized.
    # hasFrequency(f) simply checks if freq_count[f] > 0.

    def __init__(self):
        self.count = defaultdict(int)        # num -> frequency
        self.freq_count = defaultdict(int)   # frequency -> count of numbers

    def add(self, number: int) -> None:
        old_freq = self.count[number]
        if old_freq > 0:
            self.freq_count[old_freq] -= 1

        self.count[number] += 1
        new_freq = self.count[number]
        self.freq_count[new_freq] += 1

    def deleteOne(self, number: int) -> None:
        old_freq = self.count[number]
        if old_freq == 0:
            return  # Number doesn't exist

        self.freq_count[old_freq] -= 1
        self.count[number] -= 1
        new_freq = self.count[number]
        if new_freq > 0:
            self.freq_count[new_freq] += 1

    def hasFrequency(self, frequency: int) -> bool:
        return self.freq_count[frequency] > 0


# Alias for SOLUTIONS
Solution = FrequencyTracker


# ============================================================================
# JUDGE_FUNC: Execute operations and verify results
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Execute operations and compute expected results.
    """
    lines = input_data.strip().split('\n')
    operations = json.loads(lines[0])
    arguments = json.loads(lines[1])

    # Execute operations
    result = []
    obj = None

    for op, args in zip(operations, arguments):
        if op == "FrequencyTracker":
            obj = FrequencyTracker()
            result.append(None)
        elif op == "add":
            obj.add(args[0])
            result.append(None)
        elif op == "deleteOne":
            obj.deleteOne(args[0])
            result.append(None)
        elif op == "hasFrequency":
            result.append(obj.hasFrequency(args[0]))

    # Handle string vs list comparison
    if isinstance(actual, str):
        # Parse JSON string output directly
        actual = json.loads(actual)
    elif isinstance(actual, list):
        pass  # Already a list

    return actual == result


JUDGE_FUNC = judge


# ============================================================================
# solve() - stdin/stdout interface for class design problems
# ============================================================================
def solve():
    """
    Input format:
        Line 1: operations as JSON array
        Line 2: arguments as JSON 2D array

    Example:
        ["FrequencyTracker", "add", "add", "hasFrequency"]
        [[], [3], [3], [2]]
        -> [null, null, null, true]
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    operations = json.loads(lines[0])
    arguments = json.loads(lines[1])

    result = []
    obj = None

    for op, args in zip(operations, arguments):
        if op == "FrequencyTracker":
            obj = FrequencyTracker()
            result.append(None)
        elif op == "add":
            obj.add(args[0])
            result.append(None)
        elif op == "deleteOne":
            obj.deleteOne(args[0])
            result.append(None)
        elif op == "hasFrequency":
            result.append(obj.hasFrequency(args[0]))

    # Format output: null for None, true/false for booleans
    output = []
    for r in result:
        if r is None:
            output.append("null")
        elif r is True:
            output.append("true")
        elif r is False:
            output.append("false")
        else:
            output.append(str(r))

    print("[" + ",".join(output) + "]")


if __name__ == "__main__":
    solve()
