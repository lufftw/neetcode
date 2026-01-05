---

## Template Quick Reference

### 1. Basic Range Sum Query

```python
# Build prefix sum
prefix = [0]
for num in nums:
    prefix.append(prefix[-1] + num)

# Query [left, right]
range_sum = prefix[right + 1] - prefix[left]
```

### 2. Subarray Sum Equals K (Count)

```python
count = 0
prefix_sum = 0
sum_count = {0: 1}  # Initialize with empty prefix

for num in nums:
    prefix_sum += num
    count += sum_count.get(prefix_sum - k, 0)
    sum_count[prefix_sum] = sum_count.get(prefix_sum, 0) + 1
```

### 3. Longest Subarray with Sum K (or Transform)

```python
max_length = 0
prefix_sum = 0
first_occurrence = {0: -1}  # Initialize at "index -1"

for index, num in enumerate(nums):
    prefix_sum += num  # Or transformed value
    if prefix_sum in first_occurrence:
        max_length = max(max_length, index - first_occurrence[prefix_sum])
    else:
        first_occurrence[prefix_sum] = index
```

### 4. Difference Array (Range Updates)

```python
# Build difference array
diff = [0] * (n + 1)
for start, end, value in updates:
    diff[start] += value
    diff[end + 1] -= value  # Stop after end

# Reconstruct with prefix sum
result = []
current = 0
for i in range(n):
    current += diff[i]
    result.append(current)
```

### 5. 2D Prefix Sum

```python
# Build 2D prefix sum (with boundary zeros)
prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
for i in range(1, rows + 1):
    for j in range(1, cols + 1):
        prefix[i][j] = (matrix[i-1][j-1]
                       + prefix[i-1][j]
                       + prefix[i][j-1]
                       - prefix[i-1][j-1])

# Query rectangle (r1, c1) to (r2, c2)
def query(r1, c1, r2, c2):
    return (prefix[r2+1][c2+1] - prefix[r1][c2+1]
           - prefix[r2+1][c1] + prefix[r1][c1])
```

### 6. Prefix/Suffix Products (No Division)

```python
n = len(nums)
result = [1] * n

# Forward pass: prefix products
prefix = 1
for i in range(n):
    result[i] = prefix
    prefix *= nums[i]

# Backward pass: multiply by suffix products
suffix = 1
for i in range(n - 1, -1, -1):
    result[i] *= suffix
    suffix *= nums[i]
```

### Variable Naming Convention

| Variable | Purpose | Example |
|----------|---------|---------|
| `prefix_sum` | Running cumulative sum | `prefix_sum += num` |
| `sum_frequency` | Count of each prefix sum | `sum_frequency[prefix_sum]` |
| `first_occurrence` | First index of each prefix sum | `first_occurrence[prefix_sum] = index` |
| `current_seats` / `current` | Running value in prefix sum | `current += diff[i]` |
| `passenger_change` / `seat_change` | Difference array | `diff[start] += value` |


