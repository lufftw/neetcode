## Termination Guarantees (Amortized Analysis)

### Each Index Pushed Once, Popped Once

The key insight for O(n) complexity:

```
Total operations = pushes + pops
                 ≤ n + n = 2n = O(n)

Each index is:
- Pushed exactly once (when we reach it)
- Popped at most once (when a boundary is found)

Therefore, the entire algorithm is O(n) despite the inner while loop.
```

### Invariant Preservation

After each iteration:
1. Stack contains indices of elements without their boundary yet
2. Stack is monotonically ordered (by value at those indices)
3. All processed boundaries have been recorded

### Progress Guarantee

Each iteration either:
- Pops at least one element (progress on stack size), OR
- Pushes exactly one element and advances to next index

The while loop terminates because the stack shrinks with each pop, and there are only n elements total to pop.


