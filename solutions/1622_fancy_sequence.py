"""
Problem: Fancy Sequence
Link: https://leetcode.com/problems/fancy-sequence/

Write an API that generates fancy sequences using the append, addAll, and multAll operations.

Implement the Fancy class:
- Fancy() Initializes the object with an empty sequence.
- void append(val) Appends an integer val to the end of the sequence.
- void addAll(inc) Increments all existing values in the sequence by an integer inc.
- void multAll(m) Multiplies all existing values in the sequence by an integer m.
- int getIndex(idx) Gets the current value at index idx (0-indexed) modulo 10^9 + 7.

Constraints:
- 1 <= val, inc, m <= 100
- 0 <= idx <= 10^5
- At most 10^5 calls total

Topics: Math, Design, Segment Tree
"""
from typing import List
from _runner import get_solver


MOD = 10**9 + 7


SOLUTIONS = {
    "default": {
        "class": "Fancy",
        "method": "__init__",
        "is_design": True,
        "complexity": "O(1) per operation, O(log MOD) for modular inverse",
        "description": "Lazy propagation with modular inverse for efficient operations",
    },
}


# ============================================================================
# JUDGE_FUNC - For generated tests (Design problem)
# ============================================================================
def _run_fancy_simulation(methods: List[str], args: List[List[int]]) -> List:
    """Run Fancy operations and return results."""
    results = []
    obj = None

    for method, arg in zip(methods, args):
        if method == "Fancy":
            obj = Fancy()
            results.append(None)
        elif method == "append":
            obj.append(arg[0])
            results.append(None)
        elif method == "addAll":
            obj.addAll(arg[0])
            results.append(None)
        elif method == "multAll":
            obj.multAll(arg[0])
            results.append(None)
        elif method == "getIndex":
            results.append(obj.getIndex(arg[0]))

    return results


def judge(actual, expected, input_data: str) -> bool:
    """Validate Fancy Sequence result."""
    import json
    lines = input_data.strip().split('\n')
    methods = json.loads(lines[0])
    args = json.loads(lines[1])

    if expected is not None:
        return actual == expected
    else:
        correct = _run_fancy_simulation(methods, args)
        return actual == correct


JUDGE_FUNC = judge


# ============================================================================
# Solution: Lazy Propagation with Modular Inverse
# Time: O(1) for append/addAll/multAll, O(log MOD) for getIndex
# Space: O(n) for storing elements
#   - Key insight: track cumulative add/mult operations lazily
#   - Store (value, mult_at_insert, add_at_insert) for each element
#   - Use modular inverse to "undo" transformations at insertion time
# ============================================================================
class Fancy:
    # Instead of applying operations to all elements (O(n)),
    # we track cumulative multiplier (mult) and adder (add).
    #
    # Invariant: current_value = stored_value * mult + add
    #
    # When appending, we store the "inverse-transformed" value so that
    # applying the current transformation gives back the original value.
    #
    # When getIndex is called, we apply the full transformation.
    #
    # Mathematical foundation:
    #   If current state is (mult, add), and we insert value v:
    #   We store v' such that v' * mult + add = v (mod MOD)
    #   => v' = (v - add) * mult^(-1) (mod MOD)
    #
    #   For getIndex, result = stored * mult + add (mod MOD)

    def __init__(self):
        self.sequence: List[int] = []  # Inverse-transformed values
        self.mult = 1  # Cumulative multiplier
        self.add = 0   # Cumulative adder

    def append(self, val: int) -> None:
        # Store inverse-transformed value
        # v' = (val - add) * mult^(-1) mod MOD
        inverse_mult = pow(self.mult, MOD - 2, MOD)
        stored = ((val - self.add) % MOD * inverse_mult) % MOD
        self.sequence.append(stored)

    def addAll(self, inc: int) -> None:
        # Add inc to all current values
        # new_value = old_value + inc = stored * mult + add + inc
        # So we just update: add += inc
        self.add = (self.add + inc) % MOD

    def multAll(self, m: int) -> None:
        # Multiply all current values by m
        # new_value = old_value * m = (stored * mult + add) * m = stored * (mult*m) + (add*m)
        # So we update: mult *= m, add *= m
        self.mult = (self.mult * m) % MOD
        self.add = (self.add * m) % MOD

    def getIndex(self, idx: int) -> int:
        if idx >= len(self.sequence):
            return -1

        # Apply transformation: result = stored * mult + add
        stored = self.sequence[idx]
        return (stored * self.mult + self.add) % MOD


# ============================================================================
# solve() - stdin/stdout interface for Design problems
# ============================================================================
def solve(input_data: str = None, variant: str = "default") -> List:
    """
    Run Fancy operations from input data.

    Input format for Design problems:
        Line 1: JSON array of method names
        Line 2: JSON array of argument lists

    Example:
        ["Fancy","append","addAll","append","multAll","getIndex"]
        [[],[2],[3],[7],[2],[0]]
        -> [None, None, None, None, None, 10]
    """
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
        if method == "Fancy":
            obj = Fancy()
            results.append(None)
        elif method == "append":
            obj.append(arg[0])
            results.append(None)
        elif method == "addAll":
            obj.addAll(arg[0])
            results.append(None)
        elif method == "multAll":
            obj.multAll(arg[0])
            results.append(None)
        elif method == "getIndex":
            results.append(obj.getIndex(arg[0]))

    return results


if __name__ == "__main__":
    result = solve()
    print(result)
