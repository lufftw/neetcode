## Variant: Longest Happy Prefix (LeetCode 1392)

> **Problem**: A string is called a happy prefix if it is both a prefix and suffix (excluding entire string). Return the longest happy prefix of the given string.
> **Invariant**: Direct application of KMP failure function.
> **Delta from Base**: Return s[0:failure[n-1]] directly.

### Key Insight

This is the most direct application of the KMP failure function:
- `failure[n-1]` gives exactly the length of the longest proper prefix that is also a suffix
- Just return the first `failure[n-1]` characters

### Implementation

```python
class SolutionKMP:
    def longestPrefix(self, s: str) -> str:
        """
        Find longest happy prefix using KMP failure function.

        The failure function at position n-1 gives exactly what we need:
        the length of the longest proper prefix that is also a suffix.

        Time: O(n)
        Space: O(n)
        """
        string_length = len(s)

        if string_length <= 1:
            return ""

        # Build failure function
        failure: list[int] = [0] * string_length

        prefix_length = 0
        for i in range(1, string_length):
            while prefix_length > 0 and s[i] != s[prefix_length]:
                prefix_length = failure[prefix_length - 1]

            if s[i] == s[prefix_length]:
                prefix_length += 1

            failure[i] = prefix_length

        # The answer is directly failure[n-1]
        happy_prefix_length = failure[-1]

        return s[:happy_prefix_length]
```

### Alternative: Rolling Hash

```python
class SolutionRollingHash:
    def longestPrefix(self, s: str) -> str:
        """
        Find longest happy prefix using rolling hash.

        Compute prefix and suffix hashes simultaneously.
        Track longest match where both hashes are equal.

        Time: O(n)
        Space: O(1)
        """
        string_length = len(s)

        if string_length <= 1:
            return ""

        BASE = 31
        MOD = 10**9 + 7

        prefix_hash = 0
        suffix_hash = 0
        power = 1
        longest_length = 0

        # Compare prefix s[0:i+1] with suffix s[n-i-1:n]
        for i in range(string_length - 1):
            prefix_char = ord(s[i]) - ord('a') + 1
            suffix_char = ord(s[string_length - 1 - i]) - ord('a') + 1

            # Prefix hash: h = h * BASE + char (left to right)
            prefix_hash = (prefix_hash * BASE + prefix_char) % MOD

            # Suffix hash: h = h + char * power (right to left, building from end)
            suffix_hash = (suffix_hash + suffix_char * power) % MOD

            power = (power * BASE) % MOD

            if prefix_hash == suffix_hash:
                longest_length = i + 1

        return s[:longest_length]
```

### Trace Example

```
s = "ababab"

Build failure function:
Index: 0  1  2  3  4  5
Char:  a  b  a  b  a  b
LPS:   0  0  1  2  3  4

failure[-1] = 4
Longest happy prefix = "abab"

Verification:
- Prefix: s[0:4] = "abab" ✓
- Suffix: s[2:6] = "abab" ✓
```

### Key Insights

1. **Direct Application**: failure[-1] is exactly what we need
2. **Proper Prefix**: Must exclude entire string (handled by failure function)
3. **Rolling Hash Alternative**: Useful when you need to avoid preprocessing
4. **Empty String**: Return "" if no happy prefix exists

