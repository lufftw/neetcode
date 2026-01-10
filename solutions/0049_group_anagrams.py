"""
Problem: Group Anagrams
Link: https://leetcode.com/problems/group-anagrams/

Given an array of strings strs, group the anagrams together.
You can return the answer in any order.

An Anagram is a word or phrase formed by rearranging the letters of a different
word or phrase, typically using all the original letters exactly once.

Example 1:
    Input: strs = ["eat","tea","tan","ate","nat","bat"]
    Output: [["bat"],["nat","tan"],["ate","eat","tea"]]

Example 2:
    Input: strs = [""]
    Output: [[""]]

Example 3:
    Input: strs = ["a"]
    Output: [["a"]]

Constraints:
- 1 <= strs.length <= 10^4
- 0 <= strs[i].length <= 100
- strs[i] consists of lowercase English letters.

Topics: Array, Hash Table, String, Sorting
"""
import json
from typing import List, Dict, Tuple
from collections import defaultdict
from _runner import get_solver


# ============================================================================
# JUDGE_FUNC - Groups can be in any order, words within groups can be in any order
# ============================================================================
def judge(actual: List[List[str]], expected: List[List[str]], input_data: str) -> bool:
    """
    Custom validation for Group Anagrams.

    Groups can appear in any order, and words within each group can be in any order.
    We normalize by sorting each group and then sorting the list of groups.
    """
    if len(actual) != len(expected):
        return False

    # Normalize: sort each group, then sort the list of groups
    def normalize(groups: List[List[str]]) -> List[Tuple[str, ...]]:
        return sorted(tuple(sorted(group)) for group in groups)

    return normalize(actual) == normalize(expected)


JUDGE_FUNC = judge


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionSortedKey",
        "method": "groupAnagrams",
        "complexity": "O(n * k log k) time, O(n * k) space",
        "description": "Sorted string as hash key",
    },
    "sorted": {
        "class": "SolutionSortedKey",
        "method": "groupAnagrams",
        "complexity": "O(n * k log k) time, O(n * k) space",
        "description": "Sorted string as hash key",
    },
    "count": {
        "class": "SolutionCountKey",
        "method": "groupAnagrams",
        "complexity": "O(n * k) time, O(n * k) space",
        "description": "Character count tuple as hash key",
    },
}


# ============================================================================
# Solution 1: Sorted String as Key
# Time: O(n * k log k), Space: O(n * k)
#   - n = number of strings, k = max length of a string
#   - Sorting each string takes O(k log k)
#   - Hash map stores all strings: O(n * k) space
# ============================================================================
class SolutionSortedKey:
    """
    Use sorted string as hash key.

    Key insight: All anagrams, when sorted, produce the same string.
    For example, "eat", "tea", "ate" all sort to "aet".

    We use a hash map where:
    - Key: sorted version of the string
    - Value: list of original strings that sort to this key
    """

    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # Map sorted string -> list of anagrams
        anagram_groups: Dict[str, List[str]] = defaultdict(list)

        for s in strs:
            # Sort characters to get the canonical form
            key = ''.join(sorted(s))
            anagram_groups[key].append(s)

        return list(anagram_groups.values())


# ============================================================================
# Solution 2: Character Count as Key
# Time: O(n * k), Space: O(n * k)
#   - n = number of strings, k = max length of a string
#   - Counting characters is O(k), no sorting needed
#   - Theoretically faster for long strings
# ============================================================================
class SolutionCountKey:
    """
    Use character count tuple as hash key.

    Key insight: Instead of sorting, we count the frequency of each character.
    Two strings are anagrams if and only if they have the same character counts.

    We represent the count as a tuple of 26 integers (for a-z), which is hashable.
    This avoids the O(k log k) sorting cost.
    """

    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # Map character count tuple -> list of anagrams
        anagram_groups: Dict[Tuple[int, ...], List[str]] = defaultdict(list)

        for s in strs:
            # Count frequency of each character
            count = [0] * 26
            for char in s:
                count[ord(char) - ord('a')] += 1

            # Use tuple as hashable key
            key = tuple(count)
            anagram_groups[key].append(s)

        return list(anagram_groups.values())


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: strs as JSON array of strings

    Example:
        ["eat","tea","tan","ate","nat","bat"]
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')

    # Parse JSON array
    strs = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.groupAnagrams(strs)

    # Output as JSON 2D array
    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
