# Binary Search: Advanced Concepts

> **Status**: Draft for Integration
> **Target**: `meta/patterns/binary_search/` footer files
> **Priority**: ⭐⭐⭐⭐⭐ (Foundation for pattern transferability)

This document contains 8 advanced concepts that will elevate binary search documentation to the same "transferable" level as sliding window.

---

## 1. Strict vs Non-Strict Inequality Strategy ⭐⭐⭐⭐⭐

> **Core Insight**: The choice between `<` and `<=` is not about "which is correct" — it's about **invariant definition**.

### The Real Pain Point

Many developers memorize `while left <= right` but don't understand **when to use `<` vs `<=`**. This leads to:
- Off-by-one errors
- Infinite loops
- Wrong boundary detection

### Two Canonical Loop Styles

#### Style 1: `while left <= right` (Closed Interval)

```python
# Invariant: answer is in [left, right] (inclusive both ends)
left, right = 0, len(arr) - 1
while left <= right:
    mid = (left + right) // 2
    if condition(mid):
        right = mid - 1  # Exclude mid, search [left, mid-1]
    else:
        left = mid + 1   # Exclude mid, search [mid+1, right]
# Loop ends when left > right (empty interval)
```

**Use when:**
- Finding exact match
- Need to check every element
- Return -1 if not found

**Examples:** 704 (Binary Search), 33 (Search in Rotated)

#### Style 2: `while left < right` (Half-Open Interval)

```python
# Invariant: answer is in [left, right) or [left, right]
left, right = 0, len(arr)  # Note: right = len(arr), not len(arr)-1
while left < right:
    mid = (left + right) // 2
    if condition(mid):
        right = mid        # Keep mid in range, search [left, mid]
    else:
        left = mid + 1     # Exclude mid, search [mid+1, right]
# Loop ends when left == right (single candidate)
```

**Use when:**
- Finding boundary (first/last true)
- Answer guaranteed to exist
- Need the boundary position

**Examples:** 34 (First/Last Position), 35 (Search Insert), 875 (Koko Bananas)

### Decision Matrix

| Question | Style 1 (`<=`) | Style 2 (`<`) |
|----------|---------------|---------------|
| Interval type | Closed `[l, r]` | Half-open `[l, r)` |
| Initial right | `len(arr) - 1` | `len(arr)` |
| When found | Move both boundaries | Move one boundary |
| Loop ends | `left > right` | `left == right` |
| Best for | Exact match | Boundary finding |

### Why This Matters for Duplicates

With duplicates (LC 34, 81), the inequality choice determines:
- Whether you find **first** or **last** occurrence
- Whether boundary **includes** or **excludes** target

```python
# Find FIRST occurrence of target
while left < right:
    mid = (left + right) // 2
    if arr[mid] >= target:  # Include mid in left part
        right = mid
    else:
        left = mid + 1

# Find LAST occurrence of target
while left < right:
    mid = (left + right + 1) // 2  # Bias right to avoid infinite loop
    if arr[mid] <= target:  # Include mid in right part
        left = mid
    else:
        right = mid - 1
```

### The Infinite Loop Trap

When `left < right` and you do `left = mid` (without +1), you risk infinite loop:

```
┌─────────────────────────────────────────────────┐
│  left = 3, right = 4                            │
│  mid = (3 + 4) // 2 = 3                         │
│  If left = mid → left = 3 (no progress!)        │
│                                                 │
│  Solution: Use mid = (left + right + 1) // 2    │
│  mid = (3 + 4 + 1) // 2 = 4                     │
│  Now left = mid → left = 4 (progress!)          │
└─────────────────────────────────────────────────┘
```

### Covered Problems

| Problem | Inequality | Why |
|---------|-----------|-----|
| 34 First/Last Position | `<` | Finding boundaries with duplicates |
| 81 Rotated with Duplicates | `<=` | Need to check all, worst case linear |
| 875 Koko Eating Bananas | `<` | Finding minimum feasible answer |
| 1011 Ship Packages | `<` | Finding minimum capacity |
| 410 Split Array | `<` | Minimizing maximum sum |

