---

## Quick Reference Toolbox

### GCD / LCM

```python
import math

# GCD of two numbers
gcd_val = math.gcd(a, b)

# GCD of array (Python 3.9+)
gcd_all = math.gcd(*nums)

# GCD of array (older Python)
from functools import reduce
gcd_all = reduce(math.gcd, nums)

# LCM via GCD
lcm_val = a * b // math.gcd(a, b)

# LCM of array
def lcm_array(nums):
    result = nums[0]
    for num in nums[1:]:
        result = result * num // math.gcd(result, num)
    return result
```

### Prime Sieve

```python
def sieve_of_eratosthenes(n: int) -> List[int]:
    """Return all primes less than n."""
    if n < 2:
        return []
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(n ** 0.5) + 1):
        if is_prime[p]:
            for m in range(p * p, n, p):
                is_prime[m] = False
    return [i for i in range(n) if is_prime[i]]
```

### Primality Test

```python
def is_prime(n: int) -> bool:
    """Check if n is prime. O(√n)"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True
```

### Prime Factorization

```python
def prime_factors(n: int) -> List[int]:
    """Return list of prime factors (with duplicates)."""
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors
```

### Modular Exponentiation

```python
def mod_pow(base: int, exp: int, mod: int) -> int:
    """Compute base^exp % mod in O(log exp)."""
    result = 1
    base %= mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp //= 2
        base = (base * base) % mod
    return result

# Or use built-in: pow(base, exp, mod)
```

### Base Conversion

```python
def to_base(n: int, base: int) -> str:
    """Convert n to given base (2-36)."""
    if n == 0:
        return "0"
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = []
    while n:
        result.append(digits[n % base])
        n //= base
    return ''.join(reversed(result))

def from_base(s: str, base: int) -> int:
    """Convert string in given base to integer."""
    return int(s, base)
```


