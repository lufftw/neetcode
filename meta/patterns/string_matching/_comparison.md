## Pattern Comparison Table

| Problem | Algorithm | Key Technique | Time | Space |
|---------|-----------|---------------|------|-------|
| **LC 28: Find Index** | KMP / Rabin-Karp | Direct pattern search | O(n+m) | O(m) |
| **LC 214: Shortest Palindrome** | KMP | `s + '#' + reverse(s)` | O(n) | O(n) |
| **LC 459: Repeated Substring** | KMP | Period = n - failure[n-1] | O(n) | O(n) |
| **LC 1392: Longest Happy Prefix** | KMP | Return s[0:failure[n-1]] | O(n) | O(n) |

### Algorithm Selection Guide

| Use Case | Recommended Algorithm | Reason |
|----------|----------------------|--------|
| Single pattern search | KMP | Guaranteed O(n+m), simple |
| Multiple pattern search | Rabin-Karp | Hash fingerprinting |
| Finding periods | KMP failure function | Built-in property |
| Palindrome problems | KMP with concatenation | Elegant reduction |

### Failure Function Applications

| Application | How to Use failure[] |
|-------------|---------------------|
| Pattern search | Backtrack on mismatch |
| String period | Period = n - failure[n-1] |
| Longest prefix=suffix | Answer = failure[n-1] |
| Palindromic prefix | Use `s + '#' + rev(s)` |

### Time Complexity Comparison

| Algorithm | Preprocessing | Search | Total | Worst Case |
|-----------|--------------|--------|-------|------------|
| Naive | O(1) | O(nm) | O(nm) | O(nm) |
| KMP | O(m) | O(n) | O(n+m) | O(n+m) |
| Rabin-Karp | O(m) | O(n) avg | O(n+m) avg | O(nm) |
| Z-Algorithm | O(m) | O(n) | O(n+m) | O(n+m) |

