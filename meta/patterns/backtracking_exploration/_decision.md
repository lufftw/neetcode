## When to Use Backtracking

### Problem Indicators

✅ **Use backtracking when:**
- Need to enumerate all solutions (permutations, combinations, etc.)
- Decision tree structure (sequence of choices)
- Constraints can be checked incrementally
- Solution can be built piece by piece

❌ **Consider alternatives when:**
- Only need count (use DP with counting)
- Only need one solution (may use greedy or simple DFS)
- Optimization problem (consider DP or greedy)
- State space is too large even with pruning

### Decision Guide

```
Is the problem asking for ALL solutions?
├── Yes → Does solution have natural ordering/structure?
│         ├── Permutation → Use used[] array
│         ├── Subset/Combination → Use start_index
│         ├── Grid path → Use visited marking
│         └── Constraint satisfaction → Use constraint sets
└── No → Need single solution or count?
         ├── Single solution → Simple DFS may suffice
         └── Count → Consider DP
```

