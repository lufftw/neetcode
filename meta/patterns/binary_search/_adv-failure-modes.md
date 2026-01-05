## Binary Search Failure Modes

> **Core Insight**: Systematic error classification helps debug faster than trial-and-error.

### Failure Mode Taxonomy

#### Mode 1: Infinite Loop

**Symptom**: Program never terminates

**Causes**:
- `left = mid` with `mid = (left + right) // 2` when `right = left + 1`
- No boundary movement in some branch
- Wrong loop condition

**Fix**:
```python
# If doing left = mid, use ceiling division
mid = (left + right + 1) // 2

# Verify both branches move boundaries
if condition:
    right = mid      # or right = mid - 1
else:
    left = mid + 1   # Must have + 1
```

#### Mode 2: Boundary Never Moves

**Symptom**: Loop exits immediately or after 1 iteration

**Causes**:
- Wrong initial bounds
- Condition always True or always False
- Wrong inequality direction

**Fix**:
```python
# Check initial bounds include answer
assert left <= answer <= right

# Check predicate has transition
assert not predicate(left) and predicate(right)  # for first_true
```

#### Mode 3: Wrong Mid Bias

**Symptom**: Off-by-one errors, returns adjacent element

**Causes**:
- Using floor when ceiling needed (or vice versa)
- first_true vs last_true confusion

**Fix**:
```python
# first_true: floor division, move right
mid = (left + right) // 2
right = mid

# last_true: ceiling division, move left
mid = (left + right + 1) // 2
left = mid
```

#### Mode 4: Predicate Not Monotonic

**Symptom**: Wrong answer, inconsistent behavior

**Causes**:
- Predicate doesn't have clean F→T or T→F transition
- Multiple transitions in predicate

**Fix**:
```python
# Verify predicate is monotonic
# All False before all True (or vice versa)
[F, F, F, T, T, T]  # OK
[F, T, F, T, F, T]  # NOT OK - can't use binary search
```

#### Mode 5: Wrong Inequality Under Duplicates

**Symptom**: Finds wrong occurrence (first vs last)

**Causes**:
- Using `>` when should use `>=` (or vice versa)
- Not handling equality case correctly

**Fix**:
```python
# First occurrence: include mid in right part when equal
if arr[mid] >= target:
    right = mid

# Last occurrence: include mid in left part when equal
if arr[mid] <= target:
    left = mid
```

### Debug Checklist

When binary search fails, check in order:

1. ☐ **Bounds correct?** — Does `[left, right]` include the answer?
2. ☐ **Predicate monotonic?** — Clean F→T transition?
3. ☐ **Loop makes progress?** — Does interval shrink each iteration?
4. ☐ **Correct mid formula?** — Floor for first_true, ceiling for last_true?
5. ☐ **Boundary moves correct?** — Does answer stay in range?
6. ☐ **Return value correct?** — Return `left` or `right`?


