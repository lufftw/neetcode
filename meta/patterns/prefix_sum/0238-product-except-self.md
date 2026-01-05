## Product of Array Except Self (LeetCode 238)

> **Problem**: Return array where each element is the product of all other elements, without division.
> **Insight**: `result[i] = prefix_product[0..i-1] * suffix_product[i+1..n-1]`
> **Role**: PREFIX/SUFFIX PRODUCT VARIANT applying prefix sum concept to multiplication.

### Prefix and Suffix Products

```
nums:           [1,    2,    3,    4]
prefix_product: [1,    1,    2,    6]   (product of elements BEFORE i)
suffix_product: [24,   12,   4,    1]   (product of elements AFTER i)
result:         [24,   12,   8,    6]   (prefix[i] * suffix[i])
```

### Implementation (O(1) Extra Space)

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

### Trace Example

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

### Handling Zeros

This approach handles zeros naturally:
```
nums = [1, 0, 3]
prefix: [1, 1, 0]    (0 appears after we see the zero)
suffix: [0, 3, 1]    (0 appears before we see the zero)
result: [0, 3, 0]    (only the zero position gets non-zero)
```


