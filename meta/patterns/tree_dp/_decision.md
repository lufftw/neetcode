## When to Use Tree DP

### Pattern Recognition Signals

Use tree DP when you see:

1. **Binary tree structure** with optimization requirement
2. **Node-level decisions** that affect neighbors (parent/children)
3. **Constraint propagation** through tree edges
4. **Optimal substructure** where subtree solutions combine for parent

### Decision Flowchart

```
Problem on a tree?
├── No → Not tree DP
└── Yes → What's the constraint?
    ├── Node selection (include/exclude) → Include/Exclude DP
    │   └── Examples: House Robber III, Max Independent Set
    ├── Path optimization → Path Contribution DP
    │   └── Examples: Max Path Sum, Diameter
    └── Coverage/coloring → Multi-State DP
        └── Examples: Binary Tree Cameras, Vertex Cover
```

### State Design Questions

1. **What information does a parent need from children?**
   - Binary choice → 2 states
   - Path contribution → 1 value
   - Multiple scenarios → 3+ states

2. **Is the answer at the root or anywhere?**
   - At root → return from DFS
   - Anywhere → track global max/min

3. **Can negative values be ignored?**
   - Yes → clamp contributions to 0
   - No → handle negative cases

### Tree DP vs Other Patterns

| Alternative | When to Prefer |
|-------------|----------------|
| **BFS/DFS** | Just traversal, no optimization |
| **Greedy** | Local optimal = global optimal |
| **1D DP** | Tree degenerates to path |
| **Memoization** | Same subtree appears multiple times (rare in trees) |

### Common Pitfalls

1. **Forgetting base case**: Handle null nodes properly
2. **Wrong state count**: More constraints need more states
3. **Confusing return vs global**: Know what to return vs track globally
4. **Off-by-one in coverage**: Careful with parent/child relationships
