"""
Problem: Remove Duplicate Letters
Link: https://leetcode.com/problems/remove-duplicate-letters/

Given a string s, remove duplicate letters so that every letter appears once and only once. You must make sure your result is the smallest in lexicographical order among all possible results.

Example 1:
    Input: s = "bcabc"
    Output: "abc"

Example 2:
    Input: s = "cbacdcbc"
    Output: "acdb"

Constraints:
- 1 <= s.length <= 10^4
- s consists of lowercase English letters.

Topics: String, Stack, Greedy, Monotonic Stack

Hint 1: Greedily try to add one missing character. How to check if adding some character will not cause problems ? Use bit-masks to check whether you will be able to complete the sub-sequence if you add the character at some index i.

Note: This question is the same as 1081: https://leetcode.com/problems/smallest-subsequence-of-distinct-characters/
"""


from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionGreedyStack",
        "method": "removeDuplicateLetters",
        "complexity": "O(n) time, O(26) = O(1) space",
        "description": "Monotonic stack with last occurrence tracking",
    },
}


# ============================================================================
# Solution 1: Greedy Monotonic Stack with Constraints
# Time: O(n), Space: O(26) = O(1)
#   - Track last occurrence of each character for safe removal decisions
#   - Track which characters are already in the result (in_stack set)
#   - Maintain lexicographically smallest result via monotonic increasing stack
#   - Only pop if: (1) stack top > current, (2) stack top appears later
#
# Key Insight: Like Remove K Digits, but with the constraint that each
# character must appear exactly once. We can only pop a character if it
# appears again later in the string (ensuring we can add it back).
#
# Greedy Strategy:
#   1. Skip if character already in result (maintain uniqueness)
#   2. Pop larger characters that appear later (improve lexicographic order)
#   3. Add current character (extend result)
# ============================================================================
class SolutionGreedyStack:
    def removeDuplicateLetters(self, s: str) -> str:
        # Precompute last occurrence index for each character
        last_occurrence: dict[str, int] = {char: idx for idx, char in enumerate(s)}

        result_stack: list[str] = []
        in_result: set[str] = set()  # O(1) membership check

        for current_idx, char in enumerate(s):
            # Skip if already in result (each char appears exactly once)
            if char in in_result:
                continue

            # Pop characters that are:
            # 1. Lexicographically greater than current (would make result larger)
            # 2. Appear later in string (safe to remove, we can add them back)
            while (
                result_stack
                and result_stack[-1] > char
                and last_occurrence[result_stack[-1]] > current_idx
            ):
                removed_char = result_stack.pop()
                in_result.remove(removed_char)

            # Add current character to result
            result_stack.append(char)
            in_result.add(char)

        return "".join(result_stack)


def solve():
    """
    Input format (JSON literal, one per line):
        s: str

    Output: str
    """
    import sys
    import json

    data = sys.stdin.read().strip().split('\n')

    s = json.loads(data[0].strip()) if data[0].strip().startswith('"') else data[0].strip()

    solver = get_solver(SOLUTIONS)
    result = solver.removeDuplicateLetters(s)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
