# Monotonic Stack Patterns: Complete Reference

> **API Kernel**: `MonotonicStack`
> **Core Mechanism**: Boundary / Candidate Resolution via Monotonicity — maintain a stack in strictly or non-strictly increasing/decreasing order to efficiently resolve boundary queries (next greater, next smaller, span, interval expansion) in amortized O(1) per element.

This document presents the **canonical monotonic stack template** and all its major variations. Each implementation follows consistent naming conventions and includes detailed algorithmic explanations.

---

## Core Concepts

### What is a Monotonic Stack?

A monotonic stack is a stack that maintains elements in a **monotonically increasing or decreasing order**. When a new element violates this order, we pop elements from the stack until the invariant is restored.

```
Monotonic Decreasing Stack (for Next Greater Element):
┌─────────────────────────────────────────────────────────────┐
│  Push: Only push if element < stack top (maintains order)   │
│  Pop:  Pop while stack top < current element                │
│        → Each popped element finds its "next greater"       │
│                                                              │
│  Stack state: [largest, ..., smallest]                      │
│               └──── bottom ────┘  └─ top                    │
└─────────────────────────────────────────────────────────────┘
```

### Why Boundary / Candidate Resolution is the Canonical Kernel

The monotonic stack solves a fundamental class of problems: **finding the nearest element satisfying a comparison condition**. This includes:

- **Next Greater Element (NGE)**: For each element, find the first element to the right that is greater
- **Previous Smaller Element (PSE)**: For each element, find the first element to the left that is smaller
- **Span queries**: How many consecutive elements are smaller/greater?
- **Interval expansion**: How far can we extend left/right while maintaining a property?

All these reduce to the same core mechanism: **when we pop an element from the stack, the current element becomes its boundary**.

### The Core Invariant

Every monotonic stack algorithm maintains this invariant:

> **Invariant**: The stack contains candidate elements that have not yet found their boundary, ordered monotonically.

When we encounter a new element that violates the monotonic order:
1. Pop elements until order is restored
2. Each popped element has found its boundary (the current element)
3. Push the current element as a new candidate

### Stack Stores Indices (Canonical Form)

**Always store indices in the stack, not values.** This provides:
- Access to both position and value via `arr[stack[-1]]`
- Ability to compute distances (`current_index - stack[-1]`)
- Consistent interface across all monotonic stack variants

```python
# Canonical: Store indices
stack = []  # stack of indices
for i, val in enumerate(arr):
    while stack and arr[stack[-1]] < val:
        idx = stack.pop()
        # arr[idx] found its next greater at position i
    stack.append(i)  # Push index, not value
```

### Resolve on Pop Semantics

The key insight of monotonic stack is that **boundaries are resolved when elements are popped**, not when they are pushed:

```
Processing: [2, 1, 5, 6, 2, 3]

Step 1: Push 2 (idx=0)     Stack: [0]
Step 2: Push 1 (idx=1)     Stack: [0, 1]   (1 < 2, order maintained)
Step 3: See 5
        Pop 1 → 1's NGE is 5 (at idx=2)
        Pop 2 → 2's NGE is 5 (at idx=2)
        Push 5 (idx=2)     Stack: [2]
Step 4: Push 6 (idx=3)     Stack: [2, 3]
Step 5: See 2
        (2 < 6, just push)
        Push 2 (idx=4)     Stack: [2, 3, 4]
Step 6: See 3
        Pop 2 → 2's NGE is 3 (at idx=5)
        Push 3 (idx=5)     Stack: [2, 3, 5]

Final: Elements [5, 6, 3] have no NGE (remain in stack)
```

### Sub-Pattern Classification

| Sub-Pattern | Key Characteristic | Examples |
|-------------|-------------------|----------|
| **Next Greater/Smaller** | Find boundary element | LeetCode 496, 739 |
| **Circular Boundary** | 2n traversal for wrap-around | LeetCode 503 |
| **Histogram Expansion** | Left/right smaller for area | LeetCode 84, 85 |
| **Span/Distance** | Count consecutive dominated elements | LeetCode 901 |
| **Contribution Counting** | Sum via boundary products | LeetCode 907, 2104 |
| **Container/Valley** | Water trapped between walls | LeetCode 42 |
| **Greedy Monotonic** | Optimal prefix selection | LeetCode 402 |


