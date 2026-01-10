# solutions/0242_valid_anagram.py
"""
Problem: Valid Anagram
https://leetcode.com/problems/valid-anagram/

Given two strings s and t, return true if t is an anagram of s, and false
otherwise.

An Anagram is a word or phrase formed by rearranging the letters of a
different word or phrase, typically using all the original letters exactly
once.

Constraints:
- 1 <= s.length, t.length <= 5 * 10^4
- s and t consist of lowercase English letters
"""
from typing import List
from collections import Counter
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionCounter",
        "method": "isAnagram",
        "complexity": "O(n) time, O(1) space",
        "description": "Character frequency counter comparison",
    },
    "sorting": {
        "class": "SolutionSorting",
        "method": "isAnagram",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Sort both strings and compare",
    },
}


class SolutionCounter:
    """
    Hash map frequency counting for character comparison.

    Two strings are anagrams if and only if they have identical character
    frequencies. We use Counter (hash map) to count occurrences of each
    character in both strings and compare.

    Space is O(1) because the alphabet is fixed (26 lowercase letters),
    making the counter size bounded regardless of input length.
    """

    def isAnagram(self, s: str, t: str) -> bool:
        # Quick length check - anagrams must have same length
        if len(s) != len(t):
            return False

        # Count character frequencies and compare
        # Counter equality checks both keys and values
        return Counter(s) == Counter(t)


class SolutionSorting:
    """
    Sorting-based approach for anagram verification.

    Anagrams, when sorted, produce identical strings. This approach
    sorts both strings and compares. While conceptually simple, the
    O(n log n) time complexity is worse than the counting approach.

    This method is useful when hash-based solutions aren't available
    or when dealing with Unicode where alphabet size is unbounded.
    """

    def isAnagram(self, s: str, t: str) -> bool:
        # Quick length check
        if len(s) != len(t):
            return False

        # Sort both strings and compare
        return sorted(s) == sorted(t)


def judge(actual, expected, input_data: str) -> bool:
    """
    Validate anagram check using Counter.
    """
    import json

    # Parse actual if string
    if isinstance(actual, str):
        actual = json.loads(actual)

    lines = input_data.strip().split("\n")
    s = json.loads(lines[0])
    t = json.loads(lines[1])

    expected_result = Counter(s) == Counter(t)
    return actual == expected_result


JUDGE_FUNC = judge


def solve():
    import sys
    import json

    lines = sys.stdin.read().strip().split("\n")

    # Parse input: two strings
    s = json.loads(lines[0])
    t = json.loads(lines[1])

    # Get solver and check anagram
    solver = get_solver(SOLUTIONS)
    result = solver.isAnagram(s, t)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
