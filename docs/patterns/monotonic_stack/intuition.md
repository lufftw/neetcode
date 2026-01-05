# Monotonic Stack: Pattern Intuition Guide

> *"The tallest building blocks the view. Once you see something taller, everything shorter behind it becomes irrelevant."*

---

## The Situation That Calls for Monotonic Stack

Imagine standing in a city skyline, looking right. You want to know: for each building, which is the first taller building to its right?

You could check every building to the right of each one — that's O(n²). But there's a pattern: **once a tall building appears, all the shorter buildings before it will never be the answer for anything further right**. They're "shadowed" by the tall one.

**This is the essence of Monotonic Stack.**

You encounter this pattern whenever:
- You need the **nearest element** satisfying a comparison (greater/smaller)
- Elements that are "dominated" by others can be **safely discarded**
- The answer for each element is determined by a **boundary** element
- Processing order matters: **resolve on pop, not on push**

The key insight: *You're not searching — you're eliminating candidates. When a dominant element appears, weaker candidates are resolved and discarded forever.*

---

## The Invariant: Candidates Awaiting Their Boundary

Every monotonic stack algorithm maintains one sacred promise:

> **The stack contains unresolved candidates, ordered monotonically.**

```
Monotonic Decreasing Stack (for Next Greater Element):
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   Stack: [ 8,  5,  3,  2 ]   ← Decreasing order (largest at bottom)        │
│            ↑   ↑   ↑   ↑                                                    │
│            │   │   │   └── Most recent, smallest, still waiting             │
│            │   │   └────── Waiting for something > 3                        │
│            │   └────────── Waiting for something > 5                        │
│            └────────────── Waiting for something > 8                        │
│                                                                             │
│   When we see 6:                                                            │
│     - Pop 2 → 2's next greater is 6                                         │
│     - Pop 3 → 3's next greater is 6                                         │
│     - Pop 5 → 5's next greater is 6                                         │
│     - Stop at 8 (8 > 6)                                                     │
│     - Push 6 → Stack becomes [8, 6]                                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

The invariant is your compass. Every element either:
1. **Resolves** existing candidates (by being their boundary)
2. **Becomes** a new candidate (pushed onto stack)
3. **Both** — first resolve, then join

---

## The Irreversible Decision

Here's what gives monotonic stack its power:

> **Once an element is popped, its answer is determined forever.**

When you pop element X because you encountered Y:
- Y is X's "next greater" (or whatever boundary you're seeking)
- X will never be considered again
- This decision is final and correct

Why? Because:
1. Y is the **first** element that satisfies the condition (you're processing left to right)
2. Everything between X and Y was smaller (otherwise X would have been popped earlier)
3. No future element can change this relationship

```
The Finality of Pop:
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   Array:  [ 2, 1, 5, 6, 2, 3 ]                                              │
│                   ↑                                                          │
│                   When we reach 5:                                           │
│                     - Pop 1 → 1's NGE = 5 (FINAL)                           │
│                     - Pop 2 → 2's NGE = 5 (FINAL)                           │
│                                                                             │
│   Why can't something later change 1's answer?                              │
│     - 5 is already > 1                                                      │
│     - 5 comes before anything later                                         │
│     - "Next greater" means FIRST greater to the right                       │
│     - 5 wins. Forever.                                                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## The Amortized Magic: Each Element Pushed/Popped Once

Why is monotonic stack O(n)? Because:

> **Every element is pushed exactly once and popped at most once.**

```
Amortized Analysis:
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   Total operations = n pushes + at most n pops = O(n)                       │
│                                                                             │
│   Even though the inner while loop can pop multiple elements,               │
│   each element can only be popped ONCE in its lifetime.                     │
│                                                                             │
│   Think of it as: each element "pays" for its own push and pop.            │
│   No element pays twice. Total cost = O(n).                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Why Store Indices, Not Values?

Always store indices in the stack, never values directly:

```python
# Canonical form: Store indices
stack = []  # stack of indices
for i, val in enumerate(arr):
    while stack and arr[stack[-1]] < val:
        idx = stack.pop()
        # arr[idx] found its next greater at position i
        # We have both: the VALUE (arr[idx]) and POSITION (idx, i)
    stack.append(i)
