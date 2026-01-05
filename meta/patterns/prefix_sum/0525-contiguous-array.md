## Contiguous Array (LeetCode 525)

> **Problem**: Find the maximum length of a contiguous subarray with equal number of 0s and 1s.
> **Transform**: Convert 0 -> -1, then find longest subarray with sum = 0.
> **Role**: TRANSFORM VARIANT demonstrating problem reduction.

### The Transform Insight

Original problem: Count of 0s = Count of 1s in subarray
After transform (0 -> -1): Sum of subarray = 0

```
Original: [0, 1, 0, 1, 1, 0]
Transform: [-1, 1, -1, 1, 1, -1]

Subarray [0,3]: Original has 2 zeros, 2 ones ✓
                Transform sum = -1+1+(-1)+1 = 0 ✓
```

### Implementation

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

### Trace Example

```
nums = [0, 1, 0]
transform = [-1, 1, -1]

Index 0: prefix=-1, first_occurrence={0:-1, -1:0}
Index 1: prefix=0,  0 in map at -1, length=1-(-1)=2  -> max=2
Index 2: prefix=-1, -1 in map at 0, length=2-0=2    -> max=2

Answer: 2 (subarray [0,1] has one 0 and one 1)
```

### Why {0: -1} Initialization

Handles subarrays starting at index 0:
```
nums = [0, 1]
prefix sums: -1, 0

At index 1: prefix=0, need to find 0 in map
With {0: -1}: length = 1 - (-1) = 2 ✓
Without {0: -1}: 0 not in map, miss the answer
```


