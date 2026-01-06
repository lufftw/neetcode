## Decision Tree

```
Start: Two strings to compare/transform?
            │
            ▼
    ┌───────────────────┐
    │ What's the goal?  │
    └───────────────────┘
            │
    ┌───────┼───────┬───────────┐
    ▼       ▼       ▼           ▼
Find      Count   Match      Transform
common    edits   pattern    one string
chars               │
    │       │       │           │
    ▼       ▼       ▼           ▼
  LCS    Edit     Regex      Edit
         Dist.   Matching   Distance
```

## Pattern Selection Guide

### Use LCS (LC 1143) when:
- Finding common elements between two sequences
- Subsequence (not substring) problems
- Building longest/shortest common supersequence

### Use Edit Distance (LC 72) when:
- Converting one string to another
- Counting minimum operations
- Operations: insert, delete, replace

### Use Palindrome DP (LC 516) when:
- Finding palindromic subsequences
- Single string problems
- Can reduce to LCS with reversed string

### Use Regex Matching (LC 10) when:
- Pattern has wildcards (`.`, `*`)
- Boolean matching result
- Complex pattern rules

## Problem Type Recognition

| Keywords/Clues | Pattern |
|----------------|---------|
| "longest common subsequence" | LCS |
| "minimum operations to convert" | Edit Distance |
| "palindrome subsequence" | LCS with reverse |
| "pattern matching with wildcards" | Regex/Wildcard DP |
| "delete operations for two strings" | LCS-based |

## Complexity Guide

| Pattern | Time | Space | Space-Optimized |
|---------|------|-------|-----------------|
| LCS | O(mn) | O(mn) | O(min(m,n)) |
| Edit Distance | O(mn) | O(mn) | O(min(m,n)) |
| Palindrome | O(n²) | O(n²) | O(n) |
| Regex | O(mn) | O(mn) | O(n) |
