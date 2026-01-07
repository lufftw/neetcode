# 664. Strange Printer

## Problem Link
https://leetcode.com/problems/strange-printer/

## Difficulty
Hard

## Tags
- String
- Dynamic Programming

## Pattern
Interval DP - Character Printing

## API Kernel
`IntervalDP`

## Problem Summary
A printer can print a sequence of the same character, and each print covers some substring. Given a string, find the minimum number of turns needed to print it.

## Key Insight

For interval `[i, j]`:
- Base case: print `s[i]` to cover entire interval, then recursively handle rest
- Optimization: if `s[k] == s[i]` for some `k > i`, we can "extend" the first print

When `s[i] == s[j]`:
- `dp[i][j] = dp[i][j-1]` (print s[i] to cover s[j] too)

When `s[i] != s[j]`:
- Try all split points: `dp[i][j] = min(dp[i][k] + dp[k+1][j])`

## Template Mapping

```python
def strangePrinter(s: str) -> int:
    # Remove consecutive duplicates (they don't change answer)
    s = ''.join(c for i, c in enumerate(s) if i == 0 or c != s[i-1])
    n = len(s)

    if n == 0:
        return 0

    # dp[i][j] = min turns to print s[i:j+1]
    dp = [[0] * n for _ in range(n)]

    # Base case: single character needs 1 turn
    for i in range(n):
        dp[i][i] = 1

    # Fill by increasing length
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1

            # Worst case: print s[i] alone, then handle rest
            dp[i][j] = dp[i + 1][j] + 1

            # Optimization: extend s[i]'s print if s[k] == s[i]
            for k in range(i + 1, j + 1):
                if s[k] == s[i]:
                    left = dp[i + 1][k - 1] if k > i + 1 else 0
                    right = dp[k][j]
                    dp[i][j] = min(dp[i][j], left + right)

    return dp[0][n - 1]
```

## Complexity
- Time: O(n³)
- Space: O(n²)

## Why This Problem Fourth?

Strange Printer shows non-standard interval DP:
1. Optimization based on character matching
2. Different recurrence structure
3. Preprocessing to remove duplicates

## Common Mistakes

1. **Not removing duplicates** - Consecutive same chars waste computation
2. **Wrong base case** - Single char needs 1 turn
3. **Missing the optimization** - When `s[k] == s[i]`, we can combine prints

## Related Problems
- LC 546: Remove Boxes (Similar character-based DP)
- LC 1000: Minimum Cost to Merge Stones