```

Benefits:
1. **Access value**: `arr[stack[-1]]` gives the value
2. **Compute distance**: `i - stack[-1]` gives the span/gap
3. **Consistent interface**: Same code works for position-based and value-based queries

---

## The Seven Sub-Patterns

Monotonic stack solves a family of related problems:

### 1. Next Greater/Smaller Element
> *"For each element, find the nearest element that dominates it."*

Classic application. Decreasing stack for next greater, increasing for next smaller.

### 2. Circular Boundary
> *"What if the array wraps around?"*

Traverse 2n elements (or use modulo). Only push during first n.

### 3. Histogram Expansion
> *"How far can each bar extend as the shortest?"*

Find left and right boundaries where smaller bars appear. Area = height × (right - left - 1).

### 4. Span/Distance
> *"How many consecutive elements are dominated?"*

Instead of storing just indices, store (index, accumulated_span). When popping, absorb spans.

### 5. Contribution Counting
> *"Sum the contribution of each element across all subarrays."*

Each element contributes value × left_count × right_count, where counts come from boundary positions.

### 6. Container/Valley Resolution
> *"Fill water in valleys between walls."*

Decreasing stack finds left walls. When taller wall appears, compute trapped water layer by layer.

### 7. Greedy Monotonic Selection
> *"Build the optimal sequence by selectively removing elements."*

Use monotonic property to greedily keep better prefixes while respecting constraints.

---

## The Mental Model: A Waiting Line

Think of the stack as a **waiting line** at a concert:

```
The Waiting Line Mental Model:
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   People in line are waiting to be "matched" with someone taller.           │
│                                                                             │
│   Rules:                                                                    │
│   1. New person arrives at the back                                         │
│   2. Anyone shorter than the new person leaves (they found their match!)    │
│   3. New person joins the remaining line                                    │
│                                                                             │
│   The line is always sorted by height (tallest in front).                   │
│   Short people leave quickly. Tall people wait longer.                      │
│   The tallest person might never find a match (no next greater).            │
│                                                                             │
│   Line: [190cm, 180cm, 170cm]   New arrival: 175cm                          │
│         - 170cm leaves (found 175cm)                                        │
│         - Line becomes [190cm, 180cm, 175cm]                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Common Pitfalls and How to Avoid Them

### Pitfall 1: Forgetting Unresolved Elements
Elements remaining in the stack at the end have no boundary (or use sentinel).

```python
# Solution 1: Process remaining elements
while stack:
    idx = stack.pop()
    result[idx] = -1  # No next greater exists

# Solution 2: Use sentinel value
arr.append(float('inf'))  # Guarantees everything gets resolved
```

### Pitfall 2: Strict vs Non-Strict Comparison
For duplicates, decide: is `5` the "next greater" of another `5`?

```python
# Strict greater (5 is NOT greater than 5)
while stack and arr[stack[-1]] < val:

# Non-strict (5 IS greater-or-equal to 5)
while stack and arr[stack[-1]] <= val:
```

### Pitfall 3: Left vs Right Boundary
- **Next greater to RIGHT**: Process left to right, pop when current > stack top
- **Previous greater to LEFT**: Process right to left, OR process left to right and track differently

### Pitfall 4: Off-by-One in Distance
```python
# Distance from popped element to current
distance = current_idx - popped_idx  # Elements BETWEEN them = distance - 1

# Width for histogram
width = current_idx - left_boundary_idx - 1  # Excludes both boundaries
```

---

## The Template Skeleton

Every monotonic stack solution follows this skeleton:

```python
def solve(arr):
    n = len(arr)
    stack = []  # Store indices
    result = [default] * n

    for i in range(n):  # or range(2*n) for circular
        # Resolve: pop elements that found their boundary
        while stack and CONDITION(arr[stack[-1]], arr[i]):
            idx = stack.pop()
            result[idx] = COMPUTE_ANSWER(idx, i, stack)

        # Candidate: current element awaits its boundary
        stack.append(i)

    # Handle unresolved (optional, or use sentinel)
    while stack:
        idx = stack.pop()
        result[idx] = NO_BOUNDARY_VALUE

    return result
```

Where:
- `CONDITION`: When does current element resolve stack top?
- `COMPUTE_ANSWER`: What's the answer for the resolved element?
- `NO_BOUNDARY_VALUE`: Default when no boundary exists

---

## From Intuition to Implementation

Now that you understand the "why," move to [Templates](templates.md) for production-ready implementations of each sub-pattern:

1. **Next Greater Element** — The base pattern
2. **Circular Boundaries** — Handling wrap-around
3. **Histogram Areas** — Finding expansion limits
4. **Span Calculations** — Counting dominated elements
5. **Contribution Sums** — Aggregating across subarrays
6. **Container Problems** — Valley/water resolution
7. **Greedy Selection** — Building optimal sequences

Each template shows the exact code, complexity analysis, and problem-specific adaptations.

---

*The stack remembers what's waiting. The pop reveals what's found. The push adds what's hoping.*
