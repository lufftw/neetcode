# Binary Search Patterns: Complete Reference

> **API Kernel**: `BinarySearchBoundary`
> **Core Mechanism**: Systematically halve the search space by maintaining a predicate-based invariant until the boundary between true/false regions is found.

This document presents the **canonical binary search template** and all its major variations. Each implementation follows consistent naming conventions and includes detailed algorithmic explanations.

---

## Core Concepts

### What is Binary Search?

Binary search is a **divide-and-conquer** algorithm that efficiently locates a target or boundary in a sorted/monotonic search space by repeatedly halving the search interval. Instead of examining all N elements (O(n)), binary search achieves O(log n) by eliminating half the remaining candidates at each step.

```
Search Space Reduction:
┌─────────────────────────────────────────────────────────────┐
│  [    left ──────────── mid ──────────── right    ]         │
│                          │                                   │
│    ◄──── eliminate ────► │ ◄──── or eliminate ────►         │
│                          │                                   │
│  After decision: search space reduced by half               │
└─────────────────────────────────────────────────────────────┘
```

### Why Predicate/Boundary Search is the Canonical Kernel

Traditional binary search for "find exact value" is actually a **special case** of the more general **predicate boundary search**:

- **Predicate Boundary**: Find the first (or last) position where a condition becomes true
- **Exact Match**: Find where `arr[mid] == target` (predicate: `arr[i] >= target`)
- **Lower Bound**: Find first position where `arr[i] >= target`
- **Upper Bound**: Find first position where `arr[i] > target`

The predicate formulation unifies all binary search variants under one mental model:

```
Predicate View:
┌───────────────────────────────────────────────────────────┐
│  [F, F, F, F, F, T, T, T, T, T]                            │
│                ↑                                           │
│             boundary                                       │
│                                                            │
│  Find the FIRST index where predicate(arr[i]) is True     │
└───────────────────────────────────────────────────────────┘
```

### The Core Invariant

Every binary search maintains this invariant throughout execution:

> **Invariant**: The answer (if it exists) lies within the range `[left, right]`.

When the loop terminates (`left > right` or `left == right`), the boundary has been found.

### Sub-Pattern Classification

| Sub-Pattern | Key Characteristic | Examples |
|-------------|-------------------|----------|
| **Exact Match** | Find specific value | Classic binary search |
| **Lower Bound** | First position where `arr[i] >= target` | LeetCode 34, 35 |
| **Upper Bound** | First position where `arr[i] > target` | LeetCode 34 |
| **Rotated Array** | Split invariant across pivot | LeetCode 33, 81, 153 |
| **Answer Space** | Search over possible answers | LeetCode 875, 1011, 410 |
| **Peak Finding** | Neighbor comparison invariant | LeetCode 162, 852 |


