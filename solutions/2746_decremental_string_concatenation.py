"""
Problem: Decremental String Concatenation
Link: https://leetcode.com/problems/decremental-string-concatenation/

Join n strings with optional character merge. If last char of x equals first char of y,
join(x, y) saves 1 character. At each step, can join either way. Minimize final length.

Constraints:
- 1 <= words.length <= 1000
- 1 <= words[i].length <= 50
- Lowercase English letters

Topics: Array, String, DP
"""
from typing import List
from _runner import get_solver
import json
from functools import lru_cache


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "minimizeConcatenatedLength",
        "complexity": "O(n * 26 * 26) time, O(26 * 26) space",
        "description": "DP tracking first/last character of concatenated string",
    },
}


# JUDGE_FUNC for generated tests
def _reference(words: List[str]) -> int:
    """Recursive reference with memoization."""
    n = len(words)

    @lru_cache(maxsize=None)
    def dp(i, first, last):
        """Min length to form string starting with first, ending with last after i words."""
        if i == n:
            return 0

        word = words[i]
        w_first, w_last = word[0], word[-1]
        w_len = len(word)

        # Option 1: append word at the end (str + word)
        save1 = 1 if last == w_first else 0
        opt1 = dp(i + 1, first, w_last) + w_len - save1

        # Option 2: prepend word at the beginning (word + str)
        save2 = 1 if w_last == first else 0
        opt2 = dp(i + 1, w_first, last) + w_len - save2

        return min(opt1, opt2)

    return dp(1, words[0][0], words[0][-1]) + len(words[0])


def judge(actual, expected, input_data: str) -> bool:
    lines = input_data.strip().split('\n')
    words = json.loads(lines[0])
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(words)


JUDGE_FUNC = judge


# ============================================================================
# Solution: DP with First/Last Character Tracking
# Time: O(n * 26 * 26), Space: O(26 * 26)
# ============================================================================
class Solution:
    # Key insight:
    #   - Only first and last character matter for future joins
    #   - State: (index, first_char, last_char) → min length
    #   - At each step, two choices: append or prepend current word
    #
    # Transitions:
    #   - Append word: saves 1 if result's last == word's first
    #   - Prepend word: saves 1 if word's last == result's first

    def minimizeConcatenatedLength(self, words: List[str]) -> int:
        n = len(words)

        @lru_cache(maxsize=None)
        def dp(i, first, last):
            """Min additional length after processing words[i:]."""
            if i == n:
                return 0

            word = words[i]
            w_first, w_last = word[0], word[-1]
            w_len = len(word)

            # Append word at end
            save1 = 1 if last == w_first else 0
            opt1 = dp(i + 1, first, w_last) + w_len - save1

            # Prepend word at beginning
            save2 = 1 if w_last == first else 0
            opt2 = dp(i + 1, w_first, last) + w_len - save2

            return min(opt1, opt2)

        return dp(1, words[0][0], words[0][-1]) + len(words[0])


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: words (JSON array)

    Example:
        ["aa","ab","bc"]
        -> 4
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    words = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.minimizeConcatenatedLength(words)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
