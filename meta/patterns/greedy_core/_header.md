# Greedy Core Pattern

## API Kernel: `GreedyCore`

> **Core Mechanism**: Make locally optimal choices that lead to a globally optimal solution through invariant preservation.

**Greedy Core** encompasses non-interval, non-heap greedy algorithms that maintain a simple invariant during a single pass. Unlike interval scheduling (which requires sorting by end times) or heap-based greedy (which requires priority queue), these problems rely on direct state tracking and local decision-making.

---

## Three Core Kernels

| Kernel | Key Invariant | Representative Problems |
|--------|---------------|------------------------|
| **Reachability** | Track farthest reachable position | Jump Game, Jump Game II |
| **Prefix Min/Reset** | Track running minimum with conditional reset | Gas Station |
| **Sort + Match** | Sort by one dimension, greedily match | Candy, Assign Cookies, Two City Scheduling |

---

## Why NOT Interval / Heap Greedy?

| Category | Characteristics | Examples |
|----------|-----------------|----------|
| **Greedy Core** (this pattern) | Single-pass, state tracking, no complex data structures | LC 55, 45, 134, 135, 455, 1029 |
| **Interval Greedy** | Sort by interval endpoints, conflict resolution | LC 56, 435, 452 |
| **Heap Greedy** | Priority queue for dynamic selection | LC 253, 621, 1046 |

---

## Core Principle: Greedy Choice Property

A greedy algorithm works when:
1. **Greedy Choice Property**: A locally optimal choice leads to a globally optimal solution
2. **Optimal Substructure**: The optimal solution contains optimal solutions to subproblems

For Greedy Core problems, the choice is typically:
- "Extend as far as possible" (reachability)
- "Reset when deficit" (prefix minimum)
- "Match smallest available" (sorting)

---

