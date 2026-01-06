# Bitmask DP Pattern

## API Kernel: `BitmaskDP`

> **Core Mechanism**: Represent set states using integers as bitmasks, enabling efficient DP over subsets with O(1) state transitions.

## Why Bitmask DP?

Bitmask DP solves problems where:
- You need to track "which items are selected/visited"
- State space is over subsets of a small set (n ≤ 20)
- Standard DP would have exponential states

## Core Insight

An integer's binary representation encodes a subset:
```
Set: {A, B, C, D}  (indices 0, 1, 2, 3)

Bitmask   Binary   Subset
0         0000     {}
5         0101     {A, C}
15        1111     {A, B, C, D}
```

## Bit Manipulation Cheat Sheet

| Operation | Code | Example |
|-----------|------|---------|
| Set bit i | `mask | (1 << i)` | Add element i |
| Clear bit i | `mask & ~(1 << i)` | Remove element i |
| Check bit i | `(mask >> i) & 1` | Is i in set? |
| Toggle bit i | `mask ^ (1 << i)` | Flip membership |
| Count bits | `bin(mask).count('1')` | Set size |
| All bits set | `(1 << n) - 1` | Full set |

## Universal Template Structure

```python
def bitmask_dp(n, items):
    # State: dp[mask] = value for subset represented by mask
    # Iterate over all 2^n subsets
    for mask in range(1 << n):
        for i in range(n):
            if mask & (1 << i):  # If i is in current subset
                prev_mask = mask ^ (1 << i)  # Subset without i
                dp[mask] = transition(dp[prev_mask], items[i])

    return dp[(1 << n) - 1]  # Full set
```

## Pattern Variants

| Pattern | State | Transition | Example |
|---------|-------|------------|---------|
| **Subset Enumeration** | Generate all subsets | Bit operations | Subsets |
| **TSP-style** | dp[mask][last] | Visit new node | Shortest Path All Nodes |
| **Set Cover** | dp[mask] | Add person's skills | Smallest Sufficient Team |
| **Subset Sum** | dp[mask] | Include/exclude | Partition Equal Subset |

## State Space Analysis

For n elements:
- Number of subsets: 2^n
- Memory: O(2^n) for bitmask states
- Practical limit: n ≤ 20 (2^20 ≈ 10^6)

## Common Patterns

### Pattern 1: Generate All Subsets
```python
def subsets(nums):
    n = len(nums)
    result = []
    for mask in range(1 << n):
        subset = [nums[i] for i in range(n) if mask & (1 << i)]
        result.append(subset)
    return result
```

### Pattern 2: TSP / Hamiltonian Path
```python
# dp[mask][last] = min cost to visit nodes in mask, ending at last
for mask in range(1, 1 << n):
    for last in range(n):
        if not (mask & (1 << last)):
            continue
        prev_mask = mask ^ (1 << last)
        for prev in range(n):
            if prev_mask & (1 << prev):
                dp[mask][last] = min(dp[mask][last],
                                     dp[prev_mask][prev] + cost[prev][last])
```

### Pattern 3: Set Cover
```python
# dp[mask] = min items to cover skills in mask
for i in range(num_people):
    skill_mask = encode_skills(people[i])
    for mask in range(1 << num_skills):
        new_mask = mask | skill_mask
        dp[new_mask] = min(dp[new_mask], dp[mask] + 1)
```
