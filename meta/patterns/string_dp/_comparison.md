## Problem Comparison

| Problem | Core Pattern | State `dp[i][j]` | Match Transition | Mismatch Transition |
|---------|-------------|------------------|------------------|---------------------|
| **LC 1143 LCS** | Find longest common | Length of LCS | `dp[i-1][j-1] + 1` | `max(dp[i-1][j], dp[i][j-1])` |
| **LC 72 Edit Distance** | Min operations | Min edits needed | `dp[i-1][j-1]` | `1 + min(3 options)` |
| **LC 516 Palindrome** | LCS with reverse | Length of LPS | Same as LCS | Same as LCS |
| **LC 10 Regex** | Pattern matching | Boolean: matches? | `dp[i-1][j-1]` | `False` (unless `*`) |

## Pattern Evolution

```
LC 1143 LCS (Base)
    │
    │ Add operation counting
    │ Add non-zero base cases
    ↓
LC 72 Edit Distance
    │
    │ Apply to single string
    │ s vs reverse(s)
    ↓
LC 516 Palindrome Subsequence
    │
    │ Add complex pattern matching
    │ Handle . and * wildcards
    ↓
LC 10 Regex Matching
```

## Key Differences

### Base Cases

| Problem | `dp[i][0]` | `dp[0][j]` |
|---------|-----------|-----------|
| LCS | 0 | 0 |
| Edit Distance | `i` | `j` |
| Palindrome | 0 | 0 |
| Regex | `False` | `True` if `p[0:j]` is all `x*` patterns |

### Optimization Potential

| Problem | Space Optimization | Notes |
|---------|-------------------|-------|
| LCS | O(min(m,n)) | Only need previous row |
| Edit Distance | O(min(m,n)) | Only need previous row |
| Palindrome | O(n) | Single row for LCS approach |
| Regex | O(n) | Only need previous row |
