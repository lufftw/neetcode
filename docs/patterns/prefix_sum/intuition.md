# Prefix Sum: Pattern Intuition Guide

> *"The prefix sum is a ledger of the past — it remembers everything you've accumulated so you don't have to count again."*

---

## The Situation That Calls for Prefix Sum

Imagine you're a bank teller tracking an account balance. Every day, money goes in or out. A customer asks: *"What was my balance between day 5 and day 20?"*

You could add up each transaction from day 5 to day 20. But if another customer asks the same type of question for days 100-150, you're counting again from scratch.

**There's a better way.**

At the end of each day, you write down the **running total** — the cumulative balance from day 1 to now. This is your prefix sum.

Now when anyone asks about any range, you simply subtract: *balance at end of range* minus *balance just before the start*. Instant answer.

**This is the essence of Prefix Sum.**

---

## The Two Perspectives

Prefix sum problems come in two fundamental flavors:

### Perspective 1: Range Query
*"Given many range questions, answer each instantly."*

The prefix sum array is your **oracle**. Build it once in O(n), then every range sum becomes a single subtraction: `prefix[end+1] - prefix[start]`.

| Without Prefix Sum | With Prefix Sum |
|-------------------|-----------------|
| Each query: O(n) | Each query: O(1) |
| 10,000 queries × 10,000 elements = 100 million ops | 10,000 queries = 10,000 subtractions |

### Perspective 2: Subarray Sum = K
*"Find subarrays that sum to exactly K."*

The insight: if `prefix[j] - prefix[i] = K`, then the subarray from `i+1` to `j` sums to K.

**Rearranging**: `prefix[i] = prefix[j] - K`

So at each position `j`, you ask: *"How many earlier positions had a prefix sum of (current_prefix - K)?"*

A hash map answers this in O(1). The pattern becomes:
```
For each element:
    Extend prefix sum
    Count occurrences of (prefix_sum - K) in map  ← answers found!
    Record current prefix sum in map
```

---

## The Critical Initialization: {0: 1}

One subtle but crucial detail: **initialize the hash map with {0: 1}**.

Why? Consider this: if the prefix sum at position `j` equals exactly K, what prefix did we subtract?

```
prefix[j] - prefix[?] = K
prefix[j] - K = 0
```

We need a prefix of **0** to have existed. That's the "empty prefix" — the sum before the array even started. By initializing with `{0: 1}`, we say: *"Yes, there was one occurrence of sum=0 at the imaginary position -1."*

Without this, we'd miss every subarray that starts from index 0.

---

## The Inverse: Difference Array

Prefix sum has a twin that works in reverse:

| Prefix Sum | Difference Array |
|------------|------------------|
| Answers range SUM queries | Handles range UPDATE operations |
| Point values → Range sums | Range updates → Point values |
| Build: add cumulative values | Build: mark changes at boundaries |
| Query: subtract two prefix values | Query: compute prefix sum of differences |

**They are mathematical inverses.**

When you need to add a value to every element in a range `[start, end]`:
```python
diff[start] += value    # Start adding here
diff[end+1] -= value    # Stop adding after end
```

Then prefix sum of `diff` gives you the final values.

**Mental model**: Instead of painting each cell in a range, you place a "+value" marker at the start and a "-value" marker just after the end. When you sweep through left-to-right, the markers tell you to "start adding" and "stop adding."

---

## Pattern Recognition Signals

When you see these phrases, think **Prefix Sum**:

### Signal: "Sum of subarray" or "Range sum"
> *"Calculate the sum between indices i and j"*
> *"Find subarrays that sum to K"*

**Action**: Build prefix sum array, use subtraction.

### Signal: "Add value to range" or "Increment interval"
> *"Add 10 to all elements from index 3 to index 7"*
> *"Multiple range update operations"*

**Action**: Use difference array, then compute prefix sum.

### Signal: "Equal count of X and Y"
> *"Longest subarray with equal 0s and 1s"*

**Action**: Transform (0→-1), then find subarray with sum=0.

### Signal: "Multiple range queries on static array"
> *"Answer Q queries on immutable array"*

**Action**: Precompute prefix sum for O(1) queries.

---

## The 2D Extension: Inclusion-Exclusion

When you have a 2D grid and need rectangle sums, prefix sum extends naturally — but with a twist.

Building the 2D prefix:
```
prefix[i][j] = current cell
             + prefix[i-1][j]     ← top
             + prefix[i][j-1]     ← left
             - prefix[i-1][j-1]   ← subtract overlap (counted twice)
```

Querying a rectangle:
```
         ┌─────────────────────────┐
         │  A  │        B          │
         ├─────┼──────────┬────────┤
         │  C  │ ▒▒TARGET▒▒│   D    │
         │     │ ▒▒▒▒▒▒▒▒▒│        │
         └─────┴──────────┴────────┘

TARGET = Total - B - C + A
```

The top-left corner (A) gets subtracted twice (once in B, once in C), so we add it back.

---

## Common Pitfalls

### Pitfall 1: Off-by-One in Prefix Array
**Problem**: Confusion about whether `prefix[i]` includes element `i`.

**Solution**: Use convention where `prefix[i]` = sum of elements **before** index `i`.
- `prefix[0] = 0` (empty prefix)
- `prefix[i] = sum(nums[0:i])`
- Range `[left, right]` = `prefix[right+1] - prefix[left]`

### Pitfall 2: Forgetting the Empty Prefix
**Problem**: Hash map not initialized with {0: 1} or {0: -1}.

**Solution**: Always initialize for subarrays starting at index 0:
- Counting subarrays: `{0: 1}`
- Finding longest: `{0: -1}`

### Pitfall 3: Using Sliding Window with Negative Numbers
**Problem**: Trying to use sliding window for "subarray sum = K" when array has negatives.

**Solution**: Sliding window needs monotonicity. With negatives, sum isn't monotonic. Use prefix sum + hash map instead.

---

## Practice Progression

Master prefix sum through this sequence:

1. **LC 303** (Range Sum Query) — Build basic intuition
2. **LC 560** (Subarray Sum = K) — Add hash map technique
3. **LC 525** (Contiguous Array) — Transform technique (0→-1)
4. **LC 523** (Continuous Subarray Sum) — Modular arithmetic variant
5. **LC 304** (2D Range Sum) — Extend to 2D
6. **LC 238** (Product Except Self) — Prefix/suffix products
7. **LC 1094** (Car Pooling) — Difference array
8. **LC 1109** (Flight Bookings) — Canonical difference array

---

## The Unifying Principle

Prefix sum is about **trading space for time** through **precomputation**.

Instead of answering each question from scratch, you invest upfront to build a structure that makes every future answer immediate.

The prefix sum array is a **cumulative summary** of the past. It lets you query any historical range by looking at just two points — the boundaries.

*"The best time to build a prefix sum was at the start. The second best time is now."*
