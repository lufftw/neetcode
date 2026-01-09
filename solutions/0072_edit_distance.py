"""
Problem: Edit Distance
Link: https://leetcode.com/problems/edit-distance/

Given two strings word1 and word2, return the minimum number of operations
required to convert word1 to word2.

You have the following three operations permitted on a word:
- Insert a character
- Delete a character
- Replace a character

Example 1:
    Input: word1 = "horse", word2 = "ros"
    Output: 3
    Explanation:
    horse -> rorse (replace 'h' with 'r')
    rorse -> rose (remove 'r')
    rose -> ros (remove 'e')

Example 2:
    Input: word1 = "intention", word2 = "execution"
    Output: 5
    Explanation:
    intention -> inention (remove 't')
    inention -> enention (replace 'i' with 'e')
    enention -> exention (replace 'n' with 'x')
    exention -> exection (replace 'n' with 'c')
    exection -> execution (insert 'u')

Constraints:
- 0 <= word1.length, word2.length <= 500
- word1 and word2 consist of lowercase English letters.

Topics: String, Dynamic Programming
"""
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "minDistance",
        "complexity": "O(m*n) time, O(m*n) space",
        "description": "2D DP with dp[i][j] = min edits for word1[0:i] to word2[0:j]",
    },
    "space_optimized": {
        "class": "SolutionSpaceOptimized",
        "method": "minDistance",
        "complexity": "O(m*n) time, O(min(m,n)) space",
        "description": "Space-optimized using only two rows",
    },
}


# ============================================================================
# Solution 1: 2D DP
# Time: O(m*n), Space: O(m*n)
#   - Classic dual-sequence DP (Levenshtein distance)
#   - Three operations: replace, delete, insert
# ============================================================================
class Solution:
    # State: edit_cost[i][j] = min edits to convert word1[0:i] to word2[0:j]
    # Base case: edit_cost[i][0] = i (delete all), edit_cost[0][j] = j (insert all)
    # Transition: if match, edit_cost[i][j] = edit_cost[i-1][j-1]
    #             else, edit_cost[i][j] = 1 + min(replace, delete, insert)

    def minDistance(self, word1: str, word2: str) -> int:
        """
        Find minimum edit operations to transform word1 to word2.

        Core insight: Classic Levenshtein distance. If characters match, no edit
        needed (take diagonal). If mismatch, take 1 + min(replace, delete, insert).
        Base cases: converting to/from empty string requires all inserts/deletes.

        Invariant: edit_cost[i][j] = min edits to convert word1[0:i] to word2[0:j].

        Args:
            word1: Source string
            word2: Target string

        Returns:
            Minimum number of edit operations
        """
        source_len, target_len = len(word1), len(word2)

        edit_cost: list[list[int]] = [
            [0] * (target_len + 1) for _ in range(source_len + 1)
        ]

        # Base cases: converting to/from empty string
        for i in range(source_len + 1):
            edit_cost[i][0] = i  # Delete all characters from word1
        for j in range(target_len + 1):
            edit_cost[0][j] = j  # Insert all characters of word2

        for i in range(1, source_len + 1):
            for j in range(1, target_len + 1):
                if word1[i - 1] == word2[j - 1]:
                    # Characters match: no operation needed
                    edit_cost[i][j] = edit_cost[i - 1][j - 1]
                else:
                    # Mismatch: take minimum of three operations
                    replace_cost = edit_cost[i - 1][j - 1]
                    delete_cost = edit_cost[i - 1][j]
                    insert_cost = edit_cost[i][j - 1]
                    edit_cost[i][j] = 1 + min(replace_cost, delete_cost, insert_cost)

        return edit_cost[source_len][target_len]


# ============================================================================
# Solution 2: Space-Optimized
# Time: O(m*n), Space: O(min(m,n))
#   - Only need previous row to compute current row
#   - Swap shorter string to column dimension for minimal space
# ============================================================================
class SolutionSpaceOptimized:
    def minDistance(self, word1: str, word2: str) -> int:
        # Make word2 the shorter one for better space
        if len(word1) < len(word2):
            word1, word2 = word2, word1

        source_len, target_len = len(word1), len(word2)
        previous_row: list[int] = list(range(target_len + 1))
        current_row: list[int] = [0] * (target_len + 1)

        for i in range(1, source_len + 1):
            current_row[0] = i  # Base case: i deletions
            for j in range(1, target_len + 1):
                if word1[i - 1] == word2[j - 1]:
                    current_row[j] = previous_row[j - 1]
                else:
                    current_row[j] = 1 + min(
                        previous_row[j - 1],  # replace
                        previous_row[j],       # delete
                        current_row[j - 1]     # insert
                    )
            previous_row, current_row = current_row, previous_row

        return previous_row[target_len]


def solve():
    """
    Input format:
    Line 1: word1 (string)
    Line 2: word2 (string)
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')

    word1 = json.loads(lines[0])
    word2 = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.minDistance(word1, word2)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
