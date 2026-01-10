"""
Problem: Make Number of Distinct Characters Equal
Link: https://leetcode.com/problems/make-number-of-distinct-characters-equal/

Swap exactly one char from word1 with one char from word2. Return true if both
strings can have the same number of distinct characters after exactly one swap.

Constraints:
- 1 <= word1.length, word2.length <= 10^5
- Lowercase English letters only

Topics: Hash Table, String, Counting
"""
from collections import Counter
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "isItPossible",
        "complexity": "O(n + 26^2) time, O(26) space",
        "description": "Frequency counting with all 26*26 swap pairs",
    },
}


# JUDGE_FUNC for generated tests
def _reference(word1: str, word2: str) -> bool:
    """Reference implementation."""
    freq1, freq2 = Counter(word1), Counter(word2)
    d1, d2 = len(freq1), len(freq2)
    for c1 in freq1:
        for c2 in freq2:
            if c1 == c2:
                if d1 == d2:
                    return True
                continue
            new_d1 = d1 - (1 if freq1[c1] == 1 else 0) + (1 if c2 not in freq1 else 0)
            new_d2 = d2 - (1 if freq2[c2] == 1 else 0) + (1 if c1 not in freq2 else 0)
            if new_d1 == new_d2:
                return True
    return False


def judge(actual, expected, input_data: str) -> bool:
    lines = input_data.strip().split('\n')
    word1 = json.loads(lines[0])
    word2 = json.loads(lines[1])
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(word1, word2)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Try All Character Pairs
# Time: O(n + 26^2), Space: O(26)
# ============================================================================
class Solution:
    # Key insight:
    #   - Only distinct character counts matter, not positions
    #   - Build frequency tables, then try all (c1, c2) pairs
    #   - For each pair, calculate effect on distinct counts:
    #     * word1: loses c1 (distinct-- if last), gains c2 (distinct++ if new)
    #     * word2: loses c2 (distinct-- if last), gains c1 (distinct++ if new)
    #
    # Edge case: if c1 == c2, no change in distinct counts.

    def isItPossible(self, word1: str, word2: str) -> bool:
        freq1 = Counter(word1)
        freq2 = Counter(word2)

        d1 = len(freq1)  # distinct chars in word1
        d2 = len(freq2)  # distinct chars in word2

        # Try all character pairs (c1 from word1, c2 from word2)
        for c1 in freq1:
            for c2 in freq2:
                # Same character: no effect on distinct counts
                if c1 == c2:
                    if d1 == d2:
                        return True
                    continue

                new_d1 = d1
                new_d2 = d2

                # Effect on word1: loses c1, gains c2
                if freq1[c1] == 1:   # last occurrence of c1
                    new_d1 -= 1
                if c2 not in freq1:  # c2 is new to word1
                    new_d1 += 1

                # Effect on word2: loses c2, gains c1
                if freq2[c2] == 1:   # last occurrence of c2
                    new_d2 -= 1
                if c1 not in freq2:  # c1 is new to word2
                    new_d2 += 1

                if new_d1 == new_d2:
                    return True

        return False


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: word1 (JSON string)
        Line 2: word2 (JSON string)

    Example:
        "abcc"
        "aab"
        -> true
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    word1 = json.loads(lines[0])
    word2 = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.isItPossible(word1, word2)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
