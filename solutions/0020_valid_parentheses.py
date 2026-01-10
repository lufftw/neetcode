"""
Problem: Valid Parentheses
Link: https://leetcode.com/problems/valid-parentheses/

Given a string s containing just the characters '(', ')', '{', '}', '[' and ']',
determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

Example 1:
    Input: s = "()"
    Output: true

Example 2:
    Input: s = "()[]{}"
    Output: true

Example 3:
    Input: s = "(]"
    Output: false

Constraints:
- 1 <= s.length <= 10^4
- s consists of parentheses only '()[]{}'.

Topics: String, Stack
"""
import json
from _runner import get_solver


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionStack",
        "method": "isValid",
        "complexity": "O(n) time, O(n) space",
        "description": "Stack-based matching with hash map",
    },
    "stack": {
        "class": "SolutionStack",
        "method": "isValid",
        "complexity": "O(n) time, O(n) space",
        "description": "Stack-based matching with hash map",
    },
    "replace": {
        "class": "SolutionReplace",
        "method": "isValid",
        "complexity": "O(n²) time, O(n) space",
        "description": "Iterative replacement - simple but slow",
    },
}


# ============================================================================
# Solution 1: Stack with Hash Map
# Time: O(n), Space: O(n)
#   - Push opening brackets onto stack
#   - For closing brackets, check if top of stack matches
#   - Valid if stack is empty at the end
# ============================================================================
class SolutionStack:
    """
    Stack-based solution - the canonical approach.

    Key insight: The most recent unmatched opening bracket must be matched
    first (LIFO property). A stack naturally maintains this ordering.

    We use a hash map to pair closing brackets with their opening counterparts,
    making the matching check O(1).
    """

    def isValid(self, s: str) -> bool:
        # Map each closing bracket to its corresponding opening bracket
        bracket_pairs = {
            ')': '(',
            ']': '[',
            '}': '{',
        }

        # Stack to track unmatched opening brackets
        stack = []

        for char in s:
            if char in bracket_pairs:
                # Closing bracket: check if it matches the most recent opening
                if not stack or stack[-1] != bracket_pairs[char]:
                    return False
                stack.pop()
            else:
                # Opening bracket: push onto stack
                stack.append(char)

        # Valid only if all opening brackets have been matched
        return len(stack) == 0


# ============================================================================
# Solution 2: Iterative Replacement
# Time: O(n²), Space: O(n)
#   - Repeatedly remove matched pairs "()", "[]", "{}"
#   - Valid if string becomes empty
#   - Simple but inefficient for large inputs
# ============================================================================
class SolutionReplace:
    """
    Iterative replacement approach - intuitive but inefficient.

    Repeatedly remove adjacent matched pairs until no more can be removed.
    If the string becomes empty, it was valid.

    This approach is O(n²) because each replacement can take O(n) and
    we might need O(n) replacements.
    """

    def isValid(self, s: str) -> bool:
        # Keep replacing matched pairs until no changes occur
        while '()' in s or '[]' in s or '{}' in s:
            s = s.replace('()', '').replace('[]', '').replace('{}', '')

        # Valid if all brackets have been matched and removed
        return s == ''


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: s (JSON string with quotes)

    Example:
        "()"
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')

    # Parse JSON string input
    s = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.isValid(s)

    # Output as lowercase boolean (JSON format)
    print(json.dumps(result))


if __name__ == "__main__":
    solve()