---

## 2. Existence vs Optimization Binary Search ⭐⭐⭐⭐⭐

> **Core Insight**: Is the problem asking "Does it exist?" or "What's the optimal value?"

### Two Fundamental Question Types

#### Type 1: Existence Query

**Question**: "Is target present?" / "Does a valid configuration exist?"

**Return Type**: `bool` or index (with -1 for not found)

**Template**:
```python
def exists(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return True  # or return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return False  # or return -1
```

**Characteristics**:
- Search terminates early on exact match
- Uses `left <= right` to check all candidates
- Often returns boolean or index

**Examples**: 704, 33, 81

#### Type 2: Optimization Query

**Question**: "What's the minimum/maximum valid value?"

**Return Type**: The actual value (int/float)

**Template**:
```python
def find_minimum(low, high, feasible):
    while low < high:
        mid = (low + high) // 2
        if feasible(mid):
            high = mid      # mid works, try smaller
        else:
            low = mid + 1   # mid doesn't work, need larger
    return low
```

**Characteristics**:
- Never terminates early (need to find optimal)
- Uses `left < right` to converge to answer
- Always returns a value (answer guaranteed to exist)

**Examples**: 875, 1011, 410, 774, 1283, 1482

### Side-by-Side Comparison

| Aspect | Existence | Optimization |
|--------|-----------|--------------|
| Question | "Is it there?" | "What's the best?" |
| Return type | `bool` / `int` (-1) | `int` / `float` |
| Early termination | Yes (on match) | No (need boundary) |
| Loop condition | `left <= right` | `left < right` |
| Search space | Array indices | Value range |
| Predicate | `arr[mid] == target` | `feasible(mid)` |

### Mapping to Template Choice

```
┌──────────────────────────────────────────────────────────┐
│  "Does X exist?"                                          │
│  ├── Yes → Use exact match template                       │
│  │         └── Returns: found index or -1                 │
│  │                                                        │
│  "What's the minimum/maximum X?"                          │
│  ├── Yes → Use first_true / last_true template            │
│  │         └── Returns: optimal value                     │
│  │                                                        │
│  Tip: Optimization often uses "first_true" for minimize   │
│       and "last_true" for maximize                        │
└──────────────────────────────────────────────────────────┘
```

### Why first_true vs last_true?

