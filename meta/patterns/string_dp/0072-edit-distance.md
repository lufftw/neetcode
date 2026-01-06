# 72. Edit Distance

## Problem Link
https://leetcode.com/problems/edit-distance/

## Difficulty
Medium

## Tags
- String
- Dynamic Programming

## Pattern
String DP - Edit Distance (Levenshtein Distance)

## API Kernel
`StringDP`

## Problem Summary
Given two strings `word1` and `word2`, return the minimum number of operations required to convert `word1` to `word2`. You can perform three operations: insert a character, delete a character, or replace a character.

## Key Insight

Edit distance has optimal substructure with three operations:
- **Insert**: `dp[i][j] = dp[i][j-1] + 1` (insert `word2[j-1]` at end of `word1[0:i]`)
- **Delete**: `dp[i][j] = dp[i-1][j] + 1` (delete `word1[i-1]`)
- **Replace**: `dp[i][j] = dp[i-1][j-1] + 1` (replace `word1[i-1]` with `word2[j-1]`)

If characters match, no operation needed: `dp[i][j] = dp[i-1][j-1]`.

## Template Mapping

```python
def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases: transform to/from empty string
    for i in range(m + 1):
        dp[i][0] = i  # Delete all characters
    for j in range(n + 1):
        dp[0][j] = j  # Insert all characters

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]  # No operation
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j-1],  # Replace
                    dp[i-1][j],    # Delete
                    dp[i][j-1]     # Insert
                )

    return dp[m][n]
```

## Complexity
- Time: O(m * n)
- Space: O(m * n), can be optimized to O(min(m, n))

## Why This Problem Second?

Edit Distance builds on LCS:
1. Same 2D state structure
2. Adds meaningful base cases (not just 0)
3. Introduces operation counting instead of length
4. Three transitions instead of two

## Common Mistakes

1. **Forgetting base cases** - Empty string requires `i` deletions or `j` insertions
2. **Wrong transition direction** - Insert adds to `word1`, so look at `dp[i][j-1]`
3. **Not checking equality first** - Always check if characters match before operations

## Related Problems
- LC 583: Delete Operation for Two Strings (Edit distance with only deletes)
- LC 712: Minimum ASCII Delete Sum (Edit distance with ASCII cost)
- LC 161: One Edit Distance (Special case)
