# Prefix Sum Patterns: Complete Reference

> **API Kernel**: `PrefixSumRangeQuery`
> **Core Mechanism**: Precompute cumulative sums for O(1) range sum queries.

This document presents the **canonical prefix sum template** and all its major variations. Each implementation follows consistent naming conventions and includes detailed logic explanations.

---

## Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Base Template: Range Sum Query (LeetCode 303)](#2-base-template-range-sum-query-leetcode-303)
3. [Subarray Sum Equals K (LeetCode 560)](#3-subarray-sum-equals-k-leetcode-560)
4. [Contiguous Array (LeetCode 525)](#4-contiguous-array-leetcode-525)
5. [Continuous Subarray Sum (LeetCode 523)](#5-continuous-subarray-sum-leetcode-523)
6. [Range Sum Query 2D (LeetCode 304)](#6-range-sum-query-2d-leetcode-304)
7. [Product of Array Except Self (LeetCode 238)](#7-product-of-array-except-self-leetcode-238)
8. [Car Pooling (LeetCode 1094)](#8-car-pooling-leetcode-1094)
9. [Corporate Flight Bookings (LeetCode 1109)](#9-corporate-flight-bookings-leetcode-1109)
10. [Pattern Comparison](#10-pattern-comparison)
11. [Decision Flowchart](#11-decision-flowchart)
12. [Template Quick Reference](#12-template-quick-reference)

---

## 1. Core Concepts

### 1.1 The Prefix Sum Principle

Given an array `nums`, the prefix sum `P[i]` represents the sum of elements from index 0 to i-1:

```
nums:   [a, b, c, d, e]
        ↓  ↓  ↓  ↓  ↓
prefix: [0, a, a+b, a+b+c, a+b+c+d, a+b+c+d+e]
         ↑
         Empty prefix (crucial for index 0 queries)
```

**Key Formula**: Range sum `[i, j]` = `prefix[j+1] - prefix[i]`

### 1.2 Universal Template Structure

```python
def build_prefix_sum(nums: List[int]) -> List[int]:
    """
    Build prefix sum array.

    prefix[i] = sum of nums[0..i-1] (elements BEFORE index i)
    Range sum [left, right] = prefix[right+1] - prefix[left]

    Why prefix[0] = 0?
    - Handles range queries starting at index 0: sum[0..right] = prefix[right+1] - prefix[0]
    - Without it, we'd need special case handling for left=0
    """
    prefix = [0]  # Empty prefix
    for num in nums:
        prefix.append(prefix[-1] + num)
    return prefix
```

### 1.3 Pattern Variants

| Variant | API Kernel | Use When | Key Insight |
|---------|------------|----------|-------------|
| **Range Query** | `PrefixSumRangeQuery` | Multiple range sum queries | Precompute once, query O(1) |
| **Subarray Sum = K** | `PrefixSumSubarraySum` | Count/find subarrays with target sum | Hash map: `prefix - k` |
| **Difference Array** | `DifferenceArray` | Range update operations | Inverse of prefix sum |
| **2D Prefix Sum** | `PrefixSum2D` | Rectangle sum queries | Inclusion-exclusion principle |
| **Prefix Product** | `PrefixProduct` | Product of array except self | Prefix and suffix products |

### 1.4 Why Sliding Window Fails for Subarray Sum

With negative numbers, adding an element may increase or decrease the sum, breaking the monotonicity required for sliding window. Prefix sum + hash map handles this in O(n).

```
nums = [1, -1, 1]  k = 1
Window [0,0] sum=1  ✓
Window [0,1] sum=0  ✗ (but subarrays [0,0], [2,2], [0,2] all sum to 1!)

Sliding window would miss valid subarrays because sum is not monotonic.
```

---

## 2. Base Template: Range Sum Query (LeetCode 303)

> **Problem**: Handle multiple range sum queries on an immutable array efficiently.
> **Invariant**: `prefix[i]` = sum of all elements before index `i`.
> **Role**: BASE TEMPLATE for `PrefixSumRangeQuery` API Kernel.

### 2.1 Implementation

```python
class NumArray:
    """
    Range sum query with O(n) preprocessing and O(1) queries.

    Prefix Sum Mechanics:
    - prefix[0] = 0 (empty prefix, handles edge case of full array sum)
    - prefix[i] = sum(nums[0:i])
    - Range sum [left, right] = prefix[right+1] - prefix[left]

    Why prefix[right+1] - prefix[left]?
    prefix[right+1] = nums[0] + nums[1] + ... + nums[right]
    prefix[left]    = nums[0] + nums[1] + ... + nums[left-1]
    Difference      = nums[left] + nums[left+1] + ... + nums[right]

    Time: O(n) init, O(1) query | Space: O(n)
    """
    def __init__(self, nums: List[int]):
        # Initialize with 0 for empty prefix
        self.prefix_sum: List[int] = [0]
        for num in nums:
            self.prefix_sum.append(self.prefix_sum[-1] + num)

    def sumRange(self, left: int, right: int) -> int:
        return self.prefix_sum[right + 1] - self.prefix_sum[left]
```

### 2.2 Why This Works

```
Index:    0   1   2   3   4    5
nums:   [-2,  0,  3, -5,  2,  -1]
prefix: [0, -2, -2,  1, -4, -2, -3]
         ^
         Empty prefix

Query sumRange(0, 2):
  = prefix[3] - prefix[0]
  = 1 - 0 = 1
  = nums[0] + nums[1] + nums[2] = -2 + 0 + 3 = 1 ✓

Query sumRange(2, 5):
  = prefix[6] - prefix[2]
  = -3 - (-2) = -1
  = nums[2] + nums[3] + nums[4] + nums[5] = 3 + (-5) + 2 + (-1) = -1 ✓
```

### 2.3 Edge Cases

| Case | How Handled |
|------|-------------|
| Query entire array `[0, n-1]` | `prefix[n] - prefix[0]` = total sum |
| Single element `[i, i]` | `prefix[i+1] - prefix[i]` = `nums[i]` |
| Empty array | `prefix = [0]`, no valid queries |

---

## 3. Subarray Sum Equals K (LeetCode 560)

> **Problem**: Count the number of contiguous subarrays with sum equal to k.
> **Invariant**: Hash map stores count of each prefix sum seen so far.
> **Role**: CORE VARIANT for `PrefixSumSubarraySum` API Kernel.

### 3.1 Why Prefix Sum + Hash Map?

If `prefix[j] - prefix[i] = k`, then subarray `(i, j]` sums to k.

**Key Insight**: For each position j, count how many positions i exist where `prefix[i] = prefix[j] - k`.

```
nums = [1, 2, 3], k = 3

Position 0: prefix = 1, need prefix = -2 (count: 0)
Position 1: prefix = 3, need prefix = 0  (count: 1 from init)  -> Found: subarray [0,1]
Position 2: prefix = 6, need prefix = 3  (count: 1)            -> Found: subarray [2,2]

Answer: 2 subarrays with sum = 3
```

### 3.2 Implementation

```python
class SolutionPrefixSum:
    """
    Count subarrays with sum = k using prefix sum + hash map.

    Algorithm:
    1. Track running prefix sum
    2. For each position, count how many times (prefix_sum - k) appeared before
    3. Record current prefix sum for future positions

    Why Initialize {0: 1}?
    - Handles subarrays starting from index 0
    - If prefix_sum == k at position i, the subarray [0..i] sums to k
    - We need to count the "empty prefix" (sum 0 before index 0)

    Time: O(n) | Space: O(n)
    """
    def subarraySum(self, nums: List[int], k: int) -> int:
        subarray_count = 0
        prefix_sum = 0

        # Map: prefix_sum value -> count of occurrences
        # Initialize with {0: 1} for subarrays starting at index 0
        sum_frequency: dict[int, int] = {0: 1}

        for num in nums:
            # Extend prefix sum with current element
            prefix_sum += num

            # Count subarrays ending here with sum = k
            # If (prefix_sum - k) was seen before, those positions mark valid starts
            complement = prefix_sum - k
            subarray_count += sum_frequency.get(complement, 0)

            # Record current prefix sum for future elements
            sum_frequency[prefix_sum] = sum_frequency.get(prefix_sum, 0) + 1

        return subarray_count
```

### 3.3 Trace Example

```
nums = [1, 1, 1], k = 2

Step 0: prefix=1, complement=-1, count=0, map={0:1, 1:1}
Step 1: prefix=2, complement=0,  count=1, map={0:1, 1:1, 2:1}  [subarray [0,1]]
Step 2: prefix=3, complement=1,  count=2, map={0:1, 1:1, 2:1, 3:1}  [subarray [1,2]]

Answer: 2
```

### 3.4 Why {0: 1} Initialization is Critical

Without `{0: 1}`:
```
nums = [3], k = 3
prefix = 3, complement = 0
sum_frequency = {} -> count = 0  WRONG! Should be 1.
```

With `{0: 1}`:
```
nums = [3], k = 3
prefix = 3, complement = 0
sum_frequency = {0: 1} -> count = 1  ✓
```

---

## 4. Contiguous Array (LeetCode 525)

> **Problem**: Find the maximum length of a contiguous subarray with equal number of 0s and 1s.
> **Transform**: Convert 0 -> -1, then find longest subarray with sum = 0.
> **Role**: TRANSFORM VARIANT demonstrating problem reduction.

### 4.1 The Transform Insight

Original problem: Count of 0s = Count of 1s in subarray
After transform (0 -> -1): Sum of subarray = 0

```
Original: [0, 1, 0, 1, 1, 0]
Transform: [-1, 1, -1, 1, 1, -1]

Subarray [0,3]: Original has 2 zeros, 2 ones ✓
                Transform sum = -1+1+(-1)+1 = 0 ✓
```

### 4.2 Implementation

```python
class SolutionTransform:
    """
    Find longest subarray with equal 0s and 1s.

    Transform Technique:
    1. Replace 0 with -1 in the conceptual array
    2. Problem becomes: find longest subarray with sum = 0
    3. Use prefix sum + hash map (first occurrence)

    Why First Occurrence?
    - To maximize length, we want earliest position with same prefix sum
    - prefix[j] - prefix[i] = 0 means subarray (i, j] is balanced
    - Smaller i = longer subarray

    Time: O(n) | Space: O(n)
    """
    def findMaxLength(self, nums: List[int]) -> int:
        max_length = 0
        prefix_sum = 0

        # Map: prefix_sum value -> first index where this sum occurred
        # Initialize with {0: -1} for subarrays starting at index 0
        first_occurrence: dict[int, int] = {0: -1}

        for index, num in enumerate(nums):
            # Transform: treat 0 as -1
            prefix_sum += 1 if num == 1 else -1

            if prefix_sum in first_occurrence:
                # Found a balanced subarray from (first_occurrence + 1) to current
                length = index - first_occurrence[prefix_sum]
                max_length = max(max_length, length)
            else:
                # Record first occurrence for maximum length
                first_occurrence[prefix_sum] = index

        return max_length
```

### 4.3 Trace Example

```
nums = [0, 1, 0]
transform = [-1, 1, -1]

Index 0: prefix=-1, first_occurrence={0:-1, -1:0}
Index 1: prefix=0,  0 in map at -1, length=1-(-1)=2  -> max=2
Index 2: prefix=-1, -1 in map at 0, length=2-0=2    -> max=2

Answer: 2 (subarray [0,1] has one 0 and one 1)
```

### 4.4 Why {0: -1} Initialization

Handles subarrays starting at index 0:
```
nums = [0, 1]
prefix sums: -1, 0

At index 1: prefix=0, need to find 0 in map
With {0: -1}: length = 1 - (-1) = 2 ✓
Without {0: -1}: 0 not in map, miss the answer
```

---

## 5. Continuous Subarray Sum (LeetCode 523)

> **Problem**: Check if array has a contiguous subarray of size >= 2 that sums to a multiple of k.
> **Invariant**: If `prefix[j] % k == prefix[i] % k`, then subarray (i, j] sum is divisible by k.
> **Role**: MODULAR ARITHMETIC VARIANT of prefix sum.

### 5.1 The Modular Arithmetic Insight

If `prefix[j] - prefix[i]` is divisible by k, then:
`prefix[j] % k == prefix[i] % k`

This is because:
```
prefix[j] = q1 * k + r
prefix[i] = q2 * k + r  (same remainder r)
prefix[j] - prefix[i] = (q1 - q2) * k  (divisible by k!)
```

### 5.2 Implementation

```python
class SolutionModular:
    """
    Check if subarray of size >= 2 sums to multiple of k.

    Modular Arithmetic Insight:
    - (prefix[j] - prefix[i]) % k == 0 iff prefix[j] % k == prefix[i] % k
    - Track first occurrence of each remainder
    - Ensure subarray length >= 2: j - i >= 2

    Edge Case: k = 0 is not possible per constraints (k >= 1)

    Time: O(n) | Space: O(min(n, k))
    """
    def checkSubarraySum(self, nums: List[int], k: int) -> bool:
        # Map: remainder -> first index with this remainder
        # Initialize with {0: -1} for subarrays starting at index 0
        remainder_first_index: dict[int, int] = {0: -1}
        prefix_sum = 0

        for index, num in enumerate(nums):
            prefix_sum += num
            remainder = prefix_sum % k

            if remainder in remainder_first_index:
                # Check if subarray length >= 2
                if index - remainder_first_index[remainder] >= 2:
                    return True
            else:
                # Only store first occurrence (to maximize length)
                remainder_first_index[remainder] = index

        return False
```

### 5.3 Trace Example

```
nums = [23, 2, 4, 6, 7], k = 6

Index 0: prefix=23, rem=5, map={0:-1, 5:0}
Index 1: prefix=25, rem=1, map={0:-1, 5:0, 1:1}
Index 2: prefix=29, rem=5, 5 in map at 0, length=2-0=2 >= 2  -> True!

Subarray [2, 4] sums to 6, divisible by 6 ✓
```

### 5.4 Why Length >= 2 Check

Problem requires subarray of size at least 2:
```
nums = [5], k = 5
prefix = 5, remainder = 0

0 is in map at -1, length = 0 - (-1) = 1 < 2  -> False (correct!)
```

### 5.5 Edge Cases

| Case | Handling |
|------|----------|
| Consecutive zeros `[0, 0]` | prefix = 0 at both, 0 % k = 0, length 2 ✓ |
| Single element | Always false (length < 2) |
| k = 1 | Any subarray of size >= 2 works |

---

## 6. Range Sum Query 2D (LeetCode 304)

> **Problem**: Handle multiple rectangle sum queries on an immutable 2D matrix.
> **Invariant**: `prefix[i][j]` = sum of all elements in rectangle from (0,0) to (i-1, j-1).
> **Role**: 2D EXTENSION using inclusion-exclusion principle.

### 6.1 2D Prefix Sum Principle

For a 2D matrix, prefix sum extends naturally using inclusion-exclusion:

```
Building prefix[i][j]:
┌─────┬───────────┐
│  A  │     B     │
├─────┼───────────┤
│  C  │ (i-1,j-1) │
└─────┴───────────┘

prefix[i][j] = matrix[i-1][j-1] + prefix[i-1][j] + prefix[i][j-1] - prefix[i-1][j-1]
             = current cell    + top          + left          - overlap (counted twice)
```

### 6.2 Rectangle Sum Query

```
Querying region from (row1, col1) to (row2, col2):
┌─────────────────────────┐
│  A  │        B          │
├─────┼──────────┬────────┤
│     │ ████████ │        │
│  C  │ █TARGET█ │   D    │
│     │ ████████ │        │
├─────┴──────────┴────────┤
│           E             │
└─────────────────────────┘

TARGET = Total - B - C + A
       = prefix[r2+1][c2+1] - prefix[r1][c2+1] - prefix[r2+1][c1] + prefix[r1][c1]
```

### 6.3 Implementation

```python
class NumMatrix:
    """
    2D range sum query with O(m*n) preprocessing and O(1) queries.

    Prefix Sum 2D:
    - Extra row and column of zeros simplify boundary handling
    - prefix[i][j] = sum of rectangle from (0,0) to (i-1, j-1)
    - Uses inclusion-exclusion principle for both building and querying

    Time: O(m*n) init, O(1) query | Space: O(m*n)
    """
    def __init__(self, matrix: List[List[int]]):
        if not matrix or not matrix[0]:
            self.prefix_sum = [[0]]
            return

        row_count, col_count = len(matrix), len(matrix[0])

        # Extra row and column of zeros for boundary handling
        self.prefix_sum = [[0] * (col_count + 1) for _ in range(row_count + 1)]

        # Build prefix sum using inclusion-exclusion
        for row in range(1, row_count + 1):
            for col in range(1, col_count + 1):
                self.prefix_sum[row][col] = (
                    matrix[row - 1][col - 1]
                    + self.prefix_sum[row - 1][col]      # Top rectangle
                    + self.prefix_sum[row][col - 1]      # Left rectangle
                    - self.prefix_sum[row - 1][col - 1]  # Subtract overlap
                )

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return (
            self.prefix_sum[row2 + 1][col2 + 1]  # Total (origin to bottom-right)
            - self.prefix_sum[row1][col2 + 1]    # Subtract top strip
            - self.prefix_sum[row2 + 1][col1]    # Subtract left strip
            + self.prefix_sum[row1][col1]        # Add back top-left (subtracted twice)
        )
```

### 6.4 Trace Example

```
matrix = [
  [3, 0, 1, 4, 2],
  [5, 6, 3, 2, 1],
  [1, 2, 0, 1, 5]
]

prefix (with boundary zeros):
[0,  0,  0,  0,  0,  0]
[0,  3,  3,  4,  8, 10]
[0,  8, 14, 18, 24, 27]
[0,  9, 17, 21, 28, 36]

Query sumRegion(1, 1, 2, 2):
= prefix[3][3] - prefix[1][3] - prefix[3][1] + prefix[1][1]
= 21 - 4 - 9 + 3
= 11

Verification: 6 + 3 + 2 + 0 = 11 ✓
```

---

## 7. Product of Array Except Self (LeetCode 238)

> **Problem**: Return array where each element is the product of all other elements, without division.
> **Insight**: `result[i] = prefix_product[0..i-1] * suffix_product[i+1..n-1]`
> **Role**: PREFIX/SUFFIX PRODUCT VARIANT applying prefix sum concept to multiplication.

### 7.1 Prefix and Suffix Products

```
nums:           [1,    2,    3,    4]
prefix_product: [1,    1,    2,    6]   (product of elements BEFORE i)
suffix_product: [24,   12,   4,    1]   (product of elements AFTER i)
result:         [24,   12,   8,    6]   (prefix[i] * suffix[i])
```

### 7.2 Implementation (O(1) Extra Space)

```python
class SolutionPrefixSuffix:
    """
    Compute product of array except self without division.

    Two-pass Approach:
    1. Left-to-right: Build prefix products in result array
    2. Right-to-left: Multiply by suffix products using single variable

    Why No Division?
    - Problem explicitly forbids it (challenge constraint)
    - Division fails with zeros in the array
    - This approach handles zeros correctly

    Time: O(n) | Space: O(1) excluding output
    """
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        array_length = len(nums)
        result = [1] * array_length

        # Pass 1: Build prefix products
        # After this pass, result[i] = product of nums[0..i-1]
        prefix_product = 1
        for index in range(array_length):
            result[index] = prefix_product
            prefix_product *= nums[index]

        # Pass 2: Multiply by suffix products
        # After this pass, result[i] = prefix[0..i-1] * suffix[i+1..n-1]
        suffix_product = 1
        for index in range(array_length - 1, -1, -1):
            result[index] *= suffix_product
            suffix_product *= nums[index]

        return result
```

### 7.3 Trace Example

```
nums = [1, 2, 3, 4]

Pass 1 (Prefix):
index=0: result=[1,1,1,1], prefix=1*1=1
index=1: result=[1,1,1,1], prefix=1*2=2
index=2: result=[1,1,2,1], prefix=2*3=6
index=3: result=[1,1,2,6], prefix=6*4=24

Pass 2 (Suffix):
index=3: result=[1,1,2,6*1=6], suffix=1*4=4
index=2: result=[1,1,2*4=8,6], suffix=4*3=12
index=1: result=[1,1*12=12,8,6], suffix=12*2=24
index=0: result=[1*24=24,12,8,6], suffix=24*1=24

Answer: [24, 12, 8, 6]
```

### 7.4 Handling Zeros

This approach handles zeros naturally:
```
nums = [1, 0, 3]
prefix: [1, 1, 0]    (0 appears after we see the zero)
suffix: [0, 3, 1]    (0 appears before we see the zero)
result: [0, 3, 0]    (only the zero position gets non-zero)
```

---

## 8. Car Pooling (LeetCode 1094)

> **Problem**: Check if a car can pick up and drop off all passengers without exceeding capacity.
> **Insight**: Model as range updates; use difference array to track passenger count changes.
> **Role**: DIFFERENCE ARRAY VARIANT (inverse of prefix sum).

### 8.1 Difference Array Principle

Difference array is the **inverse** of prefix sum:
- **Prefix Sum**: Given point values, compute range sums in O(1)
- **Difference Array**: Given range updates, compute point values in O(n)

```
To add 'value' to range [start, end]:
  diff[start] += value   (start adding)
  diff[end+1] -= value   (stop adding after end)

Prefix sum of diff = actual values at each point
```

### 8.2 Implementation

```python
class SolutionDifferenceArray:
    """
    Check if car pooling is feasible using difference array.

    Difference Array Technique:
    1. Record passenger changes at pickup/dropoff locations
    2. Prefix sum gives actual passenger count at each location
    3. Verify no location exceeds capacity

    Key Insight:
    - Passengers board at 'from' location
    - Passengers exit at 'to' location (NOT inclusive - they're gone before 'to')
    - This creates range [from, to) updates

    Time: O(n + m) where n = trips, m = max location | Space: O(m)
    """
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        # Find max location to determine array size
        max_location = max(trip[2] for trip in trips)

        # Difference array: diff[i] = change in passenger count at location i
        passenger_change = [0] * (max_location + 1)

        # Build difference array
        for passengers, pickup_location, dropoff_location in trips:
            passenger_change[pickup_location] += passengers    # Passengers board
            passenger_change[dropoff_location] -= passengers   # Passengers exit

        # Prefix sum to compute actual passenger count at each location
        current_passengers = 0
        for delta in passenger_change:
            current_passengers += delta
            if current_passengers > capacity:
                return False

        return True
```

### 8.3 Trace Example

```
trips = [[2,1,5],[3,3,7]], capacity = 4

Location:  0   1   2   3   4   5   6   7
           ↓   ↓   ↓   ↓   ↓   ↓   ↓   ↓
diff:     [0, +2,  0, +3,  0, -2,  0, -3]

Prefix sum (passengers at each location):
loc 0: 0
loc 1: 0 + 2 = 2  ✓
loc 2: 2 + 0 = 2  ✓
loc 3: 2 + 3 = 5  > 4  ✗

Answer: False (exceeds capacity at location 3)
```

### 8.4 Why Dropoff is Exclusive

Passengers exit BEFORE the dropoff location:
```
Trip: [2, 1, 3] means 2 passengers from location 1 to 3
At location 3, they're already gone!

diff[1] += 2  (board at 1)
diff[3] -= 2  (exit at 3, so location 3 has no extra passengers)
```

---

## 9. Corporate Flight Bookings (LeetCode 1109)

> **Problem**: Given flight bookings with range [first, last] and seat count, compute total seats for each flight.
> **Insight**: Classic difference array for range updates, prefix sum to get final counts.
> **Role**: CANONICAL DIFFERENCE ARRAY problem (range update → point query).

### 9.1 Problem Structure

Each booking `[first, last, seats]` adds `seats` to flights `first` through `last` (inclusive).

```
Booking [1, 3, 10] means:
Flight 1: +10 seats
Flight 2: +10 seats
Flight 3: +10 seats

Using difference array:
diff[1-1] += 10   (start adding at flight 1, 0-indexed)
diff[3] -= 10     (stop adding after flight 3)
```

### 9.2 Implementation

```python
class SolutionDifferenceArray:
    """
    Compute total seats reserved for each flight using difference array.

    Difference Array Mechanics:
    - diff[i] = change in seat count at flight i
    - To add 'seats' to range [first, last] (1-indexed):
      diff[first-1] += seats   (start adding, convert to 0-indexed)
      diff[last] -= seats      (stop adding after last)
    - Prefix sum reconstructs actual seat counts

    Why O(n + m)?
    - O(m) to process all bookings (each is O(1))
    - O(n) to compute prefix sum
    - Much better than O(n * m) naive approach

    Time: O(n + m) where n = flights, m = bookings | Space: O(n)
    """
    def corpFlightBookings(self, bookings: List[List[int]], n: int) -> List[int]:
        # Difference array: diff[i] = change in seat count at flight i
        # Use n+1 to handle the boundary case when last == n
        seat_change = [0] * (n + 1)

        # Apply range updates using difference array technique
        for first_flight, last_flight, seat_count in bookings:
            # Convert to 0-indexed: first_flight=1 -> index 0
            seat_change[first_flight - 1] += seat_count    # Start adding seats
            seat_change[last_flight] -= seat_count         # Stop after last flight

        # Prefix sum to reconstruct actual seat counts
        total_seats = []
        current_seats = 0
        for flight_index in range(n):
            current_seats += seat_change[flight_index]
            total_seats.append(current_seats)

        return total_seats
```

### 9.3 Trace Example

```
bookings = [[1,2,10],[2,3,20],[2,5,25]], n = 5

Building difference array:
Booking [1,2,10]: diff[0]+=10, diff[2]-=10  -> [10,0,-10,0,0,0]
Booking [2,3,20]: diff[1]+=20, diff[3]-=20  -> [10,20,-10,-20,0,0]
Booking [2,5,25]: diff[1]+=25, diff[5]-=25  -> [10,45,-10,-20,0,-25]

Prefix sum:
Flight 1: 0 + 10 = 10
Flight 2: 10 + 45 = 55
Flight 3: 55 + (-10) = 45
Flight 4: 45 + (-20) = 25
Flight 5: 25 + 0 = 25

Answer: [10, 55, 45, 25, 25]
```

### 9.4 Difference Array vs Naive Approach

| Approach | Time | When Better |
|----------|------|-------------|
| Naive (update each flight) | O(n * m) | Small inputs |
| Difference Array | O(n + m) | Many overlapping ranges |

For this problem with up to 20,000 bookings and 20,000 flights, difference array is essential.

---

## 10. Pattern Comparison

### 10.1 Prefix Sum vs Sliding Window

| Aspect | Prefix Sum | Sliding Window |
|--------|------------|----------------|
| **Use When** | Negative numbers allowed | All positive or monotonic |
| **Window Type** | Any subarray (computed via difference) | Contiguous, expanding/shrinking |
| **Complexity** | O(n) time, O(n) space | O(n) time, O(1) space |
| **Key Insight** | Sum difference = subarray sum | Monotonic sum/count |

**Example**: Find subarray with sum = k
- Negative numbers: Use Prefix Sum + Hash Map (LC 560)
- Positive only: Can use Sliding Window (LC 209)

### 10.2 Prefix Sum vs Difference Array

| Aspect | Prefix Sum | Difference Array |
|--------|------------|------------------|
| **Direction** | Point values → Range sums | Range updates → Point values |
| **Build** | `prefix[i] = prefix[i-1] + nums[i-1]` | `diff[start] += val, diff[end+1] -= val` |
| **Query** | `prefix[r+1] - prefix[l]` → O(1) | Prefix sum of diff → O(n) |
| **Best For** | Many range sum queries | Many range update operations |

They are **inverses** of each other:
```
Prefix Sum: nums → prefix (cumulative sum)
Difference: prefix → nums (consecutive differences)
```

### 10.3 1D vs 2D Prefix Sum

| Aspect | 1D Prefix Sum | 2D Prefix Sum |
|--------|---------------|---------------|
| **Formula** | `prefix[j+1] - prefix[i]` | Inclusion-exclusion with 4 terms |
| **Build** | O(n) | O(m * n) |
| **Query** | O(1) | O(1) |
| **Space** | O(n) | O(m * n) |

---

## 11. Decision Flowchart

```
Start: "Range/subarray problem?"
       │
       ▼
  ┌─────────────────────┐
  │ Multiple range sum  │
  │ queries on STATIC   │───Yes──▶ Prefix Sum Range Query (LC 303, 304)
  │ array?              │
  └─────────────────────┘
       │ No
       ▼
  ┌─────────────────────┐
  │ Count/find subarrays│
  │ with target sum?    │───Yes──▶ Prefix Sum + Hash Map (LC 560, 525, 523)
  └─────────────────────┘
       │ No
       ▼
  ┌─────────────────────┐
  │ Range UPDATE        │
  │ operations?         │───Yes──▶ Difference Array (LC 1094, 1109)
  └─────────────────────┘
       │ No
       ▼
  ┌─────────────────────┐
  │ Product of all      │
  │ except current?     │───Yes──▶ Prefix/Suffix Products (LC 238)
  └─────────────────────┘
       │ No
       ▼
  Consider other patterns
```

### 11.1 Pattern Selection Guide

| Problem Signal | Pattern to Use | Example |
|----------------|----------------|---------|
| "Range sum query" + "immutable" | `PrefixSumRangeQuery` | LC 303, 304 |
| "Subarray sum equals k" | `PrefixSumSubarraySum` + Hash Map | LC 560 |
| "Equal count of X and Y" | Transform + Prefix Sum | LC 525 |
| "Subarray sum divisible by k" | Prefix Sum + Modular Arithmetic | LC 523 |
| "Add value to range [i, j]" | Difference Array | LC 1094, 1109 |
| "Product except self" | Prefix/Suffix Products | LC 238 |
| "2D rectangle sum" | 2D Prefix Sum | LC 304 |

### 11.2 Hash Map Initialization Decision

| Problem Type | Initialize With | Why |
|--------------|-----------------|-----|
| Count subarrays with sum k | `{0: 1}` | Count empty prefix |
| Longest subarray with sum k | `{0: -1}` | First occurrence at "index -1" |
| Check existence of sum k | `{0}` | Just need membership |

---

## 12. Template Quick Reference

### 12.1 1. Basic Range Sum Query

```python
# Build prefix sum
prefix = [0]
for num in nums:
    prefix.append(prefix[-1] + num)

# Query [left, right]
range_sum = prefix[right + 1] - prefix[left]
```

### 12.2 2. Subarray Sum Equals K (Count)

```python
count = 0
prefix_sum = 0
sum_count = {0: 1}  # Initialize with empty prefix

for num in nums:
    prefix_sum += num
    count += sum_count.get(prefix_sum - k, 0)
    sum_count[prefix_sum] = sum_count.get(prefix_sum, 0) + 1
```

### 12.3 3. Longest Subarray with Sum K (or Transform)

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

### 12.4 4. Difference Array (Range Updates)

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

### 12.5 5. 2D Prefix Sum

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

### 12.6 6. Prefix/Suffix Products (No Division)

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

### 12.7 Variable Naming Convention

| Variable | Purpose | Example |
|----------|---------|---------|
| `prefix_sum` | Running cumulative sum | `prefix_sum += num` |
| `sum_frequency` | Count of each prefix sum | `sum_frequency[prefix_sum]` |
| `first_occurrence` | First index of each prefix sum | `first_occurrence[prefix_sum] = index` |
| `current_seats` / `current` | Running value in prefix sum | `current += diff[i]` |
| `passenger_change` / `seat_change` | Difference array | `diff[start] += value` |



---



*Document generated for NeetCode Practice Framework — API Kernel: PrefixSumRangeQuery*
