"""
Problem: Generate Parentheses
Link: https://leetcode.com/problems/generate-parentheses/

Given n pairs of parentheses, write a function to generate all combinations
of well-formed parentheses.

Example 1:
    Input: n = 3
    Output: ["((()))","(()())","(())()","()(())","()()()"]

Example 2:
    Input: n = 1
    Output: ["()"]

Constraints:
- 1 <= n <= 8

Topics: String, Dynamic Programming, Backtracking
"""
import json
from typing import List
from _runner import get_solver


# ============================================================================
# COMPARE_MODE - Order doesn't matter for this problem
# ============================================================================
COMPARE_MODE = "sorted"


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionBacktrack",
        "method": "generateParenthesis",
        "complexity": "O(4^n / √n) time, O(n) space",
        "description": "Backtracking with open/close counters",
    },
    "backtrack": {
        "class": "SolutionBacktrack",
        "method": "generateParenthesis",
        "complexity": "O(4^n / √n) time, O(n) space",
        "description": "Backtracking with open/close counters",
    },
    "dp": {
        "class": "SolutionDP",
        "method": "generateParenthesis",
        "complexity": "O(4^n / √n) time, O(4^n / √n) space",
        "description": "Dynamic programming - build from smaller solutions",
    },
}


# ============================================================================
# Solution 1: Backtracking
# Time: O(4^n / √n), Space: O(n) excluding output
#   - Number of valid combinations is the n-th Catalan number
#   - Catalan(n) = (2n choose n) / (n+1) ≈ 4^n / (n^1.5 * √π)
# ============================================================================
class SolutionBacktrack:
    """
    Backtracking approach - the canonical interview solution.

    Key insight: At any point, we can add '(' if we haven't used all n opens,
    and we can add ')' if we have more opens than closes (to keep it balanced).

    The constraints ensure we only generate valid combinations:
    1. open_count < n: can add '('
    2. close_count < open_count: can add ')'
    """

    def generateParenthesis(self, n: int) -> List[str]:
        results: List[str] = []

        def backtrack(path: List[str], open_count: int, close_count: int) -> None:
            """
            Generate valid combinations recursively.

            Args:
                path: Current partial combination
                open_count: Number of '(' used so far
                close_count: Number of ')' used so far
            """
            # Base case: used all n pairs
            if len(path) == 2 * n:
                results.append(''.join(path))
                return

            # Choice 1: Add '(' if we haven't used all n opens
            if open_count < n:
                path.append('(')
                backtrack(path, open_count + 1, close_count)
                path.pop()

            # Choice 2: Add ')' if it won't make the string invalid
            # We can only close if there are unclosed opens
            if close_count < open_count:
                path.append(')')
                backtrack(path, open_count, close_count + 1)
                path.pop()

        backtrack([], 0, 0)
        return results


# ============================================================================
# Solution 2: Dynamic Programming
# Time: O(4^n / √n), Space: O(4^n / √n)
#   - Build solutions bottom-up using recurrence
#   - dp[n] = all valid strings with n pairs
# ============================================================================
class SolutionDP:
    """
    Dynamic programming approach.

    Key insight: A valid string with n pairs can be written as:
        "(" + (valid string with i pairs) + ")" + (valid string with n-1-i pairs)

    Where i ranges from 0 to n-1. This gives us a recurrence:
        dp[n] = union of "(" + dp[i] + ")" + dp[n-1-i] for i in 0..n-1
    """

    def generateParenthesis(self, n: int) -> List[str]:
        # dp[i] = list of valid strings with i pairs
        dp: List[List[str]] = [[] for _ in range(n + 1)]

        # Base case: empty string is the only valid string with 0 pairs
        dp[0] = ['']

        # Build up from 1 to n pairs
        for pairs in range(1, n + 1):
            for i in range(pairs):
                # j = pairs - 1 - i is the remaining pairs for the right part
                j = pairs - 1 - i

                # Combine: "(" + dp[i] + ")" + dp[j]
                for left in dp[i]:
                    for right in dp[j]:
                        dp[pairs].append('(' + left + ')' + right)

        return dp[n]


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: n (integer)

    Example:
        3
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')

    n = int(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.generateParenthesis(n)

    # Output as JSON array
    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
