## Variant: Repeated Substring Pattern (LeetCode 459)

> **Problem**: Given a string `s`, check if it can be constructed by taking a substring of it and appending multiple copies of the substring together.
> **Invariant**: Use KMP failure function property for periodic strings.
> **Delta from Base**: Check if `n % (n - failure[n-1]) == 0` and the period divides n.

### Key Insight

For a string to be constructed from repeated substrings:
- The pattern length must divide the string length evenly
- Using KMP: if `failure[n-1] > 0` and `n % (n - failure[n-1]) == 0`, the string is periodic

The minimum period length is `n - failure[n-1]`.

### Implementation

```python
class SolutionKMP:
    def repeatedSubstringPattern(self, s: str) -> bool:
        """
        Check if string is built from repeated substrings using KMP.

        Property: For periodic string, failure[n-1] = n - period_length.
        So period_length = n - failure[n-1].
        String is periodic if period_length divides n and period_length < n.

        Time: O(n)
        Space: O(n)
        """
        string_length = len(s)

        if string_length <= 1:
            return False

        # Build failure function
        failure: list[int] = [0] * string_length

        prefix_length = 0
        for i in range(1, string_length):
            while prefix_length > 0 and s[i] != s[prefix_length]:
                prefix_length = failure[prefix_length - 1]

            if s[i] == s[prefix_length]:
                prefix_length += 1

            failure[i] = prefix_length

        # Check periodicity
        longest_prefix_suffix = failure[-1]

        if longest_prefix_suffix == 0:
            return False

        period_length = string_length - longest_prefix_suffix

        # Valid if period divides string length and is not the full string
        return string_length % period_length == 0
```

### Alternative: Concatenation Trick

```python
class SolutionConcatenation:
    def repeatedSubstringPattern(self, s: str) -> bool:
        """
        Elegant trick: s + s contains s at non-boundary position iff s is periodic.

        If s = "abab", then s + s = "abababab"
        Remove first and last char: "bababa"
        This still contains "abab" because it's periodic!

        Time: O(n) with efficient string search
        Space: O(n)
        """
        doubled = s + s
        # Remove first and last character to avoid trivial matches
        return s in doubled[1:-1]
```

### Trace Example

```
s = "abab"

Build failure function:
Index: 0  1  2  3
Char:  a  b  a  b
LPS:   0  0  1  2

failure[-1] = 2
period_length = 4 - 2 = 2
4 % 2 == 0 ✓

The string is built from "ab" repeated twice.

s = "abcab"

Build failure function:
Index: 0  1  2  3  4
Char:  a  b  c  a  b
LPS:   0  0  0  1  2

failure[-1] = 2
period_length = 5 - 2 = 3
5 % 3 != 0 ✗

Not periodic.
```

### Key Insights

1. **KMP Property**: failure[n-1] reveals periodic structure
2. **Period Formula**: period = n - failure[n-1]
3. **Concatenation Trick**: Simpler but uses built-in string search
4. **Edge Cases**: Single character returns False, must have period < n

