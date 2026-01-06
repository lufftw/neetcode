# Math / Number Theory Pattern

## Table of Contents

1. [API Kernel: `MathNumberTheory`](#1-api-kernel-mathnumbertheory)
2. [The Toolbox Approach](#2-the-toolbox-approach)
3. [Key Mathematical Properties](#3-key-mathematical-properties)
4. [When to Suspect Math Patterns](#4-when-to-suspect-math-patterns)
5. [GCD of Array (LeetCode 1979)](#5-gcd-of-array-leetcode-1979)
6. [Count Primes (LeetCode 204)](#6-count-primes-leetcode-204)
7. [Excel Sheet Column Title (LeetCode 168)](#7-excel-sheet-column-title-leetcode-168)
8. [Quick Reference Toolbox](#8-quick-reference-toolbox)
9. [Decision Guide](#9-decision-guide)

---

## 1. API Kernel: `MathNumberTheory`

> **Core Mechanism**: Apply mathematical properties and number-theoretic algorithms to solve problems efficiently.

**Math/Number Theory** is less a unified pattern and more a **toolbox** of techniques. Unlike sliding window or DP, these problems are scattered across different concepts. The goal is to recognize which mathematical tool applies.

---

## 2. The Toolbox Approach

This pattern is organized as a reference of common mathematical techniques:

| Tool | When to Use | Key Operations |
|------|-------------|----------------|
| **GCD/LCM** | Find common divisors, reduce fractions | `gcd(a, b)`, `lcm(a, b) = a * b // gcd(a, b)` |
| **Prime Sieve** | Find all primes up to N | Sieve of Eratosthenes |
| **Modular Arithmetic** | Large numbers, cycling patterns | `(a + b) % m`, `(a * b) % m` |
| **Base Conversion** | Number systems, encoding | Divide/remainder loops |
| **Factorization** | Prime factors, divisor counting | Trial division, factorization |

---

## 3. Key Mathematical Properties

### 3.1 GCD (Greatest Common Divisor)

**Euclidean Algorithm**:
```
gcd(a, b) = gcd(b, a % b)
gcd(a, 0) = a
```

**Properties**:
- `gcd(a, b) = gcd(b, a)` (commutative)
- `gcd(a, b, c) = gcd(gcd(a, b), c)` (associative)
- `lcm(a, b) * gcd(a, b) = a * b`

### 3.2 Prime Numbers

**Sieve of Eratosthenes**:
1. Create boolean array for 2 to n
2. Start from 2, mark all multiples as composite
3. Move to next unmarked number, repeat
4. Remaining unmarked numbers are prime

**Time**: O(n log log n) for all primes up to n

### 3.3 Modular Arithmetic

**Properties**:
- `(a + b) % m = ((a % m) + (b % m)) % m`
- `(a * b) % m = ((a % m) * (b % m)) % m`
- `(a - b) % m = ((a % m) - (b % m) + m) % m` (add m to handle negative)

**Modular Exponentiation**: Compute `a^b % m` in O(log b) using binary exponentiation.

---

## 4. When to Suspect Math Patterns

- Problem involves **divisibility**, **factors**, or **multiples**
- Problem mentions **prime numbers**
- Problem involves **very large numbers** with modulo
- Problem asks about **cycles** or **periodicity**
- Problem involves **base conversion** or digit manipulation

---

---

## 5. GCD of Array (LeetCode 1979)

> **Problem**: Find GCD of all elements in array.
> **Tool**: Euclidean algorithm, iterative GCD.
> **Role**: Demonstrates GCD chaining via associativity.

### 5.1 Implementation

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

### 5.2 The Euclidean Algorithm

```
gcd(48, 18):
  48 = 18 * 2 + 12  →  gcd(18, 12)
  18 = 12 * 1 + 6   →  gcd(12, 6)
  12 = 6 * 2 + 0    →  gcd(6, 0) = 6

Answer: 6
```

**Why it works**: If `a = b * q + r`, then any common divisor of `a` and `b` must also divide `r`. So `gcd(a, b) = gcd(b, r)`.

### 5.3 LCM via GCD

```python
def lcm(a: int, b: int) -> int:
    return a * b // math.gcd(a, b)
```

**Property**: `gcd(a, b) * lcm(a, b) = a * b`

---

## 6. Count Primes (LeetCode 204)

> **Problem**: Count primes less than n.
> **Tool**: Sieve of Eratosthenes.
> **Role**: Demonstrates prime sieve technique.

### 6.1 Implementation

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

### 6.2 Why Start from p²?

When marking composites of prime p:
- 2p, 3p, ..., (p-1)p have already been marked by smaller primes
- p² is the first multiple of p not yet marked

**Example**: When p = 5:
- 2*5 = 10 → marked by 2
- 3*5 = 15 → marked by 3
- 4*5 = 20 → marked by 2
- 5*5 = 25 → first unmarked multiple of 5

### 6.3 Why Loop Until √n?

If n has a factor > √n, it must also have a factor < √n.
So all composites are marked by primes ≤ √n.

### 6.4 Trace Example

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

---

## 7. Excel Sheet Column Title (LeetCode 168)

> **Problem**: Convert column number to Excel title (1→A, 26→Z, 27→AA, ...).
> **Tool**: Base conversion (base-26 with 1-indexing quirk).
> **Role**: Demonstrates modified base conversion.

### 7.1 Implementation

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

### 7.2 Why Subtract 1?

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

### 7.3 Trace Example

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

### 7.4 Reverse Problem: Title to Number

```python
def titleToNumber(self, columnTitle: str) -> int:
    result = 0
    for char in columnTitle:
        result = result * 26 + (ord(char) - ord('A') + 1)
    return result
```

---

---

## 8. Quick Reference Toolbox

### 8.1 GCD / LCM

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

### 8.2 Prime Sieve

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

### 8.3 Primality Test

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

### 8.4 Prime Factorization

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

### 8.5 Modular Exponentiation

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

### 8.6 Base Conversion

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

---

---

## 9. Decision Guide

### 9.1 Problem Signal → Tool Mapping

| Signal | Tool to Use | Examples |
|--------|-------------|----------|
| "GCD", "common divisor", "reduce fractions" | Euclidean algorithm | LC 1979, 1071 |
| "Prime numbers", "count primes" | Sieve of Eratosthenes | LC 204 |
| "Very large numbers", "mod 10^9+7" | Modular arithmetic | LC 50, 372 |
| "Convert to/from base", "digit manipulation" | Base conversion | LC 168, 171 |
| "Factor", "divisors" | Prime factorization | LC 952, 1362 |

### 9.2 Complexity Reference

| Operation | Time Complexity |
|-----------|-----------------|
| GCD of two numbers | O(log(min(a, b))) |
| GCD of array | O(n * log(max)) |
| Prime sieve to n | O(n log log n) |
| Primality test | O(√n) |
| Prime factorization | O(√n) |
| Modular exponentiation | O(log exp) |

### 9.3 Common Patterns

| Pattern | When It Appears |
|---------|-----------------|
| GCD chaining | "GCD of all elements", "reduce to simplest form" |
| Sieve + precompute | Multiple primality queries |
| Mod arithmetic | "Answer mod 10^9+7" |
| Base-N | "Excel columns", "bijective numeration" |

### 9.4 Red Flags for Math Problems

- **Very large numbers**: Likely needs modular arithmetic
- **"All pairs" or "all subsets"**: May need clever math to avoid brute force
- **"Divisible by k"**: Think GCD or modular properties
- **"Power of 2/3/etc"**: Bit manipulation or log-based



---



*Document generated for NeetCode Practice Framework — API Kernel: math_number_theory*
