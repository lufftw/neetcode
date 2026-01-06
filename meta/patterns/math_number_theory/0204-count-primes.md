## Count Primes (LeetCode 204)

> **Problem**: Count primes less than n.
> **Tool**: Sieve of Eratosthenes.
> **Role**: Demonstrates prime sieve technique.

### Implementation

```python
class Solution:
    """
    Sieve of Eratosthenes: Find all primes up to n.

    Algorithm:
    1. Create boolean array is_prime[0..n], initially all True
    2. Mark 0 and 1 as not prime
    3. For each prime p starting from 2:
       - Mark all multiples of p (p², p²+p, p²+2p, ...) as composite
       - Start from p² because smaller multiples already marked
    4. Count remaining True values

    Time: O(n log log n) | Space: O(n)
    """
    def countPrimes(self, n: int) -> int:
        if n < 2:
            return 0

        # Initialize: assume all are prime
        is_prime = [True] * n
        is_prime[0] = is_prime[1] = False

        # Sieve: mark composites
        for p in range(2, int(n ** 0.5) + 1):
            if is_prime[p]:
                # Mark multiples starting from p²
                for multiple in range(p * p, n, p):
                    is_prime[multiple] = False

        return sum(is_prime)
```

### Why Start from p²?

When marking composites of prime p:
- 2p, 3p, ..., (p-1)p have already been marked by smaller primes
- p² is the first multiple of p not yet marked

**Example**: When p = 5:
- 2*5 = 10 → marked by 2
- 3*5 = 15 → marked by 3
- 4*5 = 20 → marked by 2
- 5*5 = 25 → first unmarked multiple of 5

### Why Loop Until √n?

If n has a factor > √n, it must also have a factor < √n.
So all composites are marked by primes ≤ √n.

### Trace Example

```
n = 10

Initial: [F, F, T, T, T, T, T, T, T, T]  (0,1 not prime)
          0  1  2  3  4  5  6  7  8  9

p=2: Mark 4, 6, 8
     [F, F, T, T, F, T, F, T, F, T]

p=3: Mark 9 (3² = 9)
     [F, F, T, T, F, T, F, T, F, F]

p=4 > √10, stop.

Primes: 2, 3, 5, 7 → Count = 4
```


