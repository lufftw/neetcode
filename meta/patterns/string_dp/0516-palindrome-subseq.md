## Variant: Longest Palindromic Subsequence (LeetCode 516)

> **Problem**: Given a string `s`, find the longest palindromic subsequence's length in `s`.
> **Invariant**: `dp[i][j]` = length of longest palindromic subsequence in `s[i:j+1]`.
> **Delta from Base**: Compare string with its reverse, or use interval DP on single string.

### Two Approaches

1. **LCS Approach**: LPS(s) = LCS(s, reverse(s))
2. **Interval DP Approach**: Direct computation on substring intervals

### Approach 1: Reduce to LCS

```python
class SolutionLPSviaLCS:
    def longestPalindromeSubseq(self, s: str) -> int:
        """
        Reduce to LCS: Longest palindromic subsequence equals
        LCS of string with its reverse.

        Intuition: A palindrome reads the same forward and backward.
        The common subsequence of s and reverse(s) is palindromic.

        Time: O(n^2)
        Space: O(n)
        """
        reversed_string = s[::-1]
        string_length = len(s)

        # Space-optimized LCS
        previous_row: list[int] = [0] * (string_length + 1)

        for idx_original in range(1, string_length + 1):
            current_row: list[int] = [0] * (string_length + 1)
            for idx_reversed in range(1, string_length + 1):
                if s[idx_original - 1] == reversed_string[idx_reversed - 1]:
                    current_row[idx_reversed] = previous_row[idx_reversed - 1] + 1
                else:
                    current_row[idx_reversed] = max(
                        previous_row[idx_reversed],
                        current_row[idx_reversed - 1]
                    )
            previous_row = current_row

        return previous_row[string_length]
```

### Approach 2: Interval DP (Direct)

```python
class SolutionLPSInterval:
    def longestPalindromeSubseq(self, s: str) -> int:
        """
        Direct interval DP approach.

        State: dp[i][j] = LPS length for substring s[i:j+1]
        Transition:
        - If s[i] == s[j]: dp[i][j] = dp[i+1][j-1] + 2
        - Else: dp[i][j] = max(dp[i+1][j], dp[i][j-1])

        Key insight: Fill table by increasing interval length.

        Time: O(n^2)
        Space: O(n^2), can be optimized to O(n)
        """
        string_length = len(s)

        if string_length <= 1:
            return string_length

        # dp[i][j] = LPS length for s[i:j+1]
        palindrome_length: list[list[int]] = [
            [0] * string_length
            for _ in range(string_length)
        ]

        # Base case: single character is palindrome of length 1
        for i in range(string_length):
            palindrome_length[i][i] = 1

        # Fill by increasing interval length
        for interval_length in range(2, string_length + 1):
            for start in range(string_length - interval_length + 1):
                end = start + interval_length - 1

                if s[start] == s[end]:
                    # Endpoints match: extend inner palindrome by 2
                    inner_length = palindrome_length[start + 1][end - 1] if start + 1 <= end - 1 else 0
                    palindrome_length[start][end] = inner_length + 2
                else:
                    # Endpoints don't match: take best of excluding either
                    exclude_start = palindrome_length[start + 1][end]
                    exclude_end = palindrome_length[start][end - 1]
                    palindrome_length[start][end] = max(exclude_start, exclude_end)

        return palindrome_length[0][string_length - 1]
```

### Space-Optimized Interval DP

```python
class SolutionLPSOptimized:
    def longestPalindromeSubseq(self, s: str) -> int:
        """
        Space-optimized: Only need previous diagonal values.

        We iterate by interval length, so we only need values from
        the previous length. Use 1D array with careful update order.

        Time: O(n^2)
        Space: O(n)
        """
        string_length = len(s)

        # dp[j] = LPS length ending at position j for current start
        current_row: list[int] = [1] * string_length

        for start in range(string_length - 2, -1, -1):
            # previous_diagonal saves dp[start+1][end-1] before overwrite
            previous_diagonal = 0

            for end in range(start + 1, string_length):
                # Save current value (will be diagonal for next end)
                temp = current_row[end]

                if s[start] == s[end]:
                    current_row[end] = previous_diagonal + 2
                else:
                    current_row[end] = max(current_row[end], current_row[end - 1])

                previous_diagonal = temp

        return current_row[string_length - 1]
```

### Trace Example (Interval DP)

```
s = "bbbab"

Fill by interval length:

Length 1 (base case):
  i:    0   1   2   3   4
  s:    b   b   b   a   b
dp[i]: [1] [1] [1] [1] [1]

Length 2:
dp[0][1] = s[0]==s[1]? 2 : max(dp[1][1],dp[0][0]) = 2  (b==b)
dp[1][2] = 2  (b==b)
dp[2][3] = 1  (b!=a, max(1,1))
dp[3][4] = 1  (a!=b)

Length 3:
dp[0][2] = s[0]==s[2]? dp[1][1]+2 = 3  (b==b)
dp[1][3] = 2  (b!=a)
dp[2][4] = 2  (b==b)

Length 4:
dp[0][3] = 3  (b!=a, max(dp[1][3], dp[0][2]) = max(2,3) = 3)
dp[1][4] = 3  (b==b, dp[2][3]+2 = 1+2 = 3)

Length 5:
dp[0][4] = s[0]==s[4]? dp[1][3]+2 = 4  (b==b)

Answer: 4 (subsequence "bbbb")
```

### Key Insights

1. **LCS Reduction**: LPS is a special case of LCS with string and its reverse
2. **Interval DP Pattern**: State depends on inner intervals, fill by length
3. **Space Trade-off**: O(n) space possible with careful update order
4. **Palindrome Property**: Endpoints must match to extend a palindrome


