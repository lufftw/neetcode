## Decision Tree

```
Start: Need to track "which elements are selected/visited"?
       AND set size ≤ 20?
                    │
                    ▼
              ┌─────────────────────────────────────────┐
              │   BITMASK DP is likely applicable       │
              └─────────────────────────────────────────┘
                    │
                    ▼
        ┌───────────────────────────┐
        │ What are you optimizing?  │
        └───────────────────────────┘
                    │
    ┌───────────────┼───────────────┐
    ▼               ▼               ▼
Generate all   Shortest path   Minimize count
  subsets      visiting all    to cover all
    │               │               │
    ▼               ▼               ▼
┌─────────┐   ┌───────────┐   ┌───────────┐
│ SUBSET  │   │ BFS +     │   │ SET COVER │
│ ENUM    │   │ BITMASK   │   │ DP        │
│ (LC 78) │   │ (LC 847)  │   │ (LC 1125) │
└─────────┘   └───────────┘   └───────────┘
```

## Pattern Selection Guide

### Use Subset Enumeration (LC 78) when:
- ✅ Need to generate all possible subsets
- ✅ No optimization objective
- ✅ Just enumerate possibilities
- ✅ n ≤ 15 (2^15 = 32K subsets)

### Use BFS + Bitmask (LC 847) when:
- ✅ Need shortest path in state space
- ✅ State includes "which nodes visited"
- ✅ Can revisit nodes (BFS works)
- ✅ n ≤ 12-15 (state space n × 2^n)

### Use Set Cover DP (LC 1125) when:
- ✅ Need minimum items to cover requirements
- ✅ Each item covers a subset of requirements
- ✅ Requirements can be encoded as bitmask
- ✅ m ≤ 16-20 requirements

## Red Flags - When NOT to Use Bitmask DP

| Red Flag | Why | Alternative |
|----------|-----|-------------|
| n > 20 | 2^20 ≈ 10^6, too slow | Greedy/approximation |
| Order matters | Need permutation, not subset | Backtracking |
| Continuous values | Can't encode as bits | Standard DP |
| Duplicates in set | Bits can't handle multiplicity | HashMap DP |

## Quick Pattern Identification

### Keywords → Pattern

| Keywords | Pattern |
|----------|---------|
| "all subsets", "power set" | Subset Enumeration |
| "visit all nodes", "TSP" | BFS + Bitmask |
| "minimum team", "cover all" | Set Cover DP |
| "partition into groups" | Bitmask + DP |
| "assign tasks to workers" | Bitmask + DP |

### Constraint → Pattern

| Constraint | Suggests |
|------------|----------|
| n ≤ 10 | Any bitmask pattern safe |
| n ≤ 12 | 2D bitmask (node, mask) ok |
| n ≤ 16 | 1D bitmask DP ok |
| n ≤ 20 | Tight, may need pruning |
| n > 20 | NOT bitmask DP |

## Integration with Other Patterns

Bitmask DP often combines with:

1. **BFS** (LC 847) - For shortest path in bitmask state space
2. **Standard DP** - Bitmask as one dimension
3. **Backtracking** - Generate subsets recursively
4. **Greedy** - Prune dominated choices before DP
