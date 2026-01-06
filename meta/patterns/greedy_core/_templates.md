---

## Template Quick Reference

### 1. Reachability (Can Reach End)

```python
def canReach(nums: List[int]) -> bool:
    farthest = 0
    for i in range(len(nums)):
        if i > farthest:
            return False
        farthest = max(farthest, i + nums[i])
    return True
```

### 2. Minimum Jumps (BFS-like Level Counting)

```python
def minJumps(nums: List[int]) -> int:
    if len(nums) <= 1:
        return 0

    jumps = 0
    current_end = 0
    next_farthest = 0

    for i in range(len(nums) - 1):
        next_farthest = max(next_farthest, i + nums[i])
        if i == current_end:
            jumps += 1
            current_end = next_farthest
    return jumps
```

### 3. Circular Route with Reset

```python
def findStart(gain: List[int], cost: List[int]) -> int:
    total = 0
    current = 0
    start = 0

    for i in range(len(gain)):
        net = gain[i] - cost[i]
        total += net
        current += net
        if current < 0:
            start = i + 1
            current = 0

    return start if total >= 0 else -1
```

### 4. Sort + Two-Pointer Match

```python
def greedyMatch(needs: List[int], supplies: List[int]) -> int:
    needs.sort()
    supplies.sort()

    matched = 0
    supply_idx = 0

    for need in needs:
        while supply_idx < len(supplies) and supplies[supply_idx] < need:
            supply_idx += 1
        if supply_idx < len(supplies):
            matched += 1
            supply_idx += 1

    return matched
```

### 5. Two-Pass (Bidirectional Constraints)

```python
def twoPassGreedy(values: List[int]) -> List[int]:
    n = len(values)
    result = [1] * n

    # Forward pass: left constraint
    for i in range(1, n):
        if values[i] > values[i - 1]:
            result[i] = result[i - 1] + 1

    # Backward pass: right constraint
    for i in range(n - 2, -1, -1):
        if values[i] > values[i + 1]:
            result[i] = max(result[i], result[i + 1] + 1)

    return result
```

### 6. Sort by Relative Advantage

```python
def optimalAssignment(costs: List[List[int]]) -> int:
    # costs[i] = [option_A_cost, option_B_cost]
    # Sort by advantage of A over B
    costs.sort(key=lambda x: x[0] - x[1])

    n = len(costs) // 2
    total = 0

    # First half to option A
    for i in range(n):
        total += costs[i][0]

    # Second half to option B
    for i in range(n, 2 * n):
        total += costs[i][1]

    return total
```

### Variable Naming Convention

| Variable | Purpose | Example |
|----------|---------|---------|
| `farthest` / `farthest_reachable` | Maximum reachable position | `farthest = max(farthest, i + nums[i])` |
| `current_end` | Boundary of current level/jump | `if i == current_end: jumps += 1` |
| `current_surplus` / `current` | Running balance since reset | `current += gain[i] - cost[i]` |
| `candidate_start` | Reset point candidate | `candidate_start = i + 1` |
| `satisfied_count` / `matched` | Count of successful matches | `matched += 1` |


