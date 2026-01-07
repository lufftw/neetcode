## Base Template: Find the Index of First Occurrence (LeetCode 28)

> **Problem**: Given two strings `haystack` and `needle`, return the index of the first occurrence of `needle` in `haystack`, or -1 if `needle` is not part of `haystack`.
> **Invariant**: Use KMP failure function to skip redundant comparisons.
> **Role**: BASE TEMPLATE for `StringMatching` API Kernel.

### Why This Is The Base Template

LC 28 is the purest form of string matching:
- **Single pattern search**: Find one pattern in text
- **First occurrence only**: No need to find all matches
- **Foundation for variants**: KMP failure function is the key building block

### Implementation

```python
class SolutionKMP:
    def strStr(self, haystack: str, needle: str) -> int:
        """
        Find first occurrence of needle in haystack using KMP.

        The KMP algorithm preprocesses the pattern to build a failure function.
        On mismatch, instead of restarting, we use the failure function to
        skip characters that we know will match.

        Time: O(m + n) where m = len(haystack), n = len(needle)
        Space: O(n) for the failure function
        """
        if not needle:
            return 0

        needle_length = len(needle)
        haystack_length = len(haystack)

        if needle_length > haystack_length:
            return -1

        # Build failure function (LPS array)
        # failure[i] = length of longest proper prefix of needle[0:i+1]
        # that is also a suffix
        failure: list[int] = [0] * needle_length

        prefix_length = 0
        for i in range(1, needle_length):
            # Backtrack until match or reach start
            while prefix_length > 0 and needle[i] != needle[prefix_length]:
                prefix_length = failure[prefix_length - 1]

            if needle[i] == needle[prefix_length]:
                prefix_length += 1

            failure[i] = prefix_length

        # Search using failure function
        needle_idx = 0

        for haystack_idx in range(haystack_length):
            haystack_char = haystack[haystack_idx]

            # On mismatch, use failure function to skip
            while needle_idx > 0 and haystack_char != needle[needle_idx]:
                needle_idx = failure[needle_idx - 1]

            if haystack_char == needle[needle_idx]:
                needle_idx += 1

            if needle_idx == needle_length:
                # Found first match
                return haystack_idx - needle_length + 1

        return -1
```

### Alternative: Rabin-Karp Implementation

```python
class SolutionRabinKarp:
    def strStr(self, haystack: str, needle: str) -> int:
        """
        Find first occurrence using Rabin-Karp rolling hash.

        Use polynomial rolling hash to compare windows in O(1) average.
        Verify on hash match to handle collisions.

        Time: O(m + n) average, O(mn) worst case
        Space: O(1)
        """
        if not needle:
            return 0

        needle_length = len(needle)
        haystack_length = len(haystack)

        if needle_length > haystack_length:
            return -1

        BASE = 256
        MOD = 10**9 + 7

        # Compute initial hashes
        needle_hash = 0
        window_hash = 0
        highest_power = 1

        for i in range(needle_length):
            needle_hash = (needle_hash * BASE + ord(needle[i])) % MOD
            window_hash = (window_hash * BASE + ord(haystack[i])) % MOD
            if i < needle_length - 1:
                highest_power = (highest_power * BASE) % MOD

        # Slide and compare
        for i in range(haystack_length - needle_length + 1):
            if needle_hash == window_hash:
                # Verify to avoid false positives
                if haystack[i:i + needle_length] == needle:
                    return i

            # Update hash for next window
            if i < haystack_length - needle_length:
                window_hash = (window_hash - ord(haystack[i]) * highest_power) % MOD
                window_hash = (window_hash * BASE + ord(haystack[i + needle_length])) % MOD
                window_hash = (window_hash + MOD) % MOD

        return -1
```

### Trace Example (KMP)

```
haystack = "ABABDABACDABABCABAB"
needle = "ABABCABAB"

Build failure function for "ABABCABAB":
Index:   0  1  2  3  4  5  6  7  8
Char:    A  B  A  B  C  A  B  A  B
failure: 0  0  1  2  0  1  2  3  4

Search:
Position 0-3: "ABAB" matches needle[0:4]
Position 4: 'D' != 'C', backtrack to failure[3] = 2
Position 4: 'D' != 'A', backtrack to failure[1] = 0
Position 4: 'D' != 'A', needle_idx = 0
...continue...
Position 10-18: "ABABCABAB" matches completely!

Return: 10
```

### Key Insights

1. **Failure Function**: Core of KMP - tells us where to resume on mismatch
2. **No Backtracking in Text**: Text pointer never goes backward, guaranteeing O(n)
3. **Self-Matching**: Failure function is computed by matching pattern against itself
4. **Z-Algorithm Alternative**: Z-array can solve same problems with different approach

