## Variant: Shortest Palindrome (LeetCode 214)

> **Problem**: Given a string `s`, prepend characters to make it a palindrome and return the shortest such palindrome.
> **Invariant**: Use KMP to find the longest palindromic prefix.
> **Delta from Base**: Apply KMP on `s + '#' + reverse(s)` to find longest prefix that is also suffix.

### Key Insight

The shortest palindrome is formed by:
1. Finding the longest palindromic prefix of `s`
2. Prepending the reverse of the remaining suffix

To find longest palindromic prefix, concatenate `s + '#' + reverse(s)` and compute KMP failure function. The value at the last position gives us the answer.

### Implementation

```python
class SolutionKMP:
    def shortestPalindrome(self, s: str) -> str:
        """
        Find shortest palindrome by prepending characters to s.

        Key insight: Longest palindromic prefix of s equals the longest
        proper prefix of (s + '#' + reverse(s)) that is also a suffix.

        The '#' separator prevents false matches across the boundary.

        Time: O(n)
        Space: O(n)
        """
        if not s or len(s) <= 1:
            return s

        # Create concatenated string with separator
        reversed_s = s[::-1]
        concat = s + '#' + reversed_s

        # Build failure function
        concat_length = len(concat)
        failure: list[int] = [0] * concat_length

        prefix_length = 0
        for i in range(1, concat_length):
            while prefix_length > 0 and concat[i] != concat[prefix_length]:
                prefix_length = failure[prefix_length - 1]

            if concat[i] == concat[prefix_length]:
                prefix_length += 1

            failure[i] = prefix_length

        # failure[-1] = length of longest palindromic prefix
        palindrome_prefix_length = failure[-1]

        # Prepend reverse of non-palindromic suffix
        suffix_to_prepend = reversed_s[:len(s) - palindrome_prefix_length]

        return suffix_to_prepend + s
```

### Alternative: Rolling Hash Approach

```python
class SolutionRollingHash:
    def shortestPalindrome(self, s: str) -> str:
        """
        Use rolling hash to find longest palindromic prefix.

        Compute forward and backward hashes simultaneously.
        When they match at position i, s[0:i+1] is a palindrome.

        Time: O(n)
        Space: O(1)
        """
        if not s or len(s) <= 1:
            return s

        BASE = 29
        MOD = 10**9 + 7

        forward_hash = 0
        backward_hash = 0
        power = 1
        longest_palindrome_end = 0

        for i, char in enumerate(s):
            char_val = ord(char) - ord('a') + 1

            # Forward hash: h = h * BASE + char
            forward_hash = (forward_hash * BASE + char_val) % MOD

            # Backward hash: h = h + char * BASE^i
            backward_hash = (backward_hash + char_val * power) % MOD

            if forward_hash == backward_hash:
                # Potential palindromic prefix (may need verification)
                longest_palindrome_end = i

            power = (power * BASE) % MOD

        # Prepend reverse of suffix after longest palindromic prefix
        suffix = s[longest_palindrome_end + 1:]
        return suffix[::-1] + s
```

### Trace Example

```
s = "aacecaaa"
reversed = "aaacecaa"
concat = "aacecaaa#aaacecaa"

Failure function:
Index: 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16
Char:  a  a  c  e  c  a  a  a  #  a  a  a  c  e  c  a  a
LPS:   0  1  0  0  0  1  2  2  0  1  2  2  3  4  5  6  7

failure[-1] = 7
Longest palindromic prefix = "aacecaa" (length 7)
Remaining suffix = "a"
Prepend reverse of "a" = "a"

Result: "a" + "aacecaaa" = "aaacecaaa"
```

### Key Insights

1. **Separator Is Critical**: '#' prevents matching across s and reverse(s)
2. **Failure Function Property**: failure[-1] = longest proper prefix = suffix
3. **Rolling Hash Alternative**: No separator needed, but may have false positives
4. **Why Not Brute Force**: Checking each prefix for palindrome would be O(n²)

