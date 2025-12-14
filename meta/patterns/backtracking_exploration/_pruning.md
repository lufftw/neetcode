## Pruning Techniques

### Pruning Categories

| Category | Description | Example |
|----------|-------------|---------|
| **Feasibility Bound** | Remaining elements can't satisfy constraints | Combinations: not enough elements left |
| **Target Bound** | Current path already exceeds target | Combination Sum: sum > target |
| **Constraint Propagation** | Future choices are forced/impossible | N-Queens: no valid columns left |
| **Sorted Early Exit** | If sorted, larger elements also fail | Combination Sum with sorted candidates |

### Pruning Patterns

```python
# 1. Not enough elements left (Combinations)
if remaining_elements < elements_needed:
    return

# 2. Exceeded target (Combination Sum)
if current_sum > target:
    return

# 3. Sorted early break (when candidates sorted)
if candidates[i] > remaining:
    break  # All subsequent are larger

# 4. Length/count bound
if len(path) > max_allowed:
    return
```

