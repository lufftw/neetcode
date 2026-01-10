"""
Problem: Number of Valid Words in a Sentence
Link: https://leetcode.com/problems/number-of-valid-words-in-a-sentence/

A sentence consists of lowercase letters ('a' to 'z'), digits ('0' to '9'),
hyphens ('-'), punctuation marks ('!', '.', and ','), and spaces (' ') only.

Each sentence can be broken down into one or more tokens separated by one or
more spaces ' '.

A token is a valid word if ALL of the following are true:
1. It only contains lowercase letters, hyphens, and/or punctuation (NO digits).
2. There is at most one hyphen '-'. If present, it must be surrounded by
   lowercase characters ("a-b" is valid, but "-ab" and "ab-" are not valid).
3. There is at most one punctuation mark. If present, it must be at the END
   of the token ("ab,", "cd!", and "." are valid, but "a!b" and "c.," are not).

Examples of valid words include "a-b.", "afad", "ba-c", "a!", and "!".

Given a string sentence, return the number of valid words in sentence.

Example 1:
    Input: sentence = "cat and dog"
    Output: 3
    Explanation: The valid words are "cat", "and", and "dog".

Example 2:
    Input: sentence = "!this 1-s b8d!"
    Output: 0
    Explanation: "!this" starts with punctuation (invalid position).
                 "1-s" and "b8d" contain digits.

Example 3:
    Input: sentence = "alice and bob are playing stone-game10"
    Output: 5
    Explanation: "stone-game10" contains digits, so only 5 words are valid.

Constraints:
- 1 <= sentence.length <= 1000
- sentence only contains lowercase English letters, digits, ' ', '-', '!', '.', and ','

Topics: String
"""
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "countValidWords",
        "complexity": "O(n) time, O(n) space",
        "description": "Linear scan with validation rules",
    },
}


# ============================================================================
# Solution: Linear Scan with Rule Validation
# Time: O(n), Space: O(n) where n = length of sentence
#
# For each token (space-separated), we validate:
# 1. No digits allowed
# 2. At most one hyphen, and if present, must be surrounded by letters
# 3. At most one punctuation mark, and if present, must be at the end
#
# Edge cases:
# - Empty tokens from multiple spaces -> skip
# - Single punctuation like "!" is valid
# - Hyphen at start/end is invalid
# - Punctuation not at end is invalid
# ============================================================================
class Solution:
    def countValidWords(self, sentence: str) -> int:
        """
        Count valid words in the sentence according to the rules.

        A word is valid if:
        - No digits
        - At most one hyphen, surrounded by lowercase letters
        - At most one punctuation mark, at the end

        Args:
            sentence: Input sentence with tokens separated by spaces

        Returns:
            Number of valid words
        """
        def is_valid(token: str) -> bool:
            """
            Validate a single token according to the rules.
            """
            if not token:
                return False

            n = len(token)
            hyphen_count = 0
            punctuation_count = 0

            for i, ch in enumerate(token):
                if ch.isdigit():
                    # Rule 1: No digits allowed
                    return False

                elif ch == '-':
                    # Rule 2: Hyphen rules
                    hyphen_count += 1
                    if hyphen_count > 1:
                        return False  # At most one hyphen

                    # Must be surrounded by lowercase letters
                    # Not at start, not at end, neighbors are letters
                    if i == 0 or i == n - 1:
                        return False
                    if not token[i - 1].isalpha() or not token[i + 1].isalpha():
                        return False

                elif ch in '!.,':
                    # Rule 3: Punctuation rules
                    punctuation_count += 1
                    if punctuation_count > 1:
                        return False  # At most one punctuation

                    # Must be at the end of the token
                    if i != n - 1:
                        return False

                elif ch.isalpha():
                    # Lowercase letters are always valid
                    pass

                else:
                    # Any other character is invalid
                    return False

            return True

        # Split by spaces and count valid tokens
        tokens = sentence.split()
        return sum(1 for token in tokens if is_valid(token))


def solve():
    """
    Input format:
    Line 1: sentence (JSON string)
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')

    sentence = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.countValidWords(sentence)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
