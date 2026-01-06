## Problem Comparison

| Problem | Core Pattern | State | Transition | Output |
|---------|-------------|-------|------------|--------|
| **78. Subsets** | Subset Enumeration | mask (visited) | Decode mask to subset | List of subsets |
| **847. Shortest Path** | BFS + Bitmask | (node, mask) | `mask | (1 << neighbor)` | Min path length |
| **1125. Smallest Team** | Set Cover DP | mask (skills) | `mask | person_skills` | Min team members |

## Pattern Evolution

```
Subset Enumeration (LC 78)
        ↓
    Pure bitmask iteration
    No DP needed
        ↓
BFS + Bitmask (LC 847)
        ↓
    Add position to state
    BFS for shortest path
        ↓
Set Cover DP (LC 1125)
        ↓
    Optimization DP
    Track minimum team
```

## Key Differences

### 1. State Complexity

| Problem | State Dimensions | State Space |
|---------|-----------------|-------------|
| LC 78 | 1D (mask only) | O(2^n) |
| LC 847 | 2D (node, mask) | O(n × 2^n) |
| LC 1125 | 1D (mask) + team | O(2^m) |

### 2. Traversal Strategy

| Problem | Strategy | Why |
|---------|----------|-----|
| LC 78 | Linear enumeration | Generate all subsets |
| LC 847 | BFS | Shortest path in unweighted graph |
| LC 1125 | DP with iteration | Minimize team size |

### 3. Constraint Limits

| Problem | n/m Limit | State Space | Why Limit |
|---------|-----------|-------------|-----------|
| LC 78 | n ≤ 10 | 2^10 = 1024 | Generate all subsets |
| LC 847 | n ≤ 12 | 12 × 2^12 ≈ 50K | BFS state space |
| LC 1125 | m ≤ 16 | 2^16 = 65K | DP state space |

## Common Bit Operations Across Problems

```python
# All three problems use these operations:

# 1. Set bit i (add element)
mask | (1 << i)

# 2. Check bit i (is element present?)
mask & (1 << i)  # or (mask >> i) & 1

# 3. Full mask (all elements)
(1 << n) - 1

# 4. Iterate bits
for i in range(n):
    if mask & (1 << i):
        # Process element i
```

## When to Use Each Pattern

| If you need to... | Use Pattern | Example |
|-------------------|-------------|---------|
| Generate all subsets | Enumeration (LC 78) | Subsets, Combinations |
| Find shortest path visiting all | BFS + Bitmask (LC 847) | TSP variants |
| Cover requirements with minimum | Set Cover DP (LC 1125) | Team building, task assignment |
