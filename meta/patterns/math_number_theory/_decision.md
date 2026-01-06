---

## Decision Guide

### Problem Signal → Tool Mapping

| Signal | Tool to Use | Examples |
|--------|-------------|----------|
| "GCD", "common divisor", "reduce fractions" | Euclidean algorithm | LC 1979, 1071 |
| "Prime numbers", "count primes" | Sieve of Eratosthenes | LC 204 |
| "Very large numbers", "mod 10^9+7" | Modular arithmetic | LC 50, 372 |
| "Convert to/from base", "digit manipulation" | Base conversion | LC 168, 171 |
| "Factor", "divisors" | Prime factorization | LC 952, 1362 |

### Complexity Reference

| Operation | Time Complexity |
|-----------|-----------------|
| GCD of two numbers | O(log(min(a, b))) |
| GCD of array | O(n * log(max)) |
| Prime sieve to n | O(n log log n) |
| Primality test | O(√n) |
| Prime factorization | O(√n) |
| Modular exponentiation | O(log exp) |

### Common Patterns

| Pattern | When It Appears |
|---------|-----------------|
| GCD chaining | "GCD of all elements", "reduce to simplest form" |
| Sieve + precompute | Multiple primality queries |
| Mod arithmetic | "Answer mod 10^9+7" |
| Base-N | "Excel columns", "bijective numeration" |

### Red Flags for Math Problems

- **Very large numbers**: Likely needs modular arithmetic
- **"All pairs" or "all subsets"**: May need clever math to avoid brute force
- **"Divisible by k"**: Think GCD or modular properties
- **"Power of 2/3/etc"**: Bit manipulation or log-based


