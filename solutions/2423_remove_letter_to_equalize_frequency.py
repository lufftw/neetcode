"""
Problem: Remove Letter To Equalize Frequency
Link: https://leetcode.com/problems/remove-letter-to-equalize-frequency/

Remove exactly one letter so that all remaining letters have equal frequency.
Return true if possible, false otherwise.

Constraints:
- 2 <= word.length <= 100
- word consists of lowercase English letters only.

Topics: Hash Table, String, Counting
"""
from collections import Counter
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "equalFrequency",
        "complexity": "O(26n) time, O(26) space",
        "description": "Try removing each character and check if frequencies are equal",
    },
}


# JUDGE_FUNC for generated tests
def _reference(word: str) -> bool:
    from collections import Counter
    freq = Counter(word)
    for char in freq:
        freq[char] -= 1
        non_zero = [f for f in freq.values() if f > 0]
        if len(non_zero) == 0 or len(set(non_zero)) == 1:
            return True
        freq[char] += 1
    return False


def judge(actual, expected, input_data: str) -> bool:
    import json
    word = json.loads(input_data.strip())
    # Parse actual if it's a string (JSON format from stdout)
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(word)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Brute Force with Frequency Check
# Time: O(26n), Space: O(26)
#   - For each unique character, try removing one occurrence
#   - Check if remaining frequencies are all equal
#   - At most 26 characters to try, each check is O(26)
# ============================================================================
class Solution:
    # Key insight: only need to try removing one occurrence of each unique char
    # If removing char c works, it doesn't matter which occurrence we remove
    #
    # After removal, all non-zero frequencies must be equal:
    #   - Count frequencies of all characters
    #   - For each char, decrement its count by 1
    #   - Check if all non-zero counts are equal

    def equalFrequency(self, word: str) -> bool:
        freq = Counter(word)

        # Try removing one occurrence of each unique character
        for char in freq:
            # Temporarily remove one occurrence
            freq[char] -= 1

            # Get all non-zero frequencies
            non_zero_freqs = [f for f in freq.values() if f > 0]

            # Check if all equal (or empty if all removed)
            if len(non_zero_freqs) == 0 or len(set(non_zero_freqs)) == 1:
                return True

            # Restore the count
            freq[char] += 1

        return False


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: word (JSON string with quotes)

    Example:
        "abcc"
        -> true
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')
    word = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.equalFrequency(word)

    # Output lowercase boolean for JSON compatibility
    print(json.dumps(result))


if __name__ == "__main__":
    solve()