For **minimize** problems (find minimum valid value):
```python
# Find first speed where Koko can finish
# Predicate: can_finish(speed) returns True/False
# [F, F, F, T, T, T, T] → find first T
def first_true(lo, hi, predicate):
    while lo < hi:
        mid = (lo + hi) // 2
        if predicate(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

For **maximize** problems (find maximum valid value):
```python
# Find maximum pages per day such that reading finishes
# [T, T, T, T, F, F, F] → find last T
def last_true(lo, hi, predicate):
    while lo < hi:
        mid = (lo + hi + 1) // 2  # Bias right
        if predicate(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo
```

### Problem Classification

| Problem | Type | Return | Template |
|---------|------|--------|----------|
| 704 Binary Search | Existence | Index/-1 | Exact match |
| 33 Rotated Search | Existence | Index/-1 | Exact match + pivot |
| 81 Rotated (dupes) | Existence | bool | Exact match + linear fallback |
| 35 Search Insert | Optimization | Index | first_true (>= target) |
| 875 Koko Bananas | Optimization | Speed value | first_true (can finish) |
| 1011 Ship Packages | Optimization | Capacity | first_true (can ship) |
| 410 Split Array | Optimization | Max sum | first_true (can split) |

---

## 3. Search Domain Typing: Index vs Value Domain ⭐⭐⭐⭐⭐

> **Core Insight**: Binary search doesn't always run on array indices. Understanding the **domain** is crucial for correct setup.

### Two Domain Types

#### Index Domain (Positional Search)

**Search space**: Array indices `[0, n-1]`

**What you're finding**: The position/index of an element

**Initialization**:
```python
left, right = 0, len(arr) - 1  # or len(arr) for half-open
```

**Examples**:
- Find target in sorted array → index
- Find first occurrence → index
- Find peak element → index
- Find rotation pivot → index

#### Value Domain (Answer Space Search)

**Search space**: Range of possible answer values `[min_val, max_val]`

**What you're finding**: The actual answer value (not its position)

**Initialization**:
```python
# Bounds come from problem constraints, NOT array length
left = min_possible_answer
right = max_possible_answer
```

**Examples**:
- Minimum eating speed → the speed value
- Minimum ship capacity → the capacity value
- Maximum split sum → the sum value

### Why This Distinction Matters

Common mistakes when confusing domains:

| Mistake | Cause | Fix |
|---------|-------|-----|
| `left = 0, right = len(arr)` for value search | Using index bounds for value search | Use `left = min(arr), right = sum(arr)` |
| `return left` gives wrong value | Returning index when value needed | Ensure loop finds value, not position |
| `mid` interpretation wrong | Thinking mid is index, but it's value | Be explicit: `mid_speed`, `mid_capacity` |

### Domain Classification by Problem

#### Index Domain Problems

| Problem | Search For | Bounds | Returns |
|---------|-----------|--------|---------|
| 704 Binary Search | Target index | `[0, n-1]` | Index |
| 33 Rotated Search | Target index | `[0, n-1]` | Index |
| 34 First/Last Position | Boundary index | `[0, n-1]` | Index |
| 162 Peak Element | Peak index | `[0, n-1]` | Index |
| 153 Rotated Minimum | Pivot index | `[0, n-1]` | Index |

#### Value Domain Problems

| Problem | Search For | Bounds | Returns |
|---------|-----------|--------|---------|
| 875 Koko Bananas | Eating speed | `[1, max(piles)]` | Speed |
| 1011 Ship Packages | Ship capacity | `[max(weights), sum(weights)]` | Capacity |
| 410 Split Array | Maximum sum | `[max(nums), sum(nums)]` | Sum |
| 774 Minimize Max Distance | Distance | `[0, max_gap]` | Distance |
| 1482 Min Days for Bouquets | Days | `[1, max(bloomDay)]` | Days |

### Correct Bound Initialization

For **value domain** problems, bounds must guarantee the answer is included:

```python
# 875. Koko Eating Bananas
# Speed must be at least 1 (can't eat 0 bananas/hour)
# Speed at most max(piles) (can finish largest pile in 1 hour)
left, right = 1, max(piles)

# 1011. Capacity to Ship Packages
# Capacity must hold heaviest package
# Capacity at most total weight (ship everything in 1 day)
left, right = max(weights), sum(weights)

# 410. Split Array Largest Sum
# Min sum is largest element (one per subarray)
# Max sum is total (everything in one subarray)
left, right = max(nums), sum(nums)
```

### Visual Domain Comparison

```
┌─────────────────────────────────────────────────────────────────┐
│  Index Domain                                                    │
│  ──────────────                                                  │
│  Search space: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]                   │
│                 └─────── array indices ───────┘                  │
│  mid = 4 means: "check element at position 4"                   │
│                                                                  │
│  Value Domain                                                    │
│  ────────────                                                    │
│  Search space: [1, 2, 3, ..., 1000000]                          │
│                 └─── possible answer values ───┘                 │
│  mid = 500 means: "test if 500 is a valid answer"              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Boundary Stability Rule ⭐⭐⭐⭐⭐

> **Core Insight**: Why moving left/right this way is **always safe** — the correctness guarantee of binary search.

### The Fundamental Question

> "How do we know we're not skipping the answer when we move boundaries?"

This is the **correctness proof** that separates confident programmers from those who trial-and-error.

