"""
Problem: Distribute Money to Maximum Children
Link: https://leetcode.com/problems/distribute-money-to-maximum-children/

Distribute money to children such that:
- All money is distributed
- Everyone receives at least $1
- Nobody receives exactly $4
Maximize children receiving exactly $8.

Constraints:
- 1 <= money <= 200
- 2 <= children <= 30

Topics: Math, Greedy
"""
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "distMoney",
        "complexity": "O(1) time, O(1) space",
        "description": "Greedy math with edge case handling",
    },
}


# JUDGE_FUNC for generated tests
def _reference(money: int, children: int) -> int:
    """Reference implementation."""
    # Can't give everyone at least $1
    if money < children:
        return -1

    # After giving each child $1, remaining = money - children
    remaining = money - children

    # Each child getting $8 needs $7 more (already has $1)
    # Max k = remaining // 7, but limited by children count
    k = min(children, remaining // 7)

    # After giving k children $8 (8k dollars), check remaining
    leftover = money - 8 * k
    remaining_children = children - k

    if remaining_children == 0:
        # All children got $8
        if leftover > 0:
            # Must give extra to someone, so one less "exactly $8" child
            k -= 1
    else:
        # remaining_children >= 1
        # If only 1 child left and they would get exactly $4, invalid
        if remaining_children == 1 and leftover == 4:
            k -= 1

    return k


def judge(actual, expected, input_data: str) -> bool:
    import json
    lines = input_data.strip().split('\n')
    money = json.loads(lines[0])
    children = json.loads(lines[1])
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(money, children)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Greedy Math with Edge Cases
# Time: O(1), Space: O(1)
#   - Pure mathematical analysis with careful edge case handling
# ============================================================================
class Solution:
    # Key insight: Maximize k (children getting exactly $8)
    #
    # Constraints:
    #   - Each child must get at least $1
    #   - No child gets exactly $4
    #   - All money must be distributed
    #
    # Strategy:
    #   1. Give each child $1 first (reserve children dollars)
    #   2. Remaining = money - children dollars to distribute
    #   3. Each "$8 child" needs $7 more
    #   4. Max k = min(children, remaining // 7)
    #   5. Handle edge cases: leftover must go somewhere, avoid $4

    def distMoney(self, money: int, children: int) -> int:
        # Impossible: can't give everyone at least $1
        if money < children:
            return -1

        # After giving each child $1
        remaining = money - children

        # Each $8-child needs $7 more (they already have $1)
        k = min(children, remaining // 7)

        # After giving k children $8 total
        leftover = money - 8 * k
        remaining_children = children - k

        # Edge case 1: All children got $8, but there's leftover
        # Must give extra to some child, reducing "exactly $8" count
        if remaining_children == 0 and leftover > 0:
            k -= 1

        # Edge case 2: One remaining child would get exactly $4
        # This is forbidden, so give one less child $8
        elif remaining_children == 1 and leftover == 4:
            k -= 1

        return k


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: money (integer)
        Line 2: children (integer)

    Example:
        20
        3
        -> 1
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')
    money = json.loads(lines[0])
    children = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.distMoney(money, children)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
