# Math / Number Theory: Pattern Intuition Guide

> *"Mathematics is not about numbers, equations, computations, or algorithms: it is about understanding."* — William Paul Thurston

---

## The Nature of Math Patterns

Unlike sliding window or DP, math/number theory problems don't follow a single template. They're a **toolbox** — a collection of techniques you reach for when you recognize certain signals.

The challenge: **recognizing which tool applies**.

---

## The Core Toolkit

### 1. GCD (Greatest Common Divisor)

**Mental Model**: What's the largest building block that both numbers are made of?

```
36 = 2² × 3²
48 = 2⁴ × 3
GCD = 2² × 3 = 12
```

The GCD is the intersection of prime factors (taking minimum powers).

**The Euclidean Algorithm**: Instead of factoring, repeatedly replace the larger number with the remainder:

```
gcd(48, 36) → gcd(36, 12) → gcd(12, 0) = 12
```

**Key Property**: `gcd(a, b) = gcd(b, a % b)`

### 2. Prime Numbers

**Mental Model**: Primes are the "atoms" of numbers — indivisible building blocks.

**The Sieve**: Instead of testing each number, cross out multiples:
- 2 is prime → cross out 4, 6, 8, 10...
- 3 is prime → cross out 9, 15, 21...
- 4 is crossed out, skip
- 5 is prime → cross out 25, 35...

What remains is prime.

### 3. Modular Arithmetic

**Mental Model**: Clock arithmetic. After 12, you go back to 1.

```
14 mod 12 = 2  (2 o'clock)
26 mod 12 = 2  (also 2 o'clock)
```

**Key Properties**:
- `(a + b) mod m = ((a mod m) + (b mod m)) mod m`
- `(a × b) mod m = ((a mod m) × (b mod m)) mod m`

This lets us keep numbers small during computation.

### 4. Base Conversion

**Mental Model**: Counting in different number systems.

Base 10 uses digits 0-9.
Base 2 (binary) uses 0-1.
Base 26 (Excel columns) uses A-Z.

**The Algorithm**: Repeatedly divide by base, collect remainders.

---

## Pattern Recognition Signals

### Signal: "Find GCD" or "Common divisor"
> *"What's the GCD of all elements?"*
> *"Reduce fraction to lowest terms"*

**Tool**: Euclidean algorithm, chain GCD across elements.

### Signal: "Count primes" or "Is prime"
> *"How many primes less than n?"*
> *"Check if n is prime"*

**Tool**: Sieve of Eratosthenes for bulk, √n trial for single check.

### Signal: "mod 10^9+7"
> *"Return answer modulo 10^9+7"*

**Tool**: Modular arithmetic. Apply mod at every multiplication/addition.

### Signal: "Convert to Excel column" or "Base conversion"
> *"Number to column title", "Bijective base-26"*

**Tool**: Divide-and-remainder loop with base adjustment.

---

## Common Gotchas

### Gotcha 1: 1-indexed vs 0-indexed Bases

Excel columns: A=1, B=2, ..., Z=26 (1-indexed)
Standard base-26: A=0, B=1, ..., Z=25 (0-indexed)

**Fix**: Subtract 1 before each division.

### Gotcha 2: Integer Overflow in Modular Arithmetic

```python
# Wrong: overflow before mod
result = (a * b) % MOD  # May overflow if a*b > MAX_INT

# Right: mod each operand first
result = ((a % MOD) * (b % MOD)) % MOD
```

### Gotcha 3: Sieve Optimization — Start from p²

When sieving prime p, multiples < p² are already marked by smaller primes.
Starting from p² saves significant work.

### Gotcha 4: GCD with Zero

`gcd(a, 0) = a` — zero is divisible by everything.

This is the base case that terminates the Euclidean algorithm.

---

## When Math Helps

Math patterns often provide **dramatic speedups**:

| Problem | Brute Force | With Math |
|---------|-------------|-----------|
| GCD of array | O(n × max_val) | O(n × log(max)) |
| Count primes to n | O(n√n) | O(n log log n) |
| Large exponentiation | O(exp) | O(log exp) |

The key is recognizing when a problem has mathematical structure you can exploit.

---

## Practice Progression

Master the math toolbox through this sequence:

1. **LC 1979** (GCD of Array) — Basic Euclidean algorithm
2. **LC 204** (Count Primes) — Sieve of Eratosthenes
3. **LC 168** (Excel Column Title) — Base conversion twist
4. **LC 50** (Pow(x,n)) — Binary exponentiation (extension)

---

## The Unifying Principle

Math patterns are about **recognizing structure**.

Numbers aren't just values — they have properties: divisibility, primality, periodicity. When a problem involves these properties, mathematical techniques often provide elegant, efficient solutions.

*"The tools are in your toolbox. The art is knowing when to use each one."*
