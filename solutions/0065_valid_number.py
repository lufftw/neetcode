"""
Problem: Valid Number
Link: https://leetcode.com/problems/valid-number/

A valid number has the form:
  [sign] (decimal | integer) [('e'|'E') [sign] integer]

Where:
  decimal = digits '.' [digits] | [digits] '.' digits
  integer = digits+

Constraints:
- 1 <= s.length <= 20
- s consists of letters, digits (0-9), '+', '-', or '.'.

Topics: String
"""
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "isNumber",
        "complexity": "O(n) time, O(1) space",
        "description": "DFA-based state machine parser",
    },
}


# JUDGE_FUNC for generated tests
def _reference(s: str) -> bool:
    """Reference implementation using Python's float parsing."""
    try:
        # Filter out invalid patterns that Python accepts but problem doesn't
        s = s.strip()
        if not s:
            return False
        # Check for inf/nan which Python accepts
        lower = s.lower()
        if 'inf' in lower or 'nan' in lower:
            return False
        # Check for invalid characters (letters other than e/E)
        for c in s:
            if c.isalpha() and c.lower() != 'e':
                return False
        float(s)
        return True
    except ValueError:
        return False


def judge(actual, expected, input_data: str) -> bool:
    import json
    s = json.loads(input_data.strip())
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(s)


JUDGE_FUNC = judge


# ============================================================================
# Solution: DFA-based State Machine
# Time: O(n), Space: O(1)
#   - Single pass through the string
#   - Track state transitions based on character type
# ============================================================================
class Solution:
    # Key insight: Use a deterministic finite automaton (DFA)
    #
    # States:
    #   0: start
    #   1: sign seen (for mantissa)
    #   2: digit seen (integer part)
    #   3: dot seen after digit (e.g., "3.")
    #   4: dot seen before digit (e.g., ".5" or "3.5")
    #   5: 'e' or 'E' seen
    #   6: sign seen (for exponent)
    #   7: digit seen (exponent)
    #
    # Accept states: 2, 3, 4, 7

    def isNumber(self, s: str) -> bool:
        # State transitions: state -> {char_type: next_state}
        # char types: 'sign', 'digit', 'dot', 'exp'
        transitions = {
            0: {'sign': 1, 'digit': 2, 'dot': 8},
            1: {'digit': 2, 'dot': 8},
            2: {'digit': 2, 'dot': 3, 'exp': 5},
            3: {'digit': 4, 'exp': 5},
            4: {'digit': 4, 'exp': 5},
            5: {'sign': 6, 'digit': 7},
            6: {'digit': 7},
            7: {'digit': 7},
            8: {'digit': 4},  # Dot seen at start, need digit
        }

        accept_states = {2, 3, 4, 7}

        state = 0

        for char in s:
            if char in '+-':
                char_type = 'sign'
            elif char.isdigit():
                char_type = 'digit'
            elif char == '.':
                char_type = 'dot'
            elif char in 'eE':
                char_type = 'exp'
            else:
                return False

            if state not in transitions:
                return False
            if char_type not in transitions[state]:
                return False

            state = transitions[state][char_type]

        return state in accept_states


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: s (JSON string)

    Example:
        "0"
        -> true
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')
    s = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.isNumber(s)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
