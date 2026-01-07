## Pattern Comparison Table

| Problem | State `dp[i][j]` | Base Case | Match Transition | Mismatch Transition | Objective |
|---------|------------------|-----------|------------------|---------------------|-----------|
| **LCS** | LCS length for s[0:i], t[0:j] | 0 | `dp[i-1][j-1] + 1` | `max(dp[i-1][j], dp[i][j-1])` | Maximize |
| **Edit Distance** | Min ops for s[0:i] → t[0:j] | i or j | `dp[i-1][j-1]` | `1 + min(diagonal, up, left)` | Minimize |
| **Palindrome Subseq** | LPS length for s[i:j+1] | 1 (single char) | `dp[i+1][j-1] + 2` | `max(dp[i+1][j], dp[i][j-1])` | Maximize |
| **Regex Match** | s[0:i] matches p[0:j]? | True for empty | `dp[i-1][j-1]` | False (or `*` logic) | Boolean |
| **Wildcard Match** | s[0:i] matches p[0:j]? | True for empty | `dp[i-1][j-1]` | False (or `*` logic) | Boolean |

### Transition Direction Summary

```
LCS / Edit Distance / Regex / Wildcard:
    ┌─────┬─────┐
    │ ↖   │  ←  │
    ├─────┼─────┤
    │  ↑  │ cur │
    └─────┴─────┘

↖ = diagonal (match/substitute)
← = horizontal (insert / skip in t)
↑ = vertical (delete / skip in s)

Palindrome Subsequence (Interval DP):
    ┌─────────────────┐
    │   dp[i+1][j-1]  │  (inner interval)
    ├─────┬─────┬─────┤
    │     │     │     │
    └─────┴─────┴─────┘
       ↑           ↑
   dp[i+1][j]   dp[i][j-1]
```

### Complexity Comparison

| Problem | Time | Space | Space-Optimized |
|---------|------|-------|-----------------|
| LCS | O(mn) | O(mn) | O(min(m,n)) |
| Edit Distance | O(mn) | O(mn) | O(n) |
| Palindrome Subseq | O(n²) | O(n²) | O(n) |
| Regex Match | O(mn) | O(mn) | O(n) |
| Wildcard Match | O(mn) | O(mn) | O(n) or O(1)* |

*Wildcard can achieve O(1) space with greedy + backtracking.

### Special Character Handling

| Char | Regex Meaning | Wildcard Meaning |
|------|---------------|------------------|
| `.` | Any single char | N/A |
| `?` | N/A | Any single char |
| `*` | Zero+ of PRECEDING char | Any sequence (including empty) |