### The Invariant Guarantee

**Binary search correctness depends on maintaining this invariant**:

> After each iteration, the answer (if it exists) remains within `[left, right]`.

This means:
- When we move `left = mid + 1`, we're **certain** the answer is NOT in `[old_left, mid]`
- When we move `right = mid - 1` or `right = mid`, we're **certain** the answer is NOT in `(mid, old_right]`

### Why We Never Skip the Answer

#### For `first_true` (finding first True in [F,F,F,T,T,T]):

```python
while left < right:
    mid = (left + right) // 2
    if predicate(mid):  # mid is True
        right = mid     # Answer could be mid or before, keep mid
    else:               # mid is False
        left = mid + 1  # Answer must be after mid, exclude mid
```

**Proof of correctness**:
1. If `predicate(mid)` is True → answer is `<= mid` → keep mid in range
2. If `predicate(mid)` is False → answer is `> mid` → exclude mid safely

**Visual**:
```
[F, F, F, F, T, T, T, T]
             ↑
          boundary

If mid lands on F: answer is to the right → left = mid + 1 (safe)
If mid lands on T: answer is here or left → right = mid (safe)
```

#### For `last_true` (finding last True in [T,T,T,T,F,F,F]):

```python
while left < right:
    mid = (left + right + 1) // 2  # Bias right
    if predicate(mid):  # mid is True
        left = mid      # Answer could be mid or after, keep mid
    else:               # mid is False
        right = mid - 1 # Answer must be before mid, exclude mid
```

**Proof of correctness**:
1. If `predicate(mid)` is True → answer is `>= mid` → keep mid in range
2. If `predicate(mid)` is False → answer is `< mid` → exclude mid safely

### Comparison with Sliding Window Invariant

Like sliding window's "window always satisfies constraint", binary search has:

| Technique | Invariant | Guarantee |
|-----------|-----------|-----------|
| Sliding Window | Window always satisfies constraint | Expand/contract preserves validity |
| Binary Search | Answer always in `[left, right]` | Boundary moves preserve answer |

### Common Mistakes That Violate Stability

| Mistake | Why It Breaks | Fix |
|---------|--------------|-----|
| `left = mid` with floor division | May not progress when `right = left + 1` | Use `mid = (l + r + 1) // 2` |
| `right = mid - 1` in first_true | Might exclude the answer | Use `right = mid` |
| Moving both when unsure | Double-moves can skip answer | Move only the correct boundary |

### The Safety Checklist

Before finalizing binary search code, verify:

1. ✅ **Predicate is monotonic**: All F before all T (or vice versa)
2. ✅ **Boundary move preserves answer**: New range still contains answer
3. ✅ **Loop makes progress**: Interval shrinks every iteration
4. ✅ **Termination is correct**: Final `left` (or `right`) is the answer

---

## 5. Binary Search + Greedy Combination Pattern ⭐⭐⭐⭐⭐

> **Core Insight**: Many answer-space problems are "**Greedy feasibility check + Binary search over answers**".

### The Pattern Structure

```python
def solve(nums, constraint):
    left, right = min_answer, max_answer

    def is_feasible(candidate):
        """Greedy check: can we achieve this candidate value?"""
        # Use greedy algorithm to verify feasibility
        return greedy_check(nums, candidate, constraint)

    while left < right:
        mid = (left + right) // 2
        if is_feasible(mid):
            right = mid      # or left = mid for maximize
        else:
            left = mid + 1   # or right = mid - 1 for maximize
    return left
```

### Why This Pattern Is So Common

**The "capacity/rate/limit" family** all share this structure:

