## Excel Sheet Column Title (LeetCode 168)

> **Problem**: Convert column number to Excel title (1→A, 26→Z, 27→AA, ...).
> **Tool**: Base conversion (base-26 with 1-indexing quirk).
> **Role**: Demonstrates modified base conversion.

### Implementation

```python
class Solution:
    """
    Base-26 conversion with 1-indexed twist.

    Key Insight: Excel columns are 1-indexed (A=1, not A=0).
    Standard base-26 is 0-indexed (A=0, B=1, ...).

    Fix: Subtract 1 before each division to shift to 0-indexed,
    then convert remainder to letter.

    Process:
    1. Subtract 1 (shift from 1-indexed to 0-indexed)
    2. remainder = n % 26 → maps to 'A' + remainder
    3. n = n // 26
    4. Repeat until n = 0
    5. Reverse the result (we built from right to left)

    Time: O(log₂₆ n) | Space: O(log₂₆ n)
    """
    def convertToTitle(self, columnNumber: int) -> str:
        result = []

        while columnNumber > 0:
            columnNumber -= 1  # Shift to 0-indexed
            remainder = columnNumber % 26
            result.append(chr(ord('A') + remainder))
            columnNumber //= 26

        return ''.join(reversed(result))
```

### Why Subtract 1?

Standard base-26: A=0, B=1, ..., Z=25
Excel columns: A=1, B=2, ..., Z=26

**Without -1 (wrong)**:
```
n = 26
26 % 26 = 0 → 'A' (should be 'Z')
```

**With -1 (correct)**:
```
n = 26
n -= 1 → 25
25 % 26 = 25 → 'Z' ✓
```

### Trace Example

```
columnNumber = 701 → "ZY"

Iteration 1:
  n = 701 - 1 = 700
  700 % 26 = 24 → 'Y'
  n = 700 // 26 = 26

Iteration 2:
  n = 26 - 1 = 25
  25 % 26 = 25 → 'Z'
  n = 25 // 26 = 0

Result (reversed): "ZY"
```

### Reverse Problem: Title to Number

```python
def titleToNumber(self, columnTitle: str) -> int:
    result = 0
    for char in columnTitle:
        result = result * 26 + (ord(char) - ord('A') + 1)
    return result
```


