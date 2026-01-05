## Binary Search + Greedy Combination Pattern

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