1. **Binary search** over the answer space (what's the optimal value?)
2. **Greedy simulation** to check feasibility (can this value work?)

The greedy part is crucial — it's **O(n)** and determines the overall **O(n log range)** complexity.

### Pattern Examples

#### 875. Koko Eating Bananas

```python
def minEatingSpeed(piles, h):
    left, right = 1, max(piles)

    def can_finish(speed):
        # Greedy: eat each pile, count hours
        hours = sum((pile + speed - 1) // speed for pile in piles)
        return hours <= h

    while left < right:
        mid = (left + right) // 2
        if can_finish(mid):
            right = mid
        else:
            left = mid + 1
    return left
```

#### 1011. Capacity to Ship Packages

```python
def shipWithinDays(weights, days):
    left, right = max(weights), sum(weights)

    def can_ship(capacity):
        # Greedy: load packages until capacity, count days
        day_count, current_load = 1, 0
        for w in weights:
            if current_load + w > capacity:
                day_count += 1
                current_load = 0
            current_load += w
        return day_count <= days

    while left < right:
        mid = (left + right) // 2
        if can_ship(mid):
            right = mid
        else:
            left = mid + 1
    return left
```

#### 410. Split Array Largest Sum

```python
def splitArray(nums, k):
    left, right = max(nums), sum(nums)

    def can_split(max_sum):
        # Greedy: start new subarray when sum exceeds max_sum
        splits, current_sum = 1, 0
        for num in nums:
            if current_sum + num > max_sum:
                splits += 1
                current_sum = 0
            current_sum += num
        return splits <= k

    while left < right:
        mid = (left + right) // 2
        if can_split(mid):
            right = mid
        else:
            left = mid + 1
    return left
```

### The Greedy Feasibility Check Pattern

All these problems share the same greedy structure:

```python
def is_feasible(limit):
    count = 1  # Start with 1 group/day/split
    current = 0

    for item in items:
        if current + item > limit:
            count += 1       # Start new group
            current = 0
        current += item

    return count <= allowed_groups
```

### Why This Matters for System Design

This pattern abstracts to:
- **Rate limiting**: What's the minimum rate to handle load?
- **Resource allocation**: What's the minimum capacity needed?
- **Load balancing**: What's the optimal split?

The predicate abstraction (`is_feasible`) is a powerful design pattern.

### Covered Problems

| Problem | Search For | Greedy Check |
|---------|-----------|--------------|
| 875 Koko Bananas | Min speed | Can eat all piles in h hours? |
| 1011 Ship Packages | Min capacity | Can ship all in d days? |
| 410 Split Array | Min max-sum | Can split into k subarrays? |
| 774 Min Max Distance | Min distance | Can place k gas stations? |
| 1482 Min Days | Min days | Can make m bouquets? |

---

## 6. Sentinel Bounds & Virtual Boundaries ⭐⭐⭐⭐

> **Core Insight**: `low` and `high` don't always come from the array — they come from **problem constraints**.

### Understanding Virtual Boundaries

For **answer space** problems, bounds are derived from:
- Problem constraints (min/max possible values)
- Mathematical guarantees (what must be true)

Not from:
- Array length
- Array indices

### Bound Derivation Patterns

#### Pattern 1: Minimum Capacity/Rate

The minimum must handle the largest single item:

```python
# Can't ship a package heavier than capacity
left = max(weights)

# Can't eat a pile bigger than speed × 1 hour
left = 1  # (or could be max(piles) if must finish each pile in 1 hour)
```

#### Pattern 2: Maximum Capacity/Rate

The maximum is when everything is in one group:

```python
# Ship everything in 1 day
right = sum(weights)

# Finish largest pile in 1 hour
right = max(piles)
```

### Common Bound Formulas

| Problem Type | left | right |
|-------------|------|-------|
| Min capacity | `max(items)` | `sum(items)` |
| Min speed | `1` | `max(items)` |
| Min time | `1` | `max(times)` |
| Max distance | `0` | `total_distance` |

### Why Beginners Get This Wrong

Common mistakes:

| Wrong | Why It's Wrong | Correct |
|-------|---------------|---------|
| `left = 0` for capacity | Can't have 0 capacity | `left = max(weights)` |
| `right = len(arr)` | Confusing index with value domain | `right = sum(arr)` |
| `left = 1` for all | Sometimes min must be larger | Analyze constraints |

### The Guarantee Principle

**Both bounds must guarantee the answer is included**:

1. `left` = smallest value that MIGHT work
2. `right` = largest value that DEFINITELY works

This ensures binary search can't miss the answer.

### Example: Why `max(weights)` for Shipping?

```
weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
days = 5

Q: Why can't capacity be 9?
A: We have a package weighing 10. Capacity 9 can't ship it.
   So capacity MUST be >= max(weights) = 10.

Q: Why is sum(weights) = 55 the upper bound?
A: With capacity 55, we can ship everything in 1 day.
   We'll never need more capacity than that.
```

---

## 7. Binary Search Failure Modes ⭐⭐⭐⭐

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

---

## 8. Binary Search vs Alternatives ⭐⭐⭐

> **Core Insight**: Know when NOT to use binary search.

### When Binary Search Applies

✅ **Use binary search when:**
- Sorted or monotonic property exists
- Search space can be halved by a predicate
- O(log n) gives meaningful improvement
- Clear true/false boundary exists

### When to Use Alternatives

#### Alternative 1: Hash Map (O(1) lookup)

**Use instead when:**
- Need exact match in unsorted data
- Multiple lookups expected
- Space O(n) is acceptable

**Example**: Two Sum (unsorted) — hash map beats sorting + binary search

#### Alternative 2: Two Pointers (O(n) traverse)

**Use instead when:**
- Need to examine pairs/triplets
- Sorted data but need all combinations
- Search + constraint is better expressed as pointer movement

**Example**: 3Sum — two pointers on sorted array

#### Alternative 3: Sliding Window

**Use instead when:**
- Contiguous subarray/substring
- Add/remove elements incrementally
- Window property is monotonic

**Example**: Minimum Window Substring — can't binary search, need sliding window

#### Alternative 4: Linear Scan

**Use instead when:**
- Data is small (n < 100)
- Binary search overhead not worth it
- Need to check all elements anyway

### Decision Matrix

| Problem Type | Binary Search | Alternative |
|-------------|---------------|-------------|
| Find in sorted array | ✅ Yes | - |
| Find in unsorted array | ❌ No | Hash map |
| Optimize with monotonic predicate | ✅ Yes | - |
| All pairs with constraint | ❌ No | Two pointers |
| Contiguous subarray optimization | ❌ No | Sliding window |
| Small n (< 100) | Maybe | Linear might be simpler |

### Boundary with Other Patterns

```
┌─────────────────────────────────────────────────────────────────┐
│                    Pattern Selection Guide                       │
├─────────────────────────────────────────────────────────────────┤
│  Sorted array + find element?                                    │
│  └── Binary Search                                               │
│                                                                  │
│  Sorted array + find pair summing to target?                    │
│  └── Two Pointers (not binary search each element)             │
│                                                                  │
│  Unsorted array + find pair summing to target?                  │
│  └── Hash Map                                                    │
│                                                                  │
│  Find optimal subarray length?                                   │
│  └── Sliding Window (if property monotonic in window size)     │
│  └── Binary Search (if answer space is discrete)               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Summary: The Complete Mental Model

These 8 concepts form a complete decision framework:

| # | Concept | Answers |
|---|---------|---------|
| 1 | Inequality Strategy | `<=` vs `<` — which loop style? |
| 2 | Existence vs Optimization | bool vs value — what to return? |
| 3 | Domain Typing | Index vs Value — what are bounds? |
| 4 | Boundary Stability | Why is this correct? |
| 5 | + Greedy Pattern | What's the O(n) feasibility check? |
| 6 | Sentinel Bounds | How to derive bounds? |
| 7 | Failure Modes | How to debug? |
| 8 | vs Alternatives | When NOT to use? |

With these concepts, binary search becomes as **transferable** as sliding window — a systematic approach rather than memorized templates.
