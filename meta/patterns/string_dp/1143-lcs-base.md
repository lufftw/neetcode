## Base Template: Longest Common Subsequence (LeetCode 1143)

> **Problem**: Given two strings `text1` and `text2`, return the length of their longest common subsequence.
> **Invariant**: `dp[i][j]` = length of LCS for `text1[0:i]` and `text2[0:j]`.
> **Role**: BASE TEMPLATE for `StringDP` API Kernel.

### Why This Is The Base Template

LCS is the purest form of String DP:
- **No modification operations**: Just match or skip
- **Two clear choices**: Match (diagonal) or skip one string (up/left)
- **Maximum objective**: Maximize common length

Every other String DP problem builds on this foundation by adding operations (edit distance) or constraints (regex).

### State Transition Logic

```
If text1[i-1] == text2[j-1]:
    dp[i][j] = dp[i-1][j-1] + 1     // Match: extend LCS by 1
Else:
    dp[i][j] = max(dp[i-1][j],      // Skip char in text1
                   dp[i][j-1])       // Skip char in text2
```

### Implementation

```python
class SolutionLCS:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        """
        Find the longest common subsequence of two strings.

        Algorithm:
        - Build 2D DP table where dp[i][j] = LCS length for text1[0:i], text2[0:j]
        - When characters match: extend LCS from diagonal
        - When they don't: take best of skipping either character

        Time: O(m * n) where m, n are string lengths
        Space: O(m * n), can be optimized to O(min(m, n))
        """
        string_length_1, string_length_2 = len(text1), len(text2)

        # dp[i][j] = LCS length for text1[0:i] and text2[0:j]
        # Extra row/column for empty string base cases
        lcs_table: list[list[int]] = [
            [0] * (string_length_2 + 1)
            for _ in range(string_length_1 + 1)
        ]

        # Base case: LCS with empty string is 0 (already initialized)

        # Fill table: compare each character pair
        for idx_1 in range(1, string_length_1 + 1):
            for idx_2 in range(1, string_length_2 + 1):
                char_1 = text1[idx_1 - 1]
                char_2 = text2[idx_2 - 1]

                if char_1 == char_2:
                    # Characters match: extend LCS from previous diagonal
                    lcs_table[idx_1][idx_2] = lcs_table[idx_1 - 1][idx_2 - 1] + 1
                else:
                    # No match: take best of skipping either character
                    skip_from_text1 = lcs_table[idx_1 - 1][idx_2]
                    skip_from_text2 = lcs_table[idx_1][idx_2 - 1]
                    lcs_table[idx_1][idx_2] = max(skip_from_text1, skip_from_text2)

        return lcs_table[string_length_1][string_length_2]
```

### Space-Optimized Implementation

```python
class SolutionLCSOptimized:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        """
        Space-optimized LCS using two rows instead of full table.

        Key insight: Each cell only depends on:
        - Previous row, same column (up)
        - Same row, previous column (left)
        - Previous row, previous column (diagonal)

        Time: O(m * n)
        Space: O(min(m, n))
        """
        # Ensure text2 is the shorter string for space optimization
        if len(text1) < len(text2):
            text1, text2 = text2, text1

        string_length_2 = len(text2)

        # Only need previous row and current row
        previous_row: list[int] = [0] * (string_length_2 + 1)
        current_row: list[int] = [0] * (string_length_2 + 1)

        for idx_1, char_1 in enumerate(text1, 1):
            for idx_2, char_2 in enumerate(text2, 1):
                if char_1 == char_2:
                    # Match: extend from diagonal (previous row, previous column)
                    current_row[idx_2] = previous_row[idx_2 - 1] + 1
                else:
                    # No match: max of up (previous row) and left (current row)
                    current_row[idx_2] = max(previous_row[idx_2], current_row[idx_2 - 1])

            # Swap rows for next iteration
            previous_row, current_row = current_row, previous_row

        return previous_row[string_length_2]
```

### Trace Example

```
text1 = "abcde", text2 = "ace"

DP Table:
        ""   a    c    e
    ┌────┬────┬────┬────┐
 "" │ 0  │ 0  │ 0  │ 0  │
    ├────┼────┼────┼────┤
 a  │ 0  │ 1  │ 1  │ 1  │  ← 'a' matches
    ├────┼────┼────┼────┤
 b  │ 0  │ 1  │ 1  │ 1  │  ← 'b' doesn't match, carry max
    ├────┼────┼────┼────┤
 c  │ 0  │ 1  │ 2  │ 2  │  ← 'c' matches
    ├────┼────┼────┼────┤
 d  │ 0  │ 1  │ 2  │ 2  │  ← 'd' doesn't match
    ├────┼────┼────┼────┤
 e  │ 0  │ 1  │ 2  │ 3  │  ← 'e' matches
    └────┴────┴────┴────┘

Answer: dp[5][3] = 3 (LCS is "ace")
```

### Key Insights

1. **Subsequence vs Substring**: Subsequence allows skipping; substring must be contiguous
2. **Optimal Substructure**: LCS of two strings depends on LCS of their prefixes
3. **No Greedy Solution**: Must consider all possibilities via DP
4. **Reconstruction**: Can trace back through table to find actual LCS string


