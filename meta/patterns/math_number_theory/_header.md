# Math / Number Theory Pattern

## API Kernel: `MathNumberTheory`

> **Core Mechanism**: Apply mathematical properties and number-theoretic algorithms to solve problems efficiently.

**Math/Number Theory** is less a unified pattern and more a **toolbox** of techniques. Unlike sliding window or DP, these problems are scattered across different concepts. The goal is to recognize which mathematical tool applies.

---

## The Toolbox Approach

This pattern is organized as a reference of common mathematical techniques:

| Tool | When to Use | Key Operations |
|------|-------------|----------------|
| **GCD/LCM** | Find common divisors, reduce fractions | `gcd(a, b)`, `lcm(a, b) = a * b // gcd(a, b)` |
| **Prime Sieve** | Find all primes up to N | Sieve of Eratosthenes |
| **Modular Arithmetic** | Large numbers, cycling patterns | `(a + b) % m`, `(a * b) % m` |
| **Base Conversion** | Number systems, encoding | Divide/remainder loops |
| **Factorization** | Prime factors, divisor counting | Trial division, factorization |

---

## Key Mathematical Properties

### GCD (Greatest Common Divisor)

**Euclidean Algorithm**:
```
gcd(a, b) = gcd(b, a % b)
gcd(a, 0) = a
```

**Properties**:
- `gcd(a, b) = gcd(b, a)` (commutative)
- `gcd(a, b, c) = gcd(gcd(a, b), c)` (associative)
- `lcm(a, b) * gcd(a, b) = a * b`

### Prime Numbers

**Sieve of Eratosthenes**:
1. Create boolean array for 2 to n
2. Start from 2, mark all multiples as composite
3. Move to next unmarked number, repeat
4. Remaining unmarked numbers are prime

**Time**: O(n log log n) for all primes up to n

### Modular Arithmetic

**Properties**:
- `(a + b) % m = ((a % m) + (b % m)) % m`
- `(a * b) % m = ((a % m) * (b % m)) % m`
- `(a - b) % m = ((a % m) - (b % m) + m) % m` (add m to handle negative)

**Modular Exponentiation**: Compute `a^b % m` in O(log b) using binary exponentiation.

---

## When to Suspect Math Patterns

- Problem involves **divisibility**, **factors**, or **multiples**
- Problem mentions **prime numbers**
- Problem involves **very large numbers** with modulo
- Problem asks about **cycles** or **periodicity**
- Problem involves **base conversion** or digit manipulation

---

