## GCD of Array (LeetCode 1979)

> **Problem**: Find GCD of all elements in array.
> **Tool**: Euclidean algorithm, iterative GCD.
> **Role**: Demonstrates GCD chaining via associativity.

### Implementation

```python
import math
from functools import reduce

class Solution:
    """
    Find GCD of entire array using associativity.

    Key Insight: gcd(a, b, c) = gcd(gcd(a, b), c)
    We can chain GCD across all elements.

    Method 1: Using reduce
    Method 2: Using math.gcd with *args (Python 3.9+)

    Time: O(n * log(max_val)) | Space: O(1)
    """
    def findGCD(self, nums: List[int]) -> int:
        # Method 1: Explicit reduce
        return reduce(math.gcd, nums)

        # Method 2: Python 3.9+ allows math.gcd(*nums)
        # return math.gcd(*nums)

    def findGCD_manual(self, nums: List[int]) -> int:
        """Manual implementation without library."""
        def gcd(a: int, b: int) -> int:
            while b:
                a, b = b, a % b
            return a

        result = nums[0]
        for num in nums[1:]:
            result = gcd(result, num)
            if result == 1:  # Early exit: GCD can't go below 1
                break
        return result
```

### The Euclidean Algorithm

```
gcd(48, 18):
  48 = 18 * 2 + 12  →  gcd(18, 12)
  18 = 12 * 1 + 6   →  gcd(12, 6)
  12 = 6 * 2 + 0    →  gcd(6, 0) = 6

Answer: 6
```

**Why it works**: If `a = b * q + r`, then any common divisor of `a` and `b` must also divide `r`. So `gcd(a, b) = gcd(b, r)`.

### LCM via GCD

```python
def lcm(a: int, b: int) -> int:
    return a * b // math.gcd(a, b)
```

**Property**: `gcd(a, b) * lcm(a, b) = a * b`


