## Search Domain Typing: Index vs Value Domain

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


