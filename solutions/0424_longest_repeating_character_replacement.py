# solutions/0424_longest_repeating_character_replacement.py
"""
Problem 0424 - Longest Repeating Character Replacement

Given a string s and an integer k, you can choose any character and
change it to any other uppercase English character at most k times.

Return the length of the longest substring containing the same letter
you can get after performing at most k operations.

LeetCode Constraints:
- 1 <= s.length <= 10^5
- s consists of only uppercase English letters
- 0 <= k <= s.length

Key Insight:
For any substring, the minimum changes needed to make all characters
the same is (length - maxFrequency). If this <= k, the substring is valid.

Use sliding window: expand right, and if window becomes invalid
(length - maxFreq > k), shrink from left.

Optimization: We don't need to decrease maxFreq when shrinking because
we're looking for the MAXIMUM length. If maxFreq was higher before,
we already found a valid window of that size.

Solution Approaches:
1. Sliding window with maxFreq tracking: O(n) time, O(26) space
2. Binary search on length: O(n log n) time, O(26) space
"""
from typing import List
from collections import Counter
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionSlidingWindow",
        "method": "characterReplacement",
        "complexity": "O(n) time, O(26) space",
        "description": "Sliding window with character frequency tracking",
    },
    "binary_search": {
        "class": "SolutionBinarySearch",
        "method": "characterReplacement",
        "complexity": "O(n log n) time, O(26) space",
        "description": "Binary search on answer length",
    },
}


class SolutionSlidingWindow:
    """
    Sliding window approach with frequency tracking.

    Maintain a window [left, right] and track character frequencies.
    The window is valid if (window_size - max_frequency) <= k.

    Key optimization: We only update maxFreq when it increases.
    When shrinking the window, we don't decrease maxFreq because:
    - We want the LONGEST valid window
    - If maxFreq was higher before, we already recorded that length
    - A window can only be longer if maxFreq increases again

    This makes the algorithm O(n) instead of O(26n).
    """

    def characterReplacement(self, s: str, k: int) -> int:
        count: Counter = Counter()
        max_freq = 0
        left = 0
        result = 0

        for right in range(len(s)):
            count[s[right]] += 1
            max_freq = max(max_freq, count[s[right]])

            # Window size is (right - left + 1)
            # Characters to change = window_size - max_freq
            while (right - left + 1) - max_freq > k:
                count[s[left]] -= 1
                left += 1
                # Note: We don't update max_freq here - see docstring

            result = max(result, right - left + 1)

        return result


class SolutionBinarySearch:
    """
    Binary search on the answer length.

    Binary search the window size. For each candidate size, check if
    there exists a valid window of that size using a sliding window.

    A window of size len is valid if (len - maxFreq) <= k.

    Less efficient than pure sliding window, but demonstrates
    the "binary search on answer" pattern.
    """

    def characterReplacement(self, s: str, k: int) -> int:
        def canAchieve(length: int) -> bool:
            """Check if a valid window of given length exists."""
            if length == 0:
                return True

            count: Counter = Counter()

            # Initialize window with first 'length' characters
            for i in range(length):
                count[s[i]] += 1

            max_freq = max(count.values())
            if length - max_freq <= k:
                return True

            # Slide the window
            for i in range(length, len(s)):
                count[s[i]] += 1
                count[s[i - length]] -= 1
                if count[s[i - length]] == 0:
                    del count[s[i - length]]

                max_freq = max(count.values())
                if length - max_freq <= k:
                    return True

            return False

        # Binary search on answer
        low, high = 1, len(s)
        result = 0

        while low <= high:
            mid = (low + high) // 2
            if canAchieve(mid):
                result = mid
                low = mid + 1
            else:
                high = mid - 1

        return result


def solve():
    import sys
    import json

    lines = sys.stdin.read().strip().split("\n")

    # Handle both JSON-quoted and raw string
    s = lines[0]
    if s.startswith('"') and s.endswith('"'):
        s = json.loads(s)

    k = int(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.characterReplacement(s, k)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()
