---

## Pattern Comparison

### Greedy Core vs Interval Greedy

| Aspect | Greedy Core | Interval Greedy |
|--------|-------------|-----------------|
| **Input Structure** | Arrays, sequences | Intervals with start/end |
| **Sorting** | Optional (by value/metric) | Required (by endpoint) |
| **Key Operation** | State tracking, reachability | Conflict detection, selection |
| **Examples** | LC 55, 134, 135 | LC 56, 435, 452 |

### Greedy Core vs Heap Greedy

| Aspect | Greedy Core | Heap Greedy |
|--------|-------------|-------------|
| **Data Structure** | Simple variables | Priority queue |
| **Selection** | Direct comparison | Dynamic min/max |
| **Use Case** | Single pass, fixed order | Dynamic selection |
| **Examples** | LC 55, 455, 1029 | LC 253, 621, 1046 |

### Greedy Core vs Dynamic Programming

| Aspect | Greedy Core | Dynamic Programming |
|--------|-------------|---------------------|
| **Decision** | Local optimal = Global optimal | Must consider all subproblems |
| **Backtracking** | Never reconsider | May reconsider via memoization |
| **Proof Required** | Greedy choice + optimal substructure | Recurrence relation |
| **Time Complexity** | Usually O(n) or O(n log n) | Often O(n^2) or O(n * state) |

### Three Kernels Comparison

| Kernel | Invariant | Key Technique | Problems |
|--------|-----------|---------------|----------|
| **Reachability** | Farthest reachable position | Single scan, max update | LC 55, 45 |
| **Prefix Min/Reset** | Running balance with reset | Deficit triggers reset | LC 134 |
| **Sort + Match** | Sorted order enables optimal | Two pointers / sorting | LC 135, 455, 1029 |


